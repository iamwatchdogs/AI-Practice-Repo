from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Final, TypedDict

from dotenv import load_dotenv
from openai import OpenAI


class Message(TypedDict):
    """A TypedDict for defining list of messages."""

    instructions: str
    input: str


def main() -> None:
    """Execute the main logic of the program."""
    load_dotenv()

    api_key: Final[str | None] = os.environ.get("OPENAI_API_KEY")
    base_url: Final[str] = os.environ.get(
        "OPENAI_BASE_URL", "https://api.openai.com/v1"
    )
    model: Final[str] = os.environ.get("OPENAI_MODEL", "gpt-5-nano")

    client: OpenAI = OpenAI(api_key=api_key, base_url=base_url)

    msgs_path: Path = Path(__file__).parent / "messages.json"
    hardcoded_msgs: list[Message] = json.loads(msgs_path.read_text(encoding="utf-8"))

    for message in hardcoded_msgs:
        response = client.responses.create(model=model, **message)

        print("\n", "=" * 100, "\n")
        print("📄:", message["instructions"])
        print("👨:", message["input"])
        print("🤖:", response.output_text)
        print("\n", "=" * 100, "\n")


if __name__ == "__main__":
    main()
