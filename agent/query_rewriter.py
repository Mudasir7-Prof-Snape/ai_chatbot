from config import LANGUAGE_MODEL

def rewrite_query(user_query, chat_history):

    history_text = ""

    for chat in chat_history[-5:]:  # last 5 turns only
        history_text += f"User: {chat['user']}\nAssistant: {chat['assistant']}\n"

    prompt = f"""
You are an AI assistant that improves search queries.

Use conversation history to understand context.

Conversation:
{history_text}

Current Question:
{user_query}

Rewrite the question so it is clear and complete for retrieval.

Rewritten Query:
"""

    response = LANGUAGE_MODEL.invoke(prompt)
    return response.strip()