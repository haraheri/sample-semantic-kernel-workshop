import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.kernel import create_kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/code-review", tags=["code_review"])

prompt = """
あなたは熟練のソフトウェアエンジニアです。ユーザーが指定するコードをレビューし、
改善点やバグ、非効率な箇所、セキュリティ上の懸念点を日本語で指摘してください。
パフォーマンスやコードスタイル、可読性にも注意し、必要に応じてテスト不足やエッジ
ケースの漏れも指摘してください。
より良い実装例がある場合はコードスニペットを用いて具体的に提案してください。
"""

class CodeReviewRequest(BaseModel):
    code: str


@router.post("/")
async def review_code(request: CodeReviewRequest):
    kernel, _ = create_kernel()
    try:
        agent = ChatCompletionAgent(
            kernel=kernel,
            name="code_reviewer",
            instructions=prompt,
        )
        thread = ChatHistoryAgentThread()
        review_prompt = f"以下のコードをレビューしてください:\n{request.code}"
        response = await agent.get_response(messages=review_prompt, thread=thread)
        return {"review": response.content}
    except Exception as e:
        logger.error(f"Error in review_code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
