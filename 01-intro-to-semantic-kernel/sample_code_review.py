# sample_code_review.py

import asyncio
import os

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


async def run_review() -> None:
    """Interactively ask for a file path and review its contents."""

    prompt = """
あなたは熟練のソフトウェアエンジニアです。ユーザーが指定するコードをレビューし、
改善点やバグ、非効率な箇所、セキュリティ上の懸念点を日本語で指摘してください。
パフォーマンスやコードスタイル、可読性にも注意し、必要に応じてテスト不足やエッジケースの漏れも指摘してください。
より良い実装例がある場合はコードスニペットを用いて具体的に提案してください。
まずはレビューするファイルのパスを尋ねてください。
"""

    agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="code_reviewer",
        instructions=(prompt),
    )

    thread = ChatHistoryAgentThread()

    response = await agent.get_response(
        messages="コードレビューを始めます。レビューするファイルのパスを教えてください。",
        thread=thread,
    )
    print(f"Agent: {response.content}")

    while True:
        user_input = input("User: ").strip()

        if not os.path.isfile(user_input):
            response = await agent.get_response(messages=user_input, thread=thread)
            print(f"Agent: {response.content}")
            continue

        with open(user_input, "r", encoding="utf-8") as f:
            code = f.read()

        review_prompt = f"以下のコードをレビューしてください:\n{code}"
        response = await agent.get_response(messages=review_prompt, thread=thread)
        print(f"Agent: {response.content}")
        break


if __name__ == "__main__":
    asyncio.run(run_review())
