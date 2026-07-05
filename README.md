## File Integrity Check

The tool can recursively scan a directory and calculate the SHA-256 hash for every file.

### Example

```text
[+] File Integrity Check

Scanning directory: /etc

File: /etc/passwd
SHA256:
d7d5c7...

------------------------------------------------------------

File: /etc/hosts
SHA256:
4bd123...

------------------------------------------------------------
```

This feature can be useful for:

- File integrity verification
- Security audits
- Detecting unauthorized file modifications
- Creating file inventory reports

## JSON Report

The audit results are automatically exported to a JSON file.

```bash
audit_report.json
```

The report includes:

- Audit metadata
- System information
- Disk usage
- Environment variables
- File integrity results
- Scan statistics
- Execution time

The JSON format allows the output to be integrated with dashboards, SIEM platforms, or other security automation workflows.
