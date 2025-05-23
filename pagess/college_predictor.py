"""
College Predictor page for the TS EAMCET College Predictor application.
"""
import streamlit as st
import pandas as pd
import io

from modules.data_loader import load_data
from modules.college_predictor import predict_colleges
from modules.pdf_generator import dataframe_to_pdf
from modules.constants import BRANCH_MAP
from modules.visualizations import create_branch_distribution_chart


def render():
    """Render the College Predictor page."""
    st.markdown(
        "Enter your details to find colleges you may be eligible for based on TS EAMCET 2024 cutoff ranks.")

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
            branch_options = ["N/A"] + list(BRANCH_MAP.keys())
            branch = st.selectbox("Select Branch", branch_options)

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

                # st.markdown(
                #     "Download your results in CSV, Excel, or PDF format using the buttons above")
                # st.subheader("Eligible Colleges")

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
                create_branch_distribution_chart(result)
