import streamlit as st
import pandas as pd

st.title("Chatbot UI with Streamlit")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_bot_response(user_message):
    # For demonstration, the bot returns a list of tuples.
    # Replace this with your chatbot logic or API call.
    # Example response: list of tuples (key, value) to display as a table.
    return [
        ("User Input", user_message),
        ("Response", f"Echo: {user_message}")
    ]

# Display the chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["message"])
    elif chat["role"] == "assistant":
        # Convert the list of tuples to a DataFrame and display as a table.
        df = pd.DataFrame(chat["message"], columns=["Attribute", "Content"])
        st.table(df)

# Capture user input
user_input = st.chat_input("Your message:")

if user_input:
    # Append the user message to chat history
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    # Generate bot response (a list of tuples)
    bot_response = get_bot_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "message": bot_response})
    # Rerun the app to update the chat window with the new messages
    st.experimental_rerun()
