#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sophisticated_helper_plus.py
All-in-one AI-powered CLI for dev + security workflows with:
- Themes, ASCII animations, persona switching
- Online (Gemini) + offline lint fallback (bandit/pylint/black/grep)
- Batch code review (dir), auto-fix, logs/history
- Cheat-sheet generator, one-liner guru
- Pentest guide (authorized use only) + exploit lab sandbox scaffolds
- Code generator, command fixer
- Clipboard copy, optional TTS voice readout
- Update checker

Author: Sachin Jadhav (Github - kffod)
"""

import os
import sys
import json
import time
import glob
import uuid
import queue
import shutil
import random
import string
import subprocess
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path

# ------------- Configuration -------------

APP_NAME = "Sophisticated Helper+"
AUTHOR = "Sachin Jadhav (kffod)"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

# API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

# Optional internet check for Update Checker
GITHUB_RAW_VERSION_URL = os.getenv(
    "GITHUB_RAW_VERSION_URL",
    ""  # e.g., "https://raw.githubusercontent.com/kffod/sophisticated-helper/main/VERSION"
)

# Feature flags (can be toggled from menu)
STATE = {
    "theme": "neon",
    "voice_enabled": False,
    "persona": "Architect",
    "spinner_style": "dots",
}

# ------------- Themes & Colors -------------

THEMES = {
    "neon": {
        "header": "\033[95m",
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "endc": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "accent": "\033[96m",
    },
    "mono": {
        "header": "",
        "blue": "",
        "green": "",
        "yellow": "",
        "red": "",
        "endc": "",
        "bold": "",
        "underline": "",
        "accent": "",
    },
    "hacker": {
        "header": "\033[92m",
        "blue": "\033[92m",
        "green": "\033[92m",
        "yellow": "\033[92m",
        "red": "\033[92m",
        "endc": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "accent": "\033[92m",
    },
}

PERSONAS = {
    "Architect": "You are a principal software architect. Be rigorous, pragmatic, and concise.",
    "RedTeam": "You are a seasoned red team operator and security instructor. Stress authorization and legality. Focus on risk and mitigations.",
    "Teacher": "You are a friendly teacher. Explain concepts simply with analogies and tight examples.",
    "OpsSRE": "You are an SRE. Emphasize reliability, observability, and on-call realities.",
}

SUPPORTED_CODE_EXTS = {".py", ".js", ".ts", ".go", ".java", ".rb", ".cs", ".cpp", ".c", ".php", ".rs", ".kt", ".swift"}

# ------------- Utilities -------------

def theme_color(name: str) -> str:
    return THEMES.get(STATE["theme"], THEMES["neon"]).get(name, "")

def cprint(text: str, color: str = "endc", end: str = "\n"):
    sys.stdout.write(theme_color(color) + text + theme_color("endc") + end)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner(connected: bool):
    clear_screen()
    art = r"""
