from agent.query_rewriter import rewrite_query
from retrieval.retriever import retrieve_documents
from agent.generator import generate_answer
from agent.validator import validate_answer


def agentic_rag_pipeline(user_query, chat_history):

    # # Step 1: Context-aware rewrite
    improved_query = rewrite_query(user_query, chat_history)
    print(improved_query)

    # Step 2: Retrieve
    docs = retrieve_documents(user_query)

    # Step 3: Generate
    answer = generate_answer(user_query, docs, chat_history)

    # Step 4: Validate
    # final_answer = validate_answer(user_query, answer, docs)

    # # Step 5: Retry fallback
    # if final_answer is None:
    #     docs = retrieve_documents(user_query)
    #     answer = generate_answer(user_query, docs, chat_history)
    #     return answer

    return answer