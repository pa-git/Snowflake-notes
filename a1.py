formatted_history = "\n".join(
    f"{msg['role'].upper()}: {msg['content'].strip()}"
    for msg in history
    if msg["content"] and "|" not in msg["content"]
)
