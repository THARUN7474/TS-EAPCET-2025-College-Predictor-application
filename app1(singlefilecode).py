import streamlit as st
import pandas as pd
import os
import io
from fpdf import FPDF
import plotly.express as px


# Setting page configuration for better appearance
st.set_page_config(page_title="TS EAMCET 2025 College Predictor",
                   page_icon="🎓", layout="wide")


# Defining function to load and clean data
@st.cache_data
def load_data(phase_selection):
    """
    Load data based on selected phase
    """
    # Mapping of phase selection to file names
    phase_files = {
        "Final Phase": "./Data/03_TGEAPCET_2024_FinalPhase.csv",
        "1st Phase": "./Data/01_TGEAPCET_2024_FirstPhase.csv",
        "2nd Phase": "./Data/02_TGEAPCET_2024_SecondPhase.csv"
    }

    file_path = phase_files.get(phase_selection)

    # If file doesn't exist, try to use the data in the current session
    if not os.path.exists(file_path):
        try:
            data = {}
            df = pd.read_csv("paste.txt", delimiter="\t")
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None

    # Reading CSV with proper handling of headers
    df = pd.read_csv(file_path, skipinitialspace=True)

    # Cleaning column names
    df.columns = [col.strip().replace('\n', '') for col in df.columns]

    # Converting rank columns to numeric, handling errors
    rank_columns = [
        col for col in df.columns if 'BOYS' in col or 'GIRLS' in col or 'EWS' in col]
    for col in rank_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handling missing values
    if 'Inst Code' in df.columns and 'Institute Name' in df.columns:
        df = df.dropna(subset=['Inst Code', 'Institute Name', 'Branch Code'])
    else:

        df = df.dropna(subset=['Place', 'Branch Code'])

    return df


# Function to map branch codes to full names
def get_branch_map():
    return {
        'CSE': 'COMPUTER SCIENCE AND ENGINEERING',
        'CSM': 'COMPUTER SCIENCE AND ENGINEERING (ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)',
        'CSD': 'COMPUTER SCIENCE AND ENGINEERING (DATA SCIENCE)',
        'ECE': 'ELECTRONICS AND COMMUNICATION ENGINEERING',
        'EEE': 'ELECTRICAL AND ELECTRONICS ENGINEERING',
        'CIV': 'CIVIL ENGINEERING',
        'MEC': 'MECHANICAL ENGINEERING',
        'INF': 'INFORMATION TECHNOLOGY',
        'AID': 'ARTIFICIAL INTELLIGENCE AND DATA SCIENCE',
        'CSO': 'COMPUTER SCIENCE AND ENGINEERING (IOT)',
        'CSC': 'COMPUTER SCIENCE AND ENGINEERING (CYBER SECURITY)',
        'CSB': 'COMPUTER SCIENCE AND BUSINESS SYSTEM',
        'CSW': 'COMPUTER ENGINEERING(SOFTWARE ENGINEERING)',
        'EIE': 'ELECTRONICS AND INSTRUMENTATION ENGINEERING',
        'AUT': 'AUTOMOBILE ENGINEERING',
        'AIM': 'ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING',
        'MIN': 'MINING ENGINEERING'
    }


