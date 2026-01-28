---
title: 24h API Station
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app/main.py
pinned: false
---

# 24h API Station for Hugging Face

這是一個整合了解決方案的範本倉庫，包含：
1. **Hugging Face Space 程式碼** (根目錄)：基於 Docker 與 FastAPI 的 API 伺服器設定。
2. **Cloudflare Worker 保活腳本** (`worker/` 目錄)：防止 Space 進入休眠的 Cron Trigger 腳本。

## 使用方法

### 1. 部署 Hugging Face Space
1. 在 Hugging Face 建立一個新的 Space。
2. 選擇 SDK 為 **Docker**。
3. 將此倉庫與 Space 連結，或直接上傳根目錄的檔案 (`Dockerfile`, `requirements.txt`, `app/`)。

### 2. 部署 Cloudflare Worker
1. 進入 `worker` 資料夾：
   ```bash
   cd worker
   ```
2. 修改 `src/index.ts` 中的 `spaceUrl` 為您的 Space 網址。
3. 部署 Worker：
   ```bash
   npm install
   npx wrangler deploy
   ```

## 檔案結構
- `Dockerfile`: 定義 API 執行環境
- `app/main.py`: FastAPI 主程式
- `worker/`: Cloudflare Workers 相關設定
