# カウンセリングチャットボット V3 仕様書（2025/04/22 修正版）

---

## 1. 概要

このバージョンでは、**LangGraph** による状態遷移とを実装しました。

- ノード構成と処理フロー
- `conversation_history` による会話文脈の保持
- ステージ分類＋簡易RAGによるコンテキスト強化

＞現状では単なるテキストナレッジです。ここをRAGデータベースに置き換えられるように予定しています

- 文脈をメモリーすることで一貫性のある会話が可能になっています
- 開発者ログパネルを追加しました。LLMが現在どのような状態で動いているかログ出力されます

---

## 2. LangGraph設計

### 2.1 GraphState（状態スキーマ）

```python
class GraphState(TypedDict):
    user_input: str                          # 現在の入力発言
    conversation_history: list[str]         # 過去の会話履歴（ユーザー発言＋応答）
    stage: str                               # 現在の診断ステージ（4分類）
    knowledge_summary: str                  # ステージに基づいた仮ナレッジ（RAG代替）
    response: str                            # 応答本文
    emotional_intensity: int                # 情緒スコア（仮、固定値60）
```

---

## 3. ノード構成

### 3.1 diagnose_stage

- 入力: `user_input`
- 出力: `{"stage": str}`
- 内容: ユーザー発言からステージ（4分類）を推定する

---

### 3.2 estimate_emotional_intensity

- 入力: `user_input`
- 出力: `{"emotional_intensity": 60}`
- 内容: 現状は固定スコア。将来的にLLMベースの推定に切り替え可能

---

### 3.3 retrieve_and_summarize

- 入力: `user_input`, `stage`
- 出力: `{"knowledge_summary": str}`
- 内容: ステージに応じた仮知識を取得（RAGの代替）

---

### 3.4 generate_bot_response

- 入力: `user_input`, `conversation_history`, `stage`, `knowledge_summary`
- 出力: `{"response": str, "conversation_history": list[str]}`
- 内容: 応答を生成し、`conversation_history` にユーザー発言＋応答を追記

---

## 4. LangGraph ワークフロー

```
[diagnose_stage]
       ↓
[estimate_emotion]
       ↓
[retrieve_knowledge]
       ↓
[generate_response]
       ↓
       END
```

---

## 5. 応答プロンプト構成（内部）

```
これまでの会話履歴:
ユーザー: ○○
AI: △△
ユーザー: ...

現在のユーザー発言:
○○

参考知識（ステージ: {stage}）:
{knowledge_summary}
```

---

## 6. UI構成（Streamlit）

- `st.chat_input` から発話を受け取り `app.invoke()` に渡す
- LangGraphワークフローが動作し、応答を生成
- 表示は `st.chat_message` によりネイティブなチャットUIで表示
- `conversation_history` は `GraphState` 内部で管理（セッションの会話文脈）
- 表示上は `st.session_state.history` を使い、最新10件を表示

---

## 7. 想定拡張（V4 以降）

| 項目 | 内容 |
| --- | --- |
| ✅ セッション構造化 | `conversation_history` を JSONで分離記録（発言区別） |
| ✅ 応答分岐 | `emotional_intensity` によって応答文体や内容を切替 |
| ✅ マルチモード | 「共感型」「助言型」など複数応答スタイルに分岐 |
| ✅ 高精度RAG | Chroma + FAISS による外部ドキュメント検索統合 |
| ✅ 永続化 | Firestore などでユーザーごとにセッション保存 |

---

## 8. 備考と差分

- `context` → `conversation_history` に名称変更（役割：文脈保持）
- `response_chain.py` のプロンプトが改善され、余計な説明やメタ出力を抑制
- LLMは `gpt-4o`（または `gpt-4o-mini`）に統一
- UIは `st.chat_message` を使用し、カスタムCSSを排除して安定性を向上
- スコアや診断ステージなどの中間値は開発者ログとして表示可能

---

## 📁 フォルダ構成（参考）

```
.
├── main.py                    # Streamlit UI + LangGraph起動
├── graph.py                   # LangGraphワークフロー構成
├── chains/
│   ├── stage_router_chain.py     # ステージ分類ノード
│   ├── response_chain.py         # 応答生成ノード
│   └── rag_interface.py          # 仮ナレッジ提供（将来 RAG化）
├── .env
└── requirements.txt
```

**所感**

最低限のカウンセリング機能が動作するようになりました。

V4ではRAGデータベースと連携し専門性を高める予定です。

- 正しい知識をナレッジとして導入できるか
- 精度の高いベクターデータを導入できるか

この点はプログラムの完成度とは別で専門性の高い分野になってきます。質の高いナレッジを参照できても十分な精度が得られない場合はファインチューニングが必要になると考えます。

今回のPoCでは、あくまで一貫性と臨機応変な対応を目標としていますので、専門知識の参照はRAGデータベースまでとします。
