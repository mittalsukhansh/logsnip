# logsnip

> A lightweight, AI-powered CLI tool that scans log files for critical errors and uses an LLM to diagnose root causes and suggest fixes — instantly.

---

## Features

- **Smart Filtering** — Regex-based extraction of lines containing `error`, `failed`, or `panic` (case-insensitive).
- **AI-Powered Diagnostics** — Sends flagged lines to Llama 3.3 70B (via Groq) and gets back concise root causes + fix commands.
- **Graceful Error Handling** — Handles missing files and clean logs without crashing.
- **Simple CLI** — One command to scan any log file. No configuration needed beyond an API key.

---

## Prerequisites

- **Python 3.8+**
- A free **Groq API key** — get one at [console.groq.com](https://console.groq.com/)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/logsnip.git
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
   pip install typer groq python-dotenv
   ```

4. **Set up your API key**

   Create a `.env` file in the project root:

   ```
   key=YOUR_GROQ_API_KEY
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
├── main.py          # CLI entry point (scan + version commands)
├── .env             # Groq API key (not tracked by git)
├── .gitignore       # Ignores .env, __pycache__, .venv, *.log
├── dummy.log        # Sample log file for testing
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

This project is open source. Feel free to use, modify, and distribute.