"""
College prediction functions for the TS EAMCET College Predictor.
"""

import pandas as pd
import streamlit as st
from .data_loader import load_data
from .constants import get_caste_column_name, BRANCH_MAP


@st.cache_data(ttl=1800)
def predict_colleges(rank, gender, caste, branch, phase_selection, district_filter=None):
    """
    Predict colleges based on user inputs.

    Args:
        rank (int): User's EAMCET rank
        gender (str): User's gender (Male/Female)
        caste (str): User's caste category
        branch (str): Selected branch
        phase_selection (str): Selected counseling phase
        district_filter (str, optional): District filter

    Returns:
        pandas.DataFrame: Filtered college results or None if no matches
    """
    df = load_data(phase_selection)
    if df is None:
        return None

    # Get the target column based on caste and gender
    target_column = get_caste_column_name(gender, caste)

    # Get branch mapping
    branch_map = BRANCH_MAP

    # Checking branch column name in dataframe
    branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'

    # Detect college name column
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'

    # Filtering by branch (skip if branch is "N/A")
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

# Cache your prediction function


@st.cache_data(ttl=1800)
def compare_phases(rank, gender, caste, branch, top_n=5):
    """
    Compare college predictions across different counseling phases.

    Args:
        rank (int): User's EAMCET rank
        gender (str): User's gender
        caste (str): User's caste category
        branch (str): Selected branch
        top_n (int, optional): Number of top colleges to include

    Returns:
        dict: Dictionary with phase as key and dataframe as value
    """
    phases = ["1st Phase", "2nd Phase", "Final Phase"]
    comparison = {}

    for phase in phases:
        result = predict_colleges(rank, gender, caste, branch, phase)
        if result is not None and not result.empty:
            comparison[phase] = result.head(top_n)

    return comparison

# Cache your prediction function


@st.cache_data(ttl=1800)
def get_college_branches(college_name, phase_selection, gender, caste):
    """
    Get all branches available in a specific college with their cutoffs.

    Args:
        college_name (str): Name of the college
        phase_selection (str): Selected counseling phase
        gender (str): User's gender
        caste (str): User's caste category

    Returns:
        pandas.DataFrame: Branches with cutoffs or None if no data
    """
    df = load_data(phase_selection)
    if df is None:
        return None

    # Detect college name column
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'  # In the paste.txt data, we use Place as the college identifier

    # Branch column name
    branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'

    # Get target column based on caste and gender
    target_column = get_caste_column_name(gender, caste)

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

# Cache your prediction function


@st.cache_data(ttl=1800)
def analyze_branch_cutoffs(branch_caste, branch_gender, phase="Final Phase"):
    """
    Analyze cutoff trends across different branches.

    Args:
        branch_caste (str): Caste category for analysis
        branch_gender (str): Gender for analysis
        phase (str): Counseling phase to analyze

    Returns:
        tuple: (branch_analysis, analysis_df) - Series of median ranks and dataframe for display
    """
    df = load_data(phase)
    if df is None:
        return None, None

    # Get target column based on caste and gender
    target_column = get_caste_column_name(branch_gender, branch_caste)

    # Check if column exists
    if target_column not in df.columns:
        return None, None

    # Group by branch and calculate median rank
    branch_col = 'Branch Name' if 'Branch Name' in df.columns else 'Branch Name'
    branch_analysis = df.groupby(
        branch_col)[target_column].median().sort_values()

    # Create a dataframe for display
    analysis_df = pd.DataFrame({
        'Branch': branch_analysis.index,
        'Median Closing Rank': branch_analysis.values
    })

    return branch_analysis, analysis_df
