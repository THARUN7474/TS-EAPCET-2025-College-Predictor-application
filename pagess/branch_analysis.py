"""
Branch Analysis page for the TS EAMCET College Predictor application.
"""
import streamlit as st
import pandas as pd

from modules.data_loader import load_data
from modules.constants import get_caste_column_name
from modules.visualizations import create_branch_analysis_chart

def render():
    """Render the Branch Analysis page."""
    st.subheader("Branch Analysis")
    st.markdown("Analyze cutoff trends across different engineering branches.")

    # Branch comparison form
    branch_caste = st.selectbox("Select Caste for Analysis",
                                ["OC", "BC_A", "BC_B", "BC_C", "BC_D",
                                    "BC_E", "SC", "ST", "EWS"],
                                key="branch_caste")
    branch_gender = st.selectbox("Select Gender for Analysis",
                                ["Male", "Female"],
                                key="branch_gender")

    if st.button("Analyze Branches"):
        with st.spinner("Analyzing branch cutoffs..."):
            # Get data for analysis
            df = load_data("Final Phase")
            if df is not None:
                # Get the target column name
                target_column = get_caste_column_name(branch_gender, branch_caste)

                # Check if column exists
                if target_column in df.columns:
                    # Group by branch and calculate median rank
                    branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'
                    branch_analysis = df.groupby(branch_col)[target_column].median().sort_values()

                    # Display results
                    st.subheader(f"Median Cutoff Ranks by Branch for {branch_caste} {branch_gender}")

                    # Create a bar chart of the branch analysis
                    create_branch_analysis_chart(branch_analysis)

                    # Insights
                    st.subheader("Key Insights")
                    easiest = branch_analysis.index[-1]
                    hardest = branch_analysis.index[0]
                    median_diff = branch_analysis.max() - branch_analysis.min()

                    st.markdown(f"""
                    - **Most Competitive Branch**: {hardest} (lowest median rank: {branch_analysis.min():,.0f})
                    - **Least Competitive Branch**: {easiest} (highest median rank: {branch_analysis.max():,.0f})
                    - **Rank Difference**: There's a {median_diff:,.0f} rank difference between the most and least competitive branches
                    
                    This analysis helps you understand which branches are more accessible with your rank.
                    """)
                else:
                    st.error(f"Data for {branch_caste} {branch_gender} not available in the dataset.")
            else:
                st.error("Unable to load data for analysis.")