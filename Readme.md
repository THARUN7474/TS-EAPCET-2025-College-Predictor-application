# TS EAMCET 2025 College Predictor

![TS EAMCET Logo](https://via.placeholder.com/800x200?text=TS+EAMCET+2025+College+Predictor)

A comprehensive web application to help students predict their college admission chances based on TS EAMCET 2025 rank, built with Streamlit. A web-based application built with Streamlit to predict eligible colleges based on TS EAMCET 2024 cutoff ranks. Users can input their rank, gender, caste, branch, and phase to find suitable colleges, compare cutoffs across phases, and analyze branch competitiveness.

## Demo

Live Demo: [TS EAMCET College Predictor](https://your-deployment-link-here.com)

![Application Screenshot](https://via.placeholder.com/800x450?text=Application+Screenshot)


## Features

- **College Predictor**: Find colleges based on EAMCET rank, gender, caste, branch, phase, and district.
- **Phase Comparison**: Compare cutoff ranks across 1st, 2nd, and Final phases.
- **Branch Analysis**: Visualize median cutoff ranks for different branches.
- **Interactive UI**: User-friendly interface with tabs, filters, and downloadable results.
- **District Filtering**: Narrow down colleges by district.
- **Data Visualization**: Bar charts for college distribution and branch analysis.

### 1. College Predictor
- Input your TS EAMCET rank, gender, caste, and preferred branch
- Filter colleges by district
- View colleges where you're eligible based on previous year's cutoffs
- Download results as CSV
- Visual representation of college distribution by district

### 2. Phase Comparison
- Compare how cutoffs change across counseling phases (1st Phase, 2nd Phase, Final Phase)
- Understand how waiting for later rounds might improve your options
- View top colleges for each phase side by side

### 3. Branch Analysis
- Analyze cutoff trends across different engineering branches
- Compare competitiveness of branches for your category
- Get insights on most/least competitive branches
- Visual representation of median cutoff ranks by branch

### 4. College-wise Branch Analysis
- See all available branches and their cutoffs for a specific college
- Compare branch competitiveness within the same institution
- Visual comparison of branch cutoffs
- Get insights on rank range and branch difficulty

### 5. Top 20 Colleges Guide
- Information about the top 20 engineering colleges in Telangana
- Details about college strengths and specialties
- Based on market trends, placement records, and reputation

## How It Works

The application uses TS EAMCET 2024 counseling data to predict college admission chances for 2025. By analyzing historical cutoff trends across different categories (OC, BC, SC, ST, EWS) and phases, the predictor offers personalized recommendations based on your rank and preferences.

## Installation and Usage

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/THARUN7474/TS-EAPCET-2025-College-Predictor-application.git
cd TS-EAPCET-2025-College-Predictor-application
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Access the application in your browser at `http://localhost:8501`

### Data Structure

The application expects data files in the following structure:
```
./Data/
  ├── 01_TGEAPCET_2024_FirstPhase.csv
  ├── 02_TGEAPCET_2024_SecondPhase.csv
  └── 03_TGEAPCET_2024_FinalPhase.csv
```

Each CSV should contain columns for college information, branch details, and cutoff ranks for all categories.

## Understanding Results

- **Closing Rank**: The last rank that received admission in that college/branch in 2024
- **Eligibility**: If your rank is equal to or better (lower number) than the closing rank, you're likely eligible

## Important Notes

- This tool uses historical data from TS EAMCET 2024
- Actual 2025 cutoffs may vary based on seat availability, applicant numbers, etc.
- Always verify information with official TS EAMCET counseling notifications
- Special category seats (Sports, PH, CAP, etc.) have different cutoffs not reflected in this tool

## For Developers

### File Structure
```
├── app.py                 # Main application file
├── Data/                  # Directory containing counseling data
│   ├── FirstPhase.csv
│   ├── SecondPhase.csv
│   └── FinalPhase.csv
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

### Key Functions

- `load_data()`: Loads and cleans data based on selected phase
- `predict_colleges()`: Filters colleges based on user input
- `compare_phases()`: Compares college options across different phases
- `get_college_branches()`: Gets all branches for a specific college
- `get_top_colleges()`: Returns information about top colleges

### Extending the Application

You can extend the application by:
1. Adding more data years for historical trend analysis
2. Implementing ML-based prediction for upcoming year cutoffs
3. Adding placement statistics for colleges and branches
4. Creating a personalized recommendation engine

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments

- TS EAMCET counseling data from official sources
- Streamlit for the interactive web framework
- All contributors who have helped improve this tool

## Contact

Tharun - [GitHub Profile](https://github.com/THARUN7474)

Project Link: [https://github.com/THARUN7474/TS-EAPCET-2025-College-Predictor-application](https://github.com/THARUN7474/TS-EAPCET-2025-College-Predictor-application)
