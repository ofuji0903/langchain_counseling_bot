# chains/response_chain.py
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")

def generate_response(stage: str, user_input: str, knowledge_summary: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """あなたは共感的なカウンセラーです。
        以下の情報をもとに、ユーザーに対して丁寧かつ感情に寄り添う一つの応答だけを作成してください。

        応答のルール：
        1. 思考プロセスや推論（〜と思います、〜かもしれません）は含めない
        2. ユーザーに直接語りかける口調で、実際に話しているように答える
        3. 一つの応答のみを出力する（複数の応答や選択肢は提示しない）
        4. メタコメントや内面的な言葉は使用しない
        5. 応答は必ず「あなた」に向けた直接的な言葉で始める
        6. 応答の最後に改行や追加の説明を付けない

        現在のステージ: {stage}
        """),
        ("human", """【ユーザーの発言】
{user_input}

【関連知識・情報】
{knowledge_summary}

※上記の情報を参考に、ユーザーに直接語りかける形で一つの応答のみを出力してください。""")
    ])

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "stage": stage,
        "user_input": user_input,
        "knowledge_summary": knowledge_summary
    })
