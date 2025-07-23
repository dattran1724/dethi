from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.langgraph_engine.graph import build_graph

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

chat_graph = build_graph()
state = {"history": []}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "history": [], "response": ""})

@router.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    state["user_input"] = message
    result = chat_graph.invoke(state)
    state.update(result)
    history = result.get("history", [])
    response = result.get("response", "")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": history,
        "response": response
    })
