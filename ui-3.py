import streamlit as st
import time
import pandas as pd

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

# -------------------------------------------------
# Sample Data and Initialization
# -------------------------------------------------
available_pdfs = [f"Document_{i}.pdf" for i in range(1, 21)]  # 20 PDFs available
predefined_themes = [
    "Inflation", "Income", "AI", "Healthcare", "Education", "Climate",
    "Technology", "Politics", "Economy", "Sports", "Entertainment", "Travel"
]

if 'results' not in st.session_state:
    st.session_state.results = {}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'approved_quotes' not in st.session_state:
    st.session_state.approved_quotes = {}

# -------------------------------------------------
# Sidebar: PDF and Theme Selection
# -------------------------------------------------
st.sidebar.header("Selection Options")

selected_pdfs = st.sidebar.multiselect(
    "Select PDFs (choose at least 1)",
    options=available_pdfs
)

selected_themes = st.sidebar.multiselect(
    "Select Themes (choose up to 5)",
    options=predefined_themes
)

# -------------------------------------------------
# Processing Simulation Function
# -------------------------------------------------
def process_pdfs(pdfs, themes):
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
            
            time.sleep(1)  # Simulate processing delay

            quotes = [
                f"Quote {i+1} for {pdf} on theme '{theme}': This detailed quote explores aspects of {theme}..."
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

# -------------------------------------------------
# Submission Button Handler
# -------------------------------------------------
if st.sidebar.button("Submit"):
    # Validate PDF selection (minimum 1 PDF)
    if not (len(selected_pdfs) >= 1):
        st.sidebar.error("Please select at least 1 PDF.")
    elif not (1 <= len(selected_themes) <= 5):
        st.sidebar.error("Please select between 1 and 5 themes.")
    else:
        st.session_state.processing = True
        process_pdfs(selected_pdfs, selected_themes)

# -------------------------------------------------
# Main Interface Tabs
# -------------------------------------------------
tabs = st.tabs(["Results", "Logs", "Summary"])

with tabs[0]:
    st.header("PDF Results and Quote Approval")
    if st.session_state.results:
        pdf_names = list(st.session_state.results.keys())
        pdf_tabs = st.tabs(pdf_names)
        for idx, pdf in enumerate(pdf_names):
            with pdf_tabs[idx]:
                st.subheader(f"Results for {pdf}")
                for theme, quotes in st.session_state.results[pdf].items():
                    st.markdown(f"**Theme: {theme}**")
                    approved = []
                    for quote in quotes:
                        checkbox_key = f"{pdf}_{theme}_{quote}"
                        if st.checkbox(quote, key=checkbox_key):
                            approved.append(quote)
                    st.session_state.approved_quotes[pdf][theme] = approved

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

with tabs[2]:
    st.header("Summary Grid")
    # -------------------------------------------------
    # Static HTML Table with inline CSS to match the style
    # -------------------------------------------------
    table_html = """
    <div style="overflow-x:auto;">
    <table style="border-collapse: collapse; width:100%; font-family: Arial, sans-serif; table-layout: fixed;">
      <!-- Table Header -->
      <thead>
        <tr>
          <th style="background: #005387; color: #ffffff; text-align: center; width: 10%;"></th>
          <th style="background: #005387; color: #ffffff; text-align: center; width: 18%;">C</th>
          <th style="background: #005387; color: #ffffff; text-align: center; width: 18%;">GS</th>
          <th style="background: #005387; color: #ffffff; text-align: center; width: 18%;">JPM</th>
          <th style="background: #005387; color: #ffffff; text-align: center; width: 18%;">WFC</th>
          <th style="background: #005387; color: #ffffff; text-align: center; width: 18%;">BAC</th>
        </tr>
      </thead>
      <tbody>
        <!-- Row 1: Deposits & Funding -->
        <tr>
          <td style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center; background: #0072CE; color: #ffffff; font-weight: bold; padding: 8px;">
            Deposits &amp; Funding
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            <strong>Mark Mason (CFO)</strong><br>
            "While aggregate deposits are flat to slightly down, we continue to grow checking deposits in line with repositioning the bank. I’m not expecting big net outflows."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            <strong>Denis Coleman (CFO)</strong><br>
            "We add more lending penetration to our existing clients as well as new clients. We keep investing in our brand."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            <strong>Marianne Lake (CFO)</strong><br>
            "We’ve got system-wide deposit growth still trending higher into 2025… continue to add new depositors each quarter."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            <strong>Charlie Scharf (President &amp; CEO)</strong><br>
            "There’s more deposit stability across both consumer and business than we’ve ever seen in the last decade..."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            <strong>Brian Moynihan (Chairman &amp; CEO)</strong><br>
            "This is the second straight quarter of growth in deposits for us. It’s all about strong customer relationships."
          </td>
        </tr>
        <!-- Row 2: Consumer OpEx / Credit / Spending -->
        <tr>
          <td style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center; background: #0072CE; color: #ffffff; font-weight: bold; padding: 8px;">
            Consumer OpEx / Credit / Spending
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We made progress... but we continue to look for opportunities to be more efficient. I’m not expecting big layoffs or anything like that, for now."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "Multiple avenues of growth for us in Wealth... leaning into the consumer space. It's a question of scale."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We expect consumer credit to remain strong, but we remain vigilant. No near-term crisis, but we are prepared."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "[Strategic goals.] Focusing on efficiency and cutting unnecessary overhead. We are well on track to meet the $10B target."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We have to be mindful of cost. AI is also helping us reduce overhead."
          </td>
        </tr>
        <!-- Row 3: Earnings -->
        <tr>
          <td style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center; background: #0072CE; color: #ffffff; font-weight: bold; padding: 8px;">
            Earnings
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We had a strong quarter from an earnings perspective. I'd call out the improvement in net interest margin."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "Our wealth management side is performing well. IB is cyclical, but we see green shoots as the M&amp;A pipeline recovers."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "Expecting 10–12% earnings growth yoy. We see that continuing into 2H. The environment remains stable overall."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "Earnings are up yoy, driven by higher rates. Some normalization in the mortgage business, but strong fundamentals."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We’re looking at a stable to improving environment. As always, we remain disciplined on risk."
          </td>
        </tr>
        <!-- Row 4: Capital / B&S -->
        <tr>
          <td style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center; background: #0072CE; color: #ffffff; font-weight: bold; padding: 8px;">
            Capital &amp; B&amp;S
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "Capital ratios remain robust. We plan to return $4B to shareholders next quarter."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We are well capitalized. CCAR results are encouraging. We'll do some buybacks but remain flexible."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "The regulatory environment is shifting, but we remain well above minimums. The balance sheet is strong."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We remain well above our CET1 requirements. We'll continue to optimize capital for growth opportunities."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "Basel IV is manageable. We have the resources to deploy capital in growth areas, and still return capital to shareholders."
          </td>
        </tr>
        <!-- Row 5: Reg / Others -->
        <tr>
          <td style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center; background: #0072CE; color: #ffffff; font-weight: bold; padding: 8px;">
            Reg / Others
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We’re engaged with regulators on the new changes. It’s all about compliance and staying ahead of the curve."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We're continuing to navigate the evolving environment. So far, everything is well on track."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We don't see major changes needed. We'll adapt as final rules come in, but no big structural shifts expected."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "We’ve resolved a number of legacy issues. The environment is stable. We remain in compliance."
          </td>
          <td style="border: 1px solid #ccc; padding: 8px; vertical-align: top;">
            "The U.S. has to finalize Basel III. We are prepared for it. As long as it’s balanced, it should be manageable."
          </td>
        </tr>
      </tbody>
    </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)
