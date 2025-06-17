# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def answer_secret(name:str) -> str:
    """Return the answer to the ultimate question of life, the universe, and everything"""
    return "You are scorpio. Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow! Wow!"

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! from ancloas"


if __name__ == "__main__":
    mcp.run()
