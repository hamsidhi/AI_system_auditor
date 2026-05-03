import streamlit as st
import json
from main import run_full_audit
from key_manager import KeyManager
from ai_engine import AIEngine

# Page Config
st.set_page_config(
    page_title="AI System Auditor",
    page_icon="🚀",
    layout="wide"
)

# Initialize KeyManager
km = KeyManager()

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuration")

    # API Key Section
    st.subheader("Groq API Configuration")
    stored_key = km.get_key()
    api_key_input = st.text_input("Groq API Key", value=stored_key or "", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Key"):
            km.save_key(api_key_input)
            st.success("Key saved!")
    with col2:
        if st.button("Clear Key"):
            km.clear_key()
            st.warning("Key cleared!")
            # Rerunning to update the input field
            st.rerun()

    st.divider()

    # Model Selection
    st.subheader("AI Model")
    # Use the fallback chain from AIEngine as the options
    model_options = AIEngine.MODEL_FALLBACK_CHAIN
    selected_model = st.selectbox("Primary Model", options=model_options, index=0)

# --- MAIN PANEL ---
st.title("🚀 AI System Auditor")
st.markdown("""
Audit your codebase for **security risks**, **bugs**, and **architectural health** using Groq's high-performance LLMs.
""")

# Project Path Input
project_path = st.text_input("📁 Project Directory Path", placeholder="D:\\AppData\\deepak jain\\my_project")

if st.button("Run Full Audit", type="primary"):
    if not api_key_input:
        st.error("Please provide a Groq API Key in the sidebar.")
    elif not project_path:
        st.error("Please provide a project directory path.")
    else:
        try:
            with st.spinner("🔍 Scanning files and analyzing codebase... this may take a few minutes."):
                # Execute the audit service
                report = run_full_audit(project_path, api_key_input, selected_model)

                # Store report in session state to keep it across reruns
                st.session_state["last_report"] = report
        except Exception as e:
            st.exception(f"An error occurred during audit: {e}")

# --- RESULTS DISPLAY ---
if "last_report" in st.session_state:
    report = st.session_state["last_report"]

    st.divider()
    st.header("📊 Audit Results")

    # 1. KPI Metrics
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("System Health Score", f"{report['health_score']}/100")
    with m_col2:
        st.metric("Files Scanned", report['stats']['files_scanned'])
    with m_col3:
        st.metric("Total Project Size", report['stats']['total_size'])

    # 2. Overall Summary
    st.subheader("📝 Executive Summary")
    st.info(report['overall_summary'])

    # 3. Critical Risks
    if report['critical_risks']:
        st.subheader("🚨 Top Critical Risks")
        for risk in report['critical_risks']:
            st.error(f"**{risk}**")
    else:
        st.success("No critical risks identified!")

    # 4. Detailed Issues
    st.subheader("🔍 Detailed Analysis")

    # Severity Filter
    severity_filter = st.multiselect(
        "Filter by Severity",
        options=["high", "medium", "low"],
        default=["high", "medium", "low"]
    )

    filtered_issues = [
        i for i in report['detailed_issues']
        if i.get('severity', 'low').lower() in severity_filter
    ]

    if filtered_issues:
        # Using a dataframe for a cleaner look, but we'll use an expandable list for suggestions
        st.markdown("### Issue Breakdown")
        for i in filtered_issues:
            with st.expander(f"[{i.get('severity', 'low').upper()}] {i.get('file', 'Unknown File')}: {i.get('issue', 'No issue described')}"):
                st.write(f"**File:** `{i.get('file')}`")
                st.write(f"**Suggestion:** {i.get('suggestion')}")
    else:
        st.write("No issues found matching the selected filters.")

    # 5. Export
    st.divider()
    st.subheader("📥 Export Report")
    json_report = json.dumps(report, indent=4)
    st.download_button(
        label="Download Full Report (JSON)",
        data=json_report,
        file_name="audit_report.json",
        mime="application/json"
    )
