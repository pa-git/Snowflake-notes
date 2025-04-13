
history = [
    {"role": _["role"], "content": _["content"]}
    for _ in history
    if _["content"] and "|" not in _["content"]
]
