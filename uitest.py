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
# Title and User Selections
# ---------------------------
st.title("PDF Processing Application")

st.write("Select PDFs and Themes, then click Submit to process.")

selected_pdfs = st.multiselect(
    "Select PDFs (1 to 10)",
    options=available_pdfs
)

selected_themes = st.multiselect(
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
    st.session_state.results = {}
    st.session_state.approved_quotes = {}
    st.session_state.logs = []

    total_tasks = len(pdfs) * len(themes)
    task_counter = 0

    for pdf in pdfs:
        st.session_state.results[pdf] = {}
        st.session_state.approved_quotes[pdf] = {}

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
        st.session_state.logs.append(msg)
        logs_container.text("\n".join(st.session_state.logs))

    st.session_state.processing = False
    st.success("Processing completed!")

# ---------------------------
# Submit Button
# ---------------------------
if st.button("Submit"):
    # Validate selection
    if len(selected_pdfs) < 1:
        st.error("Please select at least 1 PDF.")
    elif len(selected_pdfs) > 10:
        st.error("Please select no more than 10 PDFs.")
    elif len(selected_themes) < 1:
        st.error("Please select at least 1 theme.")
    elif len(selected_themes) > 5:
        st.error("Please select no more than 5 themes.")
    else:
        st.session_state.processing = True

# ---------------------------
# Main Layout: Tabs
# ---------------------------
if st.session_state.processing or st.session_state.results:
    # Build the tab labels: first 'Logs', then each selected PDF
    tab_labels = ["Logs"] + selected_pdfs if selected_pdfs else ["Logs"]
    tabs = st.tabs(tab_labels)

    # First tab: Logs
    with tabs[0]:
        st.header("Processing Logs")
        logs_container = st.empty()    # placeholder for real-time logs
        progress_bar = st.progress(0)  # placeholder for progress

    # One tab per PDF
    for i, pdf in enumerate(selected_pdfs, start=1):
        with tabs[i]:
            st.header(f"Results for {pdf}")
            if pdf in st.session_state.results:
                for theme, quotes in st.session_state.results[pdf].items():
                    st.markdown(f"**Theme: {theme}**")
                    approved = []
                    for quote in quotes:
                        key = f"{pdf}_{theme}_{quote}"
                        if st.checkbox(quote, key=key):
                            approved.append(quote)
                    st.session_state.approved_quotes[pdf][theme] = approved

                if st.button(f"Resubmit Approved Quotes for {pdf}"):
                    # In real code, you'd send these to your backend
                    st.write("Approved quotes submitted for", pdf)
                    st.write(st.session_state.approved_quotes[pdf])
            else:
                st.info("No results yet. Please wait for processing to complete.")

    # If we're in the middle of processing, run the logic now
    if st.session_state.processing:
        process_pdfs(selected_pdfs, selected_themes, logs_container, progress_bar)

else:
    st.info("After submitting, logs and PDF results will appear as tabs.")
