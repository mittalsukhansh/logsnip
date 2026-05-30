# logsnip
A lightweight, AI-powered Linux log diagnostic tool.

## Features
- **Smart Filtering**: Uses Regex to isolate only 'error', 'failed', or 'panic' logs.
- **AI-Powered Analysis**: Uses Llama 3.3 to provide root cause identification and fix commands.
- **Bulletproof**: Built with stability checks to handle missing files and empty logs gracefully.

## Installation
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/logsnip.git`
2. Install dependencies: `pip install typer groq python-dotenv`
3. Set your environment variables: Create a `.env` file and add `key=YOUR_GROQ_API_KEY`

## Usage
`python main.py scan <path_to_log_file>`

## Built With
- [Typer](https://typer.tiangolo.com/) for the CLI interface.
- [Groq API](https://console.groq.com/) for fast LLM inference.