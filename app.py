"""
Main entry point for the TS EAMCET 2025 College Predictor application.
"""
import streamlit as st
import logging
import pytz
from datetime import datetime
from modules.data_loader import load_data
from modules.constants import TOP_COLLEGES
from pagess import college_predictor, phase_comparison, branch_analysis, college_branches, college_search

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setting page configuration for better appearance
st.set_page_config(page_title="TS EAMCET 2025 College Predictor",
                   page_icon="🎓", layout="wide")


# def create_footer():
#     """Create a professional footer with social links and donation buttons"""

#     # Footer CSS
#     st.markdown("""
#     <style>
#         .footer-container {
#             background-color: #f8f9fa;
#             padding: 20px;
#             border-radius: 10px;
#             margin-top: 30px;
#             box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#         }

#         .footer-row {
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             padding: 10px 0;
#             border-bottom: 1px solid #e9ecef;
#         }

#         .footer-row:last-child {
#             border-bottom: none;
#         }

#         .timestamp {
#             color: #6c757d;
#             font-size: 14px;
#         }

#         .made-by {
#             font-weight: bold;
#             color: #495057;
#         }

#         .social-buttons {
#             display: flex;
#             gap: 15px;
#         }

#         .social-button {
#             display: inline-flex;
#             align-items: center;
#             background-color: #f1f3f5;
#             color: #495057;
#             padding: 8px 15px;
#             border-radius: 50px;
#             text-decoration: none;
#             transition: all 0.3s ease;
#             font-size: 14px;
#         }

#         .social-button:hover {
#             transform: translateY(-3px);
#             box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#         }

#         .github:hover {
#             background-color: #333;
#             color: white;
#         }

#         .linkedin:hover {
#             background-color: #0077b5;
#             color: white;
#         }

#         .twitter:hover {
#             background-color: #1da1f2;
#             color: white;
#         }

#         .social-icon {
#             margin-right: 8px;
#         }

#         .donation-container {
#             text-align: center;
#             padding: 15px;
#             background-color: #f8f9fa;
#             border-radius: 10px;
#         }

#         .donation-header {
#             font-weight: bold;
#             margin-bottom: 10px;
#             color: #343a40;
#         }

#         .donation-buttons {
#             display: flex;
#             justify-content: center;
#             gap: 10px;
#             margin: 15px 0;
#         }

#         .donation-button {
#             background-color: #6c757d;
#             color: white;
#             border: none;
#             padding: 8px 16px;
#             border-radius: 4px;
#             cursor: pointer;
#             transition: background-color 0.3s;
#         }

#         .donation-button:hover {
#             background-color: #495057;
#         }

#         .donation-primary {
#             background-color: #007bff;
#         }

#         .donation-primary:hover {
#             background-color: #0069d9;
#         }

#         .small-note {
#             font-size: 12px;
#             color: #6c757d;
#             font-style: italic;
#         }

#         .note-section {
#             font-size: 14px;
#             color: #6c757d;
#             margin-top: 20px;
#         }
#     </style>
#     """, unsafe_allow_html=True)

#     # Get current time in IST
#     ist = pytz.timezone('Asia/Kolkata')
#     current_time = datetime.now(ist).strftime("%I:%M %p IST on %A, %B %d, %Y")

#     # Footer HTML
#     st.markdown(f"""
#     <div class="footer-container">
#         <!-- Row 1: Time and Made By -->
#         <div class="footer-row">
#             <div class="timestamp">
#                 <strong>Last Updated</strong>: {current_time}
#             </div>
#             <div class="made-by">
#                 MADE WITH ❤️ BY BANDA THARUN
#             </div>
#         </div>

#         <!-- Row 2: Social Links -->
#         <div class="footer-row">
#             <div class="social-buttons">
#                 <a href="https://github.com/THARUN7474" target="_blank" class="social-button github">
#                     <span class="social-icon">
#                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
#                             <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
#                         </svg>
#                     </span>
#                     GitHub
#                 </a>
#                 <a href="https://www.linkedin.com/in/banda-tharun-47b489214" target="_blank" class="social-button linkedin">
#                     <span class="social-icon">
#                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
#                             <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
#                         </svg>
#                     </span>
#                     LinkedIn
#                 </a>
#                 <a href="https://x.com/BandaTharun7/" target="_blank" class="social-button twitter">
#                     <span class="social-icon">
#                         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
#                             <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865l8.875 11.633Z"/>
#                         </svg>
#                     </span>
#                     Twitter
#                 </a>
#             </div>
#         </div>

#         <!-- Row 3: Donation Section -->
#         <div class="footer-row">
#             <div class="donation-container">
#                 <div class="donation-header">Support This Project</div>
#                 <p>Your contribution helps maintain and improve this tool for everyone</p>

#                 <div class="donation-buttons">
#                     <a href="https://razorpay.me/@your-razorpay-id" target="_blank">
#                         <button class="donation-button">₹1</button>
#                     </a>
#                     <a href="https://razorpay.me/@your-razorpay-id" target="_blank">
#                         <button class="donation-button">₹4</button>
#                     </a>
#                     <a href="https://razorpay.me/@your-razorpay-id" target="_blank">
#                         <button class="donation-button">₹9</button>
#                     </a>
#                     <a href="https://razorpay.me/@your-razorpay-id" target="_blank">
#                         <button class="donation-button donation-primary">₹99</button>
#                     </a>
#                 </div>

