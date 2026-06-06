# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an MCP (Model Context Protocol) Image Tools Server that provides image processing capabilities to Claude Code. The server is implemented using the FastMCP framework and runs locally via `uv`.

## Architecture

**Core Components:**
- `server.py` - Main MCP server implementation using FastMCP framework
- `.mcp.json` - MCP server configuration for Claude Code integration (uses `uv run python server.py`)
- `requirements.txt` - Python dependencies (PIL, requests, duckduckgo-search)

**MCP Tools Available:**
- `fetch_toy_image` - Downloads toy-related images via DuckDuckGo search
- `resize_image` - Resizes images with optional aspect ratio preservation

**Directory Structure:**
- `./images/` - Working directory for downloaded and processed images

## Development Commands

### Environment Setup
```bash
# Create the virtual environment (first time only)
uv venv

# Install / sync dependencies
uv pip install -r requirements.txt
```

### MCP Server Management
```bash
# Run the server locally (stdio mode)
uv run python server.py
```

### Claude Code Integration
After making changes to the server code:
1. (If `requirements.txt` changed) run `uv pip install -r requirements.txt`
2. Use `/mcp` command in Claude Code
3. Reconnect to `image-tools-server`

Slash commands available under `.claude/commands/`:
- `/setup_image_tools_server` - first-time setup (uv venv + install)
- `/rebuild_restart_image_tools_server` - re-sync deps after changes

## Implementation Details

**FastMCP Framework**: The server uses `@mcp.tool()` decorators to register async functions as MCP tools. Each tool function returns a string result that gets wrapped in TextContent by the framework.

**Image Processing Pipeline**:
- Uses PIL (Pillow) for basic image operations
- DuckDuckGo search integration for image fetching
- All image outputs default to `./images/` directory

**Error Handling**: Each tool validates input files exist and provides descriptive error messages. Network operations include timeout and retry logic.

## Configuration Notes

The `.mcp.json` file configures the server for Claude Code using `uv run python server.py`. The server is identified as `image-tools-server` in Claude Code.

## Adding New Tools

To add new image processing tools:
1. Define async function with `@mcp.tool()` decorator
2. Include proper parameter typing and docstring
3. Follow existing error handling patterns
4. Default output to `./images/` directory unless specified
5. Reconnect via `/mcp` in Claude Code

## Dependencies Management

Core dependencies in `requirements.txt`:
- `mcp>=1.0.0` - MCP SDK
- `Pillow>=10.0.0` - Image processing
- `requests>=2.31.0` - HTTP client
- `duckduckgo-search>=6.1.0` - Image search
