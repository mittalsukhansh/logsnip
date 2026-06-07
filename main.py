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
    log_format: str = typer.Option("syslog", help="Log format: syslog, nginx, apache, journald"),  # fix 1
    output: str = typer.Option(None, help="Save report to a JSON file")
):
    if not os.path.exists(target):
        print(f"File '{target}' not found.")
        raise typer.Exit(1)

    pattern = LOG_PATTERNS.get(log_format.lower(), LOG_PATTERNS["syslog"])  # fix 1

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

    try:  # fix 4
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Linux sys-admin. For each error provided with a 'Line X' prefix, identify the root cause and provide a fix command. Output in JSON format: {\"results\": [{\"line\": \"X\", \"cause\": \"...\", \"fix\": \"...\"}]}"  # fix 2
                },
                {
                    "role": "user",
                    "content": log_payload
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
    except Exception as e:
        print(f"API call failed: {e}")
        raise typer.Exit(1)

    report_content = chat_completion.choices[0].message.content

    if not report_content:
        print("No response from the model.")
        return

    if output:
        with open(output, "w") as f:
            f.write(report_content)
        print(f"Report saved to {output}")
    else:
        try:  # fix 3
            data = json.loads(report_content)
            print(json.dumps(data, indent=4))
        except json.JSONDecodeError:
            print("Could not parse model response as JSON. Raw output:")
            print(report_content)

@app.command("version")
def version():
    print("logsnip v1.0.0")

if __name__ == "__main__":
    app()