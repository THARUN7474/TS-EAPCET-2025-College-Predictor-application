"""
Enhanced College-Specific Options Generator for the TS EAMCET College Predictor application.
Focuses on getting admission to any branch in Top 20 colleges with multiple ranking options.
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


def get_college_specific_options(gender, caste, phase="Final Phase", list_type="Manual Ranking (Our Curated List)"):
    """
    Get all branches available in Top 20 colleges for the specified category and gender.

    Args:
        gender (str): User's gender (Male/Female)
        caste (str): User's caste category
        phase (str): Which phase data to use
        list_type (str): Type of Top 20 list to use

    Returns:
        tuple: (list of top 20 options, list of remaining options)
    """
    df = load_data(phase)
    if df is None:
        return [], []

    # Detect column names
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'

    branch_col = 'Branch Code' if 'Branch Code' in df.columns else 'Branch'

    # Get the appropriate caste column
    caste_column = get_caste_column_name(gender, caste)

    # Get the selected college list
    selected_colleges = get_college_list_by_type(list_type, gender)

    top_20_options = []
    remaining_options = []
    processed_college_names = set()

    # Process Top 20 colleges first
    for i, college_info in enumerate(selected_colleges, 1):
        # print(f"Processing Top College {i}: {college_info['name']}")
        college_name = college_info["name"]
        processed_college_names.add(college_name.lower())

        # print(
        # f" Searching for college {college_name.lower().split()[0]} in dataset")

        # Find matching rows in dataset
        # college_matches = df[df[college_col].str.contains(
        #     college_name.split()[0], case=False, na=False)]
        college_matches = df[df[college_col].str.lower() ==
                             college_name.lower()]

        if not college_matches.empty:
            # Get all branches for this college
            for _, row in college_matches.iterrows():
                branch_code = row[branch_col] if branch_col in row else 'N/A'

                # Get cutoff for the specified category
                cutoff_rank = None
                if caste_column in row and pd.notna(row[caste_column]):
                    cutoff_rank = int(row[caste_column])

                top_20_options.append({
                    'College Rank': i,
                    'College': row[college_col],
                    'Branch Code': branch_code,
                    'Branch Name': BRANCH_MAP.get(branch_code, branch_code),
                    'Closing Rank': cutoff_rank if cutoff_rank else float('inf'),
                    'Tuition Fee': row.get('Tuition Fee', 'N/A'),
                    'District': row.get('Dist Code', 'N/A'),
                    'Category': f"{caste} {gender}",
                    'List Type': 'Top 20'
                })

    # Process remaining colleges (not in Top 20) - ordered by cutoff rank
    remaining_colleges_data = []

    for _, row in df.iterrows():
        college_name = row[college_col]
        # Skip if already processed in Top 20
        if any(processed_name in college_name.lower() for processed_name in processed_college_names):
            continue

        branch_code = row[branch_col] if branch_col in row else 'N/A'

        # Get cutoff for the specified category
        cutoff_rank = None
        if caste_column in row and pd.notna(row[caste_column]):
            cutoff_rank = int(row[caste_column])

        remaining_colleges_data.append({
            'College Rank': 999,  # Will be updated after sorting
            'College': college_name,
            'Branch Code': branch_code,
            'Branch Name': BRANCH_MAP.get(branch_code, branch_code),
            'Closing Rank': cutoff_rank if cutoff_rank else float('inf'),
            'Tuition Fee': row.get('Tuition Fee', 'N/A'),
            'District': row.get('Dist Code', 'N/A'),
            'Category': f"{caste} {gender}",
            'List Type': 'Other Colleges'
        })

    # Sort remaining colleges by cutoff rank (ascending - better ranks first)
    remaining_colleges_data.sort(key=lambda x: x['Closing Rank'] if isinstance(
        x['Closing Rank'], int) else float('inf'))

    # Update college ranks for remaining colleges
    for i, college_data in enumerate(remaining_colleges_data, 21):
        college_data['College Rank'] = i
        remaining_options.append(college_data)

    # Sort Top 20 options by college rank first, then by cutoff
    top_20_options.sort(key=lambda x: (x['College Rank'], x['Closing Rank'] if isinstance(
        x['Closing Rank'], int) else float('inf')))

    return top_20_options, remaining_options


def render():
    """Render the Enhanced College-Specific Options Generator page."""
    st.subheader("🎯 Web Options College-Specific Generator")
    st.markdown("""
    **Priority: College over Branch - Get into ANY branch of Top colleges!**
    """)

    # Input form
    with st.form("enhanced_college_specific_form"):
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox(
                "Select Gender",
                ["Male", "Female"],
                help="Your gender for category-specific cutoffs"
            )

        with col2:
            caste = st.selectbox(
                "Select Category",
                ["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC", "ST", "EWS"],
                help="Your caste category"
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
            - **Manual Ranking**: Hand-picked based on reputation, placements, faculty
            - **Cutoff-Based**: Ranked by most competitive cutoffs (toughest to get in first)  
            - **Gender-Specific**: Considers gender-specific admission patterns and success rates
            """
        )
        st.markdown("""You can Find Our Top 20 Colleges for TS EAMCET 2025 list in help tab of this app.
            """)

        phase = st.selectbox(
            "Select Phase Data",
            ["Final Phase", "2nd Phase", "1st Phase"],
            help="Final Phase recommended for accurate cutoffs"
        )

        # Show/Hide remaining colleges option
        show_all_colleges = st.checkbox(
            "📋 Show ALL colleges (beyond Top 20) ordered by cutoff rank",
            value=True,
            help="This will show remaining colleges in ascending order of cutoff ranks"
        )

        # Optional rank input for highlighting
        st.markdown(
            "####  Optional: Enter your rank for highlighting your chances")
        user_rank = st.number_input(
            "Your TS EAMCET Rank (Optional)",
            min_value=1,
            max_value=200000,
            value=1,
            help="If provided, we'll highlight branches where you have good chances"
        )

        generate_button = st.form_submit_button(
            "🚀 Generate College Options", type="primary")

    # Generate results
    if generate_button:
        with st.spinner("🔍 Fetching college options with selected ranking method..."):
            top_20_options, remaining_options = get_college_specific_options(
                gender=gender,
                caste=caste,
                phase=phase,
                list_type=list_type
            )

        if not top_20_options and not remaining_options:
            st.warning(
                "❌ No data found for the selected criteria. Please try different phase data.")
            return

        # Combine options for display
        all_options = top_20_options.copy()
        if show_all_colleges:
            all_options.extend(remaining_options)

        # Display results
        st.success(
            f"✅ Found {len(all_options)} total options ({len(top_20_options)} in Top 20 + {len(remaining_options)} others)!")

        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)

        # Calculate stats
        unique_colleges_top20 = len(
            set([opt['College'] for opt in top_20_options]))
        unique_colleges_total = len(
            set([opt['College'] for opt in all_options]))

        # Calculate chances if rank provided
        good_chances_top20 = 0
        good_chances_total = 0
        if user_rank > 0:
            for opt in top_20_options:
                if isinstance(opt['Closing Rank'], int) and user_rank <= opt['Closing Rank']:
                    good_chances_top20 += 1
            for opt in all_options:
                if isinstance(opt['Closing Rank'], int) and user_rank <= opt['Closing Rank']:
                    good_chances_total += 1

        with col1:
            st.metric("🏆 Top 20 Colleges", unique_colleges_top20)

        with col2:
            st.metric("🏛️ Total Colleges", unique_colleges_total)

        with col3:
            if user_rank > 0:
                st.metric("🎯 Good Chances (Top 20)", good_chances_top20)
            else:
                st.metric("📊 Top 20 Options", len(top_20_options))

        with col4:
            if user_rank > 0:
                st.metric("🎯 Total Good Chances", good_chances_total)
            else:
                st.metric("📈 Total Options", len(all_options))

        # Display ranking method info
        st.markdown(f"### 📊 Using: **{list_type}**")

        ranking_info = {
            "Manual Ranking (Our Curated List)": "🎯 Hand-curated based on overall reputation, alumni success, and industry recognition",
            "Cutoff-Based Ranking (Data-Driven)": "📈 Ranked by historical cutoff competitiveness - most selective colleges first",
            "Gender-Specific Ranking": f"⚡ Optimized for {gender} candidates based on admission patterns and success rates"
        }

        st.info(ranking_info[list_type])

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(
            ["📋 All Options", "🏆 Top 20 Focus", "🏛️ College-wise View"])

        with tab1:
            # Convert to DataFrame
            df_results = pd.DataFrame(all_options)

            # Add chance indicator if rank provided
            if user_rank > 0:
                def get_chance_indicator(closing_rank):
                    if not isinstance(closing_rank, int):
                        return "❓ Unknown"
                    elif user_rank <= closing_rank:
                        return "🟢 Good"
                    elif user_rank <= closing_rank + 2000:
                        return "🟡 Fair"
                    else:
                        return "🔴 Tough"

                df_results['Admission Chance'] = df_results['Closing Rank'].apply(
                    get_chance_indicator)

            # Add visual separator for Top 20 vs Others
            df_results['Rank Category'] = df_results['List Type']

            # Display with custom formatting
            st.dataframe(
                df_results,
                column_config={
                    "College Rank": st.column_config.NumberColumn("Rank", width="small"),
                    "College": st.column_config.TextColumn("College Name", width="large"),
                    "Branch Code": st.column_config.TextColumn("Branch", width="small"),
                    "Branch Name": st.column_config.TextColumn("Branch Name", width="large"),
                    "Closing Rank": st.column_config.NumberColumn("Last Year Cutoff", format="%d"),
                    "Tuition Fee": st.column_config.TextColumn("TutionFee", width="medium"),
                    "District": st.column_config.TextColumn("District", width="medium"),
                    "Rank Category": st.column_config.TextColumn("Category", width="small"),
                    "Admission Chance": st.column_config.TextColumn("Your Chance", width="small") if user_rank > 0 else None
                },
                hide_index=True,
                use_container_width=True
            )

            # Download option
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete List as CSV",
                data=csv,
                file_name=f"TS_EAMCET_2025_Enhanced_College_Options_{list_type.replace(' ', '_')}_{caste}_{gender}.csv",
                mime="text/csv"
            )

            excel_buffer = io.BytesIO()
            df_results.to_excel(excel_buffer, index=False)
            st.download_button(
                label="Download Results as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"TS_EAMCET_2025_Enhanced_College_Options_{list_type.replace(' ', '_')}_{caste}_{gender}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with tab2:
            # Focus on Top 20 only
            st.markdown("#### 🏆 Top 20 Colleges (Selected Ranking Method)")

            if top_20_options:
                df_top20 = pd.DataFrame(top_20_options)

                if user_rank > 0:
                    def get_chance_indicator(closing_rank):
                        if not isinstance(closing_rank, int):
                            return "❓ Unknown"
                        elif user_rank <= closing_rank:
                            return "🟢 Good"
                        elif user_rank <= closing_rank + 2000:
                            return "🟡 Fair"
                        else:
                            return "🔴 Tough"

                    df_top20['Admission Chance'] = df_top20['Closing Rank'].apply(
                        get_chance_indicator)

                st.dataframe(
                    df_top20,
                    column_config={
                        "College Rank": st.column_config.NumberColumn("Rank", width="small"),
                        "College": st.column_config.TextColumn("College Name", width="large"),
                        "Branch Code": st.column_config.TextColumn("Branch", width="small"),
                        "Branch Name": st.column_config.TextColumn("Branch Name", width="large"),
                        "Closing Rank": st.column_config.NumberColumn("Last Cutoff", format="%d"),
                        "Tuition Fee": st.column_config.TextColumn("TutionFee", width="medium"),
                        "Admission Chance": st.column_config.TextColumn("Your Chance", width="small") if user_rank > 0 else None
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.warning(
                    "No Top 20 college options found for your criteria.")

            # # Download option
            csv = df_top20.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete List as CSV",
                data=csv,
                file_name=f"TS_EAMCET_2025_Top_20_Colleges_{list_type.replace(' ', '_')}_{caste}_{gender}.csv",
                mime="text/csv"
            )

            excel_buffer = io.BytesIO()
            df_top20.to_excel(excel_buffer, index=False)
            st.download_button(
                label="Download Results as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"TS_EAMCET_2025_Top_20_Colleges_{list_type.replace(' ', '_')}_{caste}_{gender}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with tab3:
            # College-wise grouped view
            st.markdown("#### 🏛️ College-wise Branch Distribution")

            # Group by college
            college_groups = {}
            for opt in all_options:
                college_name = opt['College']
                if college_name not in college_groups:
                    college_groups[college_name] = []
                college_groups[college_name].append(opt)

            # Sort colleges by rank
            sorted_colleges = sorted(college_groups.items(), key=lambda x: min(
                opt['College Rank'] for opt in x[1]))

            for college_name, branches in sorted_colleges:
                # Determine if this is a Top 20 college
                is_top20 = any(b['List Type'] == 'Top 20' for b in branches)
                college_rank = min(b['College Rank'] for b in branches)

                emoji = "🏆" if is_top20 else "🏛️"
                rank_display = f"#{college_rank}" if college_rank < 999 else "Other"

                with st.expander(f"{emoji} {rank_display} {college_name} ({len(branches)} branches)"):
                    # # Find college rating
                    # college_rating = branches[0]['College Rating'] if branches else "Engineering College"
                    # st.markdown(f"**About**: {college_rating}")

                    # Show chances if rank provided
                    if user_rank > 0:
                        st.markdown("**Your Chances:**")
                        good_count = sum(1 for b in branches if isinstance(
                            b['Closing Rank'], int) and user_rank <= b['Closing Rank'])
                        fair_count = sum(1 for b in branches if isinstance(
                            b['Closing Rank'], int) and user_rank <= b['Closing Rank'] + 2000 and user_rank > b['Closing Rank'])

                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("🟢 Good Chances", good_count)
                        with col_b:
                            st.metric("🟡 Fair Chances", fair_count)
                        with col_c:
                            st.metric("📊 Total Branches", len(branches))

                    # Create mini dataframe for this college (sorted by cutoff)
                    college_df = pd.DataFrame(sorted(branches, key=lambda x: x['Closing Rank'] if isinstance(
                        x['Closing Rank'], int) else float('inf')))

                    # Display branch table
                    st.dataframe(
                        college_df[['Branch Code', 'Branch Name',
                                    'Closing Rank', 'Tuition Fee']],
                        hide_index=True,
                        use_container_width=True
                    )

        # with tab4:
        #     # Analysis and insights
        #     st.markdown("#### 📊 Comprehensive Analysis")

        #     # Ranking comparison
        #     st.markdown("**🏆 Top 20 College Distribution by Ranking Method:**")

        #     ranking_comparison = pd.DataFrame({
        #         'Ranking Method': ['Manual Ranking', 'Cutoff-Based', 'Gender-Specific'],
        #         'Focus': [
        #             'Overall reputation & industry recognition',
        #             'Most competitive cutoffs & selectivity',
        #             f'{gender}-specific admission success patterns'
        #         ],
        #         'Best For': [
        #             'Brand value & long-term career growth',
        #             'Highly competitive students',
        #             f'{gender} candidates seeking optimized chances'
        #         ]
        #     })

        #     st.dataframe(ranking_comparison, hide_index=True,
        #                  use_container_width=True)

        #     # Branch popularity analysis
        #     st.markdown("**📈 Most Available Branches Across All Colleges:**")

        #     branch_counts = {}
        #     for opt in all_options:
        #         branch = opt['Branch Code']
        #         if branch not in branch_counts:
        #             branch_counts[branch] = {'count': 0, 'cutoffs': []}

        #         branch_counts[branch]['count'] += 1
        #         if isinstance(opt['Closing Rank'], int):
        #             branch_counts[branch]['cutoffs'].append(
        #                 opt['Closing Rank'])

        #     # Create branch analysis
        #     branch_analysis = []
        #     for branch, data in branch_counts.items():
        #         avg_cutoff = sum(
        #             data['cutoffs']) / len(data['cutoffs']) if data['cutoffs'] else None
        #         min_cutoff = min(data['cutoffs']) if data['cutoffs'] else None

        #         branch_analysis.append({
        #             'Branch Code': branch,
        #             'Branch Name': BRANCH_MAP.get(branch, branch),
        #             'Available Colleges': data['count'],
        #             'Best Cutoff': min_cutoff,
        #             'Average Cutoff': round(avg_cutoff) if avg_cutoff else None
        #         })

        #     # Sort by availability
        #     branch_analysis.sort(
        #         key=lambda x: x['Available Colleges'], reverse=True)

        #     st.dataframe(
        #         pd.DataFrame(branch_analysis[:15]),  # Show top 15
        #         column_config={
        #             "Branch Code": st.column_config.TextColumn("Branch", width="small"),
        #             "Branch Name": st.column_config.TextColumn("Branch Name", width="large"),
        #             "Available Colleges": st.column_config.NumberColumn("Colleges", width="small"),
        #             "Best Cutoff": st.column_config.NumberColumn("Best Rank", format="%d"),
        #             "Average Cutoff": st.column_config.NumberColumn("Avg Rank", format="%d")
        #         },
        #         hide_index=True,
        #         use_container_width=True
        #     )

        # Strategy recommendations
        st.markdown("### 💡 Enhanced Strategic Recommendations")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**🎯 For {list_type}:**")

            strategy_recommendations = {
                "Manual Ranking (Our Curated List)": [
                    "Focus on brand value and alumni network",
                    "These colleges have proven industry connections",
                    "Consider all branches - reputation matters most",
                    "Perfect for long-term career growth"
                ],
                "Cutoff-Based Ranking (Data-Driven)": [
                    "Most competitive colleges listed first",
                    "Higher chances in later-ranked colleges",
                    "Data-driven approach for realistic planning",
                    "Cutoff trends show actual selectivity"
                ],
                "Gender-Specific Ranking": [
                    f"Optimized specifically for {gender} candidates",
                    "Based on historical admission success rates",
                    "Considers gender-specific trends",
                    "Higher probability of admission success"
                ]
            }

            for point in strategy_recommendations[list_type]:
                st.markdown(f"- {point}")

        with col2:
            st.markdown("**⚡ Smart Application Strategy:**")
            st.markdown("""
            - **Top 5-7 options**: Stretch goals from Top 20
            - **Next 8-10 options**: Realistic targets from Top 20
            - **Remaining slots**: Safe options from other colleges
            - **Mix branches**: Don't stick to one branch only in top colleges
            - **Geographic spread**: Consider different districts
            """)

        if user_rank > 0:
            # Personalized recommendations
            st.markdown("### 🎯 Personalized Recommendations")

            # Calculate realistic chances
            realistic_top20 = len([opt for opt in top_20_options if isinstance(
                opt['Closing Rank'], int) and user_rank <= opt['Closing Rank'] + 3000])
            realistic_total = len([opt for opt in all_options if isinstance(
                opt['Closing Rank'], int) and user_rank <= opt['Closing Rank'] + 3000])

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🏆 Realistic Top 20 Options", realistic_top20)
                st.metric("📊 Total Realistic Options", realistic_total)

            with col2:
                if realistic_top20 > 0:
                    success_rate_top20 = (
                        realistic_top20 / len(top_20_options)) * 100 if top_20_options else 0
                    st.metric("🎯 Top 20 Success Rate",
                              f"{success_rate_top20:.1f}%")

                total_success_rate = (
                    realistic_total / len(all_options)) * 100 if all_options else 0
                st.metric("📈 Overall Success Rate",
                          f"{total_success_rate:.1f}%")

        # Important notes
        st.markdown("### 📝 Important Notes")
        st.info(f"""
        **🎯 Enhanced Strategy Benefits:**
        
        1. **Multiple Ranking Options**: Choose the ranking method that aligns with your priorities
        2. **Complete Coverage**: See both Top 20 and other colleges in cutoff order
        3. **Data-Driven Insights**: Make informed decisions based on historical trends
        4. **Personalized Chances**: Get realistic probability assessments
        5. **Strategic Flexibility**: Mix top choices with safe options
        
        **⚠️ Remember**: This analysis is based on {phase} 2024 data. Actual 2025 cutoffs may vary.
        """)

        st.warning(f"""
        **🚨 Key Strategy Points**: 
        - **Top 20 List**: Based on {list_type}
        - **No Rank Filtering**: All options shown regardless of your rank
        - **Ordering Logic**: Top 20 by selected ranking, then all others by cutoff rank (ascending)
        - **Apply Strategically**: Include stretch goals, realistic targets, and safe options
        - **Branch Flexibility**: Consider all branches in top colleges for maximum opportunities
        """)


def get_ranking_methods_info():
    """Get information about different ranking methods."""
    return {
        "Manual Ranking (Our Curated List)": {
            "description": "Hand-curated based on overall reputation, faculty quality, infrastructure, and industry connections",
            "best_for": "Students prioritizing brand value and long-term career prospects",
            "methodology": "Expert analysis of college reputation, alumni success, and industry recognition"
        },
        "Cutoff-Based Ranking (Data-Driven)": {
            "description": "Ranked by historical cutoff competitiveness - most selective colleges first",
            "best_for": "Students who want data-driven college selection based on actual admission difficulty",
            "methodology": "Analysis of previous year cutoff trends and admission competitiveness"
        },
        "Gender-Specific Ranking": {
            "description": "Optimized rankings considering gender-specific admission patterns and success rates",
            "best_for": "Students who want colleges optimized for their gender's historical success patterns",
            "methodology": "Statistical analysis of gender-specific admission data and success rates"
        }
    }
    # Information box
    st.info("""
    🎯 **New Feature**: Choose from different Top 20 college rankings!
    - **Manual Ranking**: Our curated list based on overall reputation
    - **Cutoff-Based**: Ranked by historical cutoff data (most competitive first)
    - **Gender-Specific**: Optimized rankings considering gender-specific trends
    """)
