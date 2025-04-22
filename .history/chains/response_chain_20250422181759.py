# chains/response_chain.py
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import List

llm = ChatOpenAI(model="gpt-4o-mini")

def generate_response(stage: str, user_input: str, knowledge_summary: str, conversation_history: List[str] = None) -> str:
    system_prompt = f"""
あなたは共感的なカウンセラーです。
以下の会話履歴と現在のユーザー発言、そして参考知識を踏まえて、ユーザーの悩みに適切に応答してください。

# 会話履歴:
{conversation_history}

# ユーザー発言:
{user_input}

# 参考知識:
{knowledge_summary}

## 制約
- 応答は「あなた」に語りかけるように
- メタコメントや思考プロセスの記述をしない
- 応答は1つの段落で完結させる（改行や蛇足を含めない）

# 出力:
"""

    prompt = PromptTemplate.from_template(system_prompt)

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({})
