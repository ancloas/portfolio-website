from fastapi import FastAPI, Form
from pydantic import BaseModel
from core.mcp_client import client
class ChatRequest(BaseModel):
    message: str



app = FastAPI(
    title="Portfolio MCP Client",
    description="Backend API for Portfolio MCP client",
    version="1.0.0",
)





@app.post("/chat")
async def chat(message: str = Form(...)):
   response =  await client.process_query(query=message)
   return response.content

