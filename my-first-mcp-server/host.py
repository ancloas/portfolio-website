# from mcp import ClientSession, StdioServerParameters, types
# from mcp.client.stdio import stdio_client
# import asyncio
# from typing import Optional
# from contextlib import AsyncExitStack

# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
# from dotenv import load_dotenv
# from llm import client as gemini_client
# load_dotenv()  # load environment variables from .env


# # Create server parameters for stdio connection
# server_params = StdioServerParameters(
#     command="python",  # Executable
#     args=["example_server.py"],  # Optional command line arguments
#     env=None,  # Optional environment variables
# )

# class MCPClient:
#     def __init__(self):
#         # Initialize session and client objects
#         self.session: Optional[ClientSession] = None
#         self.exit_stack = AsyncExitStack()
#         self.gemini_client = gemini_client
#     # methods will go here

#     async def connect_to_server(self, server_script_path: str):
#         """Connect to an MCP server

#         Args:
#             server_script_path: Path to the server script (.py or .js)
#         """
#         is_python = server_script_path.endswith('.py')
#         is_js = server_script_path.endswith('.js')
#         if not (is_python or is_js):
#             raise ValueError("Server script must be a .py or .js file")

#         command = "python" if is_python else "node"
#         server_params = StdioServerParameters(
#             command=command,
#             args=[server_script_path],
#             env=None
#         )

#         stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
#         self.stdio, self.write = stdio_transport
#         self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

#         await self.session.initialize()

#         # List available tools
#         response = await self.session.list_tools()
#         tools = response.tools
#         print("\nConnected to server with tools:", [tool.name for tool in tools])
    

#     async def process_query(self, query: str) -> str:
#         """Process a query using Claude and available tools""" 

#         response = await self.session.list_tools() # type: ignore
#         available_tools = [{
#             "name": tool.name,
#             "description": tool.description,
#             "input_schema": tool.inputSchema
#         } for tool in response.tools]

#         # Initial Claude API call
#         response = self.anthropic.messages.create(
#             model="claude-3-5-sonnet-20241022",
#             max_tokens=1000,
#             messages=messages,
#             tools=available_tools
#         )

#         # Process response and handle tool calls
#         final_text = []

#         assistant_message_content = []
#         for content in response.content:
#             if content.type == 'text':
#                 final_text.append(content.text)
#                 assistant_message_content.append(content)
#             elif content.type == 'tool_use':
#                 tool_name = content.name
#                 tool_args = content.input

#                 # Execute tool call
#                 result = await self.session.call_tool(tool_name, tool_args) # type: ignore
#                 final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

#                 assistant_message_content.append(content)
#                 messages.append({
#                     "role": "assistant",
#                     "content": assistant_message_content # type: ignore
#                 })
#                 messages.append({
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "tool_result",
#                             "tool_use_id": content.id,
#                             "content": result.content
#                         }
#                     ] # type: ignore
#                 })

#                 # Get next response from Claude
#                 response = self.anthropic.messages.create(
#                     model="claude-3-5-sonnet-20241022",
#                     max_tokens=1000,
#                     messages=messages,
#                     tools=available_tools
#                 )

#                 final_text.append(response.content[0].text)

#         return "\n".join(final_text)


# # # Optional: create a sampling callback
# #     async def handle_sampling_message(self, 
# #     message: types.CreateMessageRequestParams,
# # ) -> types.CreateMessageResult:
# #     return types.CreateMessageResult(
# #         role="assistant",
# #         content=types.TextContent(
# #             type="text",
# #             text="Hello, world! from model",
# #         ),
# #         model="gpt-3.5-turbo",
# #         stopReason="endTurn",
# #     )


#     async def run(self):
#         async with stdio_client(server_params) as (read, write):
#             async with ClientSession(
#                 read, write, sampling_callback=handle_sampling_message # type: ignore
#             ) as session:
#                 # Initialize the connection
#                 await session.initialize()

#                 # List available prompts
#                 prompts = await session.list_prompts()

#                 # Get a prompt
#                 prompt = await session.get_prompt(
#                     "example-prompt", arguments={"arg1": "value"}
#                 )

#                 # List available resources
#                 resources = await session.list_resources()

#                 # List available tools
#                 tools = await session.list_tools()

#                 # Read a resource
#                 content, mime_type = await session.read_resource("file://some/path")

#                 # Call a tool
#                 result = await session.call_tool("tool-name", arguments={"arg1": "value"})


# if __name__ == "__main__":
#     import asyncio
#     mcp_client = MCPClient()
#     asyncio.run(mcp_client.run())