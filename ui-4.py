import streamlit as st
import time

# ----------------------------
# INITIALIZE SESSION STATE
# ----------------------------
if "processing_started" not in st.session_state:
    st.session_state.processing_started = False
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False
if "pdf_quotes" not in st.session_state:
    st.session_state.pdf_quotes = {}  # { pdf: { theme: [quotes] } }
if "logs" not in st.session_state:
    st.session_state.logs = []
if "approved_quotes" not in st.session_state:
    st.session_state.approved_quotes = {}  # { pdf: { theme: [approved quotes] } }
if "summaries" not in st.session_state:
    st.session_state.summaries = {}  # { pdf: summary }

# ----------------------------
# DUMMY DATA
# ----------------------------
available_pdfs = ["Document1.pdf", "Document2.pdf", "Document3.pdf"]
available_themes = [
    "Inflation", "Income", "AI", "Technology", "Health", "Finance",
    "Education", "Environment", "Politics", "Sports", "Culture", "Innovation"
]

# ----------------------------
# SIDEBAR: PDF & THEME SELECTION
# ----------------------------
st.sidebar.header("PDF & Theme Selection")
selected_pdfs = st.sidebar.multiselect("Select PDFs", available_pdfs)
selected_themes = st.sidebar.multiselect("Select Themes", available_themes)

# Check that both selections have at least one item.
if not selected_pdfs or not selected_themes:
    st.sidebar.warning("Please select at least one PDF and one theme.")
    submit_disabled = True
else:
    submit_disabled = False

# ----------------------------
# FUNCTION: PROCESS PDFs & EXTRACT QUOTES
# ----------------------------
def process_pdfs(pdfs, themes):
    st.session_state.processing_started = True
    st.session_state.processing_complete = False
    st.session_state.pdf_quotes = {}
    st.session_state.approved_quotes = {}
    st.session_state.logs = []
    
    total_steps = len(pdfs) * len(themes)
    step = 0

    # Placeholders for progress and logs
    progress_placeholder = st.empty()
    logs_placeholder = st.empty()

    # Process each PDF sequentially
    for pdf in pdfs:
        st.session_state.pdf_quotes[pdf] = {}
        st.session_state.approved_quotes[pdf] = {}
        for theme in themes:
            # Simulate processing delay (e.g. extracting quotes for this theme)
            time.sleep(1)
            # Simulate 5 extracted quotes per theme
            quotes = [f"{pdf} - {theme} Quote {i+1}" for i in range(5)]
            st.session_state.pdf_quotes[pdf][theme] = quotes
            
            # Log this processing step
            log_message = f"Processed theme '{theme}' for {pdf}"
            st.session_state.logs.append(log_message)
            
            # Update progress
            step += 1
            progress_placeholder.progress(int((step / total_steps) * 100))
            logs_placeholder.text("\n".join(st.session_state.logs))
        
    st.session_state.processing_complete = True
    st.success("PDF Processing Completed")

# ----------------------------
# SIDEBAR: SUBMIT BUTTON
# ----------------------------
if st.sidebar.button("Submit", disabled=submit_disabled):
    process_pdfs(selected_pdfs, selected_themes)

# ----------------------------
# MAIN AREA: DISPLAY RESULTS WHEN PROCESSING IS COMPLETE
# ----------------------------
if st.session_state.processing_started:
    st.header("Processing Results")

    # Create tabs: one for Logs and one per PDF.
    # The Summaries tab will be added later once summarization is done.
    tab_names = ["Logs"] + list(st.session_state.pdf_quotes.keys())
    tabs = st.tabs(tab_names)

    # ----- Logs Tab -----
    with tabs[0]:
        st.subheader("Logs")
        for log in st.session_state.logs:
            st.write(log)

    # ----- PDF-Specific Tabs -----
    tab_index = 1  # Start after "Logs" tab
    for pdf, themes_dict in st.session_state.pdf_quotes.items():
        with tabs[tab_index]:
            st.subheader(f"Quotes for {pdf}")
            for theme, quotes in themes_dict.items():
                st.markdown(f"**Theme: {theme}**")
                # Initialize approved quotes for this theme if needed
                if theme not in st.session_state.approved_quotes[pdf]:
                    st.session_state.approved_quotes[pdf][theme] = []
                for i, quote in enumerate(quotes):
                    # Each quote gets a checkbox for approval. Use a unique key.
                    approved = st.checkbox(quote, key=f"{pdf}_{theme}_{i}")
                    # If checked and not already added, store it
                    if approved and quote not in st.session_state.approved_quotes[pdf][theme]:
                        st.session_state.approved_quotes[pdf][theme].append(quote)
            st.markdown("### Approved Quotes")
            st.write(st.session_state.approved_quotes[pdf])
        tab_index += 1

    # ----------------------------
    # SUMMARIZATION SECTION
    # ----------------------------
    st.markdown("---")
    if st.button("Summarize"):
        # Clear previous summaries and reinitialize progress
        st.session_state.summaries = {}
        st.session_state.logs.append("Summarization started.")
        progress_placeholder = st.empty()
        progress_placeholder.progress(0)
        
        total_pdfs = len(st.session_state.approved_quotes)
        current_pdf = 0
        
        # Process each PDF's approved quotes
        for pdf, themes in st.session_state.approved_quotes.items():
            time.sleep(1)  # Simulate summarization delay
            # For demonstration, concatenate all approved quotes to form a summary.
            all_approved = []
            for quote_list in themes.values():
                all_approved.extend(quote_list)
            summary_text = f"Summary for {pdf}: " + ("; ".join(all_approved) if all_approved else "No approved quotes.")
            st.session_state.summaries[pdf] = summary_text
            current_pdf += 1
            progress_placeholder.progress(int((current_pdf / total_pdfs) * 100))
            st.session_state.logs.append(f"Summarized {pdf}")
        
        st.session_state.logs.append("Summarization completed.")
        st.success("Summarization Completed")

    # Display Summaries if they exist.
    if st.session_state.summaries:
        st.header("Summaries")
        for pdf, summary in st.session_state.summaries.items():
            st.markdown(f"**{pdf}**")
            st.write(summary)
