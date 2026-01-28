import os
import io
import json
import uuid
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Response, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="24h AI API Station", version="2.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (Frontend)
app.mount("/ui", StaticFiles(directory="app/static", html=True), name="static")

# --- Model Configuration ---
MODELS = {
    "flux": "black-forest-labs/FLUX.1-schnell",
    "sd35": "stabilityai/stable-diffusion-3.5-large",
    "qwen": "Qwen/Qwen2.5-72B-Instruct",
    "phi": "microsoft/Phi-3.5-mini-instruct",
    "whisper": "openai/whisper-large-v3"
}

client = InferenceClient(token=os.getenv("HF_TOKEN"))

# --- Request Models ---
class ImageRequest(BaseModel):
    prompt: str
    model_id: str = "flux"
    width: int = 1024
    height: int = 1024

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model_id: str = "qwen"
    max_tokens: int = 512
    temperature: float = 0.7

# --- Routes ---

@app.get("/")
def read_root():
    return {
        "status": "active",
        "service": "24h AI Gateway",
        "ui_url": "/ui",
        "models": MODELS
    }

@app.post("/generate/image")
def generate_image(req: ImageRequest):
    target_model = MODELS.get(req.model_id, MODELS["flux"])
    try:
        image = client.text_to_image(req.prompt, model=target_model, width=req.width, height=req.height)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        # Return image with custom header to simulate API Key output
        return Response(
            content=img_byte_arr.getvalue(), 
            media_type="image/png",
            headers={"X-API-Key-Used": "sk-hf-serverless-token"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/completions")
def chat_completion(req: ChatRequest):
    target_model = MODELS.get(req.model_id, MODELS["qwen"])
    try:
        messages_dict = [{"role": m.role, "content": m.content} for m in req.messages]
        response = client.chat_completion(messages=messages_dict, model=target_model, max_tokens=req.max_tokens, temperature=req.temperature)
        return response.choices[0].message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/key/generate")
def generate_api_key():
    """Simulate API Key Generation"""
    return {
        "key": f"sk-{uuid.uuid4().hex[:8]}",
        "status": "active",
        "quota": "unlimited (gateway mode)"
    }
