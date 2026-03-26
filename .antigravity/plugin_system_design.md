# Design Proposal: Modular Plugin System

This design allows the "Bread" AI agent to perform external actions (weather, stocks, etc.) without hardcoding them into the core logic. It uses **Gemini Function Calling** to dynamically select and execute independent features.

---

## 🏗️ Architecture Overview

The system consists of three main components:
1.  **Core Agent**: Manages the conversation and handles tool-call requests from Gemini.
2.  **Plugin Registry**: Automatically discovers and loads plugins from a dedicated directory.
3.  **Independent Plugins**: Self-contained modules that perform specific tasks.

---

## 🛠️ Component Design

### 1. Plugin Base Class
Define a standard interface for all features. Every plugin will:
-   **Declare its purpose**: A clear description that Gemini uses to decide when to call it.
-   **Define its parameters**: A JSON schema describing what inputs it needs (e.g., `location` for weather).
-   **Execute the task**: A Python function that performs the logic (API calls, calculations, etc.) and returns the result.

### 2. Plugin Discovery (`src/tools/`)
Plugins are stored in a `tools/` directory. On startup, the agent:
-   Scans the directory for Python files.
-   Loads each plugin dynamically.
-   Collects all "declarations" to send to the Gemini API.

### 3. Execution Flow
1.  **User Asks**: "國王麵包，今天的台北天氣怎麼樣？" (What's the weather in Taipei?)
2.  **Model Decides**: Gemini recognizes the intent and returns a **Function Call** for `get_weather(location='Taipei')`.
3.  **Agent Executes**: The core agent finds the `WeatherPlugin` in the registry and runs its `execute` method.
4.  **Agent Responds to AI**: The agent sends the result (e.g., "晴天, 25度") back to Gemini.
5.  **AI Final Response**: Gemini uses the info to answer in character: "哇！台北今天是大晴天喔，25度真舒服，適合在雲上睡覺！"

---

## 🌟 Benefits of this Design

-   **Zero-Dependency**: Adding a new feature (e.g., Stock check) only requires adding a new file in `tools/`. You don't need to touch [agent.py](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py).
-   **Scalable**: You can add dozens of tools without making the main code complex.
-   **Character Consistency**: Because the tool output is piped back through Gemini, "Bread" always stays in character when delivering the information.
-   **Testable**: Each plugin can be tested independently of the AI and the web server.

---

## 📂 Proposed File Structure

```text
src/
├── gemini/
│   └── agent.py        # Updated to handle tool calls and registries
└── tools/
    ├── __init__.py     # Registry and discovery logic
    ├── base_tool.py    # Interface definition
    ├── weather.py      # Independent weather plugin
    ├── datetime.py     # Independent time reporter
    └── stocks.py       # Independent stock checker
```

---

## ⚙️ Configuration Management

To keep each feature truly "plug and play," we recommend a **hybrid configuration strategy**:

### 1. Secrets (API Keys)
- Use the central [.env](file:///home/brandicast/github/My_LLM_Agent/.env) file at the project root for ALL keys (e.g., `WEATHER_API_KEY`).
- This keeps sensitive credentials out of the code and Git history.

### 2. Feature-Specific Settings (URLs, Limits, etc.)
We recommend the **Self-Contained Plugin Directory** approach:
```text
src/tools/
└── weather/
    ├── plugin.py       # Logic (reads config.json)
    └── config.json     # Specific settings (endpoints, defaults)
```
- **Why**: This is the most modular. To add a feature, you just drop in a folder. To remove it, you delete the folder.

Each plugin's `plugin.py` would be responsible for loading its own `config.json` relative to its file path.

---

## 📦 Dependency Isolation in Docker

Since each plugin might require different Python packages (e.g., `requests` for weather, `pandas` for stocks), we recommend using **Plugin-Specific [requirements.txt](file:///home/brandicast/github/My_LLM_Agent/requirements.txt)** files combined with a smart Docker build step.

### 1. Structure
Each plugin directory should contain its own dependency list:
```text
src/tools/
└── weather/
    ├── plugin.py
    ├── config.json
    └── requirements.txt  # Contains: requests, beautifulsoup4
```

### 2. Dockerfile Optimization
Instead of manually updating the main [requirements.txt](file:///home/brandicast/github/My_LLM_Agent/requirements.txt), we update the [Dockerfile](file:///home/brandicast/github/My_LLM_Agent/Dockerfile) to automatically discover and install all plugin-specific dependencies:

```dockerfile
# 1. Install core dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Automatically find and install all plugin requirements
# This avoids cluttering the main requirements.txt and ensures 
# each plugin is self-contained.
COPY src/tools src/tools
RUN find src/tools -name "requirements.txt" -exec pip install --no-cache-dir -r {} +
```

### 3. Benefits
- **Strict Modularity**: When you delete a plugin folder, you aren't left with "ghost" dependencies in your main [requirements.txt](file:///home/brandicast/github/My_LLM_Agent/requirements.txt).
- **Improved Caching**: Docker layers for core dependencies remain intact even if you add a new plugin with its own small requirements list.
- **Clean Development**: Developers only need to worry about the requirements of the specific tool they are building.
