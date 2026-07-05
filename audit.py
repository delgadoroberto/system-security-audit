#!/usr/bin/env python3

import os
import json
import time
import hashlib
import platform
import socket
import getpass

from datetime import datetime


class AuditReport:

    def __init__(self):

        self.report = {
            "audit_information": {
                "start_time": datetime.now().isoformat(),
                "end_time": None,
                "duration_seconds": 0
            },
            "system_information": {},
            "disk_information": {},
            "environment_variables": {},
            "file_integrity": [],
            "statistics": {
                "files_scanned": 0,
                "errors": 0
            }
        }

    def set_system_information(self):

        self.report["system_information"] = {
            "hostname": socket.gethostname(),
            "operating_system": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "current_user": getpass.getuser(),
            "current_directory": os.getcwd()
        }

    def set_disk_information(self):

        stat = os.statvfs("/")

        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bavail * stat.f_frsize
        used = total - free

        self.report["disk_information"] = {
            "total_gb": round(total / (1024 ** 3), 2),
            "used_gb": round(used / (1024 ** 3), 2),
            "free_gb": round(free / (1024 ** 3), 2)
        }

    def set_environment_variables(self):

        self.report["environment_variables"] = dict(sorted(os.environ.items()))

    def add_file_hash(self, path, sha256):

        self.report["file_integrity"].append({
            "file": path,
            "sha256": sha256
        })

        self.report["statistics"]["files_scanned"] += 1

    def add_error(self):

        self.report["statistics"]["errors"] += 1

    def finish(self, start_time):

        end_time = time.time()

        self.report["audit_information"]["end_time"] = datetime.now().isoformat()

        self.report["audit_information"]["duration_seconds"] = round(
            end_time - start_time,
            2
        )

    def export_json(self):

        with open("audit_report.json", "w", encoding="utf-8") as output:

            json.dump(
                self.report,
                output,
                indent=4
            )


def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    try:

        with open(file_path, "rb") as file:

            while chunk := file.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception:

        return None


def scan_directory(directory, report):

    if not os.path.isdir(directory):
        print("Directory not found.")
        return

    print("\nScanning files...\n")

    for root, _, files in os.walk(directory):

        for filename in sorted(files):

            path = os.path.join(root, filename)

            digest = calculate_sha256(path)

            if digest is None:
                report.add_error()
                continue

            report.add_file_hash(path, digest)

            print(f"Hashed: {path}")


def print_summary(report):

    print("\n" + "=" * 60)

    print("Audit Summary")

    print("=" * 60)

    print(
        f"Files scanned : "
        f"{report.report['statistics']['files_scanned']}"
    )

    print(
        f"Errors        : "
        f"{report.report['statistics']['errors']}"
    )

    print(
        f"Duration       : "
        f"{report.report['audit_information']['duration_seconds']} seconds"
    )

    print("\nJSON report saved as audit_report.json")


def main():

    start = time.time()

    report = AuditReport()

    report.set_system_information()

    report.set_disk_information()

    report.set_environment_variables()

    directory = input(
        "Enter directory to scan: "
    ).strip()

    scan_directory(directory, report)

    report.finish(start)

    report.export_json()

    print_summary(report)


if __name__ == "__main__":
    main()
