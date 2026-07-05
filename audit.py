#!/usr/bin/env python3

import os
import platform
import socket
import getpass
import hashlib
from datetime import datetime


def print_header():
    print("=" * 60)
    print("System Security Audit")
    print("=" * 60)


def system_information():
    print("\n[+] System Information")

    print(f"Hostname          : {socket.gethostname()}")
    print(f"Operating System  : {platform.system()}")
    print(f"OS Version        : {platform.version()}")
    print(f"Architecture      : {platform.machine()}")
    print(f"Processor         : {platform.processor()}")
    print(f"Python Version    : {platform.python_version()}")
    print(f"Current User      : {getpass.getuser()}")
    print(f"Current Directory : {os.getcwd()}")
    print(f"Audit Time        : {datetime.now()}")


def environment_variables():
    print("\n[+] Environment Variables")

    for key in sorted(os.environ):
        print(f"{key}={os.environ[key]}")


def disk_information():
    print("\n[+] Disk Usage")

    stat = os.statvfs("/")

    total = stat.f_blocks * stat.f_frsize
    free = stat.f_bavail * stat.f_frsize
    used = total - free

    print(f"Total Space : {total / (1024 ** 3):.2f} GB")
    print(f"Used Space  : {used / (1024 ** 3):.2f} GB")
    print(f"Free Space  : {free / (1024 ** 3):.2f} GB")


def calculate_sha256(file_path):
    """
    Calculate the SHA-256 hash of a file.
    """

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception as error:
        return f"Error: {error}"


def scan_directory(directory):
    """
    Scan a directory recursively and calculate SHA-256 hashes.
    """

    print("\n[+] File Integrity Check")
    print(f"Scanning directory: {directory}\n")

    if not os.path.isdir(directory):
        print("Directory not found.")
        return

    for root, _, files in os.walk(directory):

        for filename in sorted(files):

            file_path = os.path.join(root, filename)

            print(f"File: {file_path}")
            print(f"SHA256: {calculate_sha256(file_path)}")
            print("-" * 60)


def main():
    print_header()

    system_information()

    disk_information()

    environment_variables()

    directory = input(
        "\nEnter the directory to scan for SHA-256 hashes: "
    ).strip()

    scan_directory(directory)


if __name__ == "__main__":
    main()
