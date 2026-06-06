# MCP 圖片工具 Server

本 repo 同時提供 **兩個獨立的 MCP server**，皆可在 Claude Code 中使用：

| Server | 用途 | 子資料夾 |
|--------|------|----------|
| **`image-tools-server`** | 玩具圖片下載、縮放、AI 去背、裁切 | 專案根目錄 |
| **`screenshot-resize`** | 網頁截圖（portfolio 縮圖用） | [`screenshot-mcp/`](./screenshot-mcp/) |

兩者透過根目錄 [`.mcp.json`](./.mcp.json) 同時註冊，互不干擾。

- Anthropic MCP Python SDK：https://github.com/modelcontextprotocol/python-sdk

## 環境需求

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/)
- Claude Code（MCP 客戶端）

---

## Server 1：`image-tools-server`（圖片處理）

### 功能

| 工具 | 說明 |
|------|------|
| 🧸 `fetch_toy_image` | 透過 DuckDuckGo 搜尋下載玩具圖片，一次 1–10 張，自動加上 "toy" 提升搜尋品質 |
| 🖼️ `resize_image` | Lanczos 重採樣縮放，可選保持長寬比 |
| ✂️ `remove_background_as_png` | 用 `rembg` AI 模型自動去背，可選 u2net / u2netp / silueta / isnet-general-use |
| 📐 `crop_image` | 裁切成圓形、方形、矩形 |

### 安裝與啟動

1. 用 Claude Code 開啟此專案資料夾
2. 執行 slash command：

   ```
   /setup_image_tools_server
   ```

3. 完成後執行 `/mcp` 連線 `image-tools-server`

> 詳細步驟（檢查 uv、建 venv、裝依賴、確認 `.mcp.json`）見 [.claude/commands/setup_image_tools_server.md](.claude/commands/setup_image_tools_server.md)

### 使用範例

```
請用 fetch_toy_image 工具下載 3 張機器人玩具圖片到 ./images 資料夾。
```

```
幫我把 ./images/robot_toy_1.jpg 縮放到 800x600。
```

```
請把 ./images/robot_toy_1.jpg 的背景去掉，存成 PNG。
```

```
把 ./images/robot_toy_1.jpg 裁切成圓形。
```

組合用法：

> download 3 different random pictures of single castle. resize below 150px either the width or the length.

---

## Server 2：`screenshot-resize`（網頁截圖）

為 [card-personal-portfolio](https://github.com/JacobHsu/card-personal-portfolio) 量身設計，子專案可整包複製到別的 repo 獨立使用。

### 功能

| 工具 | 說明 |
|------|------|
| 📸 `screenshot_website` | 用 Playwright Chromium 渲染 URL，輸出 **600×450 PNG**（viewport 1200×900 等比縮放） |
| 🖼️ `resize_image` | 通用 Lanczos 縮放（與 Server 1 的同名工具獨立） |

### 安裝與啟動

1. 在 Claude Code 執行 slash command：

   ```
   /setup_screenshot_mcp
   ```

   此指令會：
   - 在 `screenshot-mcp/` 建立獨立 `.venv`
   - 安裝 `mcp` / `Pillow` / `playwright`
   - 下載 Chromium 二進位（首次約 150MB，存放於 `~/AppData/Local/ms-playwright/`，跨 venv 共用）
   - 跑一次 smoke test 驗證 pipeline

2. 完成後執行 `/mcp` 連線 `screenshot-resize`

> 詳細步驟見 [.claude/commands/setup_screenshot_mcp.md](.claude/commands/setup_screenshot_mcp.md) 與 [screenshot-mcp/README.md](./screenshot-mcp/README.md)。

### 使用範例

```
用 screenshot_website 把 https://jacobhsu.github.io/team_map/ 存成 mlb_map.png
```

輸出 → `screenshot-mcp/images/mlb_map.png`（600×450 PNG）。

想直接輸出到專案根目錄的 `images/`：

```
用 screenshot_website 把 https://example.com 存成 demo.png，output_dir="../images"
```

---

## 共用：重啟、結構、疑難排解

### 重啟 Server

修改 `server.py` 後：

- **只改 Python 程式碼** → 直接在 Claude Code 用 `/mcp` 重新連線即可，不需重裝依賴
- **修改 `requirements.txt`** → 執行 `uv pip install -r requirements.txt` 後再 `/mcp` 重連
- 也可使用內附的 slash command：`/rebuild_restart_image_tools_server`

### 檔案結構

```
cc-custom-mcp/
├── server.py                  # image-tools-server 主程式
├── requirements.txt           # image-tools-server 依賴
├── .mcp.json                  # Claude Code MCP 設定（兩個 server）
├── screenshot-mcp/            # screenshot-resize 子專案（可整包搬走）
│   ├── server.py
│   ├── screenshot.py
│   ├── requirements.txt
│   └── README.md
├── .claude/
│   └── commands/
│       ├── setup_image_tools_server.md
│       ├── setup_screenshot_mcp.md
│       └── rebuild_restart_image_tools_server.md
├── images/                    # image-tools-server 工作目錄
├── input/                     # 輸入圖片
├── output/                    # 輸出圖片
└── README.md                  # 本文件
```

### Python 依賴

**`image-tools-server`** (`requirements.txt`)：

- `mcp` — Anthropic Model Context Protocol SDK
- `Pillow` — 圖片處理
- `requests` — HTTP 下載
- `duckduckgo-search` — 圖片搜尋
- `rembg` — AI 去背模型

**`screenshot-resize`** (`screenshot-mcp/requirements.txt`)：

- `mcp`、`Pillow`、`playwright`

### 疑難排解

| 問題 | 處理方式 |
|------|----------|
| `uv: command not found` | `pip install uv`，或重新開啟 terminal 讓 PATH 生效 |
| `duckduckgo-search` 異常 | `uv pip install -U duckduckgo-search` |
| 圖片下載失敗 | 檢查網路；部分來源可能擋掉請求，工具會自動重試 |
| 首次去背很慢 | `rembg` 首次會下載 AI 模型（約 100MB+） |
| Playwright `Executable doesn't exist` | 進到 `screenshot-mcp/` 跑 `uv run playwright install chromium` |
| Claude Code 看不到 Server | 確認用 Claude Code 打開的是根目錄、`.mcp.json` 存在、`uv` 在 PATH 中，修改後 `/mcp` 重連 |
| 工具執行失敗 | 看 Claude Code 顯示的 stderr 訊息；確認對應子專案的 venv 與依賴 (`uv pip list`) |

---

## 開發

### 新增工具到 `image-tools-server`

在 `server.py` 加入新的 `@mcp.tool()` 函式：

```python
@mcp.tool()
async def your_new_tool(param1: str, param2: int = 10) -> str:
    """工具的功能說明 — 會顯示給 Claude 看到。"""
    # 實作
    return "結果訊息"
```

新增後在 Claude Code 用 `/mcp` 重連即可。

### 手動啟動 Server（除錯用）

```bash
# image-tools-server
uv run python server.py

# screenshot-resize
cd screenshot-mcp && uv run python server.py
```

Server 會以 stdio 模式啟動，可用 MCP inspector 或手動傳 JSON-RPC 請求測試。

---

## License

僅供學習與開發用途。請尊重圖片來源網站的服務條款與 AI 模型的授權條款。

> **注意**：本工具會從網路下載圖片並使用 AI 模型處理，請合理使用並尊重來源網站的版權與服務條款。
