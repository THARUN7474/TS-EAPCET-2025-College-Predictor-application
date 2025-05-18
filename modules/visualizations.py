"""
Data visualization functions for the TS EAMCET College Predictor.
"""
import pandas as pd
import plotly.express as px
import streamlit as st
import json


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
    st.subheader("Branch Analysis Chart")
    st.bar_chart(branch_analysis)

    # Create a DataFrame for display
    analysis_df = pd.DataFrame({
        'Branch': branch_analysis.index,
        'Median Closing Rank': branch_analysis.values
    })
    st.dataframe(analysis_df, hide_index=True, use_container_width=True)


def create_closing_ranks_chart(data, categories, title="Closing Ranks by College"):
    """
    Create a bar chart of closing ranks for colleges using Chart.js.

    Args:
        data (pd.DataFrame): DataFrame with college names and closing ranks.
        categories (list): List of category columns to plot (e.g., ['OC BOYS', 'OC GIRLS']).
        title (str): Title of the chart.
    """
    # Prepare data for the chart
    labels = data['College Name'].tolist()
    datasets = []

    # Define colors for different categories
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
              '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
              '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']

    # Create datasets for each category
    for idx, category in enumerate(categories):
        datasets.append({
            'label': category,
            'data': data[category].tolist(),
            'backgroundColor': colors[idx % len(colors)],
            'borderColor': colors[idx % len(colors)],
            'borderWidth': 1
        })

    # Chart configuration
    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": datasets
        },
        "options": {
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "Closing Rank"
                    }
                },
                "x": {
                    "title": {
                        "display": True,
                        "text": "College Name"
                    },
                    "ticks": {
                        "autoSkip": False,
                        "maxRotation": 45,
                        "minRotation": 45
                    }
                }
            },
            "plugins": {
                "legend": {
                    "display": True,
                    "position": "top"
                },
                "title": {
                    "display": True,
                    "text": title
                },
                "tooltip": {
                    "enabled": True
                }
            },
            "responsive": True,
            "maintainAspectRatio": False
        }
    }

    # Display the chart in Streamlit
    st.markdown("### Closing Ranks Visualization")
    st.write(
        "This chart shows the closing ranks for colleges offering your selected branch.")
    st.components.v1.html(f"""
        <div style="width:100%; height:400px;">
            <canvas id="closingRanksChart"></canvas>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            const ctx = document.getElementById('closingRanksChart').getContext('2d');
            new Chart(ctx, {json.dumps(chart_config)});
        </script>
    """, height=450)
