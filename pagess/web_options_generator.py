"""
Web Options Generator page for the TS EAMCET College Predictor application.
Generates optimized college and branch combinations based on user's rank and preferences.
"""
import streamlit as st
import pandas as pd
import io
from modules.data_loader import load_data
from modules.constants import (
    BRANCH_MAP, TOP_COLLEGES, TOP_COLLEGES_CUTTOFF_MALES, TOP_COLLEGES_CUTTOFF_FEMALES,
    TOP_COLLEGES__MALES, TOP_COLLEGES__FEMALES, get_caste_column_name
)


def get_college_list_by_type(list_type, gender=None):
    """
    Get the appropriate college list based on user selection.

    Args:
        list_type (str): Type of college list to use
        gender (str): User's gender (for gender-specific lists)

    Returns:
        list: List of college dictionaries with rankings
    """
    if list_type == "Manual Ranking (Our Curated List)" and gender:
        if gender == "Male":
            return TOP_COLLEGES__MALES
        else:
            return TOP_COLLEGES__FEMALES
    elif list_type == "Cutoff-Based Ranking (Data-Driven)" and gender:
        if gender == "Male":
            return TOP_COLLEGES_CUTTOFF_MALES
        else:
            return TOP_COLLEGES_CUTTOFF_FEMALES
    elif list_type == "Gender-Specific Ranking" and gender:
        if gender == "Male":
            return TOP_COLLEGES__MALES
        else:
            return TOP_COLLEGES__FEMALES
    else:
        return TOP_COLLEGES  # Default fallback


def get_web_options(user_rank, gender, caste, preferred_branches, phase="Final Phase", buffer=1000, list_type="Manual Ranking (Our Curated List)"):
    """
    Generate web options based on user's rank and preferred branches.

    Args:
        user_rank (int): User's TS EAMCET rank
        gender (str): User's gender (Male/Female)
        caste (str): User's caste category
        preferred_branches (list): List of preferred branch codes in order of priority
        phase (str): Which phase data to use
        buffer (int): Buffer to add to cutoff ranks for safety

    Returns:
        list: List of dictionaries containing college and branch recommendations
    """
    df = load_data(phase)
    if df is None:
        return []

    # Detect column names
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'

    branch_col = 'Branch Code' if 'Branch Code' in df.columns else 'Branch'

    # Get the appropriate caste column
    caste_column = get_caste_column_name(gender, caste)

    # Get the selected college list
    selected_colleges = get_college_list_by_type(list_type, gender)

    web_options = []
    priority = 1

    # For each preferred branch (in order of priority)
    for branch_code in preferred_branches:
        branch_found_in_any_college = False

        # Check each top college for this branch
        for college_info in selected_colleges:
            college_name = college_info["name"]

            # Find matching rows in dataset
            # college_matches = df[df[college_col].str.contains(
            #     college_name.split()[0], case=False, na=False)]
            college_matches = df[df[college_col].str.lower() ==
                                 college_name.lower()]

            if not college_matches.empty:
                # Look for the specific branch in this college
                branch_matches = college_matches[
                    college_matches[branch_col].str.contains(
                        branch_code, case=False, na=False)
                ]

                for _, row in branch_matches.iterrows():
                    if caste_column in row and pd.notna(row[caste_column]):
                        cutoff_rank = row[caste_column]
                        buffer_rank = cutoff_rank + buffer

                        if user_rank <= buffer_rank:
                            web_options.append({
                                'Priority': priority,
                                'College': row[college_col],
                                'Branch Code': branch_code,
                                'Branch Name': BRANCH_MAP.get(branch_code, branch_code),
                                'Last Year Cutoff': int(cutoff_rank),
                                'Your Rank': user_rank,
                                'Safety Buffer': buffer,
                                'Buffered Cutoff': int(buffer_rank),
                                'Chance': 'Good' if user_rank <= cutoff_rank else 'Fair',
                                'Tuition Fee': row.get('Tuition Fee', 'N/A'),
                                'District': row.get('Dist Code', 'N/A'),
                            })
                            branch_found_in_any_college = True
                            priority += 1

        # If branch not found in top colleges, search in all colleges
        if not branch_found_in_any_college:
            all_branch_matches = df[df[branch_col].str.contains(
                branch_code, case=False, na=False)]

            for _, row in all_branch_matches.iterrows():
                if caste_column in row and pd.notna(row[caste_column]):
                    cutoff_rank = row[caste_column]
                    buffer_rank = cutoff_rank + buffer

                    if user_rank <= buffer_rank:
                        web_options.append({
                            'Priority': priority,
                            'College': row[college_col],
                            'Branch Code': branch_code,
                            'Branch Name': BRANCH_MAP.get(branch_code, branch_code),
                            'Last Year Cutoff': int(cutoff_rank),
                            'Your Rank': user_rank,
                            'Safety Buffer': buffer,
                            'Buffered Cutoff': int(buffer_rank),
                            'Chance': 'Good' if user_rank <= cutoff_rank else 'Fair',
                            'Tuition Fee': row.get('Tuition Fee', 'N/A'),
                            'District': row.get('Dist Code', 'N/A'),
                        })
                        priority += 1

                        # Limit results to prevent too many options
                        if len(web_options) >= 50:
                            break

            if len(web_options) >= 50:
                break

    return web_options


