"""
Main entry point for the TS EAMCET 2025 College Predictor application.
"""
import streamlit as st
import logging
import pytz
from datetime import datetime
from modules.data_loader import load_data
from modules.constants import TOP_COLLEGES
from pagess import college_predictor, phase_comparison, branch_analysis, college_branches, college_search, web_options_generator, college_specific_generator, best_specific_generator
from modules.constants import TOP_COLLEGES, TOP_COLLEGES__MALES


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setting page configuration for better appearance
st.set_page_config(page_title="TS EAMCET 2025 College Predictor",
                   page_icon="🎓", layout="wide")


def create_footer():

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


def main():
    """Main function to run the Streamlit application."""
    logger.info("Starting TS EAMCET 2025 College Predictor application")

    st.title("🎓 TS EAMCET 2025 College Predictor")

    # Tabs for different functionalities
    tabs = st.tabs([
        "College Predictor",
        "Web Options branch_specific",  # New tab
        "Web Options college_specific",  # New tab
        "Web Options best_possible",  # New tab
        "College-wise Branches",
        "College Search by Branch",
        "Phase Comparison",
        # "Branch Analysis",
        "Help"
    ])

    # College Predictor Tab
    with tabs[0]:
        college_predictor.render()

    # Web Options Generator Tab (New)
    with tabs[1]:
        web_options_generator.render()

    # Web Options College Specific Generator Tab (New)
    with tabs[2]:
        college_specific_generator.render()

    # Web Options Best Possible Generator Tab (New)
    with tabs[3]:
        best_specific_generator.render()
        # st.subheader("Web Options Best Possible Generator")
        # st.markdown(
        #     "This feature is under development. Stay tuned for updates!"
        # )
        # # Placeholder for future implementation
        # st.info("Coming soon! This feature will help you find the best possible web options based on your preferences.")

    # College-wise Branches Tab
    with tabs[4]:
        college_branches.render()

    # College Search by Branch Tab
    with tabs[5]:
        college_search.render()

    # Phase Comparison Tab
    with tabs[6]:
        phase_comparison.render()

    # # Branch Analysis Tab
    # with tabs[7]:
    #     branch_analysis.render()

    # Help Tab
    with tabs[7]:
        render_help_tab()

    # Adding footer
    # Add the footer at the end of your app
    create_footer()

    st.markdown("#### ☕ Support Tharun Work ")
    st.markdown(
        """
        If you found this tool helpful, consider supporting me on [RazarPay](https://razorpay.me/@your-razorpay-id)!     Your support helps me keep building and maintaining tools like this ❤️
        """
    )
    st.markdown(
        "📚 **Find More Student Content:**\n"
        "[![LearnwithGoutham](https://img.shields.io/badge/LearnwithGoutham-darkred?logo=youtube)](https://www.youtube.com/@LearnwithGoutham) "
        "[![Goutham](https://img.shields.io/badge/Goutham-purple?logo=instagram)](https://instagram.com/gouthamsankeerth) "
        "[![Tharun](https://img.shields.io/badge/Tharun-darkorange?logo=youtube)](https://www.youtube.com/@banatharun_74)"
    )
    st.info(
        "💖 **Support This Project**\n"
        "To help keep the website running and free for everyone:\n"
        "  "
        "[Support via Razorpay](https://razorpay.me/@your-razorpay-id)"
        "Link will be updated soon! 😊"
    )
    st.success("""
    ✅ **Why Use This Tool?**
    - Save time by exploring the **most probable and optimal combinations**
    - Make informed decisions based on **rank-wise insights**
    - Avoid common mistakes in web option ordering
    - Use expert patterns to get closer to your dream seat
    """)

    st.warning("""
        ⚠️ **Disclaimer**  
        This is a **strategy reference tool**, not a guaranteed admission predictor.

        - We are **not responsible** for any admission, seat allocation, or counseling-related issues.
        - This tool is intended to serve as **guidance only**, not as a final decision-maker.
        - All recommendations are based on **available data** and **algorithms we have developed**.
        - Final allotments depend on official **counseling processes**, **cutoffs**, **seat availability**, and **your personal choices**.

        👉 Please use this tool as a **reference**, not as your final choice list.
        Always verify with official TS EAMCET counseling notifications and guidelines.""")

    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime("%I:%M %p IST on %A, %B %d, %Y")
    st.info(
        "Note: Due to changes in local and non-local quota policies for TS EAPCET 2025, cutoff ranks may increase significantly compared to previous years. For example, a 1000 rank in 2024 may correspond to a 1500–2000 rank in 2025. Please consider this while selecting your web options, as actual ranks may vary. ALL THE BEST! 😊"
    )
    st.caption(
        "**Note**: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement."
    )

    st.caption(
        f"**Last Updated:** {current_time}  \n"
    )

    st.markdown("""
    # ALL THE BEST FOR YOUR [**NEXTSTEP**](https://nextstep-student-hub.vercel.app/) OF YOUR JOURNEY!😊🎉
    """)


