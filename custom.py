import os
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import chainlit as cl
from dotenv import load_dotenv
from langchain.llms import LLM
from typing import Optional, List

# Custom LLM Implementation
class MyCustomLLM(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Replace this with your custom LLM logic.
        # For example, you might call an API, run inference locally, etc.
        return "Custom response to: " + prompt

    @property
    def _identifying_params(self):
        return {"name": "MyCustomLLM"}

    @property
    def _llm_type(self) -> str:
        return "custom"

# Load environment variables
load_dotenv('.env')

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """
         You are a friendly assistant that answers user's questions about astronomy.
         If the user's question is not about these topics, 
         respond with "Uh-oh! I do not have the information to answer your question. Ask me about Space, Planets and Stars!".
         """
        ),
        ("user", "{question}\n"),
    ]
)

@cl.on_chat_start
def main():
    # Instantiate the custom LLM for the user session
    llm_chat = MyCustomLLM()
    llm_chain = LLMChain(prompt=prompt_template, llm=llm_chat, verbose=True)

    # Store the chain in the user session for reusability
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")
    # Call the chain asynchronously
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])
    await cl.Message(content=res["text"]).send()
