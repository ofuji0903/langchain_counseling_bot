from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

stage_prompt = PromptTemplate.from_file("prompts/stage_classification.txt", input_variables=["input"])
stage_chain = LLMChain(llm=llm, prompt=stage_prompt)

loader = TextLoader("knowledge/counseling_basics.txt")
docs = loader.load()
vectordb = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings(), persist_directory="vectorstore")
vectordb.persist()
retriever = vectordb.as_retriever()

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, memory=memory)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    stage = stage_chain.run(input=user_input)
    print(f"[診断ステージ]: {stage.strip()}")

    response = qa_chain.run(user_input)
    print(f"Bot: {response}\n")
