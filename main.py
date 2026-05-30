import typer
import os
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
client = Groq(api_key=os.environ.get("key"))

app = typer.Typer()

@app.command("scan")
def scan(target: str = typer.Argument("syslog")):
    if not os.path.exists(target):
        print(f"File '{target}' not found.")
        raise typer.Exit(1)

    error_lines = []
    with open(target, "r") as f:
        read_lines = f.readlines()

    for index, line in enumerate(read_lines):
        if re.search(r"error|failed|panic", line, re.IGNORECASE):
            error_lines.append(f"Line {index + 1}: {line.strip()}")

    if error_lines:
        log_payload = "\n".join(error_lines)
        print(f"Found {len(error_lines)} critical errors:")  # fix: added space

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Linux sys-admin. I will provide log lines with 'Line X' prefixes. For each error, state the line number, the root cause, and the fix command in next line (Fix:). Be brief, no conversational filler." 
                },
                {
                    "role": "user",
                    "content": log_payload
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        print(chat_completion.choices[0].message.content)
    else:
        print("No errors found.")


@app.command("version")  # 👈 add this dummy second command
def version():
    """Show tool version."""
    print("logsnip v1.0.0")



    
if __name__ == "__main__":
    app()