"""
Data loading and processing functions for the TS EAMCET College Predictor.
"""

import os
import pandas as pd
import streamlit as st
from .constants import PHASE_FILES

@st.cache_data
def load_data(phase_selection):
    """
    Load data based on selected phase with caching for performance.
    
    Args:
        phase_selection (str): The counseling phase to load data for
        
    Returns:
        pandas.DataFrame: The loaded and cleaned data or None if loading failed
    """
    # Get file path from the phase mapping
    file_path = PHASE_FILES.get(phase_selection)

    # If file doesn't exist, try to use the data in the current session
    if not os.path.exists(file_path):
        try:
            df = pd.read_csv("paste.txt", delimiter="\t")
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None

    # Reading CSV with proper handling of headers
    try:
        df = pd.read_csv(file_path, skipinitialspace=True)
        
        # Clean the dataframe
        df = clean_dataframe(df)
        
        return df
    except Exception as e:
        st.error(f"Error loading data from {file_path}: {e}")
        return None

def clean_dataframe(df):
    """
    Clean and prepare the dataframe for use.
    
    Args:
        df (pandas.DataFrame): The raw dataframe to clean
        
    Returns:
        pandas.DataFrame: The cleaned dataframe
    """
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

def get_districts(df):
    """
    Get unique districts from the dataframe.
    
    Args:
        df (pandas.DataFrame): The dataset
        
    Returns:
        list: List of unique districts
    """
    districts = ["All Districts"]
    if df is not None and 'Dist Code' in df.columns:
        districts.extend(sorted(df['Dist Code'].unique().tolist()))
    return districts

def get_colleges(df):
    """
    Get unique colleges from the dataframe.
    
    Args:
        df (pandas.DataFrame): The dataset
        
    Returns:
        list: List of unique colleges
    """
    if df is None:
        return []
        
    # Detect college name column
    college_col = 'Institute Name' if 'Institute Name' in df.columns else 'College Name'
    if college_col not in df.columns:
        college_col = 'Place'
        
    return sorted(df[college_col].unique().tolist())