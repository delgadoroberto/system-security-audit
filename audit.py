#!/usr/bin/env python3

import os
import platform
import socket
import getpass
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


def main():
    print_header()
    system_information()
    disk_information()
    environment_variables()


if __name__ == "__main__":
    main()
