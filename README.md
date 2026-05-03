# AI System Auditor

A lightweight project analysis tool that combines static analysis with AI-powered insights using Ollama.

## Setup Steps

1. **Install Ollama**:
   Download and install Ollama from [ollama.com](https://ollama.com).

2. **Pull the Model**:
   The auditor uses `llama3` by default. Run the following command in your terminal:
   ```bash
   ollama pull llama3
   ```

3. **Install Python Dependencies**:
   The project only requires the `requests` library.
   ```bash
   pip install requests
   ```

## How to Run

1. Open your terminal and navigate to the project folder.
2. Run the auditor by passing the path to the project you want to analyze:

   ```bash
   python main.py /path/to/your/project
   ```

3. **Optional**: Use a different model if installed:
   ```bash
   python main.py /path/to/your/project --model mistral
   ```

## System Requirements
- CPU: Any modern multi-core CPU.
- RAM: 16GB recommended (required for running LLMs locally via Ollama).
- OS: Windows, macOS, or Linux.

## Project Structure
- `main.py`: Entry point and report formatter.
- `analyzer.py`: Handles file system walking and regex-based static checks.
- `ai_engine.py`: Manages communication with the Ollama API.
- `utils/helpers.py`: Utility functions for formatting.
