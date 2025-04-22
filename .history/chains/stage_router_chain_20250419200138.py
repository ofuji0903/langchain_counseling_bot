# chains/stage_router_chain.py
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o")

stage_prompt = PromptTemplate.from_template(
    "次のユーザー発言を見て、以下の4つのカテゴリのうち最も適切なものを1つだけ日本語で答えてください："
    "「雑談・初期整理」「情緒の沈み・自己否定」「過去の経験の影響」「実生活での困難・課題整理」。\n\n"
    "ユーザー発言：{input}"
)

# LangChain 1.0 以降の推奨形式
chain = stage_prompt | llm

def get_stage(user_input: str) -> str:
    result = chain.invoke({"input": user_input})
    return result.content.strip()
