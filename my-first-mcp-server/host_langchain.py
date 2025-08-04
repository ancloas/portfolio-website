from json import load
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import asyncio
import os
import time
from llm_manger import LLMManager
from dotenv import load_dotenv
import asyncio
# Initialize the Gemini model
# llm_manager = LLMManager(provider='gemini')
load_dotenv()

model = ChatGoogleGenerativeAI(
    api_key = os.getenv('GEMINI_API_KEY'),
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=3
)

async def main():
    start_time = time.time()
    # Connect to multiple MCP servers
   # Use server from examples/servers/streamable-http-stateless/


    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp"
            },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(model, tools) # type: ignore
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    return math_response

print(asyncio.run(main()))