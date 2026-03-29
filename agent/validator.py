from config import LANGUAGE_MODEL

def validate_answer(user_query, answer, context_documents):

    context_text = "\n\n".join(doc.page_content for doc in context_documents)

    prompt = f"""
Check if answer is supported by context.

Return "VALID" or "INVALID".

Question:
{user_query}

Answer:
{answer}

Context:
{context_text}
"""

    result = LANGUAGE_MODEL.invoke(prompt)

    if "INVALID" in result:
        return None

    return answer