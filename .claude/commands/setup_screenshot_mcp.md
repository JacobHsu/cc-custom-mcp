---
description: 安裝與啟動 screenshot-resize MCP server（本專案 screenshot-mcp/ 子資料夾）
---

### 安裝與啟動 screenshot-resize MCP

本指令在 `screenshot-mcp/` 子資料夾建立 venv、安裝依賴、確保 Playwright Chromium 可用，並驗證 `.mcp.json` 設定。

---

### Step 1：確認 uv 已安裝

```bash
uv --version
```

如指令不存在 → 提醒：`pip install uv`，或參考 https://docs.astral.sh/uv/。

---

### Step 2：建立 `screenshot-mcp/.venv`

檢查 `screenshot-mcp/.venv` 是否存在。

- 不存在：`cd screenshot-mcp && uv venv`
- 已存在 → 跳過。

---

### Step 3：安裝 Python 依賴

```bash
cd screenshot-mcp && uv pip install -r requirements.txt
```

驗證：

```bash
cd screenshot-mcp && uv pip list | grep -iE "playwright|mcp|pillow"
```

預期看到 `mcp`、`pillow`、`playwright` 三項。

---

### Step 4：確保 Playwright Chromium 已安裝

Chromium 二進位裝在全域路徑（Windows: `~/AppData/Local/ms-playwright/`，macOS/Linux: `~/.cache/ms-playwright/`），與 venv 無關、可跨專案共用。

偵測：

- Windows (Git Bash)：`ls ~/AppData/Local/ms-playwright 2>/dev/null | grep -E "^chromium-" | head -3`
- macOS / Linux：`ls ~/.cache/ms-playwright 2>/dev/null | grep -E "^chromium-" | head -3`

若沒有任何 chromium 目錄 → 執行（首次下載約 150MB）：

```bash
uv run --directory screenshot-mcp playwright install chromium
```

---

### Step 5：確認專案根 `.mcp.json` 設定正確

讀取根目錄 `.mcp.json`，`mcpServers` 內必須包含：

```json
"screenshot-resize": {
  "command": "uv",
  "args": ["run", "--directory", "screenshot-mcp", "python", "server.py"]
}
```

**關鍵：必須用 `--directory` 旗標**，不要用頂層的 `cwd` 欄位。某些 MCP client（含 Claude Code on Windows）不會套用 `cwd`，導致載入到根目錄的 `server.py`，暴露錯誤的工具（例如出現 `fetch_toy_image` 而非 `screenshot_website`）。

若缺失或寫法錯誤 → 合併進 `mcpServers`，**不要覆蓋既有其他 entry**。

---

### Step 6：本地 smoke test

```bash
uv run --directory screenshot-mcp python -c "import asyncio; from screenshot import capture; print(asyncio.run(capture('https://example.com', filename='setup_test.png')))"
```

成功會輸出 `Screenshot captured successfully!`，並產出 `screenshot-mcp/images/setup_test.png`。

驗證 server 暴露的工具名稱正確：

```bash
uv run --directory screenshot-mcp python -c "from server import mcp; import asyncio; print([t.name for t in asyncio.run(mcp.list_tools())])"
```

預期：`['screenshot_website', 'resize_image']`。若看到 `fetch_toy_image` → 回 Step 5 修正 `.mcp.json`。

常見錯誤：

- `ModuleNotFoundError` → 回 Step 3
- `Executable doesn't exist` → 回 Step 4
- 網路逾時 → 換 URL 重試

---

### Step 7：在 Claude Code 連線

1. `/mcp`
2. 找到 `screenshot-resize`
3. 若已連線且工具錯誤 → 先 **disconnect** 再 **connect**（client 會 cache tool list）

---

### 使用範例

```
用 screenshot_website 把 https://jacobhsu.github.io/team_map/ 存成 mlb_map.png
```

輸出：`screenshot-mcp/images/mlb_map.png`（600×450 PNG）

要輸出到別處：呼叫時加 `output_dir="../images"`。
