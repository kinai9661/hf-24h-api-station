---
title: 24h API Station
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# 24h AI API Station

This is a **Docker-based FastAPI** application deployed on Hugging Face Spaces, featuring a **Web UI** for image generation and a **Gateway API** for various AI models.

To keep this Space running 24/7 on the free tier, it uses an external **Cloudflare Worker** to ping the endpoint periodically.

## Features

- **Multi-Model Support** (Gateway Mode):
  - 🎨 **Image**: FLUX.1-schnell, Stable Diffusion 3.5 Large
  - 💬 **Chat**: Qwen2.5-72B-Instruct, Phi-3.5-mini
  - 🎙️ **Audio**: Whisper Large v3
- **Web UI**: Built-in frontend at `/ui` for testing generation.
- **FastAPI**: High-performance backend with Swagger docs at `/docs`.

## Quick Start

### 1. Set up Secrets
Go to your Space **Settings** > **Variables and secrets** and add:
- `HF_TOKEN`: Your Hugging Face Access Token (Write permission).

### 2. Access the UI
Once deployed, visit your Space URL with `/ui` appended:
`https://YOUR_SPACE_URL.hf.space/ui`

### 3. Keep-Alive Setup (Optional)
To prevent the Space from sleeping after 48h:
1. Copy the code from `worker/src/index.ts`.
2. Create a Cloudflare Worker.
3. Set the `spaceUrl` to your Space's URL.
4. Set a Cron Trigger to run every hour.

---

# 24小時 AI API 站 (中文說明)

這是一個整合了解決方案的範本倉庫，包含：
1. **Hugging Face Space 程式碼** (根目錄)：基於 Docker 與 FastAPI 的 API 伺服器設定。
2. **Cloudflare Worker 保活腳本** (`worker/` 目錄)：防止 Space 進入休眠的 Cron Trigger 腳本。
3. **Web UI**: 內建視覺化介面，位於 `/ui` 路徑。

## 使用方法

### 1. 設定 Token
為了使用 FLUX 和 Qwen 等模型，請在 Space 的 **Settings** 中設定 `HF_TOKEN`。

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