# Defining function to predict colleges
def predict_colleges(rank, gender, caste, branch, phase_selection, district_filter=None):
    df = load_data(phase_selection)
    if df is None:
        return None

    # if branch == "N/A":
    #     st.warning("Please select a valid branch.")
    #     return None
    # Mapping user input to column names
    caste_map = {
        'OC': 'OC',
        'BC_A': 'BC_A',
        'BC_B': 'BC_B',
        'BC_C': 'BC_C',
        'BC_D': 'BC_D',
        'BC_E': 'BC_E',
        'SC': 'SC',
        'ST': 'ST',
        'EWS': 'EWS GEN OU' if gender == 'Male' else 'EWS GIRLS OU'
    }

    gender_suffix = 'BOYS' if gender == 'Male' else 'GIRLS'
    if caste == 'EWS':
        target_column = caste_map[caste]
    else:
        target_column = f"{caste_map[caste]} {gender_suffix}"

    # Get branch mapping
    branch_map = get_branch_map()

    # Checking branch column name in dataframe
    branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'

    # Detect college name column
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'

    # Filtering by branch
    branch_match = branch_map.get(branch)
    filtered_df = df[df[branch_col].str.strip() == branch_match]

    # Filtering by branch (skip if branch is "N/A")----ffor all branches filtering
    if branch != "N/A":
        branch_match = branch_map.get(branch)
        filtered_df = df[df[branch_col].str.strip() == branch_match]
    else:
        filtered_df = df

    # Apply district filter if provided
    if district_filter and district_filter != "All Districts":
        district_col = 'Dist Code' if 'Dist Code' in df.columns else 'Dist Code'
        filtered_df = filtered_df[filtered_df[district_col] == district_filter]

    # Checking if target column exists
    if target_column not in filtered_df.columns:
        st.warning(
            f"No data available for {caste} {gender} in the selected branch!")
        return None

    # Filtering colleges where rank is sufficient
    filtered_df = filtered_df[filtered_df[target_column] >= rank]

    # Sorting by cutoff rank ascending
    filtered_df = filtered_df.sort_values(by=target_column, ascending=True)

    # Select columns based on available data
    available_cols = []
    if college_col in filtered_df.columns:
        available_cols.append(college_col)
    if branch_col in filtered_df.columns:
        available_cols.append(branch_col)
    if 'Place' in filtered_df.columns:
        available_cols.append('Place')
    if 'Dist Code' in filtered_df.columns:
        available_cols.append('Dist Code')
    if 'Tuition Fee' in filtered_df.columns:
        available_cols.append('Tuition Fee')
    if 'Affiliated To' in filtered_df.columns:
        available_cols.append('Affiliated To')
    if target_column in filtered_df.columns:
        available_cols.append(target_column)

    # Prepare the result dataframe with available columns
    result_df = filtered_df[available_cols].copy()

    # Rename columns for display
    rename_map = {
        'Institute Name': 'College Name',
        'Branch Name': 'Branch',
        'Dist Code': 'District',
        'Tuition Fee': 'Tuition Fee (₹)',
        target_column: 'Closing Rank'
    }

    # Only rename columns that exist
    rename_cols = {k: v for k, v in rename_map.items()
                   if k in result_df.columns}
    result_df = result_df.rename(columns=rename_cols)

    return result_df


# Function to compare colleges across phases
def compare_phases(rank, gender, caste, branch):
    phases = ["1st Phase", "2nd Phase", "Final Phase"]
    comparison = {}

    for phase in phases:
        result = predict_colleges(rank, gender, caste, branch, phase)
        if result is not None and not result.empty:
            # Get top 5 colleges for each phase
            # TODO TO UPDATE AS PER REQUIREMENT LATER WILL MAKE THIS AS USER INPUT BASED
            comparison[phase] = result.head(5)

    return comparison


# Function to get college branches based on user input
def get_college_branches(college_name, phase_selection, gender, caste):
    df = load_data(phase_selection)
    if df is None:
        return None

    # Detect college name column
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'  # In the paste.txt data, we use Place as the college identifier

    # Branch column name
    branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'

    # Mapping user input to column names
    caste_map = {
        'OC': 'OC',
        'BC_A': 'BC_A',
        'BC_B': 'BC_B',
        'BC_C': 'BC_C',
        'BC_D': 'BC_D',
        'BC_E': 'BC_E',
        'SC': 'SC',
        'ST': 'ST',
        'EWS': 'EWS GEN OU' if gender == 'Male' else 'EWS GIRLS OU'
    }

    gender_suffix = 'BOYS' if gender == 'Male' else 'GIRLS'
    if caste == 'EWS':
        target_column = caste_map[caste]
    else:
        target_column = f"{caste_map[caste]} {gender_suffix}"

    # Filter by college
    filtered_df = df[df[college_col] == college_name]

    if filtered_df.empty:
        return None

    # Select relevant columns
    available_cols = []
    if branch_col in filtered_df.columns:
        available_cols.append(branch_col)
    if 'Branch Code' in filtered_df.columns:
        available_cols.append('Branch Code')
    if target_column in filtered_df.columns:
        available_cols.append(target_column)
    if 'Tuition Fee' in filtered_df.columns:
        available_cols.append('Tuition Fee')

    # Prepare the result dataframe with available columns
    result_df = filtered_df[available_cols].copy()

    # Rename columns for display
    rename_map = {
        'Branch Name': 'Branch',
        'Tuition Fee': 'Tuition Fee (₹)',
        target_column: 'Closing Rank'
    }

    # Only rename columns that exist
    rename_cols = {k: v for k, v in rename_map.items()
                   if k in result_df.columns}
    result_df = result_df.rename(columns=rename_cols)

    # Sort by closing rank
    if 'Closing Rank' in result_df.columns:
        result_df = result_df.sort_values(by='Closing Rank', ascending=True)

    return result_df