███████╗ ██████╗ ██████╗ ██╗  ██╗██╗███████╗████████╗██╗ ██████╗ █████╗ ████████╗███████╗██████╗ 
██╔════╝██╔═══██╗██╔══██╗██║  ██║██║██╔════╝╚══██╔══╝██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
███████╗██║   ██║██████╔╝███████║██║███████╗   ██║   ██║██║     ███████║   ██║   █████╗  ██║  ██║
╚════██║██║   ██║██╔═══╝ ██╔══██║██║╚════██║   ██║   ██║██║     ██╔══██║   ██║   ██╔══╝  ██║  ██║
███████║╚██████╔╝██║     ██║  ██║██║███████║   ██║   ██║╚██████╗██║  ██║   ██║   ███████╗██████╔╝
╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝ 
"""
    cprint(art, "blue")
    cprint(f"{APP_NAME}  —  by {AUTHOR}", "accent")
    cprint(f"Persona: {STATE['persona']}  |  Theme: {STATE['theme']}  |  Voice: {'on' if STATE['voice_enabled'] else 'off'}", "yellow")
    cprint(f"LLM: {'Online' if connected else 'Offline'}", "green" if connected else "red")
    cprint("-" * 90, "header")

def ensure_txt(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def log_markdown(title: str, content: str) -> Path:
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = LOG_DIR / f"{now}__{slugify(title)}.md"
    ensure_txt(filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = "".join(ch if ch.isalnum() else "-" for ch in s)
    return "-".join(filter(None, s.split("-")))

def read_file_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def write_file_text(path: Path, text: str):
    ensure_txt(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def choose(prompt: str, options: list[str]) -> str:
    cprint(prompt, "header")
    for i, opt in enumerate(options, 1):
        cprint(f"  [{i}] {opt}", "green")
    while True:
        raw = input("Enter choice: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        cprint("Invalid choice, try again.", "red")

# ------------- Animations -------------

@contextmanager
def spinner(message="Working...", style="dots"):
    frames = {
        "dots": ["⠋","⠙","⠸","⠴","⠦","⠇"],
        "arc":  ["◜","◠","◝","◞","◡","◟"],
        "pipe": ["|","/","-","\\"],
    }.get(STATE["spinner_style"], ["⠋","⠙","⠸","⠴","⠦","⠇"])
    running = True
    def run():
        idx = 0
        while running:
            sys.stdout.write("\r" + theme_color("yellow") + f"{frames[idx % len(frames)]} {message} " + theme_color("endc"))
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(message) + 4) + "\r")
    try:
        import threading
        t = threading.Thread(target=run, daemon=True)
        t.start()
    except Exception:
        t = None
    try:
        yield
    finally:
        running = False
        if t:
            t.join(timeout=0.1)

def matrix_rain(duration=2.5):
    cols = shutil.get_terminal_size((80, 20)).columns
    end_time = time.time() + duration
    charset = string.ascii_letters + string.digits
    while time.time() < end_time:
        line = "".join(random.choice(charset) for _ in range(cols))
        cprint(line, "green")
        time.sleep(0.03)

# ------------- Clipboard & Voice -------------

def copy_to_clipboard(text: str):
    try:
        import pyperclip
        pyperclip.copy(text)
        cprint("Copied to clipboard.", "green")
    except Exception:
        cprint("Clipboard not available (install pyperclip).", "yellow")

def speak(text: str):
    if not STATE["voice_enabled"]:
        return
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        cprint("TTS unavailable (install pyttsx3).", "yellow")

# ------------- LLM Online (Gemini) -------------

def call_gemini_api(user_text: str, system_prompt: str = "") -> str | None:
    if not GEMINI_API_KEY:
        return None
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": f"{system_prompt}\n\n{user_text}"}]}
        ]
    }
    with spinner("Calling Gemini API...", STATE["spinner_style"]):
        try:
            import requests
            r = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload), timeout=60)
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            cprint(f"API error: {e}", "red")
            return None

def persona_prompt() -> str:
    return PERSONAS.get(STATE["persona"], PERSONAS["Architect"])

# ------------- Offline Analysis (fallback) -------------

def which(cmd: str) -> str | None:
    return shutil.which(cmd)

def run_cmd(cmd: list[str], timeout: int = 90) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, text=True, encoding="utf-8", errors="ignore")
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", str(e)

def offline_scan_python(path: Path) -> list[str]:
    findings = []
    if which("bandit"):
        code, out, err = run_cmd(["bandit", "-q", "-r", str(path)])
        if out.strip():
            findings.append("### Bandit\n```\n" + out.strip() + "\n```")
    if which("pylint"):
        targets = [str(p) for p in path.rglob("*.py")] if path.is_dir() else [str(path)]
        if targets:
            code, out, err = run_cmd(["pylint", "--score=n"] + targets)
            if out.strip():
                findings.append("### Pylint\n```\n" + out.strip() + "\n```")
    # naive secret grep
    patterns = ["api_key", "secret", "password", "passwd", "token", "PRIVATE_KEY", "BEGIN RSA"]
    grep_hits = []
    files = path.rglob("*") if path.is_dir() else [path]
    for f in files:
        if f.suffix.lower() in SUPPORTED_CODE_EXTS or f.suffix.lower() in {".env", ".yml", ".yaml", ".json"}:
            try:
                txt = f.read_text(encoding="utf-8", errors="ignore")
                for p in patterns:
                    if p.lower() in txt.lower():
                        grep_hits.append(f"{f}: contains '{p}'")
            except Exception:
                pass
    if grep_hits:
        findings.append("### Secret/Config Grep\n```\n" + "\n".join(grep_hits) + "\n```")
    return findings

def offline_autoformat_py(file_path: Path) -> str | None:
    """Try to autoformat in offline mode using black and isort if available."""
    changed = []
    if which("isort"):
        code, out, err = run_cmd(["isort", str(file_path)])
        changed.append("isort" if code == 0 else "")
    if which("black"):
        code, out, err = run_cmd(["black", str(file_path)])
        changed.append("black" if code == 0 else "")
    changed = [x for x in changed if x]
    if changed:
        return f"Applied: {', '.join(changed)}"
    return None

# ------------- Core Features -------------

def select_file_or_dir(prompt="Enter file or directory path: ") -> Path | None:
    path = input(prompt).strip().strip('"').strip("'")
    if not path:
        cprint("No path provided.", "red"); return None
    p = Path(path)
    if not p.exists():
        cprint("Path not found.", "red"); return None
    return p

def review_single_file(file_path: Path) -> tuple[str, str]:
    code_text = read_file_text(file_path)
    prompt = f"""
