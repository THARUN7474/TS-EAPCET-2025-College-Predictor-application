"""
Best Possible WebOptions Generator for TS EAMCET College Predictor application.
Generates optimized college and branch combinations following the strategic hierarchy:
🥇 Top 1–5 Colleges: CSE / CSE-aligned branches → ECE
🥈 Top 6–10 Colleges: CSE / CSE-aligned branches → ECE  
🥉 Top 11–15 Colleges: CSE / CSE-aligned branches → ECE
⚙️ Top 1–10 Colleges: Other branches (EEE, Mech, Civil, etc.)
🛠️ Top 16–20 Colleges: CSE / ECE / Other branches
🧩 Beyond Top 20 Colleges: Listed by ascending cutoff order
"""
import streamlit as st
import pandas as pd
import io
from modules.data_loader import load_data
from modules.constants import (
    BRANCH_MAP, TOP_COLLEGES, TOP_COLLEGES_CUTTOFF_MALES, TOP_COLLEGES_CUTTOFF_FEMALES,
    TOP_COLLEGES__MALES, TOP_COLLEGES__FEMALES, get_caste_column_name
)

# Define branch priorities and categories
CSE_BRANCHES = [
    'CSE', 'INF', 'AIM', 'CSM', 'CSD', 'CSA', 'AID', 'CSI', 'CSO', 'CSC', 'AI',
    'CSB', 'CSW', 'CIC', 'CSA', 'CSI', 'CSDN', 'CSN', 'CE'
]

CSE_ALIGNED_BRANCHES = [
    # Note: 'CDS', 'CST', 'DS', 'IOT', 'CS' are not in BRANCH_MAP — add only if you plan to support them
]

ECE_BRANCHES = [
    'ECE'
]

OTHER_CORE_BRANCHES = [
    'EEE', 'MEC', 'CIV', 'CHE', 'BIO', 'ANE', 'AUT', 'MIN',
    'MMT', 'MTM', 'MTR', 'GEO', 'AGR', 'FT', 'PHM', 'TXT', 'BT',  'ECM', 'EEC', 'ETM', 'ECI',
    'BPL', 'BSE', 'DRY', 'EIE'
]


def get_college_list_by_type(list_type, gender=None):
    """Get the appropriate college list based on user selection."""
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
    else:
        return TOP_COLLEGES


