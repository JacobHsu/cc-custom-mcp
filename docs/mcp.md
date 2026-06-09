

設定方式: 
1. .mcp.json 
```json
    "icon-generator": {
      "type": "sse",
      "url": "https://icon-generator-mcp-pi.vercel.app/sse"
    }
```
2. 執行 claude 開啟 Claude Code CLI 
3. 執行 /mcp > 點擊 icon-generator > 點擊 Reconnect
4. 再次執行 /mcp > 點擊 icon-generator > 點擊 View Tools，查看有什麼工具可以使用 
5. Esc 退出 mcp 設定頁面 
6. Play with it. Here is a prompt exapmle:
 
"Generate an icon of cat."
 
注意：由於 Vercel 只允許短暫的 session 連線，因此 SSE 傳輸方式的 Response session 會較長被中斷。建議每次使用前，都點擊 Reconnect 

