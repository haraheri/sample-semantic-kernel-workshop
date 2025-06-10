import os
from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# 必要な環境変数（.envや環境変数でセットして下さい）
# AZURE_OPENAI_ENDPOINT
# AZURE_OPENAI_API_KEY
# AZURE_OPENAI_DEPLOYMENT_NAME

kernel = Kernel()
kernel.add_service(AzureChatCompletion())

prompt = """{{$input}}

TL;DR in one sentence:"""

input_text = """
Azure Semantic Kernelは、AIワークフローのためのオーケストレーションエンジンです。
複数のAIサービスと連携し、タスク自動化や知識ベース拡張を実現できます。
PythonとC#の両方に対応しています。
"""

# 必要パラメータは最新のものに合わせてください
result = kernel.invoke(
    prompt_template=prompt,
    input_variables={"input": input_text},
    max_tokens=100,
    temperature=0.2
)
print("要約:", result)