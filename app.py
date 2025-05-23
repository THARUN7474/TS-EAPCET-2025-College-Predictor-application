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


col1, col2 = st.columns([2, 2])

with col1:

    st.info(
        "📚 **Find More Student Content:**\n"
        "[![LearnwithGoutham](https://img.shields.io/badge/LearnwithGoutham-darkred?logo=youtube)](https://www.youtube.com/@LearnwithGoutham) "
        "[![Goutham](https://img.shields.io/badge/Goutham-purple?logo=instagram)](https://instagram.com/gouthamsankeerth) "
        "[![Tharun](https://img.shields.io/badge/Tharun-darkorange?logo=youtube)](https://www.youtube.com/@banatharun_74)"
        "  "
        "  "
        "  "
        "  "
        "  "
        "  ""    🚀 "
    )

with col2:
    st.info(
        "💖 **Support This Project**\n"
        "To help keep the website running and free for everyone:\n"
        "  "
        "[Support via Razorpay](https://razorpay.me/@your-razorpay-id)"
    )


def create_footer():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime("%I:%M %p IST on %A, %B %d, %Y")

    st.markdown("---")
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown(
            """
            ### 👨‍💻 MADE BY

            **Tharun**  
            [![GitHub](https://img.shields.io/badge/GitHub-THARUN7474-black?logo=github)](https://github.com/THARUN7474)
            [![LinkedIn](https://img.shields.io/badge/LinkedIn-Banda%20Tharun-blue?logo=linkedin)](https://www.linkedin.com/in/banda-tharun-47b489214)
            [![Twitter](https://img.shields.io/badge/Twitter-BandaTharun7-1da1f2?logo=twitter)](https://x.com/BandaTharun7/)
            [![YouTube](https://img.shields.io/badge/YouTube-BandaTharun-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/@banatharun_74)
            """
        )

    with col2:
        st.markdown(
            """
            ### 🙎‍♂️ With Support

            **Goutham**  
            [![Instagram](https://img.shields.io/badge/Instagram-gouthamsankeerth-purple?logo=instagram)](https://instagram.com/gouthamsankeerth)
            [![YouTube](https://img.shields.io/badge/YouTube-LearnwithGoutham-red?logo=youtube)](https://www.youtube.com/@LearnwithGoutham)
            [![Telegram](https://img.shields.io/badge/Telegram-gouthamsankeerth-2CA5E0?logo=telegram)](https://t.me/careerguidance_gouthamsankeerth)
            """
        )
    # st.info(
    #     "Support This Project(for website maintenance): [Donate via Razorpay](https://razorpay.me/@your-razorpay-id)"
    # )
    st.markdown("#### ☕ Support Tharun Work ")
    st.markdown(
        """
        If you found this tool helpful, consider supporting me on [RazarPay](https://razorpay.me/@your-razorpay-id)!     Your support helps me keep building and maintaining tools like this ❤️
        """
    )

    # # Optional: Add BuyMeACoffee Button
    # st.markdown(
    #     """
    #     <a href="https://www.buymeacoffee.com/bandatharun74" target="_blank">
    #         <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me a Coffee" height="60">
    #     </a>
    #     """,
    #     unsafe_allow_html=True,
    # )

    st.markdown("---")
    st.caption(
        "**Note**: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement."
    )
    st.caption(
        f"**Last Updated:** {current_time}  \n"
    )


def main():
    """Main function to run the Streamlit application."""
    logger.info("Starting TS EAMCET 2025 College Predictor application")

    st.title("🎓 TS EAMCET 2025 College Predictor")

    # Tabs for different functionalities
    tabs = st.tabs([
        "College Predictor",
        "College-wise Branches",
        "College Search by Branch",
        "Phase Comparison",
        "Branch Analysis",
        "Help"
    ])

    # College Predictor Tab
    with tabs[0]:
        college_predictor.render()

    # Phase Comparison Tab
    with tabs[1]:
        college_branches.render()

    # Branch Analysis Tab
    with tabs[2]:
        college_search.render()

    # College-wise Branch Analysis Tab
    with tabs[3]:
        phase_comparison.render()

    # College Search by Branch Tab
    with tabs[4]:
        branch_analysis.render()

    # Help Tab
    with tabs[5]:
        render_help_tab()

    # Adding footer
    # Add the footer at the end of your app
    create_footer()
    st.markdown("---")


def render_help_tab():
    """Render the Help tab content."""
    st.markdown("""
    **Note**: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary
    due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement.
    """)
    st.subheader("Help & Information")
    st.markdown("""
    ### How to Use This Tool
    
    1. **College Predictor Tab**:
       - Enter your TS EAMCET rank, gender, caste, and preferred branch
       - Select which phase data you want to use (Final is recommended for accuracy)
       - Optionally filter by district to find colleges in specific areas
       - Click "Predict Colleges" to see your eligible options
                
    2 **College-wise Branches Tab**:
       - View all branches and their cutoffs for a specific college
       - Compare the difficulty level of different branches within the same institution
       - See the list of top 20 colleges based on market trends
    
    3. **College Search by Branch Tab**:
       - Enter your desired branch, caste, and gender to find colleges offering that branch
       - Use the 'N/A' option for caste to see closing ranks across all categories
       - View additional details like fees, place, and district for each college
    
    4. **Phase Comparison Tab**:
       - Compare how college cutoffs change across different counseling phases
       - This helps you understand if waiting for later rounds might improve your options
    
    5. **Branch Analysis Tab**:
       - Analyze which branches have higher or lower cutoff ranks
       - Useful for exploring alternative branches if your desired one is too competitive

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
