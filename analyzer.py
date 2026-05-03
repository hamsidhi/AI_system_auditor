import os
import re
from pathlib import Path

class Analyzer:
    """Performs static analysis and file system scanning."""

    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        self.report_data = {
            "static_issues": [],
            "files_scanned": 0,
            "total_size": 0
        }

    def scan_files(self):
        """Walks through the folder and reads all supported files."""
        files_to_analyze = []

        # Common extensions to analyze
        valid_extensions = {'.py', '.js', '.html', '.css', '.json', '.txt', '.yaml', '.yml', '.env', '.conf', '.ini'}

        # Directories to ignore
        ignore_dirs = {'.git', '__pycache__', 'dist', 'build', 'venv', '.venv', 'node_modules'}

        for root, dirs, files in os.walk(self.folder_path):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix

                # Basic size check
                size = file_path.stat().st_size
                self.report_data["total_size"] += size
                if size > 1024 * 500: # 500KB limit for AI analysis to avoid context overflow
                    self.report_data["static_issues"].append({
                        "file": str(file_path),
                        "issue": "File size too large for AI analysis",
                        "severity": "low",
                        "suggestion": "Split the file into smaller modules."
                    })

                if ext in valid_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            files_to_analyze.append((str(file_path), content))
                    except Exception as e:
                        self.report_data["static_issues"].append({
                            "file": str(file_path),
                            "issue": f"Could not read file: {e}",
                            "severity": "medium",
                            "suggestion": "Check file encoding."
                        })

                self.report_data["files_scanned"] += 1

        return files_to_analyze

    def check_security_risks(self, content, file_path):
        """Basic regex-based security check for hardcoded keys."""
        risks = []
        patterns = {
            "API Key": r"(?i)(api_key|secret|password|token|access_key)\s*=\s*['\"].+['\"]",
            "Private Key": r"-----BEGIN PRIVATE KEY-----",
            "IP Address": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        }

        for risk_type, pattern in patterns.items():
            if re.search(pattern, content):
                risks.append({
                    "file": file_path,
                    "issue": f"Potential hardcoded {risk_type} detected",
                    "severity": "high",
                    "suggestion": "Use environment variables or a secret manager."
                })
        return risks
