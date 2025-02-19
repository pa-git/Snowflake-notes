import streamlit as st
import time

# ---------------------------
# Sample Data and Initialization
# ---------------------------

# Simulate available PDFs and predefined themes
available_pdfs = [f"Document_{i}.pdf" for i in range(1, 21)]  # 20 PDFs available
predefined_themes = [
    "Inflation", "Income", "AI", "Healthcare", "Education", "Climate",
    "Technology", "Politics", "Economy", "Sports", "Entertainment", "Travel"
]

# Initialize session state variables if not already present
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
    "Select PDFs (choose between 5 and 10)",
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
    logs_placeholder = st.empty()

    total_tasks = len(pdfs) * len(themes)
    task_counter = 0

    # Loop over each selected PDF
    for pdf in pdfs:
        st.session_state.results[pdf] = {}      # Will hold {theme: [quotes]}
        st.session_state.approved_quotes[pdf] = {}  # For approved quotes per theme

        # Log starting the PDF processing
        log_msg = f"Starting processing for {pdf}."
        st.session_state.logs.append(log_msg)
        logs_placeholder.text("\n".join(st.session_state.logs))
        
        # Process each theme for this PDF
        for theme in themes:
            log_msg = f"Processing theme '{theme}' for {pdf}."
            st.session_state.logs.append(log_msg)
            logs_placeholder.text("\n".join(st.session_state.logs))
            
            # Simulate a processing delay (replace with your actual processing logic)
            time.sleep(1)

            # Simulate extraction of 5 quotes
            quotes = [f"Quote {i+1} for {pdf} on theme '{theme}'." for i in range(5)]
            st.session_state.results[pdf][theme] = quotes
            st.session_state.approved_quotes[pdf][theme] = []  # Initialize empty approved list

            log_msg = f"Completed processing theme '{theme}' for {pdf}."
            st.session_state.logs.append(log_msg)
            logs_placeholder.text("\n".join(st.session_state.logs))

            task_counter += 1
            progress_bar.progress(task_counter / total_tasks)
        
        log_msg = f"Finished processing for {pdf}."
        st.session_state.logs.append(log_msg)
        logs_placeholder.text("\n".join(st.session_state.logs))

    st.session_state.processing = False
    st.success("Processing completed!")

# ---------------------------
# Submission Button Handler
# ---------------------------

if st.sidebar.button("Submit"):
    # Validate PDF selection (5 to 10 PDFs)
    if not (5 <= len(selected_pdfs) <= 10):
        st.sidebar.error("Please select between 5 and 10 PDFs.")
    # Validate theme selection (up to 5 themes, at least 1)
    elif not (1 <= len(selected_themes) <= 5):
        st.sidebar.error("Please select between 1 and 5 themes.")
    else:
        st.session_state.processing = True
        # Start processing (this loop will update logs and progress bar in real-time)
        process_pdfs(selected_pdfs, selected_themes)

# ---------------------------
# Main Interface Tabs: Logs & Results
# ---------------------------

tabs = st.tabs(["Logs", "Results"])

with tabs[0]:
    st.header("Processing Logs")
    if st.session_state.logs:
        st.text("\n".join(st.session_state.logs))
    else:
        st.info("Logs will appear here once processing starts.")

with tabs[1]:
    st.header("PDF Results and Quote Approval")
    if st.session_state.results:
        # Create a tab for each processed PDF
        pdf_names = list(st.session_state.results.keys())
        pdf_tabs = st.tabs(pdf_names)
        for idx, pdf in enumerate(pdf_names):
            with pdf_tabs[idx]:
                st.subheader(f"Results for {pdf}")
                # For each theme within the PDF, display the quotes and approval checkboxes
                for theme, quotes in st.session_state.results[pdf].items():
                    st.markdown(f"**Theme: {theme}**")
                    approved = []
                    for quote in quotes:
                        # Create a unique key for each checkbox to avoid collisions
                        checkbox_key = f"{pdf}_{theme}_{quote}"
                        if st.checkbox(quote, key=checkbox_key):
                            approved.append(quote)
                    # Update approved quotes in session state
                    st.session_state.approved_quotes[pdf][theme] = approved

                # Button to (re)submit approved quotes for this PDF
                if st.button(f"Resubmit Approved Quotes for {pdf}"):
                    # Replace the following with your backend submission logic
                    st.write("Approved quotes submitted for", pdf)
                    st.write(st.session_state.approved_quotes[pdf])
    else:
        st.info("Results will appear here after processing is complete.")
