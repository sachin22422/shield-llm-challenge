import spacy
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class PromptRequest(BaseModel):
    """Defines the structure of the incoming request from the frontend."""
    prompt: str

class Entity(BaseModel):
    """Defines the structure for a single detected entity."""
    text: str
    label: str

class ProcessResponse(BaseModel):
    """Defines the structure of the response sent back to the frontend."""
    entities: List[Entity]
    llm_response: str
    sanitized_prompt: str

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    exit()

app = FastAPI(title="PrivChat PII Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3" 

@app.post("/process", response_model=ProcessResponse)
async def process_prompt(request: PromptRequest):
    """
    Receives a prompt, processes it for PII, gets a response from a local LLM,
    and returns the structured results.
    """
    prompt_text = request.prompt
    print(f"\n--- [Received Prompt] ---\n{prompt_text}\n")

    doc = nlp(prompt_text)
    entities = [Entity(text=ent.text, label=ent.label_) for ent in doc.ents]
    
    print("--- [Detected Named Entities (spaCy)] ---")
    if not entities:
        print("No entities detected.")
    else:
        for ent in entities:
            print(f"- Text: {ent.text}, Type: {ent.label}")
    print("-" * 20)
    
    sanitized_prompt = prompt_text

    for ent in reversed(doc.ents):
        start = ent.start_char
        end = ent.end_char
        sanitized_prompt = f"{sanitized_prompt[:start]}[{ent.label_}]{sanitized_prompt[end:]}"
    
    print(f"\n--- [Sanitized Prompt to LLM] ---\n{sanitized_prompt}\n")

    try:
        llm_request_payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"Based on the following text, provide a concise response. Text: {sanitized_prompt}",
            "stream": False 
        }
        
        response = requests.post(OLLAMA_API_URL, json=llm_request_payload, timeout=60)
        response.raise_for_status() 
        
        response_data = response.json()
        llm_response = response_data.get("response", "Error: No response content from LLM.").strip()

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        raise HTTPException(status_code=503, detail=f"Could not connect to the Ollama service at {OLLAMA_API_URL}. Is Ollama running?")
    
    print(f"\n--- [Response from LLM ({OLLAMA_MODEL})] ---\n{llm_response}\n")

    return ProcessResponse(
        entities=entities,
        llm_response=llm_response,
        sanitized_prompt=sanitized_prompt
    )

@app.get("/")
def read_root():
    return {"message": "PrivChat API is running. Send a POST request to /process to analyze text."}
    