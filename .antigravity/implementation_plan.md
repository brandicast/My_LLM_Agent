# Implement Datetime Plugin

The goal is to implement a Datetime plugin for the "Bread" AI agent that supports inquiring about the current date and time locally, as well as in other cities, following the architecture outlined in [.antigravity/plugin_system_design.md](file:///home/brandicast/github/My_LLM_Agent/.antigravity/plugin_system_design.md).

## User Review Required
> [!IMPORTANT]
> - **Timezone Identification**: It is most reliable if we rely on Gemini's function calling to directly pass **IANA standard timezone strings** (e.g., `America/New_York`, `Asia/Taipei`) as the parameter instead of raw city names ("New York", "Taipei"). This avoids having to implement custom city-to-timezone lookups or use Geocoding APIs. Do you agree with this approach?
> - **Python Version & Libraries**: Python 3.9+ includes the built-in `zoneinfo` module. For seamless cross-platform usage (particularly on Windows) it usually requires the `tzdata` package. We will add `tzdata` to the tool's isolated `requirements.txt`.
> - **Plugin Core Loading**: The [agent.py](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py) does not currently possess the `src/tools/` registry logic mentioned in `plugin_system_design.md`. Should this plan also include updating `agent.py` to automatically load tools, or are you planning to handle the plugin core loading system separately/afterward? The current plan assumes the plugin module architecture itself is ready.

## Proposed Changes

### Datetime Plugin Module

#### [NEW] src/tools/datetime/plugin.py
- **Compliance with loader.py**:
  - The `loader.py` script automatically discovers modules containing a `plugin.py` file. It expects the module to have a standalone function `get_tools()` that returns a list of callable functions.
  - Gemini SDK automatically builds tool schemas by inspecting standard Python docstrings, type hints, and function arguments.
- **Implementation**:
  - Define `get_current_datetime(city: str = None) -> str` (or `timezone: str = None`).
  - Write a comprehensive docstring describing the function's purpose and its `city` (or `timezone`) parameter so Gemini knows exactly when and how to call it.
  - Implement timezone resolution logic using Python's `datetime` and `zoneinfo`.
  - Export the tool by defining:
    ```python
    def get_tools():
        return [get_current_datetime]
    ```

#### [NEW] src/tools/datetime/requirements.txt
- Add `tzdata` to support standard IANA timezone lookups cross-platform, especially if Windows support is needed.

## Verification Plan

### Automated Tests
- If a testing framework is configured (like `pytest`), we will add a unit test asserting `get_current_datetime("Asia/Taipei")` returns a predictably formatted timestamp.
- We will test that calling it without a timezone parameter correctly outputs the default time from `config.json`.

### Manual Verification
- Once the plugin is integrated, prompt the agent with: "現在台灣時間幾點？" (What time is it in Taiwan now?)
- Prompt the agent with: "紐約現在的日期與時間？" (What's the date and time in New York right now?)
- Ensure the agent effectively maps the prompt to invoke the `get_current_datetime` tool with the appropriate IANA timezone strings, and subsequently returns an in-character response containing the accurate time.
