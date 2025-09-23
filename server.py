from fastmcp import FastMCP
from mcp.types import TextContent

# Initialize the MCP server
mcp = FastMCP(name="Test MCP Server")


# Define a tool that returns a content array
@mcp.tool
def get_content() -> list[TextContent]:
    """Return two text samples. OpenAI will only see the first one."""
    result = [
        {
            "type": "text",
            "text": "This is the text description that should appear first.",
        },
        {
            "type": "text",
            "text": "This is the text description that should appear second.",
        },
    ]
    return [TextContent.model_validate(result) for result in result]


# Run the server (defaults to http://localhost:8000)
if __name__ == "__main__":
    mcp.run(transport="http", stateless_http=True)
