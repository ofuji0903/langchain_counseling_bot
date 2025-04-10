# LangChain Counseling Bot

This is a minimal counseling support chatbot built with LangChain. It can:

- Classify user's input into counseling stages (rapport, listening, advice, etc.)
- Retrieve knowledge from external documents
- Maintain conversational context using memory

## Setup

1. Clone this repo
2. Create `.env` from `.env.example` and add your OpenAI API key
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the chatbot:

```bash
python main.py
```

## Example
```
User: 最近ストレスがひどくて寝れません
[診断ステージ]: 傾聴（active listening）
Bot: ストレスの状況について詳しく教えていただけますか？また、セルフケアとしては呼吸法も効果的です。
```

---

This project demonstrates LangChain's use of prompt chaining, vector-based document retrieval (RAG), and conversational memory.


---

main.py（全体の処理ロジック）
主な流れ：
.env を読み込んで APIキーなど設定

OpenAIの ChatOpenAI（GPT-3.5）を使用

ConversationBufferMemory で会話履歴を保持

ステージ分類プロンプトを読み込み → LLMChain で診断段階を推論

TextLoader でナレッジ（テキスト）を読み込み → Chroma に埋め込み
>簡易版でナレッジはテキストファイルのみ。本来は事前にテキストやPDFをバッチ処理でEmbedding → VectorStoreに保存

Retriever を通して関連情報を検索

RetrievalQA により、ユーザー発言に対するナレッジ応答を生成

ループで対話を続ける（exit で終了）