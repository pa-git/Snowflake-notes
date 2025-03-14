import streamlit as st
import time
import os
import random
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="PDF Quote Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed_pdfs' not in st.session_state:
    st.session_state.processed_pdfs = set()
if 'extraction_complete' not in st.session_state:
    st.session_state.extraction_complete = False
if 'summarization_complete' not in st.session_state:
    st.session_state.summarization_complete = False
if 'approved_quotes' not in st.session_state:
    st.session_state.approved_quotes = {}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'current_process' not in st.session_state:
    st.session_state.current_process = None
if 'summaries' not in st.session_state:
    st.session_state.summaries = {}

# Predefined themes
THEMES = [
    "Inflation", "Income", "Employment", "Economy", "AI", 
    "Technology", "Climate", "Healthcare", "Education", 
    "Housing", "Transportation", "Energy"
]

# Mock PDF data for demonstration
SAMPLE_PDFS = [
    "Economic_Report_2024.pdf", 
    "Technology_Trends.pdf", 
    "Climate_Impact_Analysis.pdf", 
    "Healthcare_Policy_Review.pdf", 
    "Education_Statistics.pdf",
    "Housing_Market_Analysis.pdf"
]

# Function to simulate PDF processing
def process_pdf(pdf_name, themes, progress_bar, log_placeholder):
    st.session_state.current_process = "extraction"
    quotes_by_theme = {}
    
    # Process each theme for the PDF
    total_steps = len(themes)
    for i, theme in enumerate(themes):
        # Log the current processing step
        log_message = f"Processing PDF: {pdf_name} - Theme: {theme}"
        st.session_state.logs.append(log_message)
        log_placeholder.markdown("\n".join(st.session_state.logs))
        
        # Simulate processing time
        time.sleep(random.uniform(0.5, 1.5))
        
        # Generate 5 mock quotes for this theme
        quotes = [f"Quote {j+1} from {pdf_name} about {theme}: Lorem ipsum dolor sit amet, consectetur adipiscing elit." for j in range(5)]
        quotes_by_theme[theme] = quotes
        
        # Update progress
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)
        
        # Store quotes in session state if not already there
        if pdf_name not in st.session_state.approved_quotes:
            st.session_state.approved_quotes[pdf_name] = {}
        st.session_state.approved_quotes[pdf_name][theme] = [False] * len(quotes)
        
        # Add to the set of processed PDFs so we can create tabs
        st.session_state.processed_pdfs.add(pdf_name)
        
    return quotes_by_theme

# Function to simulate summarization
def generate_summaries(progress_bar, log_placeholder):
    st.session_state.current_process = "summarization"
    summaries = {}
    
    # Get all approved quotes
    approved_quotes_list = []
    for pdf_name, themes_data in st.session_state.approved_quotes.items():
        for theme, approvals in themes_data.items():
            quotes = [f"Quote {j+1} from {pdf_name} about {theme}: Lorem ipsum dolor sit amet, consectetur adipiscing elit." for j in range(5)]
            approved = [quotes[i] for i, is_approved in enumerate(approvals) if is_approved]
            if approved:
                approved_quotes_list.append((pdf_name, theme, approved))
    
    # Process approved quotes
    total_steps = len(approved_quotes_list)
    for i, (pdf_name, theme, quotes) in enumerate(approved_quotes_list):
        # Log the current summarization step
        log_message = f"Summarizing quotes from {pdf_name} for theme: {theme}"
        st.session_state.logs.append(log_message)
        log_placeholder.markdown("\n".join(st.session_state.logs))
        
        # Simulate processing time
        time.sleep(random.uniform(0.5, 1.0))
        
        # Generate a mock summary
        if theme not in summaries:
            summaries[theme] = []
        summaries[theme].append(f"Summary for {theme} from {pdf_name}: Based on the approved quotes, we can conclude that...")
        
        # Update progress
        progress = (i + 1) / total_steps if total_steps > 0 else 1.0
        progress_bar.progress(progress)
    
    return summaries

