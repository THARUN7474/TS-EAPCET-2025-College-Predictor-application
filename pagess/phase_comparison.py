"""
Phase Comparison page for the TS EAMCET College Predictor application.
"""
import streamlit as st
from modules.constants import BRANCH_MAP
from modules.college_predictor import compare_phases


def render():
    """Render the Phase Comparison page."""
    st.subheader("Compare Colleges Across Different Phases")
    st.markdown(
        "See how college cutoffs change across different phases of counseling.")

    # Create input form for comparison
    with st.form("comparison_form"):
        col1, col2 = st.columns(2)

        with col1:
            comp_rank = st.number_input(
                "Your EAMCET Rank", min_value=1, max_value=200000, step=1, key="comp_rank")
            comp_gender = st.selectbox(
                "Gender", ["Male", "Female"], key="comp_gender")

        with col2:
            comp_caste = st.selectbox("Caste", [
                "OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC", "ST", "EWS"], key="comp_caste")
            comp_branch = st.selectbox("Branch", list(
                BRANCH_MAP.keys()), key="comp_branch")

        compare_button = st.form_submit_button(
            "Compare Phases", type="primary")

    if compare_button:
        if comp_rank < 1:
            st.error("Please enter a valid rank!")
        else:
            with st.spinner("Comparing across phases..."):
                phase_comparison = compare_phases(
                    comp_rank, comp_gender, comp_caste, comp_branch)

            if not phase_comparison:
                st.warning(
                    "No data available for comparison. Try adjusting your criteria.")
            else:
                st.success("Phase Comparison Complete!")

                for phase, data in phase_comparison.items():
                    st.subheader(f"{phase} Top Colleges")
                    st.dataframe(data, hide_index=True,
                                 use_container_width=True)

                # Explanation of comparison results
                st.info("""
                **What does this comparison tell you?**
                
                - **1st Phase**: These are the initial cutoffs, typically higher
                - **2nd Phase**: Often shows reduced cutoffs as seats start getting filled
                - **Final Phase**: Represents the final admission opportunity, usually with lowest cutoffs
                
                If you see your preferred college in later phases but not earlier ones, it means your chances improve in later rounds of counseling.
                """)
