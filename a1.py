with gr.Blocks(css=custom_css) as demo:
    gr.ChatInterface(
        analyst_chat,
        title="Chat with Your Contracts",
        type="messages",
        flagging_mode="manual",
        flagging_options=["Correct", "Incorrect"],
        save_history=True,
        theme=gr.themes.Default(primary_hue="blue"),
    )
    
    # Footer section
    gr.HTML('<div class="footer">🔒 Your chat is private and secure. Powered by GPT-4o.</div>')

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("SERVER_PORT")),
        auth=authentication()
    )