def render():
    """Render the Web Options Generator page."""
    st.subheader("🎯 Web Options Branch-specific Generator")
    st.markdown("""
    Generate optimized college and branch combinations based on your rank and preferences. - Prioritizing your preferred branches in order
    """)

    # Input form
    with st.form("web_options_form"):
        col1, col2 = st.columns(2)

        with col1:
            user_rank = st.number_input(
                "Enter your TS EAMCET Rank",
                min_value=1,
                max_value=200000,
                value=1,
                help="Your TS EAMCET 2025 rank"
            )

            gender = st.selectbox(
                "Select Gender",
                ["Male", "Female"],
                help="Your gender for category-specific cutoffs"
            )

            # College list type selection
            st.markdown("#### 🏆 Choose Your Top 20 College Ranking Method")
            list_type = st.radio(
                "Select ranking method:",
                [
                    "Manual Ranking (Our Curated List)",
                    "Cutoff-Based Ranking (Data-Driven)",
                    # "Gender-Specific Ranking"
                ],
                help="""
                - **Manual Ranking**: OUR Hand-picked based on reputation, placements, faculty
                - **Cutoff-Based**: Ranked by most competitive cutoffs (toughest to get in first)  
                - **Gender-Specific**: Considers gender-specific admission patterns and success rates
                """
            )

        with col2:
            phase = st.selectbox(
                "Select Phase Data",
                ["Final Phase", "2nd Phase", "1st Phase"],
                help="Final Phase is recommended for most accurate cutoffs"
            )

            caste = st.selectbox(
                "Select Category",
                ["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC", "ST", "EWS"],
                help="Your caste category"
            )

            buffer = st.slider(
                "Safety Buffer (ranks)",
                min_value=0,
                max_value=5000,
                value=1000,
                step=500,
                help="Additional ranks added to cutoff for safety margin"
            )

            st.markdown(""" Find Our Top 20 Colleges for TS EAMCET 2025 list in help tab of this app.
            """)

        # Branch selection
        st.markdown(
            "### 🎓 Select Your Preferred Branches (Select branches in your order of priority)")
        st.markdown("""
        The options will be arranged based on your priority order and your priority list of branches will be displayed below after you click the **Generate Web Options** button.
        """)

        available_branches = list(BRANCH_MAP.keys())

        popular_branches = [
            'CSE',  # COMPUTER SCIENCE AND ENGINEERING
            # COMPUTER SCIENCE AND ENGINEERING (ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)
            'CSM',
            'CSD',  # COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)
            'INF',  # INFORMATION TECHNOLOGY
            'AID',  # ARTIFICIAL INTELLIGENCE AND DATA SCIENCE
            'CSO',  # COMPUTER SCIENCE AND ENGINEERING (IOT)
            'CSC',  # COMPUTER SCIENCE AND ENGINEERING (CYBER SECURITY)
            'CSB',  # COMPUTER SCIENCE AND BUSINESS SYSTEM
            'CSW',  # COMPUTER ENGINEERING (SOFTWARE ENGINEERING)
            # CSE (IOT AND CYBER SECURITY INCLUDING BLOCK CHAIN TECHNOLOGY)
            'CIC',
            'CSA',  # COMPUTER SCIENCE AND ENGG (ARTIFICIAL INTELLIGENCE)
            'CSI',  # COMPUTER SCIENCE AND INFORMATION TECHNOLOGY
            'CSDN',  # COMPUTER SCIENCE & DESIGN
            'CSN',  # COMPUTER SCIENCE AND ENGINEERING (NETWORKS)
            'CE',   # COMPUTER ENGINEERING
            'AI',   # ARTIFICIAL INTELLIGENCE
            'AIM',  # ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING
            'ECE',  # ELECTRONICS AND COMMUNICATION ENGINEERING
            'EEE',   # ELECTRICAL AND ELECTRONICS ENGINEERING
            'MEC',  # MECHANICAL ENGINEERING
        ]

        other_branches = [
            b for b in available_branches if b not in popular_branches]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Popular Branches:**")
            selected_popular = []
            for branch in popular_branches:
                if st.checkbox(f"{branch} - {BRANCH_MAP[branch]}", key=f"pop_{branch}"):
                    selected_popular.append(branch)

        with col2:
            st.markdown("**Other Branches:**")
            selected_other = []
            for branch in other_branches:
                if st.checkbox(f"{branch} - {BRANCH_MAP[branch]}", key=f"other_{branch}"):
                    selected_other.append(branch)

        # Combine selections
        all_selected = selected_popular + selected_other

        if all_selected:
            st.markdown("**📋 Your Priority Order:**")
            for i, branch in enumerate(all_selected, 1):
                st.write(f"{i}. **{branch}** - {BRANCH_MAP[branch]}")

        generate_button = st.form_submit_button(
            "🚀 Generate Web Options", type="primary")

    # Generate results
    if generate_button:
        if not all_selected:
            st.error("⚠️ Please select at least one preferred branch!")
            return

        if user_rank <= 0:
            st.error("⚠️ Please enter a valid rank!")
            return

        with st.spinner("🔍 Analyzing colleges and generating your personalized web options..."):
            web_options = get_web_options(
                user_rank=user_rank,
                gender=gender,
                caste=caste,
                preferred_branches=all_selected,
                phase=phase,
                buffer=buffer,
                list_type=list_type
            )

        if not web_options:
            st.warning(
                "❌ No suitable options found with your current criteria. Try increasing the safety buffer or selecting more branches.")

            # Suggestions
            st.markdown("### 💡 Suggestions:")
            st.markdown("""
            - Increase the safety buffer to 2000-3000 ranks
            - Select additional branches as backup options
            - Consider looking at 2nd Phase data which might have higher cutoffs
            - Check if your rank and category combination is correct
            """)
        else:
            # Display results
            st.success(f"✅ Found {len(web_options)} recommended web options!")

            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                good_chances = len(
                    [opt for opt in web_options if opt['Chance'] == 'Good'])
                st.metric("🎯 Good Chances", good_chances)

            with col2:
                fair_chances = len(
                    [opt for opt in web_options if opt['Chance'] == 'Fair'])
                st.metric("⚡ Fair Chances", fair_chances)

            with col3:
                unique_colleges = len(
                    set([opt['College'] for opt in web_options]))
                st.metric("🏛️ Unique Colleges", unique_colleges)

            with col4:
                top_college_options = len([opt for opt in web_options if any(
                    top['name'] in opt['College'] for top in TOP_COLLEGES)])
                st.metric("⭐ Top 20 Colleges Possible options",
                          top_college_options)

            # Results table
            st.markdown("### 📊 Your Personalized Web Options")

            # Convert to DataFrame for better display
            df_results = pd.DataFrame(web_options)

            # Style the dataframe
            st.dataframe(
                df_results,
                column_config={
                    "Priority": st.column_config.NumberColumn("Priority", width="small"),
                    "College": st.column_config.TextColumn("College Name", width="large"),
                    "Branch Code": st.column_config.TextColumn("Branch", width="small"),
                    "Branch Name": st.column_config.TextColumn("Branch Name", width="large"),
                    "Last Year Cutoff": st.column_config.NumberColumn("Last Year Cutoff", format="%d"),
                    "Your Rank": st.column_config.NumberColumn("Your Rank", format="%d"),
                    "Buffered Cutoff": st.column_config.NumberColumn("Safe Cutoff", format="%d"),
                    "Chance": st.column_config.TextColumn("Admission Chance", width="small"),
                    "Tuition Fee": st.column_config.TextColumn("Fee", width="medium"),
                    "District": st.column_config.TextColumn("District", width="medium")
                },
                hide_index=True,
                use_container_width=True
            )

            # Download option
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Web Options as CSV",
                data=csv,
                file_name=f"TS_EAMCET_2025_WebOptions_Rank_{user_rank}.csv",
                mime="text/csv"
            )

            excel_buffer = io.BytesIO()
            df_results.to_excel(excel_buffer, index=False)
            st.download_button(
                label="Download Results as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"TS_EAMCET_2025_WebOptions_Rank_{list_type.replace(' ', '_')}_{caste}_{gender}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Key insights
            # st.markdown("### 🔍 Key Insights")

            # Priority branch analysis
            priority_branches = df_results.groupby(
                'Branch Code').size().sort_values(ascending=False)

            # col1, col2 = st.columns(2)

            # with col1:
            st.markdown("**🎯 Branch-wise Opportunities:**")
            for branch, count in priority_branches.head(5).items():
                st.write(f"• **{branch}**: {count} colleges")

            # with col2:
            #     st.markdown("**⭐ Top College Matches:**")
            #     top_matches = [opt for opt in web_options[:5]]
            #     for opt in top_matches:
            #         st.write(f"• {opt['College']} - {opt['Branch Code']}")

            # Important notes
            st.markdown("### 📝 Important Notes")
            st.info(f"""
            **🎯 Pro Tips for Web Option Filling:**
            
            1. **Follow the Priority Order**: The options are arranged by your branch preferences
            2. **Mix Good & Fair Chances**: Include both safe and stretch options
            3. **Don't Skip Top Colleges**: Always include top colleges even if chances seem low
            4. **Geographic Preference**: Consider location and travel convenience
            5. **Fee Structure**: Check fee affordability for your selected options
            
            **⚠️ Remember**: This analysis is based on {phase} 2024 data. Actual 2025 cutoffs may vary.
            """)

            st.warning("""
            **🚨 Disclaimer**: 
            - This tool uses previous year's data with safety buffers
            - Actual admission depends on various factors including seat matrix changes
            - Always verify with official TS EAMCET counseling guidelines
            - Consider this as a reference tool, not a guarantee of admission
            """)


# Additional helper function for branch statistics
def get_branch_statistics(branch_code, phase="Final Phase"):
    """Get statistics for a specific branch across all colleges."""
    df = load_data(phase)
    if df is None:
        return None

    branch_col = 'Branch Code' if 'Branch Code' in df.columns else 'Branch'
    branch_data = df[df[branch_col].str.contains(
        branch_code, case=False, na=False)]

    if branch_data.empty:
        return None

    # Calculate statistics for different categories
    stats = {
        'total_colleges': len(branch_data),
        'avg_cutoff_oc_boys': branch_data['OC BOYS'].mean() if 'OC BOYS' in branch_data.columns else None,
        'min_cutoff_oc_boys': branch_data['OC BOYS'].min() if 'OC BOYS' in branch_data.columns else None,
        'max_cutoff_oc_boys': branch_data['OC BOYS'].max() if 'OC BOYS' in branch_data.columns else None,
    }

    return stats
