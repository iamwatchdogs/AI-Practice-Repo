from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Final, TypedDict

from dotenv import load_dotenv
from openai import OpenAI


class Conversation(TypedDict):
    """A TypeDict for defining list of conversations."""

    instructions: str
    input: str


def main() -> None:
    """Execute the main logic of the program.

    Args: None
    Returns: None

    """
    load_dotenv()

    api_key: Final[str | None] = os.environ.get("OPENAI_API_KEY")
    base_url: Final[str] = os.environ.get(
        "OPENAI_BASE_URL", "https://api.openai.com/v1"
    )
    model: Final[str] = os.environ.get("OPENAI_MODEL", "gpt-5-nano")

    client: OpenAI = OpenAI(api_key=api_key, base_url=base_url)

    convo_path: Path = Path(__file__).parent / "conversations.json"
    hardcoded_conversations: list[Conversation] = json.loads(
        convo_path.read_text(encoding="utf-8")
    )

    for conversation in hardcoded_conversations:
        response = client.responses.create(model=model, **conversation)
        print("\n", "=" * 100, "\n")
        print("📄:", conversation["instructions"])
        print("👨:", conversation["input"])
        print("🤖:", response.output_text)
        print("\n", "=" * 100, "\n")


if __name__ == "__main__":
    main()
