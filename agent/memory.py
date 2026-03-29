def get_chat_history(session_state):
    return session_state.get("chat_history", [])


def update_chat_history(session_state, user, assistant):

    if "chat_history" not in session_state:
        session_state["chat_history"] = []

    session_state["chat_history"].append({
        "user": user,
        "assistant": assistant
    })