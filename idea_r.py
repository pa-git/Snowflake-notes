import os
import json
import openai

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Set your OpenAI API key. Either use the OPENAI_API_KEY environment variable
# or replace "YOUR_API_KEY" with your actual key.
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")

# ------------------------------------------------------------------
# System Message (kept separate from the prompt template)
# ------------------------------------------------------------------
SYSTEM_MESSAGE = (
    "You are a helpful assistant that extracts relevant quotes from investor relations call transcripts."
)

# ------------------------------------------------------------------
# Prompt Template (kept separate from the GPT-4 querying function)
# ------------------------------------------------------------------
PROMPT_TEMPLATE = """
You are a skilled financial analyst who can extract the most relevant quotes from investor relations call transcripts.

Theme: {theme}
Theme Description: {theme_description}

Focus for Theme:
{theme_focus}

Below are 20 chunks from the transcript of a recent investor relations call from a big bank:
------------------------------------------------
{chunks_text}
------------------------------------------------

Your task is to identify the five quotes from these chunks that are most relevant to the theme.
Please return your answer as a JSON array containing exactly five strings, each string being one quote.
The JSON should look like this:
[
  "Quote 1",
  "Quote 2",
  "Quote 3",
  "Quote 4",
  "Quote 5"
]
Make sure to return only the JSON in your response.
"""

def build_prompt(theme, theme_description, theme_focus, chunks_text):
    """
    Builds the prompt by filling in the prompt template with the provided parameters.
    """
    return PROMPT_TEMPLATE.format(
        theme=theme,
        theme_description=theme_description,
        theme_focus=theme_focus,
        chunks_text=chunks_text
    )

# ------------------------------------------------------------------
# Function to Load, Split, Index the PDF, and Retrieve Top Chunks
# ------------------------------------------------------------------
def get_relevant_chunks(pdf_path, query, k=20):
    """
    Loads a PDF, splits it into chunks using a recursive text splitter, indexes the chunks
    in a ChromaDB vector store with OpenAI embeddings, and then retrieves the top-k chunks
    most relevant to the provided query.
    
    Returns a string with the retrieved chunks formatted for the prompt.
    """
    # Load the PDF using LangChain's PyPDFLoader.
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split the documents into smaller chunks.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)

    # Create embeddings using OpenAIEmbeddings.
    embeddings = OpenAIEmbeddings()

    # Create (or load) a ChromaDB index from the chunks.
    vectorstore = Chroma.from_documents(
        split_docs,
        embeddings,
        collection_name="investors_call",
        persist_directory="chroma_db"
    )

    # Retrieve the top-k most relevant chunks using the query.
    relevant_docs = vectorstore.similarity_search(query, k=k)

    # Format the retrieved chunks for inclusion in the prompt.
    chunks_text = "\n\n".join(
        [f"Chunk {i+1}:\n{doc.page_content}" for i, doc in enumerate(relevant_docs)]
    )
    return chunks_text

# ------------------------------------------------------------------
# Function to Query GPT-4 for the Relevant Quotes
# ------------------------------------------------------------------
def query_gpt4(prompt):
    """
    Sends the provided prompt (with system and user messages) to GPT-4
    and returns the assistant's completion.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )
    return response['choices'][0]['message']['content']

# ------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------
def main():
    # Define the theme, its description, and what to focus on.
    theme = "NII"
    theme_description = (
        "A financial metric that compares the interest earned on assets to the interest paid on liabilities. "
        "NII is a key indicator of a bank's profitability."
    )
    
    theme_focus = (
        "For the theme 'NII' (Net Interest Income), look for quotes discussing the bank's interest income on assets, "
        "interest expenses on liabilities, net interest margin, and any commentary regarding changes in interest rates "
        "or the cost of funds. The selected quotes should provide insights into how the bank manages its income relative "
        "to its liabilities."
    )
    
    # Path to the PDF document (update as needed).
    pdf_path = "investors_call.pdf"
    
    # Retrieve 20 relevant chunks from the PDF using the theme description as the query.
    chunks_text = get_relevant_chunks(pdf_path, query=theme_description, k=20)
    
    # Build the prompt using the separate prompt template.
    prompt = build_prompt(theme, theme_description, theme_focus, chunks_text)
    
    # Query GPT-4 using the constructed prompt.
    gpt4_response = query_gpt4(prompt)
    
    # Try to parse the response as JSON.
    try:
        quotes = json.loads(gpt4_response)
        print("Extracted Quotes:")
        print(json.dumps(quotes, indent=2))
    except json.JSONDecodeError:
        print("Error: The response could not be parsed as valid JSON. Here is the raw response:")
        print(gpt4_response)

if __name__ == "__main__":
    main()
