### Check whether uv is installed
Use the command below to check whether uv is installed.
```bash
uv --version
```

If not, remind the user to install uv first (`pip install uv` or see https://docs.astral.sh/uv/) and abort the command execution here.

### Sync dependencies to reflect changes in python code or requirements
```bash
uv pip install -r requirements.txt
```

If the virtual environment does not exist yet, create it first:
```bash
uv venv
uv pip install -r requirements.txt
```

### Restart the MCP server
Remind the user to use the ```/mcp``` command, look for ```image-tools-server``` and reconnect.
