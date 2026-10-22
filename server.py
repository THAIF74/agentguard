from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from .state import state
from .audit import AuditLog

app = FastAPI()
audit = AuditLog()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return HTMLResponse(Path("ui/index.html").read_text())

@app.get("/api/events")
def get_events():
    return {
        "frozen": state.frozen,
        "events": audit.entries(limit=50)
    }

@app.post("/api/freeze")
def toggle_freeze():
    state.frozen = not state.frozen
    return {"frozen": state.frozen}