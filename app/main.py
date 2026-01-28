from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "active", "message": "24h API Station is running"}

@app.post("/generate")
def generate(data: InputData):
    # Your AI generation logic here
    return {"result": f"Generated image for: {data.prompt}"}
