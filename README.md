#  Sophisticated Helper+

**AI-powered CLI assistant for developers, security researchers, and engineers.**  
Created by **Sachin Jadhav** — GitHub: [kffod/Sophisticated‑Helper](https://github.com/kffod/Sophisticated-Helper)

<img width="1251" height="695" alt="image" src="https://github.com/user-attachments/assets/14e8f472-18fd-4b2f-aac1-09877b0696bf" />


---

##  Features
- **Stylish UX**: ASCII animations, matrix rain, themes, persona switching  
- **Security Tools**:
  - Code reviews (LLM + offline fallback with Bandit/Pylint/grep)
  - Auto‑fix mode (LLM or `black`/`isort`)
  - Pentest assistance (with disclaimer)
  - Exploit lab generator (for local learning)
- **Developer Tools**:
  - Code generation (secure & production-ready)
  - Shell command fixer
  - General assistant (dev/security answers)
  - Cheat-sheet generator
  - One-liner guru
- **Utilities**:
  - Clipboard copy
  - Voice readout (via `pyttsx3`)
  - Logs & exports (`logs/`, `exports/`)
  - Update checker (GitHub-based)

---

##  Installation & Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/kffod/Sophisticated-Helper.git
   cd Sophisticated-Helper
   chmod +x sophisticated_helper_plus.py
   ```

2. **Install dependencies**:
   ```bash
   pip install requests pyperclip pyttsx3 black isort pylint bandit
   ```

3. **Fix Windows line endings (if needed)**:
   ```bash
   sudo apt install dos2unix -y   # if not installed
   dos2unix sophisticated_helper_plus.py
   ```

4. **Set up environment variables**:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   export GEMINI_MODEL="gemini-1.5-flash-latest"
   export GITHUB_RAW_VERSION_URL="https://raw.githubusercontent.com/kffod/Sophisticated-Helper/main/VERSION"
   ```

5. **Run the CLI**:
   ```bash
   ./sophisticated_helper_plus.py
   ```

---

##  Quick Reference

| Menu Option | What It Does |
|-------------|--------------|
| General Assistant | Ask anything — dev/security/product Q&As |
| Pentest Assistant | Guided pentest walkthroughs (authorized use only) |
| Code Review | Review a file/dir (LLM + offline fallback) |
| Fix Shell Command | Fix broken Linux commands with explanation |
| Generate Code | Write complete programs based on your spec |
| Cheat‑sheet Generator | Generate Markdown cheat-sheets |
| One-liner Guru | Explain concepts in one line + bullet points |
| Exploit Lab Mode | Generate vulnerable demo apps for learning |
| Settings | Choose themes, persona, voice, spinner |
| Update Checker | Check for newer versions on GitHub |

---

##  Output Locations

- `logs/`: Stores expert answers and chat history  
- `exports/`: Contains generated code, reports, cheat-sheets, labs

---

##  Personas

Switch assistant mode via Settings:
- **Architect** — Strategic and pragmatic
- **RedTeam** — Security-oriented guidance
- **Teacher** — Simple, analogy-rich explanations
- **OpsSRE** — Observability and resilience-focused

---

##  Legal Notice

- **Pentest workflows require explicit authorization.**
- **Use responsibly.** The author is not liable for misuse.

---

##  What’s Next?

- Plugin system for custom workflow extensions  
- More exploit lab templates (e.g., FastAPI, Next.js)  
- Dockerized version for easy deployment

---

##  Author

**Sachin Jadhav** — GitHub: [kffod](https://github.com/kffod)  
Sophisticated Helper+ — Your AI-powered CLI sidekick for coding & security
