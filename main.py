import json
import argparse
from analyzer import Analyzer
from ai_engine import AIEngine
from utils.helpers import format_bytes, print_severity

def run_full_audit(project_path, api_key, model=None):
    """
    Service layer function that performs the full audit process.
    Returns a dictionary containing the complete report.
    """
    analyzer = Analyzer(project_path)
    ai = AIEngine(api_key=api_key, model=model)

    # 1. Static Scanning
    files_to_analyze = analyzer.scan_files()

    all_ai_analyses = {}
    final_issues = list(analyzer.report_data["static_issues"])

    # 2. AI Analysis
    for file_path, content in files_to_analyze:
        # Static security check
        sec_risks = analyzer.check_security_risks(content, file_path)
        final_issues.extend(sec_risks)

        # AI analysis
        analysis = ai.analyze_file(file_path, content)
        all_ai_analyses[file_path] = analysis

        # Integrate AI found issues into the final list
        for issue_obj in analysis.get("issues", []):
            issue_obj["file"] = file_path
            final_issues.append(issue_obj)

    # 3. Final System Report
    final_summary = ai.generate_final_report(all_ai_analyses)

    # 4. Final Data Construction
    full_report = {
        "project_path": project_path,
        "stats": {
            "files_scanned": analyzer.report_data["files_scanned"],
            "total_size": format_bytes(analyzer.report_data["total_size"]),
        },
        "health_score": final_summary.get("health_score", 0),
        "critical_risks": final_summary.get("critical_risks", []),
        "overall_summary": final_summary.get("overall_summary", ""),
        "detailed_issues": final_issues
    }

    return full_report

def main():
    parser = argparse.ArgumentParser(description="AI System Auditor - Analyze your project for issues and health.")
    parser.add_argument("path", help="Path to the project folder to audit")
    parser.add_argument("--api-key", required=True, help="Groq API Key")
    parser.add_argument("--model", default=None, help="Groq model to use")
    args = parser.parse_args()

    print(f"\n🚀 Starting AI System Audit for: {args.path}")
    print("-" * 50)

    try:
        full_report = run_full_audit(args.path, args.api_key, args.model)

        # Output: JSON File
        with open("audit_report.json", "w") as f:
            json.dump(full_report, f, indent=4)

        # Output: CLI Display
        print("\n" + "=" * 60)
        print(f" AI SYSTEM AUDIT REPORT")
        print("=" * 60)
        print(f"Health Score: {full_report['health_score']}/100")
        print(f"Project Size: {full_report['stats']['total_size']}")
        print(f"Files Scanned: {full_report['stats']['files_scanned']}")
        print("-" * 60)
        print(f"\nOVERALL SUMMARY:\n{full_report['overall_summary']}")

        print("\nTOP CRITICAL RISKS:")
        for risk in full_report['critical_risks']:
            print(f" - {risk}")

        print("\nDETAILED ISSUES:")
        for issue in full_report['detailed_issues']:
            sev = print_severity(issue.get('severity', 'low'))
            print(f"{sev} {issue.get('file', 'N/A')}: {issue.get('issue')}")
            print(f"     Suggestion: {issue.get('suggestion')}")
            print("-" * 30)

        print(f"\n✅ Audit complete. Full report saved to audit_report.json")
    except Exception as e:
        print(f"\n❌ Audit failed: {e}")

if __name__ == "__main__":
    main()
