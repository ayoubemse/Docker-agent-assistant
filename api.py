from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from agent import agent
from docker_agent import run_agent
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Docker agent API", description="API for interacting with Docker agent commands and documentation.", version="1.0.0")



class CommandRequest(BaseModel):
    command: str
    thread_id: str = "default"

class CommandResponse(BaseModel):
    output: str
    thread_id: str

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=CommandResponse)
async def chat_endpoint(request: CommandRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    try:
        response = run_agent(agent, request.command, config=config)
        return CommandResponse(output=response or "", thread_id=request.thread_id)
    except Exception as e:
        if "tool_use` ids were found without `tool_result`" in str(e):
            agent.update_state(config, {"messages": []})
            response = run_agent(agent, request.command, config=config)
            return CommandResponse(output=response, thread_id=request.thread_id)
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)