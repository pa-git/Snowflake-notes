import streamlit as st
import time

# ---------------------------
# Sample Data and Initialization
# ---------------------------
available_pdfs = [f"Document_{i}.pdf" for i in range(1, 21)]
predefined_themes = [
    "Inflation", "Income", "AI", "Healthcare", "Education", "Climate",
    "Technology", "Politics", "Economy", "Sports", "Entertainment", "Travel"
]

if 'results' not in st.session_state:
    st.session_state.results = {}  # {pdf_name: {theme: [quotes]}}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'approved_quotes' not in st.session_state:
    st.session_state.approved_quotes = {}  # {pdf_name: {theme: [approved quotes]}}

# ---------------------------
# Sidebar: PDF and Theme Selection
# ---------------------------
st.sidebar.header("Selection Options")

selected_pdfs = st.sidebar.multiselect(
    "Select PDFs (1 to 10)",
    options=available_pdfs
)

selected_themes = st.sidebar.multiselect(
    "Select Themes (1 to 5)",
    options=predefined_themes
)

# ---------------------------
# Processing Function
# ---------------------------
def process_pdfs(pdfs, themes, logs_container, progress_bar):
    """
    Simulate processing PDFs by extracting quotes per theme.
    Logs and progress updates are shown only in the Logs tab via 'logs_container'.
    """
    # Reset data structures
    st.session_state.results = {}
    st.session_state.approved_quotes = {}
    st.session_state.logs = []

    total_tasks = len(pdfs) * len(themes)
    task_counter = 0

    for pdf in pdfs:
        st.session_state.results[pdf] = {}
        st.session_state.approved_quotes[pdf] = {}

        # Log starting the PDF
        msg = f"Starting processing for {pdf}."
        st.session_state.logs.append(msg)
        logs_container.text("\n".join(st.session_state.logs))

        for theme in themes:
            msg = f"Processing theme '{theme}' for {pdf}."
            st.session_state.logs.append(msg)
            logs_container.text("\n".join(st.session_state.logs))

            # Simulate a delay
            time.sleep(1)

            # Simulate extracted quotes
            quotes = [f"Quote {i+1} for {pdf} on theme '{theme}'." for i in range(5)]
            st.session_state.results[pdf][theme] = quotes
            st.session_state.approved_quotes[pdf][theme] = []

            msg = f"Completed theme '{theme}' for {pdf}."
            st.session_state.logs.append(msg)
            logs_container.text("\n".join(st.session_state.logs))

            task_counter += 1
            progress_bar.progress(task_counter / total_tasks)

        msg = f"Finished processing for {pdf}."
  
