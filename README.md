# OpenAI Responses API MCP Multi-Content Bug Report

## Executive Summary

The OpenAI Responses API with remote MCP support fails to properly handle tools that return multiple `TextContent` items in an array. When an MCP tool returns an array containing multiple text content objects, only the first text item is included in the response output, silently dropping all subsequent text items.

## Bug Description

### Expected Behavior
When an MCP tool returns an array of multiple `TextContent` objects, all text content should be included in the response output, properly formatted and in the correct order.

### Actual Behavior
Only the first `TextContent` object from the array is included in the response. All subsequent text content items are silently dropped without any error or warning.

### Impact
This bug prevents MCP tools from returning structured multi-part responses, severely limiting the usefulness of the MCP integration. Key impacts include:
- Cannot return multiple text segments from a single tool call
- Cannot interleave text and image content (e.g., text description followed by an image URL followed by more text)
- Cannot build structured multimodal responses that are common in documentation, tutorials, and reports

## Reproduction Steps

### Prerequisites
- Python 3.12+
- OpenAI API key
- ngrok account (for exposing local server)

### Quick Start

1. **Clone this repository:**
    ```bash
    git clone https://github.com/arcaputo3/openai-responses-mcp-bug.git
    cd openai-responses-mcp-bug
    ```

2. **Install dependencies:**
    ```bash
    uv sync
    ```

3. **Create `.env` file with your OpenAI API key:**
    ```bash
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    ```

4. **Start the MCP server:**
    ```bash
    uv run server.py
    ```
    The server will run on `http://localhost:8000`

5. **In a new terminal, expose the server using ngrok:**
    ```bash
    ngrok http 8000
    # Or if you have a custom domain:
    # ngrok http 8000 --url=your-custom-domain.ngrok.app
    ```

6. **Copy the HTTPS URL from ngrok and add it to your `.env` file:**
    ```bash
    # Add this line to your .env file
    MCP_URL=https://abc123.ngrok.io
    ```

7. **Run the OpenAI API call:**
    ```bash
    uv run call_openai_with_mcp.py
    ```

## Code Overview

### MCP Server (`server.py`)
The server defines a simple tool `get_content()` that returns an array of two `TextContent` objects:
```python
[
    TextContent(type="text", text="This is the text description that should appear first."),
    TextContent(type="text", text="This is the text description that should appear second.")
]
```

### OpenAI Client (`call_openai_with_mcp.py`)
Makes a request to the OpenAI Responses API with MCP tool integration, asking it to call the `get_content` tool and return its content verbatim.

## Expected vs Actual Output

### Expected Response Output
The response should contain both text items from the MCP tool response. Both text content objects should be included in the output.

### Actual Response Output
When running `uv run call_openai_with_mcp.py`, the response shows that only the first text item is included:

```json
{
  "id": "resp_68d1e53c8d44819688a5a3e5252e20590e5593cefd6820f8",
  "output": [
    {
      "id": "mcp_68d1e542359c819698009274fada4c430e5593cefd6820f8",
      "arguments": "{}",
      "name": "get_content",
      "server_label": "test",
      "type": "mcp_call",
      "output": "This is the text description that should appear first."
    },
    {
      "id": "msg_68d1e54528648196a499d1e0805f36880e5593cefd6820f8",
      "content": [
        {
          "text": "This is the text description that should appear first.",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ]
}
```

**⚠️ Critical Issue:** The second text content item ("This is the text description that should appear second.") is completely missing from the response. The MCP tool returns an array with two TextContent objects, but only the first one appears in the OpenAI response.

## Technical Analysis

### Root Cause Hypothesis
The OpenAI Responses API appears to be incorrectly handling the array of `TextContent` objects returned by MCP tools. Instead of processing all items in the array, it only processes the first item and ignores the rest.

### MCP Protocol Compliance
According to the MCP (Model Context Protocol) specification, tools can return arrays of content items, and all items should be processed and included in the response. This bug represents a deviation from the expected MCP behavior.

## Workarounds

Until this bug is fixed, potential workarounds include:
1. Concatenating all text content into a single `TextContent` object on the MCP server side
2. Using multiple tool calls instead of returning multiple items in a single call
3. Encoding multiple text segments in a structured format (e.g., JSON) within a single text content item

## Environment Details

- **OpenAI Python SDK:** 1.108.2
- **FastMCP:** 2.12.3
- **Python Version:** 3.12+
- **Operating System:** Tested on macOS

## Related Issues

- This bug may be related to general array handling in MCP tool responses
- Similar issues may exist with other content types (images, etc.) when multiple items are returned

## License

This bug demonstration code is provided as-is for the purpose of bug reporting and testing.
