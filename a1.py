def format_history_as_markdown(history):
    # Only keep the last 10 items (5 turns)
    history = history[-10:]

    md = ""
    for i in range(0, len(history), 2):
        turn_num = (i // 2) + 1
        md += f"---- Turn {turn_num} ----\n"

        for j in range(2):
            if i + j < len(history):
                msg = history[i + j]
                author = msg["author"].capitalize()
                content = msg["content"].strip()
                md += f"**{author}:** {content}\n"

        md += "\n"

    return md