Act as a senior staff software engineer and principal security architect.
{persona_prompt()}
Do a deep review of {file_path.name}. Use clear headings & bullet points. Be concise but thorough.

Cover:
1) Security (OWASP, secrets, auth, input validation)
2) Best Practices & Maintainability
3) Performance & Complexity
4) Tests & Observability (logs/metrics)
5) Prioritized Actionable Fixes
6) Example commands to validate

Return clean Markdown only.

CODE:
```{code_text}```
"""
    res = call_gemini_api(prompt)
    if res is None:
        # offline path
        cprint("No LLM online — using offline scanners.", "yellow")
        findings = offline_scan_python(file_path if file_path.is_dir() else file_path.parent)
        if not findings:
            res = f"# Review for {file_path.name}\n\n_No online LLM or local scanners produced output._"
        else:
            res = "# Offline Review (Aggregated)\n\n" + "\n\n".join(findings)
    return res, code_text

def review_path():
    p = select_file_or_dir("Enter code file OR directory for review: ")
    if not p: return
    items = []
    if p.is_file():
        items = [p]
    else:
        for ext in SUPPORTED_CODE_EXTS:
            items.extend(p.rglob(f"*{ext}"))
        items = sorted(items)
    if not items:
        cprint("No supported code files found.", "yellow"); return

    all_reports = []
    for f in items:
        cprint(f"Reviewing: {f}", "blue")
        rep, _ = review_single_file(f)
        all_reports.append(f"## {f}\n\n{rep}\n")

    merged = f"# Review Report for {p}\n\n" + "\n\n".join(all_reports)
    out = EXPORT_DIR / f"review_report_{slugify(str(p))}.md"
    write_file_text(out, merged)
    cprint(f"Saved: {out}", "green")
    speak("Review complete.")
    # Offer auto-fix pass
    if input("Run Auto-Fix pass? (y/N): ").strip().lower() == "y":
        auto_fix_path(p)

def auto_fix_path(p: Path):
    if GEMINI_API_KEY:
        cprint("Auto-fix via LLM (safe rewrite).", "yellow")
        for f in ([p] if p.is_file() else [*p.rglob("*")]):
            if f.is_file() and f.suffix.lower() in SUPPORTED_CODE_EXTS:
                try:
                    src = read_file_text(f)
                    prompt = f"""
You will rewrite code to address common issues and keep logic intact.
- Keep APIs compatible unless obviously wrong.
- Improve security (validate inputs, avoid injection, remove secrets).
- Improve readability and performance (when low risk).
- Add minimal comments where helpful.
- Return ONLY raw code.

FILE: {f.name}
SOURCE:
```{src}```
"""
                    ans = call_gemini_api(prompt)
                    if ans and "```" in ans:
                        ans = "\n".join(ans.strip().split("\n")[1:-1])
                    if ans and ans.strip():
                        fixed_path = f.with_suffix(f.suffix + ".fixed")
                        write_file_text(fixed_path, ans)
                        cprint(f"Auto-fixed → {fixed_path}", "green")
                except Exception as e:
                    cprint(f"Auto-fix failed for {f}: {e}", "red")
    else:
        cprint("No LLM online, attempting offline auto-format for Python files.", "yellow")
        for f in ([p] if p.is_file() else [*p.rglob("*.py")]):
            note = offline_autoformat_py(f)
            if note:
                cprint(f"{f}: {note}", "green")

def generate_code():
    prompt_text = input("Describe the program you want (be specific): ").strip()
    out_file = input("Output file (e.g., app.py) [optional]: ").strip()
    sys_prompt = f"{persona_prompt()} Return ONLY raw code, no fences, no commentary."
    ans = call_gemini_api(f"Generate a production-ready, maintainable, secure implementation.\n\nSpec:\n{prompt_text}", sys_prompt)
    if ans is None:
        cprint("Online code generation unavailable (no API).", "red"); return
    # strip fences if present
    if ans.strip().startswith("```"):
        ans = "\n".join(ans.strip().split("\n")[1:-1])
    if out_file:
        path = EXPORT_DIR / out_file
        write_file_text(path, ans)
        cprint(f"Wrote code → {path}", "green")
    else:
        cprint("\n--- Generated Code ---\n", "header"); print(ans)
    if input("Copy to clipboard? (y/N): ").lower().strip() == "y":
        copy_to_clipboard(ans)

def fix_command():
    broken = input("Enter the broken shell command: ").strip()
    pmt = f"""Act as a Linux expert. Fix the command and explain.