# Main application
def main():
    st.title("PDF Quote Extraction and Summarization")
    
    # Create a multi-tab layout with main tabs
    tab_selection, tab_logs, tab_results, tab_summaries = st.tabs([
        "Select PDFs & Themes", 
        "Logs", 
        "Results",
        "Summaries" if st.session_state.summarization_complete else "Hidden"
    ])
    
    # Tab 1: PDF and Theme Selection
    with tab_selection:
        st.header("PDF and Theme Selection")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_pdfs = st.multiselect(
                "Select PDFs to process",
                options=SAMPLE_PDFS,
                default=None,
                help="Select one or more PDFs for quote extraction"
            )
        
        with col2:
            selected_themes = st.multiselect(
                "Select themes to extract",
                options=THEMES,
                default=None,
                help="Select one or more themes for quote extraction"
            )
        
        # Validate selections before enabling submit button
        if not selected_pdfs:
            st.warning("Please select at least one PDF.")
        if not selected_themes:
            st.warning("Please select at least one theme.")
        
        submit_disabled = not (selected_pdfs and selected_themes)
        
        if st.button("Submit", disabled=submit_disabled):
            st.session_state.extraction_complete = False
            st.session_state.summarization_complete = False
            st.session_state.processed_pdfs = set()
            st.session_state.logs = []
            st.session_state.approved_quotes = {}
            st.session_state.summaries = {}
            
            # Create progress bar and log area
            progress_bar = st.progress(0)
            log_placeholder = st.empty()
            
            # Process each PDF
            for pdf_index, pdf_name in enumerate(selected_pdfs):
                st.session_state.logs.append(f"Starting processing of {pdf_name}")
                log_placeholder.markdown("\n".join(st.session_state.logs))
                
                # Process the PDF with selected themes
                quotes_by_theme = process_pdf(pdf_name, selected_themes, progress_bar, log_placeholder)
                
                # Update overall progress
                overall_progress = (pdf_index + 1) / len(selected_pdfs)
                progress_bar.progress(overall_progress)
            
            st.session_state.extraction_complete = True
            st.session_state.logs.append("Quote extraction complete!")
            log_placeholder.markdown("\n".join(st.session_state.logs))
            
            # Rerun to show the PDF tabs
            st.experimental_rerun()
    
    # Tab 2: Logs
    with tab_logs:
        st.header("Processing Logs")
        log_container = st.container()
        with log_container:
            st.markdown("\n".join(st.session_state.logs))
    
    # Tab 3: Results with PDF sub-tabs
    with tab_results:
        st.header("Extraction Results")
        
        if not st.session_state.processed_pdfs:
            st.info("No PDFs have been processed yet. Please select PDFs and themes, then click 'Submit'.")
        else:
            # Create sub-tabs for each processed PDF
            pdf_tabs = st.tabs([f"{pdf}" for pdf in st.session_state.processed_pdfs])
            
            # PDF Sub-Tabs
            for i, pdf_name in enumerate(st.session_state.processed_pdfs):
                with pdf_tabs[i]:
                    st.subheader(f"Extracted Quotes from {pdf_name}")
                    
                    if pdf_name in st.session_state.approved_quotes:
                        for theme, approvals in st.session_state.approved_quotes[pdf_name].items():
                            st.subheader(f"Theme: {theme}")
                            
                            quotes = [f"Quote {j+1} from {pdf_name} about {theme}: Lorem ipsum dolor sit amet, consectetur adipiscing elit." for j in range(5)]
                            
                            for j, quote in enumerate(quotes):
                                key = f"{pdf_name}_{theme}_{j}"
                                st.session_state.approved_quotes[pdf_name][theme][j] = st.checkbox(
                                    quote,
                                    value=st.session_state.approved_quotes[pdf_name][theme][j],
                                    key=key
                                )
            
            # Summarization button (only show if extraction is complete)
            if st.session_state.extraction_complete:
                st.header("Quote Summarization")
                if st.button("Summarize Approved Quotes"):
                    st.session_state.summarization_complete = False
                    
                    # Create progress bar and update log placeholder
                    progress_bar = st.progress(0)
                    log_placeholder = st.empty()
                    
                    # Generate summaries
                    st.session_state.logs.append("Starting summarization process...")
                    log_placeholder.markdown("\n".join(st.session_state.logs))
                    
                    st.session_state.summaries = generate_summaries(progress_bar, log_placeholder)
                    
                    st.session_state.summarization_complete = True
                    st.session_state.logs.append("Summarization complete!")
                    log_placeholder.markdown("\n".join(st.session_state.logs))
                    
                    # Rerun to show the summaries tab
                    st.experimental_rerun()
    
    # Summaries Tab (only show if summarization is complete)
    if st.session_state.summarization_complete:
        with tab_summaries:
            st.header("Generated Summaries")
            
            if not st.session_state.summaries:
                st.warning("No summaries available. Please select and approve quotes first.")
            else:
                for theme, summaries in st.session_state.summaries.items():
                    st.subheader(f"Theme: {theme}")
                    for summary in summaries:
                        st.markdown(f"**{summary}**")
                        st.markdown("---")

# Run the application
if __name__ == "__main__":
    main()
