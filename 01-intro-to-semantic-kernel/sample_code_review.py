# sample_code_review.py

import asyncio
import os

from semantic_kernel.agents import (
    AgentGroupChat,
    ChatCompletionAgent,
)
from semantic_kernel.agents.strategies import (
    DefaultTerminationStrategy,
    SequentialSelectionStrategy,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory


async def run_review() -> None:
    """Interactively ask for a file path and review its contents."""

    prompt = """
あなたは熟練のソフトウェアエンジニアです。ユーザーが指定するコードをレビューし、
改善点やバグ、非効率な箇所、セキュリティ上の懸念点を日本語で指摘してください。
パフォーマンスやコードスタイル、可読性にも注意し、必要に応じてテスト不足やエッジケースの漏れも指摘してください。
より良い実装例がある場合はコードスニペットを用いて具体的に提案してください。
まずはレビューするファイルのパスを尋ねてください。
"""

    style_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="StyleReviewer",
        instructions=prompt + "\nあなたの役割はコードスタイルと可読性に焦点を当てて指摘することです。",
    )

    bug_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="BugReviewer",
        instructions=prompt + "\nあなたの役割はバグや論理的誤りを見つけて指摘することです。",
    )

    security_agent = ChatCompletionAgent(
        service=AzureChatCompletion(),
        name="SecurityReviewer",
        instructions=prompt + "\nあなたの役割はセキュリティ上の問題点に焦点を当てて指摘することです。",
    )

    group_chat = AgentGroupChat(
        agents=[style_agent, bug_agent, security_agent],
        selection_strategy=SequentialSelectionStrategy(),
        termination_strategy=DefaultTerminationStrategy(maximum_iterations=3),
    )

    group_chat.history = ChatHistory()

    await group_chat.add_chat_message("コードレビューを始めます。レビューするファイルのパスを教えてください。")
    async for response in group_chat.invoke():
        print(f"{response.name}: {response.content}")
    group_chat.is_complete = False

    while True:
        user_input = input("User: ").strip()

        if not os.path.isfile(user_input):
            await group_chat.add_chat_message(user_input)
            async for response in group_chat.invoke():
                print(f"{response.name}: {response.content}")
            group_chat.is_complete = False
            continue

        with open(user_input, "r", encoding="utf-8") as f:
            code = f.read()

        review_prompt = f"以下のコードをレビューしてください:\n{code}"
        await group_chat.add_chat_message(review_prompt)
        async for response in group_chat.invoke():
            print(f"{response.name}: {response.content}")
        break


if __name__ == "__main__":
    asyncio.run(run_review())
