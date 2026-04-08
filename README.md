# Gemini Agent

A powerful, Gemini-powered chat agent designed with advanced context management and a modular tool system. This project allows for persistent, intelligent conversations with real-world data fetching capabilities.

## 🚀 Key Features

- **Gemini Integration**: Powered by Google's Gemini models for high-quality natural language processing.
- **Context Compression**: Automatically summarizes long conversation histories once they exceed size limits (e.g., 100KB), ensuring the agent retains context without hitting token limits.
- **Modular Tooling**: Integrated plugin system currently supporting:
  - **Weather Tool**: Fetches real-time weather information.
  - **Datetime Tool**: Provides current time across different time zones.
- **Persistence**: Chat histories are serialized and stored, allowing sessions to be resumed seamlessly.
- **Web Interface**: Includes a Flask-based portal for easy interaction and archive viewing.

## 📅 Project Milestones

1.  **Context Compression Engine**: Implementation of the `summarize_and_compress` logic using AI to condense histories.
2.  **Tool Integration**: Addition of the modular plugin loader and the first two core tools (`weather` and `datetime`).

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Google Gemini API Key

### Local Setup
1.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure environment variables**:
    Create a `.env` file from the sample:
    ```bash
    cp .env.sample .env
    # Edit .env with your API_KEY
    ```

### ⚠️ Technical Compatibility Notes

#### Werkzeug Version
The project strictly uses **`Werkzeug==3.1.6`**. 
> [!IMPORTANT]
> Version 3.1.7 and above introduced changes that restrict access between containers using `servicename:port` mappings. For backward compatibility and stable inter-container networking, do not upgrade beyond 3.1.6.

#### WSL & Network Access
When running the agent inside **WSL (Windows Subsystem for Linux)**, the service runs on a virtual network internal to your machine. To access the agent from outside the local machine (e.g., from another device on your LAN), you must configure port forwarding on the Windows host.

Run the following command in a Windows PowerShell (Admin):
```powershell
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=<WSL_IP>
```
*Replace `<WSL_IP>` with the result of `hostname -I` run inside WSL.*

## 🐳 Running with Docker

You can also run the agent as a container:
```bash
docker build -t gemini-agent .
docker run -p 5000:5000 -e API_KEY=your_key_here gemini-agent
```

## 📂 Project Structure

- `src/gemini/agent.py`: Core logic for LLM interaction and context management.
- `src/tools/`: Plugin directory for external capabilities.
- `src/server.py`: Flask application entry point.
- `history/`: Persistent storage for chat sessions and markdown archives.
