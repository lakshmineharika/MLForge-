# MLForge Claude Code Integration

This module provides automatic tracing integration between Claude Code and MLForge.

## Module Structure

- **`config.py`** - Configuration management (settings files, environment variables)
- **`hooks.py`** - Claude Code hook setup and management
- **`cli.py`** - MLForge CLI commands (`MLForge autolog claude`)
- **`tracing.py`** - Core tracing logic and processors
- **`hooks/`** - Hook implementation handlers

## Installation

```bash
pip install MLForge
```

## Usage

Set up Claude Code tracing in any project directory:

```bash
# Set up tracing in current directory
MLForge autolog claude

# Set up tracing in specific directory
MLForge autolog claude -d ~/my-project

# Set up with custom tracking URI
MLForge autolog claude -u file://./custom-mlruns
MLForge autolog claude -u sqlite:///MLForge.db

# Set up with Databricks
MLForge autolog claude -u databricks -e 123456789

# Check status
MLForge autolog claude --status

# Disable tracing
MLForge autolog claude --disable
```

## How it Works

1. **Setup**: The `MLForge autolog claude` command configures Claude Code hooks in a `.claude/settings.json` file
2. **Automatic Tracing**: When you use the `claude` command in the configured directory, your conversations are automatically traced to MLForge
3. **View Traces**: Use `MLForge server` to view your conversation traces

## Configuration

The setup creates two types of configuration:

### Claude Code Hooks

- **PostToolUse**: Captures tool usage during conversations
- **Stop**: Processes complete conversations into MLForge traces

### Environment Variables

- `MLForge_CLAUDE_TRACING_ENABLED=true`: Enables tracing
- `MLForge_TRACKING_URI`: Where to store traces (defaults to local `.claude/MLForge/runs`)
- `MLForge_EXPERIMENT_ID` or `MLForge_EXPERIMENT_NAME`: Which experiment to use

## Examples

### Basic Local Setup

```bash
MLForge autolog claude
cd .
claude "help me write a function"
MLForge server --backend-store-uri sqlite:///MLForge.db
```

### Databricks Integration

```bash
MLForge autolog claude -u databricks -e 123456789
claude "analyze this data"
# View traces in Databricks
```

### Custom Project Setup

```bash
MLForge autolog claude -d ~/my-ai-project -u sqlite:///MLForge.db -n "My AI Project"
cd ~/my-ai-project
claude "refactor this code"
MLForge server --backend-store-uri sqlite:///MLForge.db
```

## Troubleshooting

### Check Status

```bash
MLForge autolog claude --status
```

### Disable Tracing

```bash
MLForge autolog claude --disable
```

### View Raw Configuration

The configuration is stored in `.claude/settings.json`:

```bash
cat .claude/settings.json
```

## Requirements

- Python 3.10+ (required by MLForge)
- MLForge installed (`pip install MLForge`)
- Claude Code CLI installed