def render_help_tab():
    """Render the Help tab content for the TS EAMCET 2024 College Predictor and Web Options Tool."""

    st.markdown("""
    ### 📌 Disclaimer
    This tool is based on the **TS EAMCET 2024 cutoff ranks** published in the TGEAPCET 2024 Last Rank Statement. 
    Please note that actual admissions may vary due to:
    - Special category reservations (PH, CAP, NCC, Sports, etc.)
    - Management quotas and spot admissions
    - Student withdrawals and internal college policies
    """)

    st.subheader("🆘 Help & Information")
    st.info("""
    #### How to Use This Tool

    #### 1. **College Predictor Tab**
    - Enter your **TS EAMCET rank**, **gender**, **category (caste)**, and **preferred branch**.
    - Choose the counseling phase (✅ *Final phase is recommended for most accurate predictions*).
    - Filter by **district** (optional).
    - Click **"Predict Colleges"** to get a list of eligible colleges and branches.

    #### 2. **Web Options Branch Specific Generator Tab**
    - Input your **rank, gender, and category**.
    - Select your **preferred branches in priority order**.
    - Set a **safety buffer** (e.g., +300 ranks) to increase chances of admission.
    - Receive a **customized, strategic list** of college-branch combinations.
    - Download the result as a **CSV** for easy web options entry.

    #### 3. **Web Options - College Specific Generator Tab**
    - Enter your **rank**.
    - View **branches available in top 20 colleges** based on our focused data.
    - Download the list for reference during the web options process.

    #### 4. **Web Options - Best Possible Generator Tab** 
    - Get **personalized suggestions** for the best possible college-branch combinations.
    - Leverages your preferences and rank to optimize admission chances.

    #### 5. **College-wise Branches Tab**
    - Select any college to view **all its offered branches** and their **cutoff ranks**.
    - Easily compare difficulty levels of different departments within a single college.
    - View insights on the **top 20 colleges** based on trends and demand.

    #### 6. **College Search by Branch Tab**
    - Search for colleges offering your **preferred branch**.
    - Customize the search by **gender** and **caste** (or use ‘N/A’ to view all categories).
    - See additional data like **location, district, and tuition fees**.

    #### 7. **Phase Comparison Tab**
    - Track how cutoff ranks change across **different counseling phases**.
    - Helps in deciding whether to wait for later rounds or lock in early.

    #### 8. **Branch Analysis Tab**
    - Explore which branches have **higher or lower competition**.
    - Ideal for discovering **alternative branches** with better admission chances.

    ---

    ### 🧠 Understanding Your Results

    - **Closing Rank**: The last rank admitted for a specific branch in 2024.
    - **Eligibility**: If your rank is **equal to or better (lower)** than the closing rank, you have a good chance of admission.
    - **Web Options List**: Ordered based on your preferences, safety buffer, and strategic fit.

    ---

    ### 🧰 Web Options Generator – Key Features

    - ✅ **Priority-Based Output**: College-branch options arranged by your chosen branch order.
    - 🎯 **Safety Buffer**: Adds a margin to cutoff ranks for safer predictions.
    - 🏆 **Top College Focus**: Emphasizes top 20 reputed institutions for best outcomes.
    - 🧠 **Smart Filtering**: Balances ambitious choices with realistic chances.
    - 📥 **Download Option**: Export your personalized list for direct use in web counseling.

    ---

    ### ⚠️ Important Notes

    - This tool uses **TS EAMCET 2024** data for estimation purposes only.
    - **2025 cutoffs may vary** based on the number of applicants, category-wise competition, and seat availability.
    - Always verify with the **official TS EAMCET counseling notifications**.
    - Special category seats (e.g., Sports, PH, NCC, CAP) are **not included** in general cutoff ranks.
    - The **Web Options Generator** is a strategy assistant — always include some **top colleges**, even if your chances are slim, to maximize outcomes.

    """)

    st.markdown("---")
    st.subheader(
        "Top 20 Engineering Colleges in Telangana (Based on Our Expert Analysis)")

    for i, college in enumerate(TOP_COLLEGES__MALES):
        with st.expander(f"{i+1}. {college['name']}"):
            st.write(college['details'])

    st.info("""
    **Note about this list**: 
    
    This ranking is based on general market trends, placement records, and academic reputation. 
    The actual ranking may vary based on specific branches, infrastructure, and other factors.
    """)


if __name__ == "__main__":
    main()
