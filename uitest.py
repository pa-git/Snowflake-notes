import streamlit as st
import pandas as pd
import time

# Configure page layout and custom CSS.
st.set_page_config(layout="wide", page_title="PDF Quote Extractor")
custom_css = """
<style>
/* Remove extra side padding and increase progress bar height, remove rounded corners */
.block-container {
    padding-left: 1rem;
    padding-right: 1rem;
}
div[role="progressbar"] > div {
    height: 40px !important;
    border-radius: 0 !important;
}
* {
    border-radius: 0 !important;
}
/* Hide the header text for the first column (the checkbox column) in the data editor */
div[data-baseweb="data-table"] thead tr th:first-child {
    color: transparent !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------
# Sample Data and Initialization
# ---------------------------
available_pdfs = [f"Document_{i}.pdf" for i in range(1, 21)]
predefined_themes = [
    "Inflation", "Income", "AI", "Healthcare", "Education", "Climate",
    "Technology", "Politics", "Economy", "Sports", "Entertainment", "Travel"
]

if 'results' not in st.session_state:
    st.session_state.results = {}  # {pdf: {theme: [quotes]}}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'approved_quotes' not in st.session_state:
    st.session_state.approved_quotes = {}  # {pdf: {theme: [approved quotes]}}

# ---------------------------
# Sidebar: PDF and Theme Selection
# ---------------------------
st.sidebar.header("Selection Options")

selected_pdfs = st.sidebar.multiselect(
    "Select PDFs (choose at least 1)",
    options=available_pdfs
)

selected_themes = st.sidebar.multiselect(
    "Select Themes (choose up to 5)",
    options=predefined_themes
)

# ---------------------------
# Processing Simulation Function
# ---------------------------
def process_pdfs(pdfs, themes):
    """
    Simulate processing PDFs by extracting longer dummy quotes for each theme.
    Each PDF is processed sequentially for all selected themes.
    """
    st.session_state.results = {}
    st.session_state.approved_quotes = {}
    st.session_state.logs = []
    progress_bar = st.progress(0)
    log_placeholder = st.empty()  # Shows only the latest log message in real time.
    
    total_tasks = len(pdfs) * len(themes)
    task_counter = 0

    for pdf in pdfs:
        st.session_state.results[pdf] = {}       # To store quotes per theme.
        st.session_state.approved_quotes[pdf] = {}  # To store approved quotes per theme.
        
        log_msg = f"Starting processing for {pdf}."
        st.session_state.logs.append(log_msg)
        log_placeholder.text(st.session_state.logs[-1])
        
        for theme in themes:
            log_msg = f"Processing theme '{theme}' for {pdf}."
            st.session_state.logs.append(log_msg)
            log_placeholder.text(st.session_state.logs[-1])
            
            # Simulate processing delay.
            time.sleep(1)
            
            # Generate 5 longer dummy quotes.
            quotes = [
                f"Quote {i+1} for {pdf} on theme '{theme}': Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                for i in range(5)
            ]
            st.session_state.results[pdf][theme] = quotes
            st.session_state.approved_quotes[pdf][theme] = []  # Initialize empty approved list.
            
            log_msg = f"Completed processing theme '{theme}' for {pdf}."
            st.session_state.logs.append(log_msg)
            log_placeholder.text(st.session_state.logs[-1])
            
            task_counter += 1
            progress_bar.progress(task_counter / total_tasks)
            
        log_msg = f"Finished processing for {pdf}."
        st.session_state.logs.append(log_msg)
        log_placeholder.text(st.session_state.logs[-1])
        
    st.session_state.processing = False
    st.success("Processing completed!")

# ---------------------------
# Submission Button Handler
# ---------------------------
if st.sidebar.button("Submit"):
    if len(selected_pdfs) < 1:
        st.sidebar.error("Please select at least 1 PDF.")
    elif not (1 <= len(selected_themes) <= 5):
        st.sidebar.error("Please select between 1 and 5 themes.")
    else:
        st.session_state.processing = True
        process_pdfs(selected_pdfs, selected_themes)

# ---------------------------
# Main Interface Tabs: Results & Logs (Results first)
# ---------------------------
tabs = st.tabs(["Results", "Logs"])

with tabs[0]:
    st.header("PDF Results and Quote Approval")
    if st.session_state.results:
        pdf_names = list(st.session_state.results.keys())
        pdf_tabs = st.tabs(pdf_names)
        for pdf in pdf_names:
            with pdf_tabs[pdf_names.index(pdf)]:
                st.subheader(f"Results for {pdf}")
                approved_for_pdf = {}
                for theme, quotes in st.session_state.results[pdf].items():
                    st.markdown(f"**Theme: {theme}**")
                    # Build a DataFrame with two columns: a boolean for selection and the quote text.
                    # The "Select" column will serve as the checkbox column.
                    df = pd.DataFrame({
                        "Select": [False] * len(quotes),
                        "Quote": quotes
                    })
                    # Display the grid using the data editor. The header for "Select" is hidden via CSS.
                    edited_df = st.data_editor(
                        df,
                        key=f"{pdf}_{theme}_grid",
                        use_container_width=True,
                        num_rows="dynamic"
                    )
                    # Extract the quotes where the checkbox is checked.
                    approved_quotes = edited_df.loc[edited_df["Select"] == True, "Quote"].tolist()
                    approved_for_pdf[theme] = approved_quotes
                st.session_state.approved_quotes[pdf] = approved_for_pdf
                if st.button(f"Resubmit Approved Quotes for {pdf}"):
                    st.write("Approved quotes for", pdf, ":", st.session_state.approved_quotes[pdf])
    else:
        st.info("Results will appear here after processing is complete.")

with tabs[1]:
    st.header("Processing Logs")
    if st.session_state.logs:
        st.text("\n".join(st.session_state.logs))
    else:
        st.info("Logs will appear here once processing starts.")
