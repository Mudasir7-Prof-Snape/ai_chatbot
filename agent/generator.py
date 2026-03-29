from config import LANGUAGE_MODEL

def generate_answer(user_query, context_documents, chat_history):

    context_text = "\n\n".join(
        f"[Page {doc.metadata.get('page', 'N/A')}]\n{doc.page_content}"
        for doc in context_documents
    )

    history_text = ""
    for chat in chat_history[-5:]:
        history_text += f"User: {chat['user']}\nAssistant: {chat['assistant']}\n"

    prompt = f"""
You are a highly accurate AI assistant.

Use:
1. Document context (primary source)
2. Conversation history (for understanding)

STRICT RULES:
- Answer ONLY from document context
- Use history only for reference
- If not found say: "I could not find the answer in the document"

Conversation History:
{history_text}

Context:
{context_text}

Question:
{user_query}

Answer:
"""

    response = LANGUAGE_MODEL.invoke(prompt)
    return response.strip()