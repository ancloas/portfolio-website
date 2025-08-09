from os import name
from av_mcp_client import MCPClient, LLMManager 
import asyncio
from dotenv import load_dotenv

load_dotenv()

llm_manager =LLMManager(provider='gemini')

client=  MCPClient(llm_manager=llm_manager, server_urls=['127.0.0.1:8000'])



async def main():
    llm_manager = LLMManager(provider='gemini')
    # Example: connect to two servers, one HTTP and one local script
    server_urls = [
        "http://127.0.0.1:8000/mcp",
        # "python path/to/other_server.py",  # For stdio, if needed
    ]
    client = MCPClient(llm_manager, server_urls)
    try:
        await client.connect_to_servers()
        await client.register_tools()
        await client.chat_loop()
    except Exception as E:
        print(E)
    finally:
        await client.cleanup()



if __name__ == "__main__":
    import sys
    asyncio.run(main())