from fastapi import APIRouter
from pydantic import BaseModel
from app.chatbot.chatbot import process_message

router = APIRouter()

class MCPRequest(BaseModel):
    type: str
    tool: str
    input: dict

@router.post("/mcp")
def mcp_handler(req: MCPRequest):

    if req.tool == "chat":
        message = req.input.get("message", "")

        return {
            "type": "tool_response",
            "tool": "chat",
            "output": process_message(message)
        }

    return {
        "type": "error",
        "tool": req.tool,
        "output": {"error": "Unknown tool"}
    }

@router.get("/mcp/tools")
def mcp_tools():
    return {
        "tools": [
            {
                "name": "chat",
                "description": "Hospital chatbot (appointments + doctors)"
            }
        ]
    }