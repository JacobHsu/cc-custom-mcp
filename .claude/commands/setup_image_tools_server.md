### 安裝與啟動 image-tools-server（首次設定用）

本指令會自動完成 uv 環境建立、依賴安裝，並提示使用者連線 MCP server。

---

### Step 1：檢查 uv 是否已安裝

```bash
uv --version
```

如果指令不存在，請提醒使用者先安裝 uv：

```bash
pip install uv
```

或參考 https://docs.astral.sh/uv/，安裝完後重新執行本指令。

---

### Step 2：建立虛擬環境

檢查專案根目錄是否已有 `.venv` 資料夾。

- 若**不存在** → 執行：
  ```bash
  uv venv
  ```
- 若**已存在** → 跳過此步驟，告訴使用者 venv 已就緒。

---

### Step 3：安裝依賴

```bash
uv pip install -r requirements.txt
```

> 提醒使用者：第一次安裝 `rembg` 較重，需耐心等候（會下載 PyTorch 等套件）。

安裝完成後，可選擇性執行 `uv pip list` 確認依賴清單。

---

### Step 4：確認 `.mcp.json` 設定正確

讀取 `.mcp.json`，確認內容為：

```json
{
  "mcpServers": {
    "image-tools-server": {
      "command": "uv",
      "args": ["run", "python", "server.py"]
    }
  }
}
```

如果不一致，提醒使用者本指令預期的設定為 uv 版本，並詢問是否要覆寫。

---

### Step 5：提示使用者連線 MCP server

提醒使用者：
1. 在 Claude Code 執行 `/mcp` 指令
2. 找到 `image-tools-server`
3. 點選 connect / reconnect

---

### Step 6（可選）：本地測試 server 是否能啟動

```bash
uv run python server.py --help
```

或快速試跑（會卡在 stdio 等待 input，按 Ctrl+C 結束）：

```bash
uv run python server.py
```

若出現 `ModuleNotFoundError`，回到 Step 3 重新安裝依賴。