def get_hardcoded_best_list(list_type="Manual Ranking (Our Curated List)", gender="Male"):
    """
    Generate Type 1: Hardcoded Best List - Pre-generated optimal order
    This shows the ideal strategy without considering specific rank.
    """
    selected_colleges = get_college_list_by_type(list_type, gender)
    hardcoded_options = []
    priority = 1

    # Top 1-5 Colleges: CSE/CSE-aligned → ECE
    # st.write("🥇 **Top 1-5 Colleges Priority Order:**")
    for i in range(min(5, len(selected_colleges))):
        college = selected_colleges[i]

        # CSE branches first
        for branch in CSE_BRANCHES:  # Top CSE branches
            hardcoded_options.append({
                'Priority': priority,
                'College_Tier': f"Top {i+1}",
                'College': college["name"],
                'Branch_Code': branch,
                'Branch_Name': BRANCH_MAP.get(branch, branch),
                'Strategy': 'Prime CSE in Top 5',
                'Note': 'Highest Priority - Best College + Best Branch'
            })
            priority += 1

    for i in range(min(5, len(selected_colleges))):
        college = selected_colleges[i]
        # ECE branches
        for branch in ECE_BRANCHES[:1]:  # Only ECE
            hardcoded_options.append({
                'Priority': priority,
                'College_Tier': f"Top {i+1}",
                'College': college["name"],
                'Branch_Code': branch,
                'Branch_Name': BRANCH_MAP.get(branch, branch),
                'Strategy': 'ECE in Top 5',
                'Note': 'High Priority - Top College + Core Branch'
            })
            priority += 1

    # Top 6-10 Colleges: CSE/CSE-aligned → ECE
    # st.write("🥈 **Top 6-10 Colleges Priority Order:**")
    for i in range(5, min(10, len(selected_colleges))):
        college = selected_colleges[i]

        # CSE branches
        for branch in CSE_BRANCHES:
            hardcoded_options.append({
                'Priority': priority,
                'College_Tier': f"Top {i+1}",
                'College': college["name"],
                'Branch_Code': branch,
                'Branch_Name': BRANCH_MAP.get(branch, branch),
                'Strategy': 'CSE in Top 6-10',
                'Note': 'Very Good - Excellent College + Premium Branch'
            })
            priority += 1

    for i in range(5, min(10, len(selected_colleges))):
        college = selected_colleges[i]
        # ECE
        hardcoded_options.append({
            'Priority': priority,
            'College_Tier': f"Top {i+1}",
            'College': college["name"],
            'Branch_Code': 'ECE',
            'Branch_Name': BRANCH_MAP.get('ECE', 'ECE'),
            'Strategy': 'ECE in Top 6-10',
            'Note': 'Good - Strong College + Core Branch'
        })
        priority += 1

    # Top 11-15 Colleges: CSE/CSE-aligned → ECE
    # st.write("🥉 **Top 11-15 Colleges Priority Order:**")
    for i in range(10, min(20, len(selected_colleges))):
        college = selected_colleges[i]

        # Top CSE branches only
        for branch in CSE_BRANCHES:
            hardcoded_options.append({
                'Priority': priority,
                'College_Tier': f"Top {i+1}",
                'College': college["name"],
                'Branch_Code': branch,
                'Branch_Name': BRANCH_MAP.get(branch, branch),
                'Strategy': 'CSE in Top 11-15',
                'Note': 'Good - Decent College + Premium Branch'
            })
            priority += 1

    for i in range(10, min(20, len(selected_colleges))):
        college = selected_colleges[i]
        # ECE
        hardcoded_options.append({
            'Priority': priority,
            'College_Tier': f"Top {i+1}",
            'College': college["name"],
            'Branch_Code': 'ECE',
            'Branch_Name': BRANCH_MAP.get('ECE', 'ECE'),
            'Strategy': 'ECE in Top 11-15',
            'Note': 'Decent - Average College + Core Branch'
        })
        priority += 1

    # Top 1-10 Colleges: Other Core Branches (backup strategy)
    # st.write("⚙️ **Top 1-10 Colleges - Other Core Branches (Backup):**")
    for i in range(min(10, len(selected_colleges))):
        college = selected_colleges[i]

        for branch in OTHER_CORE_BRANCHES:
            hardcoded_options.append({
                'Priority': priority,
                'College_Tier': f"Top {i+1}",
                'College': college["name"],
                'Branch_Code': branch,
                'Branch_Name': BRANCH_MAP.get(branch, branch),
                'Strategy': 'Core Branches in Top 10',
                'Note': 'Backup - Excellent College + Traditional Branch'
            })
            priority += 1

    for i in range(10, min(20, len(selected_colleges))):
        college = selected_colleges[i]

        for branch in OTHER_CORE_BRANCHES:
            hardcoded_options.append({
                'Priority': priority,
                'College_Tier': f"Top {i+1}",
                'College': college["name"],
                'Branch_Code': branch,
                'Branch_Name': BRANCH_MAP.get(branch, branch),
                'Strategy': 'Core Branches in Top 16-20',
                'Note': 'Lower Tier College + Traditional Branch'
            })
        priority += 1

    return hardcoded_options


