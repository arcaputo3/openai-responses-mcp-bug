import os

from dotenv import load_dotenv
from openai import OpenAI


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI()

    response = client.responses.create(
        model="gpt-5-nano",
        input="Call the `get_content` tool and return its output verbatim.",
        reasoning={"summary": "auto"},
        tools=[
            {
                "type": "mcp",
                "server_label": "test",
                "server_url": os.getenv("MCP_URL"),
                "require_approval": "never",
            }
        ],
    )

    print(response.model_dump_json(indent=2))
