"""
Constants and mappings used throughout the application.
"""

# Branch code to full name mapping
BRANCH_MAP = {
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

# Phase to file path mapping
PHASE_FILES = {
    "Final Phase": "./data/03_TGEAPCET_2024_FinalPhase.csv",
    "1st Phase": "./data/01_TGEAPCET_2024_FirstPhase.csv",
    "2nd Phase": "./data/02_TGEAPCET_2024_SecondPhase.csv"
}

# Caste mapping for column names


def get_caste_column_name(gender, caste):
    """
    Get the caste column name based on caste and gender.

    Args:
        caste (str): The caste category (OC, BC_A, etc.)
        gender (str): The gender (Male or Female)

    Returns:
        str: The column name in the dataset
    """
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

    if caste == 'EWS':
        return caste_map[caste]
    else:
        gender_suffix = 'BOYS' if gender == 'Male' else 'GIRLS'
        return f"{caste_map[caste]} {gender_suffix}"


# List of top colleges
TOP_COLLEGES = [
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
