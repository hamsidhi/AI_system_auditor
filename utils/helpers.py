import os

def format_bytes(size):
    """Converts bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def print_severity(severity):
    """Returns a colored indicator for severity."""
    colors = {
        "high": "\033[91m[HIGH]\033[0m",
        "medium": "\033[93m[MEDIUM]\033[0m",
        "low": "\033[94m[LOW]\033[0m"
    }
    return colors.get(severity.lower(), "[INFO]")
