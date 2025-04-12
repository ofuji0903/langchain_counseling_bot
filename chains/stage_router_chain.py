from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-4o")

stage_prompt = PromptTemplate.from_template(
    "次のユーザー発言を見て、以下の4つのカテゴリのうち最も適切なものを1つだけ日本語で答えてください："
    "「雑談・初期整理」「情緒の沈み・自己否定」「過去の経験の影響」「実生活での困難・課題整理」。\n\n"
    "ユーザー発言：{input}"
)

stage_chain = LLMChain(llm=llm, prompt=stage_prompt)

def get_stage(user_input: str) -> str:
    return stage_chain.run(input=user_input).strip()