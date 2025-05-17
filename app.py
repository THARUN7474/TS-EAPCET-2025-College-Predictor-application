"""
Main entry point for the TS EAMCET 2025 College Predictor application.
"""
import streamlit as st
from modules.data_loader import load_data
from modules.constants import TOP_COLLEGES
from pagess import college_predictor, phase_comparison, branch_analysis, college_branches

# Setting page configuration for better appearance
st.set_page_config(page_title="TS EAMCET 2025 College Predictor",
                   page_icon="🎓", layout="wide")


def main():
    """Main function to run the Streamlit application."""
    st.title("🎓 TS EAMCET 2025 College Predictor")

    # Tabs for different functionalities
    tabs = st.tabs([
        "College Predictor",
        "Phase Comparison",
        "Branch Analysis",
        "College-wise Branches",
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

    # Help Tab
    with tabs[4]:
        render_help_tab()

    # Adding footer
    st.markdown("---")
    st.markdown("""
    **Note**: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary 
    due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement.
    """)


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
