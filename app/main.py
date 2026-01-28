import os
import io
import json
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Response, UploadFile, File
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="24h AI API Station", version="2.0")

# --- Model Configuration ---
MODELS = {
    # Image Generation
    "flux": "black-forest-labs/FLUX.1-schnell",
    "sd35": "stabilityai/stable-diffusion-3.5-large",
    
    # Text Generation (LLM)
    "qwen": "Qwen/Qwen2.5-72B-Instruct",
    "phi": "microsoft/Phi-3.5-mini-instruct",
    
    # Audio Transcription
    "whisper": "openai/whisper-large-v3"
}

# Initialize Client
# HF_TOKEN must be set in Space Secrets
client = InferenceClient(token=os.getenv("HF_TOKEN"))

# --- Request Models ---
class ImageRequest(BaseModel):
    prompt: str
    model_id: str = "flux" # Options: flux, sd35
    width: int = 1024
    height: int = 1024

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model_id: str = "qwen" # Options: qwen, phi
    max_tokens: int = 512
    temperature: float = 0.7

# --- Routes ---

@app.get("/")
def read_root():
    return {
        "status": "active",
        "service": "24h AI Gateway",
        "models": MODELS
    }

@app.post("/generate/image")
def generate_image(req: ImageRequest):
    """
    Text-to-Image Generation
    """
    target_model = MODELS.get(req.model_id, MODELS["flux"])
    
    try:
        image = client.text_to_image(
            req.prompt,
            model=target_model,
            width=req.width,
            height=req.height
        )
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return Response(content=img_byte_arr.getvalue(), media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@app.post("/chat/completions")
def chat_completion(req: ChatRequest):
    """
    LLM Chat Completion (OpenAI-compatible format)
    """
    target_model = MODELS.get(req.model_id, MODELS["qwen"])
    
    try:
        # Convert Pydantic models to dict
        messages_dict = [{"role": m.role, "content": m.content} for m in req.messages]
        
        response = client.chat_completion(
            messages=messages_dict,
            model=target_model,
            max_tokens=req.max_tokens,
            temperature=req.temperature
        )
        
        # Return the structured response directly
        return response.choices[0].message
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat generation failed: {str(e)}")

@app.post("/audio/transcriptions")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Automatic Speech Recognition (Whisper)
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Use the raw API for audio since InferenceClient.automatic_speech_recognition 
        # wrapper can be tricky with file uploads in FastAPI
        # We'll use the client's post method for simplicity or the ASR wrapper if possible.
        # Here we use the simpler high-level method which accepts bytes
        
        result = client.automatic_speech_recognition(
            file_content,
            model=MODELS["whisper"]
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
