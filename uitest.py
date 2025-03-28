import streamlit as st
import time

# Set page configuration for wide layout
st.set_page_config(layout="wide", page_title="PDF Quote Extractor")

# Custom CSS for layout and styling adjustments
custom_css = """
<style>
/* Use more screen space by reducing container padding */
.block-container {
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Remove all rounded corners for all elements */
* {
    border-radius: 0 !important;
}

/* Style all buttons with dark blue background and bold white text */
.stButton button {
    background-color: #00008B !important;
    color: white !important;
    font-weight: bold !important;
    border: none !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------
# Sample Data and Initialization
# ---------------------------
available_pdfs = [f"Document_{i}.pdf" for i in range(1, 21)]  # 20 PDFs available
predefined_themes = [
    "Inflation", "Income", "AI", "Healthcare", "Education", "Climate",
    "Technology", "Politics", "Economy", "Sports", "Entertainment", "Travel"
]

if 'results' not in st.session_state:
    st.session_state.results = {}  # {pdf_name: {theme: [quotes, ...]}}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'approved_quotes' not in st.session_state:
    st.session_state.approved_quotes = {}  # {pdf_name: {theme: [approved quotes, ...]}}

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
    Simulate processing PDFs by extracting quotes per theme.
    Each PDF is processed sequentially with all themes.
    """
    st.session_state.results = {}
    st.session_state.approved_quotes = {}
    st.session_state.logs = []
    progress_bar = st.progress(0)
    # Placeholder to show only the most recent log message in real time
    log_placeholder = st.empty()

    total_tasks = len(pdfs) * len(themes)
    task_counter = 0

    for pdf in pdfs:
        st.session_state.results[pdf] = {}
        st.session_state.approved_quotes[pdf] = {}

        log_msg = f"Starting processing for {pdf}."
        st.session_state.logs.append(log_msg)
        log_placeholder.text(st.session_state.logs[-1])
        
        for theme in themes:
            log_msg = f"Processing theme '{theme}' for {pdf}."
            st.session_state.logs.append(log_msg)
            log_placeholder.text(st.session_state.logs[-1])
            
            # Simulate a processing delay
            time.sleep(1)

            # Generate longer example quotes
            quotes = [
                f"Quote {i+1} for {pdf} on theme '{theme}': This detailed quote explores various aspects of {theme}, providing deep insights and comprehensive analysis of the underlying issues and trends."
                for i in range(5)
            ]
            st.session_state.results[pdf][theme] = quotes
            st.session_state.approved_quotes[pdf][theme] = []

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
    # Validate PDF selection (minimum 1 PDF)
    if not (len(selected_pdfs) >= 1):
        st.sidebar.error("Please select at least 1 PDF.")
    # Validate theme selection (between 1 and 5)
    elif not (1 <= len(selected_themes) <= 5):
        st.sidebar.error("Please select between 1 and 5 themes.")
    else:
        st.session_state.processing = True
        process_pdfs(selected_pdfs, selected_themes)

# ---------------------------
# Main Interface Tabs: Results first, Logs second
# ---------------------------
tabs = st.tabs(["Results", "Logs"])

with tabs[0]:
    st.header("PDF Results and Quote Approval")
    if st.session_state.results:
        # Create a tab for each processed PDF
        pdf_names = list(st.session_state.results.keys())
        pdf_tabs = st.tabs(pdf_names)
        for idx, pdf in enumerate(pdf_names):
            with pdf_tabs[idx]:
                st.subheader(f"Results for {pdf}")
                for theme, quotes in st.session_state.results[pdf].items():
                    st.markdown(f"**Theme: {theme}**")
                    approved = []
                    # Display each quote with a checkbox to its immediate left
                    for quote in quotes:
                        checkbox_key = f"{pdf}_{theme}_{quote}"
                        if st.checkbox(quote, key=checkbox_key):
                            approved.append(quote)
                    st.session_state.approved_quotes[pdf][theme] = approved

                # Button to resubmit approved quotes for this PDF
                if st.button(f"Resubmit Approved Quotes for {pdf}"):
                    st.write("Approved quotes submitted for", pdf)
                    st.write(st.session_state.approved_quotes[pdf])
    else:
        st.info("Results will appear here after processing is complete.")

with tabs[1]:
    st.header("Processing Logs")
    if st.session_state.logs:
        st.text("\n".join(st.session_state.logs))
    else:
        st.info("Logs will appear here once processing starts.")
