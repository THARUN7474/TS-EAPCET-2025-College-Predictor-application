# TS EAMCET 2025 College Predictor

A web-based application built with Streamlit to predict eligible colleges based on TS EAMCET 2024 cutoff ranks. Users can input their rank, gender, caste, branch, and phase to find suitable colleges, compare cutoffs across phases, and analyze branch competitiveness.

## Features

- **College Predictor**: Find colleges based on EAMCET rank, gender, caste, branch, phase, and district.
- **Phase Comparison**: Compare cutoff ranks across 1st, 2nd, and Final phases.
- **Branch Analysis**: Visualize median cutoff ranks for different branches.
- **Interactive UI**: User-friendly interface with tabs, filters, and downloadable results.
- **District Filtering**: Narrow down colleges by district.
- **Data Visualization**: Bar charts for college distribution and branch analysis.

## Prerequisites

- Python 3.8+
- Streamlit
- Pandas
- A CSV file containing TS EAMCET 2024 cutoff data (e.g., 03_TGEAPCET_2024_FinalPhase.csv)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ts-eamcet-predictor.git
   cd ts-eamcet-predictor
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Place the TS EAMCET cutoff CSV files in the Data/ directory.
5. Run the application:

   ```bash
   streamlit run app.py
   ```

## Project Structure

```
ts-eamcet-predictor/
├── Data/                    # Directory for CSV data files
├── src/                     # Source code for modular components
│   ├── __init__.py
│   ├── data_loader.py       # Data loading and cleaning logic
│   ├── predictor.py         # College prediction logic
│   ├── ui_components.py     # Streamlit UI components
│   ├── constants.py         # Constants like branch mappings
├── app.py                   # Main application entry point
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── .gitignore               # Git ignore file
```

## Usage

1. Open the app in your browser (default: http://localhost:8501).
2. Use the **College Predictor** tab to input your details and find eligible colleges.
3. Use the **Phase Comparison** tab to compare cutoffs across phases.
4. Use the **Branch Analysis** tab to explore branch competitiveness.
5. Refer to the **Help** tab for guidance on using the tool.

## Deployment

To deploy on Streamlit Cloud or another platform:

1. Push your code to a GitHub repository.
2. Ensure requirements.txt lists all dependencies:

   ```
   streamlit
   pandas
   ```

3. Create a Streamlit Cloud account and connect your repository.
4. Specify app.py as the entry point and ensure the Data/ directory is included in the repository.
5. Deploy the app and access it via the provided URL.

## Contributing

1. Fork the repository.
2. Create a feature branch (git checkout -b feature/new-feature).
3. Commit changes (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature/new-feature).
5. Open a Pull Request.

## License

MIT License

## Notes

- The app uses historical TS EAMCET 2024 data. Actual 2025 cutoffs may vary.
- Ensure CSV files are correctly formatted and placed in the Data/ directory.
- For issues or feature requests, open a GitHub issue.
