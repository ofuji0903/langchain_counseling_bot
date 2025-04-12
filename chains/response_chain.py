from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-4o")

response_prompt = PromptTemplate.from_template(
    "あなたはカウンセラーです。以下のナレッジに基づいて、ユーザーの発言に対して思いやりを持って応答してください。\n\n"
    "【ナレッジ】\n{context}\n\n"
    "【ユーザーの発言】\n{user_input}\n\n"
    "【カウンセラーの応答】"
)

response_chain = LLMChain(llm=llm, prompt=response_prompt)

def generate_response(stage: str, user_input: str, context: str) -> str:
    return response_chain.run(user_input=user_input, context=context).strip()