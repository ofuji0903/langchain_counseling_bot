# chains/stage_router_chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import List

def get_stage(user_input: str, conversation_history: List[str] = None) -> str:
    # conversation_historyは現時点では使用しない
    # Step 3以降で使用する予定
    prompt = ChatPromptTemplate.from_messages([
        ("system", """あなたはカウンセリングの専門家です。
        ユーザーの入力から、以下の4つのステージのどれに該当するかを判断してください。

        1. 傾聴: ユーザーが自分の気持ちや状況を話している段階
        2. 共感: ユーザーの感情に寄り添い、理解を示す段階
        3. 提案: 具体的な解決策やアドバイスを提供する段階
        4. 振り返り: これまでの会話を振り返り、まとめる段階

        回答は必ず「傾聴」「共感」「提案」「振り返り」のいずれか1つを返してください。
        """),
        ("human", "{input}")
    ])

    chain = (
        prompt
        | ChatOpenAI(model="gpt-4-turbo-preview")
        | StrOutputParser()
    )

    return chain.invoke({"input": user_input})
