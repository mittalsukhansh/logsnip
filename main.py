import typer
import os
from dotenv import load_dotenv
from groq import Groq
import re
import json

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = typer.Typer()

LOG_PATTERNS = {
    "syslog":   r"error|failed|panic",
    "nginx":    r"error|crit|alert|emerg",
    "apache":   r"error|crit|alert",
    "journald": r"error|failed|panic|segfault"
}

@app.command("scan")
def scan(
    target: str = typer.Argument(..., help="Path to the log file"),
    log_format: str = typer.Option("syslog", help="Log format: syslog, nginx, apache, journald"),
    output: str = typer.Option(None, help="Save report to a JSON file")
):
    if not os.path.exists(target):
        print(f"File '{target}' not found.")
        raise typer.Exit(1)

    pattern = LOG_PATTERNS.get(log_format.lower(), LOG_PATTERNS["syslog"])

    error_lines = []
    with open(target, "r") as f:
        read_lines = f.readlines()

    for index, line in enumerate(read_lines):
        if re.search(pattern, line, re.IGNORECASE):
            error_lines.append(f"Line {index + 1}: {line.strip()}")

    if not error_lines:
        print("No errors found.")
        return

    log_payload = "\n".join(error_lines)
    print(f"Found {len(error_lines)} issues. Analyzing...")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are an expert Linux sys-admin. "
                    "For every error provided, identify the root cause concisely and provide one single command to fix it. "
                    "Output strictly in JSON format: {'results': [{'line': 'X', 'explanation': '...', 'fix_command': '...'}]}"
                )
            },
            {"role": "user", "content": log_payload}
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    report_content = chat_completion.choices[0].message.content
    
    # Handle Output
    if output:
        with open(output, "w") as f:
            f.write(report_content)
        print(f"\n[+] Report successfully saved to {output}")
    else:
        # This parses the JSON and prints it beautifully for the human eye
        data = json.loads(report_content)
        
        print("\n--- 🛠️  Diagnostic Report ---")
        for item in data.get("results", []):
            print(f"Line {item['line']}:")
            print(f"  Issue: {item['explanation']}")
            print(f"  Fix:   {item['fix_command']}\n")


@app.command("version")
def version():
    print("logsnip v1.0.0")

if __name__ == "__main__":
    app()