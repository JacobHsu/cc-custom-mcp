# screenshot-resize MCP

獨立可攜的 MCP server，把任意網址渲染成 **600×450 PNG** — 設計成一個資料夾 `screenshot-mcp/` 直接丟進任何專案就能用。

## 工具

- **`screenshot_website(url, output_dir, filename, wait_seconds)`** — 用無頭 Chromium 渲染網址（1200×900 viewport，4:3），縮放成 600×450 PNG。
- **`resize_image(image_path, width, height, output_path, maintain_aspect)`** — 用 Lanczos 演算法縮放任意圖片。

## 目錄結構

```
screenshot-mcp/
├── server.py           # FastMCP 工具註冊
├── screenshot.py       # 截圖與縮放實作
├── requirements.txt    # mcp, Pillow, playwright
├── .mcp.sample.json    # 樣板：複製/合併到新專案根的 .mcp.json
├── images/             # 預設輸出目錄
└── README.md
```

跟外層專案零耦合 — 資料夾本身就是可攜的單位。

---

## 檔案歸屬：什麼放哪裡

移植前先弄清楚每個檔案的位置約定：

| 檔案 | 必須位置 | 原因 |
|---|---|---|
| `server.py` | `screenshot-mcp/` | MCP 進入點，被 `--directory screenshot-mcp` 載入 |
| `screenshot.py` | `screenshot-mcp/` | 被 `server.py` import |
| `requirements.txt` | `screenshot-mcp/` | `uv pip install` 建 venv 用 |
| `.venv/` | `screenshot-mcp/` | uv 在此資料夾建立虛擬環境，**不複製，新專案重建** |
| `.mcp.json` | **新專案根** | Claude Code 只讀專案根的 `.mcp.json` |
| `.claude/commands/setup_screenshot_mcp.md` | **新專案根** | Claude Code 只掃描專案根的 `.claude/commands/` |
| `.mcp.sample.json` | `screenshot-mcp/`（樣板） | 樣板跟原始碼放一起，**Claude Code 不會讀它** |
| `README.md` | `screenshot-mcp/` | 跟程式碼綁在一起 |
| `images/` 輸出 | 視 `output_dir` 而定 | 預設 `screenshot-mcp/images/`，可傳 `../images` 寫到專案根 |

**移植 = 三件事：**
1. 複製整個 `screenshot-mcp/` 資料夾（步驟 1）
2. 新增/合併 `.mcp.json` 到新專案根（步驟 2）
3. 複製 `setup_screenshot_mcp.md` 到 `.claude/commands/`（步驟 3，選用但建議）

---

## 移植到新專案

### 1. 複製資料夾

複製**整個 `screenshot-mcp/` 資料夾**（不是只有裡面的檔案）到新專案的根目錄：

```bash
cp -r screenshot-mcp /path/to/new-project/
```

複製後的新專案結構：

```
new-project/
├── .mcp.json           # 步驟 2 會建立或更新
└── screenshot-mcp/     # 這個資料夾，名稱保留
    ├── server.py
    ├── screenshot.py
    ├── requirements.txt
    └── ...
```

（也可以用 `git subtree` 或 submodule — 看你的 repo 策略而定。）若你重新命名資料夾，記得同步修改步驟 2 的 `--directory` 參數。

### 2. 在新專案根目錄的 `.mcp.json` 註冊 server

`.mcp.json` 必須放在**新專案根目錄**（跟 `screenshot-mcp/` 同層）。Claude Code 只會讀專案根的 `.mcp.json` — **不會**讀 `screenshot-mcp/` 裡的任何 JSON。

本資料夾附了 `.mcp.sample.json` 作為樣板，**不要直接放在 `screenshot-mcp/` 下使用**，要複製內容到新專案根的 `.mcp.json`。

兩種情況：

**A. 新專案根還沒有 `.mcp.json`** → 直接複製樣板：

```bash
cp screenshot-mcp/.mcp.sample.json .mcp.json
```

內容如下（已含正確的 `--directory` 寫法）：

```json
{
  "mcpServers": {
    "screenshot-resize": {
      "command": "uv",
      "args": ["run", "--directory", "screenshot-mcp", "python", "server.py"]
    }
  }
}
```

**B. 新專案根已經有 `.mcp.json`**（例如已使用其他 MCP server）→ 把 `screenshot-resize` 那段**合併**進現有的 `mcpServers` 物件，**不要整檔覆蓋**：

```json
{
  "mcpServers": {
    "已存在的-server": { "...": "..." },
    "screenshot-resize": {
      "command": "uv",
      "args": ["run", "--directory", "screenshot-mcp", "python", "server.py"]
    }
  }
}
```

**為什麼要用 `--directory` 而非 `cwd`：** MCP 規範裡頂層 `cwd` 欄位是 optional，部分 client（包含 Windows 上的 Claude Code）不會套用，結果 server 從專案根目錄載入錯誤的 `server.py` 並暴露錯誤工具。`uv run --directory` 是 uv 原生旗標，跨平台行為一致。

### 3. 複製 slash command（選用但建議）

把原專案的 `.claude/commands/setup_screenshot_mcp.md` 複製到新專案根的同樣位置，這樣在新專案內可以直接用 `/setup_screenshot_mcp` 一鍵跑完安裝與驗證流程。

```bash
mkdir -p /path/to/new-project/.claude/commands
cp .claude/commands/setup_screenshot_mcp.md /path/to/new-project/.claude/commands/
```

跳過此步驟不影響 MCP 運作，只是少了 slash command 的便利性。

### 4. 安裝依賴

```bash
cd screenshot-mcp
uv venv
uv pip install -r requirements.txt
uv run playwright install chromium   # ~150MB，每台機器只需一次
```

Playwright 把 Chromium 裝在全域路徑（Windows 是 `~/AppData/Local/ms-playwright/`，macOS/Linux 是 `~/.cache/ms-playwright/`），所以同一台機器上其他專案不用再下載一次。

### 5. Smoke test（選用）

```bash
uv run --directory screenshot-mcp python -c "import asyncio; from screenshot import capture; print(asyncio.run(capture('https://example.com', filename='setup_test.png')))"
```

預期輸出 `Screenshot captured successfully!`，並在 `screenshot-mcp/images/setup_test.png` 產出檔案。

### 6. 在 Claude Code 連線

`/mcp` → 找到 `screenshot-resize` → **connect**。

若之前連線過舊設定，**先 disconnect 再 reconnect** — Claude Code 會把工具列表 cache 在 session 內。

---

## 使用方式

```
用 screenshot_website 把 https://jacobhsu.github.io/team_map/ 存成 mlb_map.png
```

預設輸出 → `screenshot-mcp/images/mlb_map.png`。

要改輸出位置，傳 `output_dir`：

```
用 screenshot_website 把 https://example.com 存成 demo.png，output_dir 設為 ../assets/images
```

需要其他尺寸（例如 2× retina 1200×900），用 `resize_image` 接著處理。

---

## 疑難排解

| 症狀 | 解法 |
|---|---|
| `screenshot-resize` 底下工具列表出現 `fetch_toy_image` | server 載入錯檔案。確認 `.mcp.json` 用了 `--directory screenshot-mcp`，然後 reconnect。 |
| `ModuleNotFoundError: playwright` | 進 `screenshot-mcp/` 重跑 `uv pip install -r requirements.txt`。 |
| `Executable doesn't exist at .../chromium` | 跑 `uv run --directory screenshot-mcp playwright install chromium`。 |
| `page.goto` 出現 `TimeoutError` | 加大 `wait_seconds`，或確認目標 URL 可達。 |
