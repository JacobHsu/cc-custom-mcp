# MCP 圖片工具 Server

一個 Model Context Protocol (MCP) Server，為 Claude Code 提供圖片處理工具。功能包含：從網路下載玩具圖片、調整圖片大小、AI 去背、以及圖片裁切。

- Anthropic MCP Python SDK：https://github.com/modelcontextprotocol/python-sdk

## 功能

### 🧸 玩具圖片下載 (`fetch_toy_image`)
- 透過 DuckDuckGo 搜尋下載玩具相關圖片
- 自動在搜尋詞前加上 "toy" 提升搜尋品質
- 一次可下載 1–10 張圖片
- 圖片儲存到指定資料夾

### 🖼️ 圖片縮放 (`resize_image`)
- 將圖片調整到指定尺寸
- 可選擇是否保持長寬比
- 採用 Lanczos 演算法重採樣，畫質高
- 支援常見圖片格式

### ✂️ AI 去背 (`remove_background_as_png`)
- 使用 rembg 模型自動去背
- 可選擇模型：u2net、u2netp、silueta、isnet-general-use
- 輸出透明背景的 PNG
- 保留主體細節

### 📐 圖片裁切 (`crop_image`)
- 將圖片裁切成圓形、方形、矩形

### 📸 網站截圖 (`screenshot_website`)
- 用 headless Chromium 開啟任意 URL，產出 **600×450 PNG**
- 尺寸對齊 [card-personal-portfolio](https://jacobhsu.github.io/card-personal-portfolio/) 的 project 卡片
- viewport 採 1200×900（4:3），縮放後完全不變形
- 可選參數：`output_dir`、`filename`、`wait_seconds`（等動畫穩定）

## 環境需求

- Python 3.11 以上
- [uv](https://docs.astral.sh/uv/)（推薦的執行方式）
- Claude Code（MCP 客戶端）

## 安裝與啟動（uv 版本）

本專案改為使用 `uv` 在本地端執行 MCP Server，**不再依賴 Docker**。

1. 用 Claude Code 開啟此專案資料夾
2. 執行 slash command：

   ```
   /setup_image_tools_server
   ```

3. 完成後執行 `/mcp` 連線 `image-tools-server`

> 詳細步驟（檢查 uv、建 venv、裝依賴、確認 `.mcp.json`）見 [.claude/commands/setup_image_tools_server.md](.claude/commands/setup_image_tools_server.md)

## 使用範例

連線成功後，可以在 Claude Code 中這樣請求：
> download 3 different random pictures of single castle. resize below 150px either the width or the length.

### 下載玩具圖片
```
請用 fetch_toy_image 工具下載 5 張機器人玩具圖片到 ./images 資料夾。
```

### 調整圖片尺寸
```
幫我把 ./images/robot_toy_1.jpg 縮放到 800x600。
```

### 移除背景
```
請把 ./images/robot_toy_1.jpg 的背景去掉，存成 PNG。
```

### 裁切成圓形
```
把 ./images/robot_toy_1.jpg 裁切成圓形。
```

### 產生 portfolio 用網站縮圖
```
用 screenshot_website 幫 https://jacobhsu.github.io/team_map/ 產出一張 portfolio 用的縮圖，存成 team_map.png。
```
產出位置：`./images/team_map.png`（600×450 PNG），可直接放到 `card-personal-portfolio/assets/images/` 取代既有 `project-*.png`。

> 首次使用前需安裝 Chromium：`uv run playwright install chromium`（約 150MB，只需一次）。

## 重啟 Server

修改 `server.py` 後：

- **只改 Python 程式碼** → 直接在 Claude Code 用 `/mcp` 重新連線即可，不需重裝依賴
- **修改 `requirements.txt`** → 執行 `uv pip install -r requirements.txt` 後再 `/mcp` 重連
- 也可使用內附的 slash command：`/rebuild_restart_image_tools_server`

## 檔案結構

```
cc-custom-mcp/
├── server.py                  # MCP Server 主程式
├── tools/
│   └── screenshot.py          # 網站截圖工具實作
├── requirements.txt           # Python 依賴
├── .mcp.json                  # Claude Code MCP 設定（uv 版）
├── Dockerfile                 # 舊版 Docker 設定（保留，可不用）
├── README.md                  # 本文件
├── .claude/
│   └── commands/
│       └── rebuild_restart_image_tools_server.md
├── images/                    # 下載與處理後的圖片
├── input/                     # 輸入圖片
└── output/                    # 輸出圖片
```

## Python 依賴

- **mcp** — Anthropic Model Context Protocol SDK
- **Pillow** — 圖片處理
- **requests** — HTTP 下載
- **duckduckgo-search** — 圖片搜尋
- **playwright** — headless Chromium 網站截圖
- **rembg** — AI 去背模型

## 疑難排解

### 1. `uv: command not found`
安裝 uv：`pip install uv`，或重新開啟 terminal 讓 PATH 生效。

### 2. `duckduckgo-search` 套件問題
```bash
uv pip install -U duckduckgo-search
```

### 3. 圖片下載失敗
- 檢查網路連線
- 部分來源網站可能擋掉請求，工具會自動重試

### 4. 首次去背很慢
- `rembg` 會下載 AI 模型（約 100MB+），首次需要時間
- 確認硬碟空間足夠

### 4-1. `screenshot_website` 報 `Executable doesn't exist`
- Playwright 還沒裝瀏覽器，執行：`uv run playwright install chromium`

### 5. Claude Code 看不到 Server
- 確認用 Claude Code 打開的是專案根目錄（而非父層）
- 確認 `.mcp.json` 存在於根目錄
- 確認 `uv` 在系統 PATH 中
- 修改設定後重連 `/mcp`

### 6. 工具執行失敗
- 看 Claude Code 顯示的 stderr 訊息
- 確認虛擬環境已建立且依賴已安裝（`uv pip list`）
- 確認檔案路徑可存取

## （已淘汰）Docker 執行方式

舊版本透過 Docker 執行：

```bash
docker build -t mcp-toy-image-tools-server .
```

並搭配 `.mcp.json` 的 docker 設定。本專案已改為 uv 方案，因為：

- 不需要 Docker Desktop
- 啟動更快、資源更省
- 跨機器分享只要 clone repo 就能用

`Dockerfile` 保留供有特殊需求的使用者參考。

## 開發：新增工具

在 `server.py` 加入新的 `@mcp.tool()` 函式：

```python
@mcp.tool()
async def your_new_tool(param1: str, param2: int = 10) -> str:
    """工具的功能說明 — 會顯示給 Claude 看到。"""
    # 實作
    return "結果訊息"
```

新增後在 Claude Code 用 `/mcp` 重連即可。

## 測試 Server

```bash
uv run python server.py
```

讓 Server 在 stdio 模式啟動，可用 MCP inspector 或手動傳入 JSON-RPC 請求測試。

## License

僅供學習與開發用途。請尊重圖片來源網站的服務條款與 AI 模型的授權條款。

---

**注意**：本工具會從網路下載圖片並使用 AI 模型處理，請合理使用並尊重來源網站的版權與服務條款。
