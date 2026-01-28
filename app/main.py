import os
import io
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables (useful for local dev, in Space use Secrets)
load_dotenv()

app = FastAPI()

# Model Configuration
# FLUX.1-schnell is fast and suitable for API usage
MODEL_ID = "black-forest-labs/FLUX.1-schnell"

# Initialize Client
# HF_TOKEN should be set in Space Settings > Secrets
client = InferenceClient(token=os.getenv("HF_TOKEN"))

class GenerateRequest(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024

@app.get("/")
def read_root():
    return {
        "status": "active", 
        "service": "24h API Gateway", 
        "model": MODEL_ID
    }

@app.post("/generate")
def generate_image(req: GenerateRequest):
    """
    Generate an image using HF Serverless Inference API.
    Returns PNG image bytes.
    """
    try:
        # Call the remote Serverless API
        # This runs on HF's GPU cluster, not on the local CPU container
        image = client.text_to_image(
            req.prompt,
            model=MODEL_ID,
            width=req.width,
            height=req.height
        )
        
        # Convert PIL Image to Bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return Response(content=img_byte_arr.getvalue(), media_type="image/png")
        
    except Exception as e:
        print(f"Error generation image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