Format EXACTLY:
CORRECTED_COMMAND_START
<cmd>
CORRECTED_COMMAND_END
EXPLANATION_START
<why>
EXPLANATION_END

Broken: "{broken}"
"""
    ans = call_gemini_api(pmt, persona_prompt())
    if ans is None:
        cprint("Online fixer unavailable.", "red"); return
    try:
        fixed = ans.split("CORRECTED_COMMAND_START")[1].split("CORRECTED_COMMAND_END")[0].strip()
        expl = ans.split("EXPLANATION_START")[1].split("EXPLANATION_END")[0].strip()
        cprint("\nCorrected Command:\n", "green"); print(fixed)
        cprint("\nExplanation:\n", "yellow"); print(expl)
        if input("Copy command to clipboard? (y/N): ").lower().strip() == "y":
            copy_to_clipboard(fixed)
    except Exception:
        cprint("Could not parse. Raw output below:", "red"); print(ans)

def general_assistant():
    q = input("Ask anything (dev/security/product): ").strip()
    pmt = f"""{persona_prompt()}
Answer with clear headings & bullets. Keep it crisp, no fluff. ≤ 16 lines if possible.
Question: "{q}"
"""
    ans = call_gemini_api(pmt)
    if ans is None:
        cprint("Online assistant unavailable.", "red"); return
    cprint("\n--- Expert Answer ---\n", "header"); print(ans)
    speak(ans)
    if input("Save to file? (y/N): ").lower().strip() == "y":
        path = log_markdown(f"general_answer_{slugify(q)[:40]}", ans)
        cprint(f"Saved: {path}", "green")

def pentest_assistant():
    cprint("** Authorized Use Only ** — Only test systems you own or have explicit written permission for.", "red")
    scenario = input("Pentest question/scenario: ").strip()
    pmt = f"""{persona_prompt()}

Start with a clear **LEGALITY DISCLAIMER**: Only use with explicit written authorization.
Provide:
1) Objective
2) Tools
3) Step-by-step (with exact commands + plain-English explanation)
4) Expected outcome
5) Interpreting results
6) Defensive mitigations

Keep it professional, educational, and responsible.

Request: "{scenario}"
"""
    ans = call_gemini_api(pmt)
    if ans is None:
        cprint("Online guide unavailable.", "red"); return
    path = EXPORT_DIR / f"pentest_guide_{slugify(scenario)[:40]}.md"
    write_file_text(path, ans)
    cprint(f"Saved → {path}", "green")

def cheat_sheet_generator():
    topic = input("Cheat-sheet topic (e.g., docker basics, linux net): ").strip()
    pmt = f"""{persona_prompt()}
Create a concise cheat-sheet for "{topic}".
Rules:
- Bullets, short commands, tiny examples
- Group logically with headings
- Fit on 1–2 screens of text
Return Markdown only.
"""
    ans = call_gemini_api(pmt)
    if ans is None:
        cprint("Online generator unavailable.", "red"); return
    path = EXPORT_DIR / f"cheatsheet_{slugify(topic)}.md"
    write_file_text(path, ans)
    cprint(f"Saved → {path}", "green")

def one_liner_guru():
    topic = input("Topic for a one-liner (e.g., JWT security): ").strip()
    pmt = f"""{persona_prompt()}
Give a powerful, plain-English one-liner summary for: {topic}
Then give 2–3 bullet reference points (not links, just names).
Total ≤ 5 lines.
"""
    ans = call_gemini_api(pmt)
    if ans is None:
        cprint("Online mode unavailable.", "red"); return
    cprint("\n--- One-liner ---\n", "header"); print(ans)
    if input("Copy to clipboard? (y/N): ").lower().strip() == "y":
        copy_to_clipboard(ans)

def exploit_lab_mode():
    cprint("This will create intentionally vulnerable sample code for **LOCAL LAB ONLY**.", "yellow")
    lab = choose("Choose vulnerability to simulate:", [
        "SQL Injection (Python Flask)",
        "XSS (Node Express)",
        "Command Injection (Python)",
        "Insecure Deserialization (Java)",
    ])
    pmt = f"""{persona_prompt()}
