---
trigger: always_on
---

Environment Rule:

This project uses a local virtual environment in .venv/.

Before executing any terminal command, verify if the virtual environment is active.

If .venv does not exist, run python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt.

Always use source .venv/bin/activate at the start of every terminal session.