#                 <div class="small-note">
#                     Your support helps maintain servers and enables further development of this free tool
#                 </div>
#             </div>
#         </div>
#     </div>

#     <!-- Note section below footer -->
#     <div class="note-section">
#         <strong>Note</strong>: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary
#         due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement.
#     </div>
#     """, unsafe_allow_html=True)

def create_footer():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime("%I:%M %p IST on %A, %B %d, %Y")

    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"**Last Updated:** {current_time}  \n"
        )
    with col2:
        st.markdown(
            "MADE BY   -"
            "[![GitHub](https://img.shields.io/badge/GitHub-THARUN7474-black?logo=github)](https://github.com/THARUN7474) "
            "- "
            "[![LinkedIn](https://img.shields.io/badge/LinkedIn-Banda%20Tharun-blue?logo=linkedin)](https://www.linkedin.com/in/banda-tharun-47b489214) "
            "- "
            "[![Twitter](https://img.shields.io/badge/Twitter-BandaTharun7-1da1f2?logo=twitter)](https://x.com/BandaTharun7/)"
        )
    st.info(
        "Support This Project: [Donate ₹1/  ₹4/  ₹7/  ₹99 or more via Razorpay](https://razorpay.me/@your-razorpay-id)"
    )
    st.caption(
        "**Note**: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement."
    )


def main():
    """Main function to run the Streamlit application."""
    logger.info("Starting TS EAMCET 2025 College Predictor application")

    st.title("🎓 TS EAMCET 2025 College Predictor")

    # Tabs for different functionalities
    tabs = st.tabs([
        "College Predictor",
        "Phase Comparison",
        "Branch Analysis",
        "College-wise Branches",
        "College Search by Branch",
        "Help"
    ])

    # College Predictor Tab
    with tabs[0]:
        college_predictor.render()

    # Phase Comparison Tab
    with tabs[1]:
        phase_comparison.render()

    # Branch Analysis Tab
    with tabs[2]:
        branch_analysis.render()

    # College-wise Branch Analysis Tab
    with tabs[3]:
        college_branches.render()

    # College Search by Branch Tab
    with tabs[4]:
        college_search.render()

    # Help Tab
    with tabs[5]:
        render_help_tab()

    # Adding footer
    # Add the footer at the end of your app
    create_footer()
    st.markdown("---")
    # st.markdown("""
    # **Note**: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary
    # due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement.
    # """)
    # st.markdown(f"**Last Updated**: 07:33 PM IST on Sunday, May 18, 2025")
    # st.markdown("MADE WITH ❤️ BY [BANDA THARUN]")
    # st.markdown("GitHub: [BANDA THARUN](https://github.com/THARUN7474 )")
    # st.markdown(
    #     "LinkedIn: [BANDA THARUN](https://www.linkedin.com/in/banda-tharun-47b489214 )")
    # st.markdown("Twitter: [BANDA THARUN](https://x.com/BandaTharun7/ )")
    # st.markdown(
    #     "**Support This Project**: [Donate ₹1 via Razorpay](https://razorpay.me/@your-razorpay-id)")


def render_help_tab():
    """Render the Help tab content."""
    st.subheader("Help & Information")
    st.markdown("""
    ### How to Use This Tool
    
    1. **College Predictor Tab**:
       - Enter your TS EAMCET rank, gender, caste, and preferred branch
       - Select which phase data you want to use (Final is recommended for accuracy)
       - Optionally filter by district to find colleges in specific areas
       - Click "Predict Colleges" to see your eligible options
    
    2. **Phase Comparison Tab**:
       - Compare how college cutoffs change across different counseling phases
       - This helps you understand if waiting for later rounds might improve your options
    
    3. **Branch Analysis Tab**:
       - Analyze which branches have higher or lower cutoff ranks
       - Useful for exploring alternative branches if your desired one is too competitive
       
    4. **College-wise Branches Tab**:
       - View all branches and their cutoffs for a specific college
       - Compare the difficulty level of different branches within the same institution
       - See the list of top 20 colleges based on market trends
    
    5. **College Search by Branch Tab**:
       - Enter your desired branch, caste, and gender to find colleges offering that branch
       - Use the 'N/A' option for caste to see closing ranks across all categories
       - View additional details like fees, place, and district for each college

    ### Understanding the Results
    
    - **Closing Rank**: The last rank that got admission in that college/branch in 2024
    - **Your eligibility**: If your rank is equal to or better (lower number) than the closing rank, you likely qualify
    
    ### Important Notes
    
    - This tool uses historical data from TS EAMCET 2024
    - Actual 2025 cutoffs may vary based on seat availability, number of applicants, etc.
    - Always verify information with official TS EAMCET counseling notifications
    - Special category seats (sports, PH, CAP, etc.) have different cutoffs not reflected here
    """)


if __name__ == "__main__":
    main()