# Get top colleges list (I'll need to update this) tharun do it after thourgh research
# TODO TO UPDATE THIS LATER
def get_top_colleges():
    return [
        {"name": "CBIT Hyderabad",
            "details": "Known for excellent placements in CSE and ECE branches"},
        {"name": "VNRVJIET Hyderabad",
            "details": "Strong academics and good infrastructure"},
        {"name": "Vasavi College of Engineering",
            "details": "Consistent placement record and quality education"},
        {"name": "MGIT Hyderabad", "details": "Good placements for CSE and IT branches"},
        {"name": "Gokaraju Rangaraju Institute of Engineering and Technology",
            "details": "Good infrastructure and placements"},
        {"name": "CVR College of Engineering",
            "details": "Strong academics and industry connections"},
        {"name": "KMIT Hyderabad", "details": "Known for IT and CSE programs"},
        {"name": "Malla Reddy College of Engineering and Technology",
            "details": "Large campus with good facilities"},
        {"name": "Sreenidhi Institute of Science and Technology",
            "details": "Good campus and placement opportunities"},
        {"name": "CMR College of Engineering & Technology",
            "details": "Decent infrastructure and faculty"},
        {"name": "BVRIT Hyderabad", "details": "Good placements for core branches"},
        {"name": "CMRIT Hyderabad", "details": "Growing reputation for placements"},
        {"name": "Vardhaman College of Engineering",
            "details": "Good infrastructure and academics"},
        {"name": "JNTUH College of Engineering Hyderabad",
            "details": "Government college with strong academics"},
        {"name": "MVSR Engineering College",
            "details": "Established reputation with good faculty"},
        {"name": "Matrusri Engineering College",
            "details": "Good location and decent placements"},
        {"name": "JBIET Hyderabad",
            "details": "Large campus with multiple specializations"},
        {"name": "SNIST Hyderabad", "details": "Good infrastructure and faculty"},
        {"name": "Muffakham Jah College of Engineering and Technology",
            "details": "Known for quality education"},
        {"name": "VJIT Hyderabad", "details": "Decent placements and infrastructure"}
    ]


# Function to convert DataFrame to PDF
# TODO TO UPDATE THIS LATER TO MAKE THE OUTPUT PDF MORE BEAUTIFUL AND READABLE
# This is a basic implementation, YOU can enhance it with better formatting THARUN
def dataframe_to_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    # Table header
    col_width = pdf.w / (len(df.columns) + 1)
    row_height = pdf.font_size * 1.5

    # Header
    for col in df.columns:
        # Remove or replace non-latin1 characters in header
        safe_col = str(col).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(col_width, row_height, safe_col, border=1)
    pdf.ln(row_height)

    # Rows
    for i, row in df.iterrows():
        for item in row:
            # Convert to string and remove/replace non-latin1 characters
            safe_item = str(item).replace("₹", "Rs.").encode(
                'latin-1', 'replace').decode('latin-1')
            pdf.cell(col_width, row_height, safe_item, border=1)
        pdf.ln(row_height)
    return pdf.output(dest='S').encode('latin-1')


