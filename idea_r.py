import openai
import PyPDF2
import json
import os

# Set your OpenAI API key. Either set the OPENAI_API_KEY environment variable
# or replace "YOUR_API_KEY" with your actual key.
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")

# ------------------------------------------------------------------
# Prompt Template (separate from the GPT-4 querying function)
# ------------------------------------------------------------------
PROMPT_TEMPLATE = """
You are a skilled financial analyst who can extract the most relevant quotes from investor relations call transcripts.

Theme: {theme}
Theme Description: {theme_description}

Focus for Theme:
{theme_focus}

Below is the transcript of a recent investor relations call from a big bank:
------------------------------------------------
{pdf_text}
------------------------------------------------

Your task is to identify the five quotes from the transcript that are most relevant to the theme.
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

def build_prompt(theme, theme_description, theme_focus, pdf_text):
    """
    Builds the prompt by filling in the prompt template with the provided parameters.
    """
    return PROMPT_TEMPLATE.format(
        theme=theme,
        theme_description=theme_description,
        theme_focus=theme_focus,
        pdf_text=pdf_text
    )

# ------------------------------------------------------------------
# Helper Function to Extract Text from the PDF
# ------------------------------------------------------------------
def extract_text_from_pdf(pdf_path):
    """
    Extracts and concatenates text from all pages of a PDF file.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ------------------------------------------------------------------
# Function to Query GPT-4 for the Relevant Quotes
# ------------------------------------------------------------------
def query_gpt4(prompt):
    """
    Sends the provided prompt to GPT-4 and returns the assistant's completion.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts relevant quotes from investor relations call transcripts."},
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
    # Define the theme and its description.
    theme = "NII"
    theme_description = (
        "A financial metric that compares the interest earned on assets to the interest paid on liabilities. "
        "NII is a key indicator of a bank's profitability."
    )
    
    # Define what the model should focus on for this theme.
    theme_focus = (
        "For the theme 'NII' (Net Interest Income), look for quotes discussing the bank's interest income on assets, "
        "interest expenses on liabilities, net interest margin, and any commentary regarding changes in interest rates "
        "or the cost of funds. The selected quotes should provide insights into how the bank manages its income relative "
        "to its liabilities."
    )
    
    # Path to the PDF document (update as needed).
    pdf_path = "investors_call.pdf"
    
    # Extract text from the PDF document.
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Build the prompt using the separate prompt template.
    prompt = build_prompt(theme, theme_description, theme_focus, pdf_text)
    
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
