# Implementation Plan - History Compression and Archiving

Implement a system to compress long chat histories using AI summarization and archive original histories as Markdown files organized by date.

## Proposed Changes

### Gemini Agent Implementation ([src/gemini/agent.py](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py))

- Add `HISTORY_MAX_SIZE` global variable (default 100KB).
- Implement [get_history_size(history)](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py#156-164) to estimate the byte size of the chat history.
- Implement [archive_to_markdown(user_id, history)](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py#88-108) to save the current history as a Markdown file in `history/YYYY-MM-DD/user_id.md`.
- Implement [summarize_and_compress(user_id)](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py#109-142) to replace bulky history with an AI-generated summary.
    - **Constraint Handling**: To ensure the summary is small, use a system prompt that explicitly limits word count. If the summary still exceeds `HISTORY_MAX_SIZE`, perform a second, more aggressive truncation or summarize the summary itself.
- Integrate these into the [ask](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py#52-87) flow:
    - Check size before sending new messages.
    - Archive and compress if size limit is exceeded.

### Web Server ([src/server.py](file:///home/brandicast/github/My_LLM_Agent/src/server.py))

- Add `/archives` endpoint to list archived dates.
- Add `/archives/<date>` endpoint to list users with archived history on that date.
- Add `/archives/<date>/<user_id>` endpoint to serve the Markdown content.
- Replace the current `/` route with a friendly HTML portal.
- **Refactoring**: Move the HTML/CSS content into `resources/portal.html`.
- Update [src/server.py](file:///home/brandicast/github/My_LLM_Agent/src/server.py) to serve the portal by reading the template file.

## Verification Plan

### Automated Tests
- Mock the Gemini model to return a fixed summary.
- Simulate sending many messages to trigger the 100KB limit (or lower it for testing).
- Verify files are created in the expected directory structure.

### Manual Verification
- Send long messages to the `/chat` endpoint.
- Check the [history/](file:///home/brandicast/github/My_LLM_Agent/src/gemini/agent.py#165-171) directory for the new folders and [.md](file:///home/brandicast/.gemini/antigravity/brain/8b75e227-c67a-411c-a33b-320cde70aeaa/task.md) files.
- Access the new `/archives` endpoints in the browser to verify readability.
