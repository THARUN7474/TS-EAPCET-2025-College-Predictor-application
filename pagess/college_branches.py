"""
College-wise Branch Analysis page for the TS EAMCET College Predictor application.
"""
import streamlit as st
import plotly.express as px

from modules.data_loader import load_data
from modules.college_predictor import get_college_branches
from modules.visualizations import create_branch_cutoff_chart, create_branch_comparison_plot
from modules.constants import TOP_COLLEGES


def render():
    """Render the College-wise Branch Analysis page."""
    st.subheader("College-wise Branch Analysis")
    st.markdown(
        "View all available branches and their cutoffs for a specific college.")

    # College selection form
    with st.form("college_branch_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Get college options from data
            df = load_data("Final Phase")
            college_options = []
            if df is not None:
                # Detect college name column
                college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
                if college_col not in df.columns:
                    college_col = 'Place'
                college_options = sorted(df[college_col].unique().tolist())

            selected_college = st.selectbox(
                "Select College", college_options, key="selected_college")
            selected_phase = st.selectbox("Select Phase Data",
                                          ["Final Phase", "2nd Phase", "1st Phase"],
                                          key="college_phase")

        with col2:
            college_gender = st.selectbox("Select Gender",
                                          ["Male", "Female"],
                                          key="college_gender")
            college_caste = st.selectbox("Select Caste",
                                         ["OC", "BC_A", "BC_B", "BC_C",
                                          "BC_D", "BC_E", "SC", "ST", "EWS"],
                                         key="college_caste")

        view_button = st.form_submit_button("View Branch Cutoffs")

    if view_button and selected_college:
        with st.spinner("Fetching branch data..."):
            branch_data = get_college_branches(
                selected_college, selected_phase, college_gender, college_caste)

            if branch_data is None or branch_data.empty:
                st.warning(
                    f"No data available for {selected_college} in the {selected_phase} for {college_caste} {college_gender}.")
            else:
                st.success(
                    f"Found {len(branch_data)} branches at {selected_college}")

                # Show branch data in a table
                st.dataframe(
                    branch_data,
                    column_config={
                        "Branch": st.column_config.TextColumn(width="large"),
                        "Branch Code": st.column_config.TextColumn(width="small"),
                        "Tuition Fee (₹)": st.column_config.NumberColumn(format="₹%d"),
                        "Closing Rank": st.column_config.NumberColumn(format="%d")
                    },
                    hide_index=True,
                    use_container_width=True
                )

                # # Create a bar chart of branch cutoffs
                # if 'Closing Rank' in branch_data.columns and 'Branch' in branch_data.columns:
                #     create_branch_cutoff_chart(branch_data)

                #     # Optional: Add Plotly visualization for better UI
                #     # Uncomment this for the enhanced UI version
                #     """
                #     fig = create_branch_comparison_plot(branch_data)
                #     if fig:
                #         st.plotly_chart(fig, use_container_width=True)
                #     """

                #     # Insights
                #     st.subheader("Key Insights")
                #     min_rank = branch_data['Closing Rank'].min()
                #     max_rank = branch_data['Closing Rank'].max()
                #     hardest_branch = branch_data.loc[branch_data['Closing Rank'].idxmin(
                #     )]['Branch']
                #     easiest_branch = branch_data.loc[branch_data['Closing Rank'].idxmax(
                #     )]['Branch']

                #     st.markdown(f"""
                #     - **Most Competitive Branch**: {hardest_branch} (rank: {min_rank:,.0f})
                #     - **Least Competitive Branch**: {easiest_branch} (rank: {max_rank:,.0f})
                #     - **Rank Range**: {max_rank - min_rank:,.0f} ranks difference between highest and lowest cutoffs
                    
                #     These insights help you choose the most suitable branch based on your rank.
                #     """)

                if 'Closing Rank' in branch_data.columns and 'Branch' in branch_data.columns:
                    st.subheader("Branch Cutoff Comparison")
                    chart_data = branch_data.set_index('Branch')['Closing Rank']
                    st.bar_chart(chart_data)

                    st.subheader("Key Insights")
                    # Remove rows with NaN in 'Closing Rank'
                    valid_data = branch_data.dropna(subset=['Closing Rank'])

                    if not valid_data.empty:
                        min_rank = valid_data['Closing Rank'].min()
                        max_rank = valid_data['Closing Rank'].max()
                        hardest_branch = valid_data.loc[valid_data['Closing Rank'].idxmin()]['Branch']
                        easiest_branch = valid_data.loc[valid_data['Closing Rank'].idxmax()]['Branch']

                        st.markdown(f"""
                        - **Most Competitive Branch**: {hardest_branch} (rank: {min_rank:,.0f})
                        - **Least Competitive Branch**: {easiest_branch} (rank: {max_rank:,.0f})
                        - **Rank Range**: {max_rank - min_rank:,.0f} ranks difference between highest and lowest cutoffs

                        These insights help you choose the most suitable branch based on your rank.
                        """)
                    else:
                        st.warning("No valid closing rank data available for insights.")

                # ...existing code...

                    # Top Colleges Section
                st.markdown("---")
                st.subheader(
                    "Top 20 Engineering Colleges in Telangana (Based on Market Trends)")

                for i, college in enumerate(TOP_COLLEGES):
                    with st.expander(f"{i+1}. {college['name']}"):
                        st.write(college['details'])

                st.info("""
                **Note about this list**: 
                
                This ranking is based on general market trends, placement records, and academic reputation. 
                The actual ranking may vary based on specific branches, infrastructure, and other factors.
                """)
