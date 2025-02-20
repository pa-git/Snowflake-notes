import streamlit as st
import time

# ---------------------------
# Page Setup and Custom CSS
# ---------------------------
st.set_page_config(layout="wide", page_title="PDF Quote Extractor")
st.markdown(
    """
    <style>
    /* Remove all rounded corners */
    * {
        border-radius: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Sample Data and Initialization
# ---------------------------
available_pdfs = [f"Document_{i}.pdf" for i in range(1, 21)]  # 20 PDFs available
predefined_themes = [
    "Inflation", "Income", "AI", "Healthcare", "Education", "Climate",
    "Technology", "Politics", "Economy", "Sports", "Entertainment", "Travel"
]

if 'results' not in st.session_state:
    st.session_state.results = {}  # structure: { pdf: { theme: [quotes] } }
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'approved_quotes' not in st.session_state:
    st.session_state.approved_quotes = {}  # structure: { pdf: { theme: [approved quotes] } }

# ---------------------------
# Sidebar: PDF and Theme Selection
# ---------------------------
st.sidebar.header("Selection Options")
selected_pdfs = st.sidebar.multiselect(
    "Select PDFs (choose at least 1)",
    options=available_pdfs,
)
selected_themes = st.sidebar.multiselect(
    "Select Themes (choose up to 5)",
    options=predefined_themes,
)

# ---------------------------
# Processing Simulation Function
# ---------------------------
def process_pdfs(pdfs, themes):
    """
    Simulate processing PDFs by extracting quotes per theme.
    For each PDF, each selected theme is processed sequentially.
    """
    st.session_state.results = {}
    st.session_state.approved_quotes = {}
    st.session_state.logs = []
    progress_bar = st.progress(0)
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

            # Simulate processing delay (replace with actual processing)
            time.sleep(1)

            # Simulate extraction of 5 longer quotes for the given PDF and theme.
            long_quote = (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            )
            quotes = [
                f"{long_quote} (Quote {i+1} for {pdf} on theme '{theme}')" for i in range(5)
            ]
            st.session_state.results[pdf][theme] = quotes
            st.session_state.approved_quotes[pdf][theme] = []  # Initialize as empty list

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
# Main Interface Tabs: Results (first) and Logs (second)
# ---------------------------
tabs = st.tabs(["Results", "Logs"])

with tabs[0]:
    st.header("PDF Results and Quote Approval")
    if st.session_state.results:
        # For each processed PDF, create a sub-tab
        pdf_names = list(st.session_state.results.keys())
        pdf_tabs = st.tabs(pdf_names)
        for idx, pdf in enumerate(pdf_names):
            with pdf_tabs[idx]:
                st.subheader(f"Results for {pdf}")
                for theme, quotes in st.session_state.results[pdf].items():
                    st.markdown(f"**Theme: {theme}**")
                    # For each quote, simulate a table row with two columns:
                    #  - Left: interactive checkbox
                    #  - Right: quote text in a bordered cell
                    for i, quote in enumerate(quotes):
                        # Alternate row colors: white for even rows, light grey for odd rows.
                        row_color = "#ffffff" if i % 2 == 0 else "#f0f0f0"
                        col1, col2 = st.columns([1, 9])
                        with col1:
                            # Render checkbox without a label
                            approved = st.checkbox("", key=f"{pdf}_{theme}_{i}")
                        with col2:
                            st.markdown(
                                f"<div style='border:1px solid black; padding:5px; background-color:{row_color}; border-radius:0;'>{quote}</div>",
                                unsafe_allow_html=True,
                            )
                        # Save approved quotes if checkbox is checked
                        if approved and quote not in st.session_state.approved_quotes[pdf][theme]:
                            st.session_state.approved_quotes[pdf][theme].append(quote)

                    # Button to (re)submit approved quotes for this PDF and theme.
                    if st.button(f"Resubmit Approved Quotes for {pdf} - {theme}", key=f"resubmit_{pdf}_{theme}"):
                        st.write("Approved quotes submitted for", pdf, "theme", theme)
                        st.write(st.session_state.approved_quotes[pdf][theme])
    else:
        st.info("Results will appear here after processing is complete.")

with tabs[1]:
    st.header("Processing Logs")
    if st.session_state.logs:
        st.text("\n".join(st.session_state.logs))
    else:
        st.info("Logs will appear here once processing starts.")
