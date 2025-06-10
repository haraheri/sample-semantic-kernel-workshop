# sample_code_review.py

import sys
import os
import asyncio

from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

async def review_code(code: str) -> str:
    # 非同期でAIにレビューを依頼
    kernel = Kernel()
    kernel.add_service(AzureChatCompletion())  # .env で設定済み

    prompt = """
あなたは熟練のソフトウェアエンジニアです。以下のコードをレビューしてください。
- 改善点・バグ・非効率な箇所があれば日本語で指摘してください
- 必要に応じて具体的な修正例も提示してください

# レビュー対象コード
{{$input}}
"""
    # invoke は await が必要
    result = await kernel.invoke(
        prompt_template=prompt,
        input_variables={"input": code},
        max_tokens=1000,
        temperature=0.2,
    )
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python sample_code_review.py <target_file>")
        sys.exit(1)

    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print(f"File not found: {target_file}")
        sys.exit(1)

    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    # asyncio.run でコルーチンを実行
    review = asyncio.run(review_code(code))
    print(review)

if __name__ == "__main__":
    main()