# Creating Streamlit UI
def main():
    st.title("🎓 TS EAMCET 2025 College Predictor")

    # Tabs for different functionalities
    tabs = st.tabs(["College Predictor", "Phase Comparison", "Branch Analysis",
                   "College-wise Branches", "Help"])

    # College Predictor
    with tabs[0]:
        st.markdown(
            "Enter your details to find colleges you may be eligible for based on TS EAMCET cutoff ranks.")

        # Creating input form
        with st.form("predictor_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                rank = st.number_input(
                    "Enter your EAMCET Rank", min_value=1, max_value=200000, step=1)
                gender = st.selectbox("Select Gender", ["Male", "Female"])

            with col2:
                caste = st.selectbox("Select Caste", [
                                     "OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC", "ST", "EWS"])
                branch_options = ["N/A"] + list(get_branch_map().keys())
                branch = st.selectbox(
                    "Select Branch", branch_options)
                # branch = st.selectbox(
                #     "Select Branch", list(get_branch_map().keys()))

            with col3:
                phase = st.selectbox("Select Phase Data", [
                                     "Final Phase", "2nd Phase", "1st Phase"])
                # Get district options from data
                df = load_data(phase)
                districts = ["All Districts"]
                if df is not None and 'Dist Code' in df.columns:
                    districts.extend(sorted(df['Dist Code'].unique().tolist()))
                district_filter = st.selectbox("Filter by District", districts)

            submit_button = st.form_submit_button("Predict Colleges")

        # Processing form submission
        if submit_button:
            if rank < 1:
                st.error("Please enter a valid rank!")
            else:
                with st.spinner("Finding colleges..."):
                    result = predict_colleges(
                        rank, gender, caste, branch, phase, district_filter)

                if result is None or result.empty:
                    st.warning(
                        "No colleges found matching your criteria. Try adjusting your rank or preferences.")
                else:
                    st.success(
                        f"Found {len(result)} colleges where you may be eligible!")

                    # Create three columns for the download buttons
                    col_csv, col_excel, col_pdf = st.columns(3)

                    with col_csv:
                        csv = result.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name=f"eamcet_colleges_{rank}_{caste}_{branch}.csv",
                            mime="text/csv"
                        )

                    with col_excel:
                        excel_buffer = io.BytesIO()
                        result.to_excel(excel_buffer, index=False)
                        st.download_button(
                            label="Download Results as Excel",
                            data=excel_buffer.getvalue(),
                            file_name=f"eamcet_colleges_{rank}_{caste}_{branch}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    with col_pdf:
                        pdf_bytes = dataframe_to_pdf(result)
                        st.download_button(
                            label="Download Results as PDF",
                            data=pdf_bytes,
                            file_name=f"eamcet_colleges_{rank}_{caste}_{branch}.pdf",
                            mime="application/pdf"
                        )

                    st.markdown(
                        "Download your results in CSV, Excel, or PDF format using the buttons above i suggest you to use CSV or Excel for better formatting and in next update i will add a better UI for PDF")
                    # st.markdown("---")
                    st.subheader("Eligible Colleges")

                    # Displaying results in a beautiful table
                    st.dataframe(
                        result,
                        column_config={
                            "College Name": st.column_config.TextColumn(width="large"),
                            "Branch": st.column_config.TextColumn(width="medium"),
                            "Place": st.column_config.TextColumn(width="medium"),
                            "District": st.column_config.TextColumn(width="small"),
                            "Tuition Fee (₹)": st.column_config.NumberColumn(format="₹%d"),
                            "Closing Rank": st.column_config.NumberColumn(format="%d"),
                            "Affiliated To": st.column_config.TextColumn(width="small")
                        },
                        hide_index=True,
                        use_container_width=True
                    )

                    # College count by district visualization
                    if 'District' in result.columns:
                        district_counts = result['District'].value_counts()
                        if not district_counts.empty:
                            st.subheader("College Distribution by District")
                            st.bar_chart(district_counts)

    # Phase Comparison
    # TODO TO UPDATE THIS AS USER INPUT BASED LATER
    with tabs[1]:
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
                    get_branch_map().keys()), key="comp_branch")

            compare_button = st.form_submit_button("Compare Phases")

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

    # Branch Analysis
    with tabs[2]:
        st.subheader("Branch Analysis")
        st.markdown(
            "Analyze cutoff trends across different engineering branches.")

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
                    # Mapping user input to column names
                    caste_map = {
                        'OC': 'OC',
                        'BC_A': 'BC_A',
                        'BC_B': 'BC_B',
                        'BC_C': 'BC_C',
                        'BC_D': 'BC_D',
                        'BC_E': 'BC_E',
                        'SC': 'SC',
                        'ST': 'ST',
                        'EWS': 'EWS GEN OU' if branch_gender == 'Male' else 'EWS GIRLS OU'
                    }

                    gender_suffix = 'BOYS' if branch_gender == 'Male' else 'GIRLS'
                    if branch_caste == 'EWS':
                        target_column = caste_map[branch_caste]
                    else:
                        target_column = f"{caste_map[branch_caste]} {gender_suffix}"

                    # Check if column exists
                    if target_column in df.columns:
                        # Group by branch and calculate median rank
                        branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'
                        branch_analysis = df.groupby(
                            branch_col)[target_column].median().sort_values()

                        # Display results
                        st.subheader(
                            f"Median Cutoff Ranks by Branch for {branch_caste} {branch_gender}")

                        # Create a bar chart of the branch analysis
                        st.bar_chart(branch_analysis)

                        # Show the data in a table
                        analysis_df = pd.DataFrame({
                            'Branch': branch_analysis.index,
                            'Median Closing Rank': branch_analysis.values
                        })
                        st.dataframe(analysis_df, hide_index=True,
                                     use_container_width=True)

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
                        st.error(
                            f"Data for {branch_caste} {branch_gender} not available in the dataset.")
                else:
                    st.error("Unable to load data for analysis.")

    # College-wise Branch Analysis
    with tabs[3]:
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
                                              ["Final Phase", "2nd Phase",
                                                  "1st Phase"],
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

                    # Insights
                    #TODO TO UPDATE THIS LATER--as it slows down the app
                    # st.subheader("Key Insights")
                    # if 'Closing Rank' in branch_data.columns and 'Branch' in branch_data.columns:
                    #     st.subheader("Branch Cutoff Comparison")

                    #     # Plotly horizontal bar chart
                    #     fig = px.bar(
                    #         branch_data.sort_values('Closing Rank'),
                    #         x='Closing Rank',
                    #         y='Branch',
                    #         orientation='h',
                    #         color='Closing Rank',
                    #         color_continuous_scale='Blues',
                    #         labels={'Closing Rank': 'Closing Rank',
                    #                 'Branch': 'Branch'},
                    #         title='Closing Ranks by Branch'
                    #     )
                    #     st.plotly_chart(fig, use_container_width=True)

                        # (Optional) Box plot to show distribution
                        # fig_box = px.box(branch_data, x='Closing Rank', y='Branch', orientation='h')
                        # st.plotly_chart(fig_box, use_container_width=True)

                    # Create a bar chart of branch cutoffs
                    if 'Closing Rank' in branch_data.columns and 'Branch' in branch_data.columns:
                        st.subheader("Branch Cutoff Comparison")
                        chart_data = branch_data.set_index('Branch')[
                            'Closing Rank']
                        st.bar_chart(chart_data)

                        # Insights
                        st.subheader("Key Insights")
                        min_rank = branch_data['Closing Rank'].min()
                        max_rank = branch_data['Closing Rank'].max()
                        hardest_branch = branch_data.loc[branch_data['Closing Rank'].idxmin(
                        )]['Branch']
                        easiest_branch = branch_data.loc[branch_data['Closing Rank'].idxmax(
                        )]['Branch']

                        st.markdown(f"""
                        - **Most Competitive Branch**: {hardest_branch} (rank: {min_rank:,.0f})
                        - **Least Competitive Branch**: {easiest_branch} (rank: {max_rank:,.0f})
                        - **Rank Range**: {max_rank - min_rank:,.0f} ranks difference between highest and lowest cutoffs
                        
                        These insights help you choose the most suitable branch based on your rank.
                        """)

        # Top Colleges Section
        st.markdown("---")
        st.subheader(
            "Top 20 Engineering Colleges in Telangana (Based on Market Trends)")

        top_colleges = get_top_colleges()

        for i, college in enumerate(top_colleges):
            with st.expander(f"{i+1}. {college['name']}"):
                st.write(college['details'])

        st.info("""
        **Note about this list**: 
        
        This ranking is based on general market trends, placement records, and academic reputation. 
        The actual ranking may vary based on specific branches, infrastructure, and other factors.
        
        You should update this list with the most current information about top colleges.
        """)

    with tabs[4]:
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

    # Adding footer
    st.markdown("---")
    st.markdown("**Note**: This predictor uses TS EAMCET 2024 cutoff ranks. Actual admissions may vary due to special categories, dropouts, or spot admissions. Data sourced from TGEAPCET 2024 Last Rank Statement.")


if __name__ == "__main__":
    main()