Generate a tiny, intentionally vulnerable demo for local lab ONLY: {lab}.
Include:
- Minimal README instructions (run locally)
- Clear warnings
- Tiny app code exposing the vulnerability
- A quick exploit example
Return a zipped, code-block separated structure: 
[README.md], [app file(s)] with filenames indicated. No external DB; use in-memory or sqlite.
"""
    ans = call_gemini_api(pmt)
    if ans is None:
        cprint("Online mode unavailable.", "red"); return
    out = EXPORT_DIR / f"lab_{slugify(lab)}.md"
    write_file_text(out, ans)
    cprint(f"Saved → {out}", "green")

def update_checker():
    if not GITHUB_RAW_VERSION_URL:
        cprint("No version URL configured. Set GITHUB_RAW_VERSION_URL.", "yellow")
        return
    try:
        import requests
        with spinner("Checking latest version..."):
            r = requests.get(GITHUB_RAW_VERSION_URL, timeout=10)
            r.raise_for_status()
            latest = r.text.strip()
        local = "dev-local"
        cprint(f"Latest: {latest} | Local: {local}", "green")
        if latest != local:
            cprint("You might be out of date. Pull the latest from the repo.", "yellow")
    except Exception as e:
        cprint(f"Update check failed: {e}", "red")

# ------------- Settings / UX -------------

def toggle_theme():
    STATE["theme"] = choose("Select theme:", list(THEMES.keys()))

def toggle_persona():
    STATE["persona"] = choose("Select persona:", list(PERSONAS.keys()))

def toggle_voice():
    STATE["voice_enabled"] = not STATE["voice_enabled"]
    cprint(f"Voice is now {'ON' if STATE['voice_enabled'] else 'OFF'}.", "green")

def set_spinner():
    STATE["spinner_style"] = choose("Spinner style:", ["dots", "arc", "pipe"])

def show_matrix():
    matrix_rain(2.5)

# ------------- Main Menu -------------

def main_menu():
    while True:
        connected = GEMINI_API_KEY is not None
        banner(connected)
        cprint("Pick an option:", "header")
        actions = [
            ("General Assistant", general_assistant),
            ("Pentest Assistant (Authorized use only)", pentest_assistant),
            ("Code Review (file/dir)", review_path),
            ("Fix Shell Command", fix_command),
            ("Generate Code", generate_code),
            ("Cheat-sheet Generator", cheat_sheet_generator),
            ("One-liner Guru", one_liner_guru),
            ("Exploit Lab Mode (LOCAL LAB ONLY)", exploit_lab_mode),
            ("Theme / Persona / Voice / Spinner", settings_menu),
            ("Update Checker", update_checker),
            ("Exit", lambda: sys.exit(0)),
        ]
        for i, (name, _) in enumerate(actions, 1):
            cprint(f"  [{i}] {name}", "green")
        choice = input("\nEnter your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(actions):
            _, fn = actions[int(choice) - 1]
            try:
                fn()
            except KeyboardInterrupt:
                cprint("\nInterrupted.", "yellow")
            except Exception as e:
                cprint(f"Error: {e}", "red")
            input("\nPress Enter to return to menu...")
        else:
            cprint("Invalid choice.", "red")
            time.sleep(0.6)

def settings_menu():
    while True:
        banner(GEMINI_API_KEY is not None)
        cprint("Settings:", "header")
        opts = [
            ("Change Theme", toggle_theme),
            ("Change Persona", toggle_persona),
            ("Toggle Voice TTS", toggle_voice),
            ("Spinner Style", set_spinner),
            ("Matrix Rain Demo", show_matrix),
            ("Back", None),
        ]
        for i, (name, _) in enumerate(opts, 1):
            cprint(f"  [{i}] {name}", "green")
        choice = input("\nEnter your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(opts):
            name, fn = opts[int(choice) - 1]
            if fn is None:
                return
            try:
                fn()
            except Exception as e:
                cprint(f"Error: {e}", "red")
            input("\nPress Enter...")
        else:
            cprint("Invalid choice.", "red")
            time.sleep(0.5)

# ------------- Entrypoint -------------

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        cprint("\nChalta hu. Goodbye👋🙋‍♂️!Be secure bhailog", "yellow")
        sys.exit(0)
