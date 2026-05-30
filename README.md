# logsnip

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![LLM](https://img.shields.io/badge/LLM-Llama%203.3%2070B-orange)

> Diagnosing Linux system failures manually wastes hours. logsnip automates log triage using AI — isolating critical errors and delivering root-cause analysis in seconds.

---

## Motivation

Manual log analysis during system failures is slow, error-prone, and requires deep domain knowledge. logsnip was built to reduce Mean Time To Repair (MTTR) by automating the triage step — letting developers and sysadmins focus on fixing, not searching.

---

## Features

- **Intelligent Log Triage** — Regex pipeline isolates high-severity events (`error`, `failed`, `panic`) from thousands of lines in milliseconds.
- **AI-Powered Diagnostics** — Sends flagged lines to Llama 3.3 70B (via Groq) and returns concise root-cause analysis with actionable fix commands.
- **Fault-Tolerant CLI** — Gracefully handles missing files and clean logs without crashing.
- **Plug-and-Play Interface** — One command to scan any log file. Minimal configuration — just an API key.

---

## Prerequisites

- **Python 3.8+**
- A free **Groq API key** — get one at [console.groq.com](https://console.groq.com/)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/mittalsukhansh/logsnip.git
   cd logsnip
   ```

2. **Create a virtual environment** *(recommended)*

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**

   Create a `.env` file in the project root:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   > **Note:** The `.env` file is git-ignored by default — your key stays local.

---

## Usage

### Scan a log file

```bash
python main.py scan <path_to_log_file>
```

**Example:**

```bash
python main.py scan /var/log/syslog
```

If no file path is provided, it defaults to `syslog` in the current directory:

```bash
python main.py scan
```

### Check the version

```bash
python main.py version
```

```
logsnip v1.0.0
```

### Get help

```bash
python main.py --help
python main.py scan --help
```

---

## Example

Given a log file like this:

```
May 25 17:35:12 kernel: [ 0.000000] Linux version 5.15.0-generic
May 25 17:36:01 systemd[1]: Started System Logging Service.
May 25 17:38:45 NetworkManager[845]: <error> [1685000000.1234] wifi: AP connection failed
```

Running:

```bash
python main.py scan dummy.log
```

Produces output similar to:

```
Found 1 critical errors:

Line 3: wifi: AP connection failed
Root cause: NetworkManager failed to associate with the wireless access point.
Fix:
sudo systemctl restart NetworkManager
```

> The AI response will vary — it adapts to the actual log content.

---

## Project Structure

```
logsnip/
├── main.py            # CLI entry point (scan + version commands)
├── requirements.txt   # Python dependencies
├── .env               # Groq API key (not tracked by git)
├── .gitignore         # Ignores .env, __pycache__, .venv, *.log
├── dummy.log          # Sample log file for testing
├── LICENSE            # MIT License
└── README.md
```

---

## How It Works

1. **Read** — Opens the target log file and reads all lines.
2. **Filter** — Uses a regex (`error|failed|panic`, case-insensitive) to extract only the problematic lines, preserving their original line numbers.
3. **Diagnose** — Sends the filtered lines to the Groq API (Llama 3.3 70B) with a system prompt instructing the model to act as a Linux sys-admin and return concise root causes with fix commands.
4. **Display** — Prints the AI-generated diagnosis to the terminal.

---

## Built With

| Tool | Purpose |
|------|---------|
| [Typer](https://typer.tiangolo.com/) | CLI framework |
| [Groq](https://console.groq.com/) | Fast LLM inference API |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |
| [Llama 3.3 70B](https://huggingface.co/meta-llama) | Language model for log analysis |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
