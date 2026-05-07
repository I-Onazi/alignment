from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from alignment.validator import validate_sequences
from alignment.needleman_wunsch import NeedlemanWunsch

app = FastAPI(title="Needleman-Wunsch Alignment API")

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class ValidationRequest(BaseModel):
    seq1: str
    seq2: str

class AlignmentParams(BaseModel):
    seq1: str
    seq2: str
    match: int
    mismatch: int
    gap: int

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.post("/api/validate")
async def validate_input(request: ValidationRequest):
    is_valid, message, seq_type = validate_sequences(request.seq1, request.seq2)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    return {"message": "Valid sequences", "type": seq_type}

@app.post("/api/initialize")
async def initialize_alignment(params: AlignmentParams):
    is_valid, _, _ = validate_sequences(params.seq1, params.seq2)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid sequences")
        
    nw = NeedlemanWunsch(params.seq1, params.seq2, params.match, params.mismatch, params.gap)
    matrix = nw.initialize_matrix()
    
    return {
        "matrix": matrix,
        "rows": params.seq1,
        "cols": params.seq2
    }

@app.post("/api/fill")
async def fill_alignment(params: AlignmentParams):
    is_valid, _, _ = validate_sequences(params.seq1, params.seq2)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid sequences")
        
    nw = NeedlemanWunsch(params.seq1, params.seq2, params.match, params.mismatch, params.gap)
    matrix, traceback_matrix = nw.fill_matrix()
    results = nw.get_traceback()
    
    return {
        "matrix": matrix,
        "traceback_matrix": traceback_matrix,
        "rows": params.seq1,
        "cols": params.seq2,
        "results": results
    }