def get_rank_based_best_list(user_rank, gender, caste, phase="Final Phase", buffer=1000, list_type="Manual Ranking (Our Curated List)"):
    """
    Generate Type 2: Rank-based Best List - Adapts based on candidate's rank
    """
    df = load_data(phase)
    if df is None:
        return []

    # Detect column names
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'

    branch_col = 'Branch Code' if 'Branch Code' in df.columns else 'Branch'
    caste_column = get_caste_column_name(gender, caste)

    selected_colleges = get_college_list_by_type(list_type, gender)
    rank_based_options = []
    priority = 1

    def check_and_add_branch(college_name, branches_to_check, tier_name, strategy_name):
        nonlocal priority
        options_added = 0

        # Find college in dataset
        college_matches = df[df[college_col].str.lower() ==
                             college_name.lower()]

        if not college_matches.empty:
            for branch_code in branches_to_check:
                branch_matches = college_matches[
                    college_matches[branch_col].str.contains(
                        branch_code, case=False, na=False)
                ]

                for _, row in branch_matches.iterrows():
                    if caste_column in row and pd.notna(row[caste_column]):
                        cutoff_rank = row[caste_column]
                        buffer_rank = cutoff_rank + buffer

                        if user_rank <= buffer_rank:
                            rank_based_options.append({
                                'Priority': priority,
                                'College_Tier': tier_name,
                                'College': row[college_col],
                                'Branch_Code': branch_code,
                                'Branch_Name': BRANCH_MAP.get(branch_code, branch_code),
                                'Last_Year_Cutoff': int(cutoff_rank),
                                'Your_Rank': user_rank,
                                'Buffered_Cutoff': int(buffer_rank),
                                'Chance': 'Good' if user_rank <= cutoff_rank else 'Fair',
                                'Strategy': strategy_name,
                                'Tuition_Fee': row.get('Tuition Fee', 'N/A'),
                                'District': row.get('Dist Code', 'N/A'),
                            })
                            priority += 1
                            options_added += 1
                            break  # Take first match for this branch

        return options_added

    # Top 1-5 Colleges: CSE/CSE-aligned → ECE
    for i in range(min(5, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1}"

        # Check CSE branches first
        check_and_add_branch(college_name, CSE_BRANCHES,
                             tier, "Prime CSE in Top 5")
        # Then CSE-aligned
        check_and_add_branch(
            college_name, CSE_ALIGNED_BRANCHES, tier, "CSE-Aligned in Top 5")

    for i in range(min(5, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1}"
        # Then ECE
        check_and_add_branch(college_name, ECE_BRANCHES, tier, "ECE in Top 5")

    # Top 6-10 Colleges: CSE/CSE-aligned → ECE
    for i in range(5, min(10, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1}"

        check_and_add_branch(college_name, CSE_BRANCHES,
                             tier, "CSE in Top 6-10")
        check_and_add_branch(college_name, CSE_ALIGNED_BRANCHES,
                             tier, "CSE-Aligned in Top 6-10")

    for i in range(5, min(10, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1}"
        check_and_add_branch(college_name, ECE_BRANCHES,
                             tier, "ECE in Top 6-10")

    # Top 11-20 Colleges: CSE/CSE-aligned → ECE
    for i in range(10, min(20, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1}"

        check_and_add_branch(college_name, CSE_BRANCHES,
                             tier, "CSE in Top 11-15")
        check_and_add_branch(college_name, CSE_ALIGNED_BRANCHES,
                             tier, "CSE-Aligned in Top 11-20")

    for i in range(10, min(20, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1}"
        check_and_add_branch(college_name, ECE_BRANCHES,
                             tier, "ECE in Top 11-20")

    # Top 1-10 Colleges: Other Core Branches (backup)
    for i in range(min(10, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1} (Backup)"

        check_and_add_branch(college_name, OTHER_CORE_BRANCHES,
                             tier, "Core Branches in Top 1-10")

    # Top 15-20 Colleges: Other Core Branches (backup)
    for i in range(10, min(20, len(selected_colleges))):
        college = selected_colleges[i]
        college_name = college["name"]
        tier = f"Top {i+1} (Backup)"

        check_and_add_branch(college_name, OTHER_CORE_BRANCHES,
                             tier, "Core Branches Backup")

    # Beyond Top 20: All colleges sorted by ascending cutoff
    beyond_top20_colleges = df[~df[college_col].str.lower().isin(
        [college["name"].lower() for college in selected_colleges]
    )]

    # Sort by cutoff rank ascending
    if caste_column in beyond_top20_colleges.columns:
        beyond_top20_colleges = beyond_top20_colleges.sort_values(
            by=caste_column, ascending=True
        )
        # .head(100) # Limit to avoid too many results

        for _, row in beyond_top20_colleges.iterrows():
            if pd.notna(row[caste_column]):
                cutoff_rank = row[caste_column]
                buffer_rank = cutoff_rank + buffer

                branch_code = row[branch_col] if pd.notna(
                    row[branch_col]) else 'Unknown'

                rank_based_options.append({
                    'Priority': priority,
                    'College_Tier': 'Beyond Top 20',
                    'College': row[college_col],
                    'Branch_Code': branch_code,
                    'Branch_Name': BRANCH_MAP.get(branch_code, branch_code),
                    'Last_Year_Cutoff': int(cutoff_rank),
                    'Your_Rank': user_rank,
                    'Buffered_Cutoff': int(buffer_rank),
                    'Chance': 'Good' if user_rank <= cutoff_rank else 'Fair',
                    'Strategy': 'Ascending Cutoff Order',
                    'Tuition_Fee': row.get('Tuition Fee', 'N/A'),
                    'District': row.get('Dist Code', 'N/A'),
                })
                priority += 1

                # if len(rank_based_options) >= 75:  # Limit total results
                #     break

    return rank_based_options


def render():
    """Render the Best Possible WebOptions Generator page."""
    st.subheader("🎯 Best Possible WebOptions Generator")

    st.markdown("""
   If you're confused between a top college or a dream branch or Do not know what to prioritize, this tool helps you discover **data-backed combinations** that give you the best shot at securing a seat.
    """)

    # st.markdown("""
    # > ⚙️ Please enter your **Rank**, **Category**, and **Gender** and **other details** to continue.
    # """)

    # Strategy Selection
    st.markdown("#### 🎮 Choose Your Strategy Type")
    strategy_type = st.radio(
        "Select the type of web options list you want:",
        [
            "🤖 Smart Rank-Based List (Recommended)",
            "📋 Complete Strategic Template"
        ],
        help="""
    **Smart Rank-Based**: Customized for your rank - shows only realistic options \n
    **Strategic Template**: Shows the complete ideal strategy pattern (all possibilities)
    """
    )

    # Common inputs
    with st.form("best_options_form"):
        col1, col2 = st.columns(2)

        with col1:
            if strategy_type == "🤖 Smart Rank-Based List (Recommended)":
                user_rank = st.number_input(
                    "Enter your TS EAMCET Rank",
                    min_value=1,
                    max_value=200000,
                    value=1,
                    help="Your TS EAMCET 2025 rank"
                )
            else:
                user_rank = None
                st.info("📋 Template mode - rank not required")

            gender = st.selectbox(
                "Select Gender",
                ["Male", "Female"],
                help="Gender affects college ranking and cutoff data"
            )

            if strategy_type == "🤖 Smart Rank-Based List (Recommended)":
                caste = st.selectbox(
                    "Select Category",
                    ["OC", "BC_A", "BC_B", "BC_C", "BC_D",
                        "BC_E", "SC", "ST", "EWS"],
                    help="Your caste category for cutoff comparison"
                )
            else:
                caste = "OC"  # Default for template

        with col2:
            list_type = st.selectbox(
                "College Ranking Method",
                [
                    "Manual Ranking (Our Curated List)",
                    "Cutoff-Based Ranking (Data-Driven)"
                ],
                help="Choose the Top 20 college ranking methodology"
            )

            if strategy_type == "🤖 Smart Rank-Based List (Recommended)":
                phase = st.selectbox(
                    "Select Phase Data",
                    ["Final Phase", "2nd Phase", "1st Phase"],
                    help="Final Phase recommended for most accurate cutoffs"
                )

                buffer = st.slider(
                    "Safety Buffer (ranks)",
                    min_value=0,
                    max_value=5000,
                    value=1000,
                    step=500,
                    help="Additional safety margin added to cutoffs"
                )
            else:
                phase = "Final Phase"
                buffer = 1000

        generate_button = st.form_submit_button(
            "🚀 Generate Best Possible WebOptions",
            type="primary"
        )

    # Generate Results
    if generate_button:
        if strategy_type == "🤖 Smart Rank-Based List (Recommended)":
            if user_rank <= 0:
                st.error("⚠️ Please enter a valid rank!")
                return

            with st.spinner("🔍 Analyzing your rank and generating personalized strategic options..."):
                web_options = get_rank_based_best_list(
                    user_rank=user_rank,
                    gender=gender,
                    caste=caste,
                    phase=phase,
                    buffer=buffer,
                    list_type=list_type
                )

            if not web_options:
                st.warning(
                    "❌ No suitable options found with current criteria.")
                st.markdown("### 💡 Suggestions:")
                st.markdown("""
                - Increase safety buffer to 2000-3000 ranks
                - Try different phase data (2nd Phase might have higher cutoffs)
                - Consider that your rank might need broader branch exploration
                """)
                return

            # Display results for rank-based list
            st.success(
                f"✅ Found {len(web_options)} strategic web options tailored for rank {user_rank}!")

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                good_chances = len(
                    [opt for opt in web_options if opt.get('Chance') == 'Good'])
                st.metric("🎯 Good Chances", good_chances)

            with col2:
                fair_chances = len(
                    [opt for opt in web_options if opt.get('Chance') == 'Fair'])
                st.metric("⚡ Fair Chances", fair_chances)

            with col3:
                top_colleges = len(
                    [opt for opt in web_options if 'Top' in opt.get('College_Tier', '')])
                st.metric("⭐ Top College Options", top_colleges)

            with col4:
                cse_options = len([opt for opt in web_options if opt.get(
                    'Branch_Code', '') in CSE_BRANCHES])
                st.metric("💻 CSE/ CSE related Options", cse_options)

            # Strategy breakdown
            st.markdown("### 📊 Your Strategic WebOptions")

            df_results = pd.DataFrame(web_options)

            # Enhanced display
            st.dataframe(
                df_results,
                column_config={
                    "Priority": st.column_config.NumberColumn("Priority", width="small"),
                    "College_Tier": st.column_config.TextColumn("Tier", width="small"),
                    "College": st.column_config.TextColumn("College Name", width="large"),
                    "Branch_Code": st.column_config.TextColumn("Branch", width="small"),
                    "Branch_Name": st.column_config.TextColumn("Branch Name", width="large"),
                    "Last_Year_Cutoff": st.column_config.NumberColumn("Last Cutoff", format="%d"),
                    "Buffered_Cutoff": st.column_config.NumberColumn("Safe Cutoff", format="%d"),
                    "Chance": st.column_config.TextColumn("Chance", width="small"),
                    "Strategy": st.column_config.TextColumn("Strategy", width="medium"),
                },
                hide_index=True,
                use_container_width=True
            )

            # Download options
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Strategic WebOptions (CSV)",
                data=csv,
                file_name=f"Best_WebOptions_Rank_{user_rank}_{caste}_{gender}.csv",
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

        else:  # Template mode
            st.markdown("### 📋 Complete Strategic Template")
            st.info("This shows the complete strategic hierarchy. Use this as a reference to understand the optimal web option filling pattern.")

            with st.spinner("📋 Generating complete strategic template..."):
                template_options = get_hardcoded_best_list(list_type, gender)

            st.success(
                f"✅ Generated complete strategic template with {len(template_options)} options!")

            # Display template
            df_template = pd.DataFrame(template_options)

            st.dataframe(
                df_template,
                column_config={
                    "Priority": st.column_config.NumberColumn("Priority", width="small"),
                    "College_Tier": st.column_config.TextColumn("Tier", width="small"),
                    "College": st.column_config.TextColumn("College Name", width="large"),
                    "Branch_Code": st.column_config.TextColumn("Branch", width="small"),
                    "Branch_Name": st.column_config.TextColumn("Branch Name", width="large"),
                    "Strategy": st.column_config.TextColumn("Strategy", width="medium"),
                    "Note": st.column_config.TextColumn("Note", width="large"),
                },
                hide_index=True,
                use_container_width=True
            )

            # Download template
            csv = df_template.to_csv(index=False)
            st.download_button(
                label="📥 Download Strategic Template (CSV)",
                data=csv,
                file_name=f"Strategic_WebOptions_Template_{list_type.replace(' ', '_')}_{gender}.csv",
                mime="text/csv"
            )

            excel_buffer = io.BytesIO()
            df_template.to_excel(excel_buffer, index=False)
            st.download_button(
                label="Download Results as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"TS_EAMCET_2025_WebOptions_Rank_{list_type.replace(' ', '_')}_{caste}_{gender}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Common insights section
        st.markdown("### 🎯 Strategic Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🏆 Hierarchy Explanation:**")
            st.markdown("""
             \n
            - 🥇 **Top 1–5 Colleges**: CSE/CSE Aligned branches → ECE branch  
            - 🥈 **Top 6–10 Colleges**: CSE/CSE Aligned branches → ECE branch 
            - 🥉 **Top 11–20 Colleges**: CSE/CSE Aligned branches → ECE branch 
            - ⚙️ **Top 1–10 Colleges**: EEE/Mech/Civil and other branches 
            - 🛠️ **Top 11–20 Colleges**: EEE/Mech/Civil and other branches 
            - 🧩 **Beyond Top 20**: Ascending cutoff order 
            - This advanced tool follows our optimized hierarchy
            """)

        with col2:
            st.markdown("**💡 Strategic Tips:**")
            st.markdown("""
             - **Never skip top colleges** - even for less preferred branches 
             - **CSE AND CSE RELATED branches** have highest ROI and placement rates 
             - **ECE** is the best core branch alternative 
             - **EEE/Mech** in top colleges > CSE in average colleges 
             - **Location matters** - consider travel and accommodation
            """)

        # Important disclaimers
        st.markdown("### ⚠️ Important Notes")
        st.warning("""
        **🚨 Strategic Disclaimers:**
        
        1. **This is a strategic framework** - actual success depends on cutoff variations
        2. **Mix strategies** - don't put all options in one tier
        3. **Consider personal factors** - location, fees, personal interests
        4. **Verify official data** - always cross-check with official TS EAMCET guidelines
        5. **Market dynamics** - IT/CS job market is competitive but rewarding
        
        **Remember**: The best web option is one that balances college reputation, branch preference, and realistic admission chances.
        """)

        st.info(f"""
        **📈 Success Formula**: 
        - 40% options from your stretch tier (slightly above your rank)
        - 40% options from your target tier (around your rank)  
        - 20% options from your safety tier (well below your rank)
        
        This ensures you have ambitious goals while securing fallback options.
        """)

    st.info("""
    💡 **How It Works**  
    This tool uses expert-verified strategies and past cutoff trends to auto-generate web options in a **smart hierarchical order**:
    - Prioritizing **CSE** → **CSE Aligned** (like AI, DS, IT) → **ECE**
    - Suggesting top colleges first, then best-fit branches within your range
    - Offering fallback options in top colleges and beyond, just in case your top preferences are out of reach
    """)

    st.warning("""
    ⚠️ **Disclaimer**  
    This is a **strategy reference tool**, not a guaranteed admission predictor.

    - We are **not responsible** for any admission issues.
    - Use this tool as **guidance**, not a final decision-maker.
    - Final seat allotment depends on **counseling**, **cutoffs**, **seat availability**, and **your final preferences**.

    👉 If you already have strong preferences for **specific colleges or branches**, we recommend using other tools on this website to **customize your web options**.
    """)

    


if __name__ == "__main__":
    render()
