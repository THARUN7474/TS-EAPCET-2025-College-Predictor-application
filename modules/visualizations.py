"""
Data visualization functions for the TS EAMCET College Predictor.
"""
import pandas as pd
import plotly.express as px
import streamlit as st

def create_branch_distribution_chart(result_df):
    """
    Create a bar chart showing college distribution by district.
    
    Args:
        result_df (pandas.DataFrame): DataFrame containing college prediction results
        
    Returns:
        None: Directly renders the chart in Streamlit
    """
    if 'District' in result_df.columns:
        district_counts = result_df['District'].value_counts()
        if not district_counts.empty:
            st.subheader("College Distribution by District")
            st.bar_chart(district_counts)

def create_branch_cutoff_chart(branch_data):
    """
    Create a bar chart showing branch cutoffs for a specific college.
    
    Args:
        branch_data (pandas.DataFrame): DataFrame containing branch cutoff data
        
    Returns:
        None: Directly renders the chart in Streamlit
    """
    if 'Closing Rank' in branch_data.columns and 'Branch' in branch_data.columns:
        st.subheader("Branch Cutoff Comparison")
        chart_data = branch_data.set_index('Branch')['Closing Rank']
        st.bar_chart(chart_data)

def create_branch_comparison_plot(branch_data):
    """
    Create a Plotly horizontal bar chart for branch comparison.
    
    Args:
        branch_data (pandas.DataFrame): DataFrame containing branch cutoff data
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if 'Closing Rank' in branch_data.columns and 'Branch' in branch_data.columns:
        fig = px.bar(
            branch_data.sort_values('Closing Rank'),
            x='Closing Rank',
            y='Branch',
            orientation='h',
            color='Closing Rank',
            color_continuous_scale='Blues',
            labels={'Closing Rank': 'Closing Rank', 'Branch': 'Branch'},
            title='Closing Ranks by Branch'
        )
        return fig
    return None

def create_branch_analysis_chart(branch_analysis):
    """
    Create a bar chart for branch analysis across all colleges.
    
    Args:
        branch_analysis (pandas.Series): Series containing median cutoff ranks by branch
        
    Returns:
        None: Directly renders the chart in Streamlit
    """
    st.bar_chart(branch_analysis)
    
    # Create a DataFrame for display
    analysis_df = pd.DataFrame({
        'Branch': branch_analysis.index,
        'Median Closing Rank': branch_analysis.values
    })
    st.dataframe(analysis_df, hide_index=True, use_container_width=True)