from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.chatbot.chatbot import process_message
from app.mcp.server import router as mcp_router

app = FastAPI()

app.include_router(mcp_router)

# templates
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "chat.html")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = process_message(request.message)
    return {"response": response}

# .venv\Scripts\activate
# uvicorn app.main:app --reload

# Rest API url = http://127.0.0.1:8000/chat