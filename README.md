<div align="center">
  <img src="https://img.icons8.com/nolan/256/shield.png" alt="Avinya Logo" width="120" />
  <h1>🛡️ Avinya Code Reviewer</h1>
  <p><strong>Local AI-Powered Automated Code Auditing CLI</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Ollama-Local_LLM-black.svg?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
    <img src="https://img.shields.io/badge/CrewAI-Agents-orange.svg?style=for-the-badge&logo=robot&logoColor=white" alt="CrewAI" />
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" />
  </p>
</div>

---

**Avinya** is a privacy-first, CLI-based code reviewer that utilizes a multi-agent system powered by **Ollama** and **CrewAI**. It performs structural and logic-based code audits, transforming local repositories into comprehensive, versioned HTML security and code quality reports without your code ever leaving your machine.

## ✨ Key Features

*   **🔒 100% Local Execution:** Absolute privacy. Your source code is analyzed securely offline.
*   **🧠 Deep Intelligence:** Detects business logic flaws, race conditions, and structural vulnerabilities that standard linters miss, using `qwen2.5:7b` via Ollama.
*   **🤖 Multi-Agent Crew:** Specialized agents (Summarizer, Syntax Reviewer, Logic Analyzer, Orchestrator) work in sequence for highly contextual validation.
*   **📊 Comprehensive Reporting:** Generates a visually appealing, single-file HTML dashboard with code health scores, style consistency charts, and color-coded severity metrics.
*   **⚡ Smart Caching:** Utilizes SHA-256 directory hashing to avoid redundant scans. Cached reports open instantly if code hasn't changed.

## 📦 Dependencies

Avinya relies on a combination of Python libraries and system-level tools to perform complete code analysis:

### System Requirements
*   **[Python 3.8+](https://www.python.org/):** Core runtime.
*   **[Ollama](https://ollama.com/):** For running the AI model inference locally.
*   **[Flake8](https://flake8.pycqa.org/):** System/Environment installation required for Python syntax linting.
*   **[ESLint](https://eslint.org/):** System installation required for JavaScript/TypeScript syntax linting.

### Python Libraries
Ensure these libraries are installed in your environment:
*   `crewai`: Orchestrates the specialized AI agent workflows.
*   `pydantic`: Enforces deterministic JSON data layouts from the LLMs.
*   `jinja2`: Template engine for generating the final HTML report.
*   `beautifulsoup4`: Parses and manipulates HTML for versioning and merging previous reports.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url> avinya
   cd avinya
   ```

2. **Set up the Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies:**
   ```bash
   pip install crewai pydantic jinja2 beautifulsoup4
   ```

4. **Install System Dependencies:**
   Make sure you have Ollama running, and the deterministic linters installed:
   ```bash
   pip install flake8
   npm install -g eslint
   ```

5. **Start Ollama & Pull the Model:**
   ```bash
   ollama run qwen2.5:7b
   ```

## 🚀 Usage

Run Avinya pointing directly to the target local codebase directory you wish to scan:

```bash
python main.py /path/to/your/codebase
```

### CLI Arguments

| Argument | Description |
| :--- | :--- |
| `path` | **(Required)** The absolute or relative path to the repository directory. |
| `--force` | **(Optional)** Force a new scan and bypass the SHA-256 cache. |
| `-v`, `--verbose` | **(Optional)** Enable verbose logger to watch the CrewAI agents "think" in real-time. |

**Example:**
```bash
python main.py ./codebases/flawed -v
```

1. Avinya hashes the directory. 
2. Deterministic tools (regex for secrets/APIs, `flake8`/`eslint` for syntax) pre-process the codebase.
3. The AI Crew consumes context and analyzes the code.
4. The tool automatically opens `<folder_name>_avinya_report.html` in your default browser.

## 🏗️ Architecture (The "Brain")

Avinya divides the cognitive workload among specialized AI personas:

| Agent | Responsibility | Output |
| :--- | :--- | :--- |
| 🗺️ **Summarizer** | Maps contextual logic, purpose, and operations per file. | JSON map of file logic |
| 🔍 **API / Regex Tools** | Extracts API routes, hardcoded URLs, IPs, and secrets. | Raw list of exposed endpoints and secrets |
| 💅 **Syntax Reviewer** | Audits code style, modularity, and checks linter compliance. | Review of architectural consistency |
| 🕵️ **Logic Analyzer** | Acts as a red-teamer. Locates logical flaws and race conditions. | Highly-critical vulnerability report |
| 👨‍💼 **Orchestrator** | Quality control manager. Filters out vague findings. | Consolidated, verified Pydantic object |
| 🎨 **Reporter** | Frontend architect. | Dynamic HTML Dashboard |

---
<div align="center">
  <p><i>Built for privacy, security, and developer speed.</i></p>
</div>
