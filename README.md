# AI System Auditor

A professional AI-powered codebase auditor that performs static analysis and deep architectural reviews using the Groq API.

## 🚀 Features
- **Static Analysis**: Detects hardcoded secrets, oversized files, and basic security risks.
- **AI-Driven Audit**: Leverages high-performance LLMs (via Groq) to summarize file purposes and identify complex bugs or architectural smells.
- **Smart Context Management**: Implements smart truncation to handle large files without losing structural context.
- **Robust Reliability**: Built-in model fallback chain to ensure high availability even during API rate limits.
- **Modern Dashboard**: Professional Streamlit web interface for visualizing health scores, critical risks, and detailed issues.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hamsidhi/AI_system_auditor.git
   cd AI_system_auditor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Supported File Types
The auditor currently analyzes text-based source files:
- **Code**: `.py`, `.js`, `.html`, `.css`
- **Config/Data**: `.json`, `.yaml`, `.yml`, `.env`, `.conf`, `.ini`
- **Documentation**: `.txt`

*Note: Binary files (like `.pdf`, `.docx`, `.png`) are scanned for size and security risks but their contents are not processed by the AI.*

## 💻 Usage

### Web Interface (Recommended)
Run the Streamlit dashboard:
```bash
streamlit run app.py
```
1. Enter your **Groq API Key** in the sidebar.
2. Provide the absolute path to the project you wish to audit.
3. Click **Run Full Audit**.

### CLI Mode
For automated or head-less audits:
```bash
python main.py "C:/path/to/your/project" --api-key "your_groq_key"
```

## ⚙️ Configuration
The tool uses `config/key.json` to securely persist your API key locally. You can also set the `GROQ_API_KEY` environment variable.

## 🛡️ Security
This tool is designed for security auditing. It does not transmit your code to any storage; it only sends the content to Groq's inference endpoints for real-time analysis.

## 📄 License
MIT License
