---
name: setup
description: Configure MLForge tracing for Claude Code.
disable-model-invocation: true
---

# MLForge Tracing Setup

Run this skill ONLY when the user explicitly asks to configure MLForge tracing.

1. Run `MLForge-claude-code setup --help` and read the available options.
2. Ask the user for each required value. Do not pick defaults silently. All values come from the user.
3. Run `MLForge-claude-code setup` with the collected options.
4. Echo the CLI output. Briefly state the settings file path, tracking URI, experiment, and that tracing is enabled for the next Claude conversation.
