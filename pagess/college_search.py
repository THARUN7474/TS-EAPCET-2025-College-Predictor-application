"""
Branch cutoffs in all colleges page for the TS EAMCET College Predictor application.
"""
import streamlit as st
import pandas as pd
import numpy as np

from modules.data_loader import load_data
from modules.constants import get_caste_column_name


def render():
    """Render the College Search by Branch page."""
    st.subheader("College Search by Branch")
    st.markdown(
        "Find colleges offering your desired branch, along with closing ranks and other details.")

    # Form for user inputs
    df = load_data("Final Phase")
    if df is None:
        st.error("Unable to load data for college search.")
        return

    # Get unique branches from the dataset
    branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'
    branches = sorted(df[branch_col].str.strip().unique())

    selected_branch = st.selectbox(
        "Select Desired Branch", branches, key="college_search_branch")
    selected_caste = st.selectbox("Select Caste Category",
                                  ["N/A", "OC", "BC_A", "BC_B", "BC_C",
                                      "BC_D", "BC_E", "SC", "ST", "EWS"],
                                  key="college_search_caste")
    selected_gender = st.selectbox(
        "Select Gender", ["Male", "Female"], key="college_search_gender")

    if st.button("Search Colleges"):
        with st.spinner("Searching colleges..."):
            if df is not None:
                # Filter data by branch
                filtered_df = df[df[branch_col].str.strip() ==
                                 selected_branch].copy()

                if filtered_df.empty:
                    st.warning(
                        f"No colleges found offering {selected_branch}.")
                    return

                # Prepare display columns based on caste selection
                if selected_caste == "N/A":
                    # Show closing ranks for all categories
                    rank_columns = ['OC BOYS', 'OC GIRLS', 'BC_A BOYS', 'BC_A GIRLS', 'BC_B BOYS',
                                    'BC_B GIRLS', 'BC_C BOYS', 'BC_C GIRLS', 'BC_D BOYS', 'BC_D GIRLS',
                                    'BC_E BOYS', 'BC_E GIRLS', 'SC BOYS', 'SC GIRLS', 'ST BOYS',
                                    'ST GIRLS', 'EWS GEN OU', 'EWS GIRLS OU']
                    display_columns = ['Institute Name',
                                       'Place', 'Tuition Fee'] + rank_columns
                    result_df = filtered_df[display_columns].rename(columns={
                        'Institute Name': 'College Name',
                        'Place': 'Place',
                        'Tuition Fee': 'Tuition Fee (₹)'
                    })

                    # Convert rank columns to integer for display, using a consistent missing value representation
                    for col in rank_columns:
                        # First ensure all numbers are properly represented as numbers, not strings
                        result_df[col] = pd.to_numeric(
                            result_df[col], errors='coerce')
                        # Now convert to int or missing value placeholder
                        result_df[col] = result_df[col].apply(
                            lambda x: int(x) if pd.notnull(x) else "-"
                        )
                else:
                    # Show closing rank for the selected caste-gender combination
                    target_column = get_caste_column_name(
                        selected_gender, selected_caste)
                    if target_column not in df.columns:
                        st.error(
                            f"Data for {selected_caste} {selected_gender} not available in the dataset.")
                        return
                    display_columns = ['Institute Name',
                                       'Place', 'Tuition Fee', target_column]
                    result_df = filtered_df[display_columns].rename(columns={
                        'Institute Name': 'College Name',
                        'Place': 'Place',
                        'Tuition Fee': 'Tuition Fee (₹)',
                        target_column: 'Closing Rank'
                    })

                    # Ensure all numbers are properly represented as numbers
                    result_df['Closing Rank'] = pd.to_numeric(
                        result_df['Closing Rank'], errors='coerce')

                    # Make a copy of the column for sorting purposes
                    result_df['Rank_for_sorting'] = result_df['Closing Rank']

                    # Format closing rank as integer without decimals for display
                    result_df['Closing Rank'] = result_df['Closing Rank'].apply(
                        lambda x: int(x) if pd.notnull(x) else "-"
                    )

                    # Sort by the numeric column with NaN values at the end
                    result_df = result_df.sort_values(
                        'Rank_for_sorting', na_position='last')

                    # Remove the temporary sorting column
                    result_df = result_df.drop('Rank_for_sorting', axis=1)

                # Format Tuition Fee for display
                result_df['Tuition Fee (₹)'] = result_df['Tuition Fee (₹)'].apply(
                    lambda x: f"{int(x):,}" if pd.notnull(x) else "N/A"
                )

                # Add S.No column
                result_df.insert(0, 'S.No', range(1, len(result_df) + 1))

                # Rearrange columns in the desired order
                if selected_caste != "N/A":
                    result_df = result_df[[
                        'S.No', 'College Name', 'Place', 'Closing Rank', 'Tuition Fee (₹)']]

                # Display results
                st.subheader(f"Colleges Offering {selected_branch}")
                st.markdown(
                    f"Showing results for {selected_caste if selected_caste != 'N/A' else 'All Categories'} ({selected_gender})")

                # Style the table
                st.dataframe(
                    result_df,
                    use_container_width=True
                )

                # Insights
                if selected_caste != "N/A":
                    st.subheader("Key Insights")

                    # Get numeric columns from result_df for insights
                    ranks_df = filtered_df[display_columns].rename(columns={
                        target_column: 'Closing Rank'
                    })

                    # Convert to numeric for calculations
                    ranks_df['Closing Rank'] = pd.to_numeric(
                        ranks_df['Closing Rank'], errors='coerce')

                    # Filter out None values for insights
                    valid_ranks = ranks_df['Closing Rank'].dropna()

                    if not valid_ranks.empty:
                        lowest_rank = valid_ranks.min()
                        highest_rank = valid_ranks.max()

                        lowest_college = filtered_df.loc[ranks_df['Closing Rank']
                                                         == lowest_rank, 'Institute Name'].values[0]
                        highest_college = filtered_df.loc[ranks_df['Closing Rank']
                                                          == highest_rank, 'Institute Name'].values[0]

                        # Fix for comma-formatted strings in Tuition Fee
                        avg_fee = filtered_df['Tuition Fee'].mean()

                        st.markdown(f"""
                        - **Lowest Closing Rank**: {int(lowest_rank)} at {lowest_college}
                        - **Highest Closing Rank**: {int(highest_rank)} at {highest_college}
                        - **Average Tuition Fee**: ₹{avg_fee:,.0f}
                        
                        Use this information to shortlist colleges that match your rank.
                        """)
                    else:
                        st.warning(
                            "No valid closing rank data available for analysis.")
