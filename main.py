import argparse
import hashlib
import json
import os
import sys
import webbrowser
import urllib.request
import urllib.error
from pathlib import Path

class Colors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_info(msg):
    print(f"{Colors.OKCYAN}[*] {msg}{Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.OKGREEN}[+] {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}[-] {msg}{Colors.ENDC}", file=sys.stderr)

def print_warning(msg):
    print(f"{Colors.WARNING}[!] {msg}{Colors.ENDC}")

def check_ollama(base_url="http://localhost:11434"):
    try:
        urllib.request.urlopen(base_url, timeout=2).read()
        return True
    except Exception:
        return False

from crewai import Crew, Process, LLM

# ... (omitted determinism imports) ...
from tools.linter import run_linter
from tools.regex_finder import extract_apis_and_secrets

from agents.summarizer import create_summarizer_agent
from tasks.summarizer_task import create_summarizer_task

from agents.syntax_reviewer import create_syntax_reviewer_agent
from tasks.syntax_reviewer_task import create_syntax_reviewer_task

from agents.logic_analyzer import create_logic_analyzer_agent
from tasks.logic_analyzer_task import create_logic_analyzer_task

from agents.orchestrator import create_orchestrator_agent
from tasks.orchestrator_task import create_orchestrator_task

from agents.reporter import generate_report

def hash_file(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def hash_directory(directory: Path) -> str:
    ignore_dirs = {'.git', 'venv', 'env', 'node_modules', '__pycache__', '.avinya'}
    ignore_files = {'.DS_Store'}
    file_hashes = []
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in sorted(files):
            if file in ignore_files:
                continue
            filepath = Path(root) / file
            if filepath.is_file():
                file_hashes.append(hash_file(filepath))
                
    file_hashes.sort()
    final_hasher = hashlib.sha256()
    for h in file_hashes:
        final_hasher.update(h.encode('utf-8'))
    return final_hasher.hexdigest()

def check_cache(target_dir: Path, current_hash: str) -> bool:
    avinya_dir = target_dir / '.avinya'
    state_file = avinya_dir / 'state.json'
    
    if state_file.exists():
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
                if state.get('hash') == current_hash:
                    return True
        except (json.JSONDecodeError, IOError):
            pass
    return False

def update_cache(target_dir: Path, current_hash: str):
    avinya_dir = target_dir / '.avinya'
    avinya_dir.mkdir(exist_ok=True)
    state_file = avinya_dir / 'state.json'
    with open(state_file, 'w') as f:
        json.dump({'hash': current_hash}, f)

def main():
    parser = argparse.ArgumentParser(description="Avinya: Local AI Code Reviewer")
    parser.add_argument("path", type=str, help="Path to the repository/folder to scan")
    parser.add_argument("--force", action="store_true", help="Force a scan even if code hasn't changed")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose CrewAI agent execution logs")
    args = parser.parse_args()
    
    target_dir = Path(args.path).resolve()
    
    if not target_dir.exists() or not target_dir.is_dir():
        print_error(f"Directory '{target_dir}' does not exist.")
        sys.exit(1)
        
    print_info(f"Starting Avinya scan for {target_dir}")
    current_hash = hash_directory(target_dir)
    print_info(f"Codebase Hash: {current_hash}")
    
    report_path = target_dir / f"{target_dir.name}_avinya_report.html"
    
    if not args.force and check_cache(target_dir, current_hash) and report_path.exists():
        print_success("Codebase hasn't changed. Opening cached report...")
        webbrowser.open(f"file://{report_path.resolve()}")
        sys.exit(0)
        
    print_info("Change detected or forced scan. Proceeding with analysis.")
    
    # 0. Pre-Flight Checks
    if not check_ollama():
        print_error("Ollama engine is not running or accessible at http://localhost:11434.")
        print_warning("Please start the Ollama service to proceed.")
        sys.exit(1)
    
    # 1. Deterministic Tools
    print_info("Running deterministic tools (Linters & Regex Scrapers)...")
    try:
        linter_output = run_linter(target_dir)
        regex_findings = extract_apis_and_secrets(target_dir)
    except Exception as e:
        print_error(f"Failed executing deterministic tools: {str(e)}")
        sys.exit(1)
    
    # 2. Setup Ollama
    print_info("Initializing AI Agents (Ollama: qwen2.5:7b)...")
    llm = LLM(model="ollama/qwen2.5:7b", base_url="http://localhost:11434")
    
    # 3. Agents
    summarizer = create_summarizer_agent(llm)
    syntax_rev = create_syntax_reviewer_agent(llm)
    logic_anal = create_logic_analyzer_agent(llm)
    orchestra = create_orchestrator_agent(llm)
    
    # 4. Tasks (Sequential)
    task1 = create_summarizer_task(summarizer, str(target_dir))
    task2 = create_syntax_reviewer_task(syntax_rev, linter_output)
    task3 = create_logic_analyzer_task(logic_anal, regex_findings)
    task4 = create_orchestrator_task(orchestra)
    
    # Let task4 rely on context from task1, 2, 3
    task4.context = [task1, task2, task3]
    
    # 5. The Crew
    crew = Crew(
        agents=[summarizer, syntax_rev, logic_anal, orchestra],
        tasks=[task1, task2, task3, task4],
        process=Process.sequential,
        verbose=args.verbose
    )
    
    try:
        print_info("Starting the multi-agent CrewAI execution.")
        print_info("Agents are analyzing the repository. This may take a few minutes...")
        # Execute the crew
        result = crew.kickoff()
        
        # Pydantic Output Validation
        if not hasattr(task4, 'output') or not task4.output or not task4.output.pydantic:
            print_error("Orchestrator failed to produce the correctly formatted Pydantic JSON structure.")
            if args.verbose:
                print_error(f"Raw Result Dump:\n{result}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print_warning("\nScan interrupted by user. Exiting gracefully.")
        sys.exit(0)
    except Exception as e:
        print_error(f"A fatal error occurred during CrewAI execution: {str(e)}")
        sys.exit(1)
        
    final_state = task4.output.pydantic.dict()
    
    print_info("Generating self-contained HTML Report...")
    template_dir = Path(__file__).parent / 'templates'
    final_report = generate_report(final_state, target_dir, template_dir)
    
    update_cache(target_dir, current_hash)
    
    print_success(f"Success! Report generated at: {final_report}")
    webbrowser.open(f"file://{final_report.resolve()}")

if __name__ == "__main__":
    main()
