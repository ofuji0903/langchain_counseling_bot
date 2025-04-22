# chains/response_chain.py
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o")

response_prompt = PromptTemplate.from_template(
    "カウンセリング文脈で、ステージ「{stage}」に該当するユーザーの発言「{input}」に対して、"
    "以下の知識をもとに、共感的かつ具体的なアドバイスを出してください。\n\n"
    "ナレッジ：{knowledge}"
)

# LangChain 1.x 推奨形式
chain = response_prompt | llm

def generate_response(stage: str, user_input: str, knowledge: str) -> str:
    result = chain.invoke({
        "stage": stage,
        "input": user_input,
        "knowledge": knowledge
    })
    return result.content.strip()
