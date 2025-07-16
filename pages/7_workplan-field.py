import streamlit as st
import pandas as pd
import os
from io import StringIO
from typing import Tuple, Dict, List
import datetime

# --- Constants and Fallback Data ---
# Ensure these file paths are correct relative to your script's location
EXCEL_FILE_PATH = "KSHEERSAGAR LTD File.xlsx"
GOVIND_FILE_PATH = "GovindCompiledReport_June.xlsx" # New Constant
SDDPL_FILE_PATH = "SDDPLCompiledReport_June.xlsx"   # New Constant

FARMER_IDENTIFIER = "Farmer"
BMC_IDENTIFIER = "BMC"
FIELD_TEAM_IDENTIFIER = "FieldTeam"
TRAINING_IDENTIFIER = "Training"

FALLBACK_FARMERS_CSV = """
Farmer_ID,Farmer_Name,Village,District,BMC_ID,Milk_Production_Liters_Daily,Cattle_Count,Women_Empowerment_Flag,Animal_Welfare_Score
F001,Rajesh Kumar,Nandgaon,Pune,BMC001,15,5,No,4
F002,Priya Sharma,Lonikand,Pune,BMC002,22,8,Yes,5
F003,Amit Singh,Shirur,Pune,BMC001,18,6,No,3
"""
FALLBACK_BMCS_CSV = """
BMC_ID,BMC_Name,District,Capacity_Liters,Daily_Collection_Liters,Quality_Fat_Percentage,Quality_SNF_Percentage,Quality_Adulteration_Flag,Quality_Target_Fat,Quality_Target_SNF,Utilization_Target_Percentage,Animal_Welfare_Compliance_Score_BMC,Women_Empowerment_Participation_Rate_BMC,Date
BMC001,Nandgaon BMC,Pune,1000,750,3.5,8.0,No,3.8,8.2,80,4.0,50,2025-07-15
BMC002,Lonikand BMC,Pune,1200,800,3.2,7.8,Yes,3.8,8.2,80,4.5,70,2025-07-15
BMC003,Daund BMC,Pune,800,700,3.9,8.1,No,3.8,8.2,80,4.2,60,2025-07-15
"""
FALLBACK_FIELD_TEAMS_CSV = """
Team_ID,Team_Leader,District_Coverage,Max_BMC_Coverage,Training_Type,Training_Date,BMC_ID_Trained,Farmer_ID_Trained,Training_Outcome_Score
FT001,Ravi Kumar,Pune,5,Quality Improvement,2025-06-01,BMC001,,85
"""

FALLBACK_TRAINING_DATA = """
Training_Topic,Aug'23,Sep'23,Oct'23,Nov'23,Dec'23,Jan'24,Feb'24,Mar'24,Apr'24,May'24,Jun'24,Jul'24,Aug'24,Sep'24,Oct'24,Nov'24,Dec'24,Sum_Till_Date
Farmer's Training on AW (25 mins),92,31,15,19,11,17,17,6,17,17,21,28,20,15,20,17,17,380
Women Farmer's Training on Dairy Business (25 mins),73,32,30,16,16,41,42,14,43,43,66,58,56,42,42,63,93,770
Farmer's Training on Breeding and Nutrition (25 mins),83,31,15,40,43,71,46,18,48,54,82,81,94,54,63,70,70,963
Farmer's Training on Clean Milk Prod. (25 mins),107,67,41,65,52,66,42,18,60,71,92,88,91,81,97,76,74,1188
Farmer's Training on AW (25 mins) (Women),7,22,34,18,28,23,17,6,14,16,28,18,11,18,29,13,28,330
Women Farmer's Training on Dairy Business (25 mins) (Women),6,20,32,15,28,18,13,5,14,12,22,16,9,15,25,10,23,283
Farmer's Training on Breeding and Nutrition (25 mins) (Women),6,24,36,18,28,23,17,6,18,16,27,19,12,18,29,13,24,334
Farmer's Training on CMP (25 mins) (Women),7,24,35,18,28,23,18,6,5,10,28,17,12,19,29,13,28,320
"""

SUMMARY_DATA = """
Training_Topic,Jan'24,Feb'24,Mar'24,Apr'24,May'24,Jun'24,Jul'24,Aug'24,Sep'24,Oct'24,Nov'24,Dec'24,Total_Training,No_of_Farmers
Farmer's Training on AW (25 mins),40,34,12,31,33,49,46,31,33,49,30,45,433,3464
Women Farmer's Training on Dairy Business (25 mins),120,101,68,119,123,94,135,122,125,138,112,124,1381,11048
Farmer's Training on Breeding and Nutrition (25 mins),94,63,24,66,70,109,100,106,72,92,83,94,973,7784
Farmer's Training on CMP (25 mins),89,60,24,65,81,120,105,103,100,126,89,102,1064,8512
Total,343,258,128,281,307,372,386,362,330,405,314,365,3851,30808
"""

# --- Workplan specific constants and data storage ---
WORKPLAN_FILE_PATH = "daily_workplans.csv"

# --- UPDATED: Admin Authorized Emails ---
AUTHORIZED_ADMIN_EMAILS = [
    "mkaushal@tns.org",
    "rsomanchi@tns.org",
    "ksuneha@tns.org",
    "shifalis@tns.org"
]

FIELD_TEAM_MEMBERS = [
    "Dr. Sachin Wadapalliwar",
    "Bhushan Sananse",
    "Nilesh Dhanwate",
    "Subhrat",
    "Aniket Govenkar",
]

ACTIVITIES = [
    "Monitoring and evaluation of farms and BMCs",
    "Training: DEOs, QIs, MPOs, BCF and Lead Farmers",
    "Assessment: KS 1.0 Endline and KS 2.0 Baseline",
    "Governance: Weekly/Monthly",
]

st.set_page_config(layout="wide")


# --- New Data Loading Functions for Govind and SDDPL ---

@st.cache_data(show_spinner="Loading Govind BMC data...")
def load_govind_bmc_data() -> pd.DataFrame:
    """Loads and processes Govind BMC data."""
    try:
        govind_df = pd.read_excel(GOVIND_FILE_PATH)
        # Rename columns to a standardized format (or create new ones)
        govind_df.rename(columns={
            'BMC Code': 'BMC_ID',
            'MCC Name': 'BMC_Name',
            'Milk Qty. (LTR)': 'Daily_Collection_Liters',
            'Utilization': 'Utilization_Percentage_Calculated', # This is already a percentage in Govind
            'FAT': 'Quality_Fat_Percentage',
            'CLR': 'Quality_CLR_Percentage', # New column
            'SNF': 'Quality_SNF_Percentage',
            'Antibiotic Positive Qty': 'Quality_AB_Positive', # Assuming a measure of positive tests
            'Sulpha': 'Quality_Sulpha',
            'Beta': 'Quality_Beta', # Assuming Beta is MBRP in this context based on typical dairy tests
            'Capa': 'Quality_Capa',
            'Afla': 'Quality_Aflatoxins',
            'Date': 'Date'
        }, inplace=True)
        
        # Add 'District' column if available or set a default/placeholder
        if 'District' not in govind_df.columns:
            govind_df['District'] = 'Unknown' # Placeholder, adjust if district can be derived
        
        # Add a source column
        govind_df['Source'] = 'Govind'

        # Convert relevant columns to numeric, coercing errors to NaN
        numeric_cols = ['Daily_Collection_Liters', 'Utilization_Percentage_Calculated', 
                        'Quality_Fat_Percentage', 'Quality_CLR_Percentage', 'Quality_SNF_Percentage',
                        'Quality_AB_Positive', 'Quality_Sulpha', 'Quality_Beta', 
                        'Quality_Capa', 'Quality_Aflatoxins']
        for col in numeric_cols:
            govind_df[col] = pd.to_numeric(govind_df[col], errors='coerce')
            
        # Convert date column
        govind_df['Date'] = pd.to_datetime(govind_df['Date'], errors='coerce')
        
        # Ensure BMC_ID is string
        govind_df['BMC_ID'] = govind_df['BMC_ID'].astype(str)

        st.success("Govind BMC data loaded!")
        return govind_df
    except FileNotFoundError:
        st.warning(f"Govind BMC file not found: {GOVIND_FILE_PATH}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading Govind BMC data: {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner="Loading SDDPL BMC data...")
def load_sddpl_bmc_data() -> pd.DataFrame:
    """Loads and processes SDDPL BMC data."""
    try:
        sddpl_df = pd.read_excel(SDDPL_FILE_PATH)
        # Rename columns to a standardized format
        sddpl_df.rename(columns={
            'BMC': 'BMC_ID',
            'Area': 'District', # Assuming Area maps to District
            'Total Milk': 'Daily_Collection_Liters',
            'Alcohol Positive': 'Quality_Alcohol_Positive',
            'AB Positive Milk': 'Quality_AB_Positive',
            'AFM1 Positive': 'Quality_Aflatoxins', # Assuming AFM1 refers to Aflatoxins
            '4IN1 STRIP': 'Quality_MBRP', # Assuming 4IN1 STRIP refers to MBRP
            'Date': 'Date'
        }, inplace=True)

        # Add placeholder columns if they don't exist in SDDPL but are needed for common BMC DF
        # Initialize with pd.NA and then fill as appropriate
        common_cols = ['BMC_Name', 'Capacity_Liters', 'Utilization_Percentage_Calculated', 
                        'Quality_Fat_Percentage', 'Quality_SNF_Percentage', 'Quality_Adulteration_Flag',
                        'Quality_CLR_Percentage', 'Quality_Sulpha', 'Quality_Beta', 'Quality_Capa']
        for col in common_cols:
            if col not in sddpl_df.columns:
                sddpl_df[col] = pd.NA # Use pd.NA for missing values

        # Fill specific SDDPL quality metrics if they are available
        if 'BTS & CAP Negative Milk' in sddpl_df.columns:
            # You might derive a positive/negative flag from this. Assuming if >0, it's 'No' adulteration.
            # Otherwise, consider 'Yes' if the value is 0 or NaN, indicating an issue.
            sddpl_df['Quality_Adulteration_Flag'] = sddpl_df['BTS & CAP Negative Milk'].apply(lambda x: 'No' if pd.notna(x) and x > 0 else 'Yes')
        
        # Add a source column
        sddpl_df['Source'] = 'SDDPL'

        # Convert relevant columns to numeric, coercing errors to NaN
        numeric_cols = ['Daily_Collection_Liters', 'Quality_Alcohol_Positive', 
                        'Quality_AB_Positive', 'Quality_Aflatoxins', 'Quality_MBRP']
        for col in numeric_cols:
            sddpl_df[col] = pd.to_numeric(sddpl_df[col], errors='coerce')
        
        # Convert date column
        sddpl_df['Date'] = pd.to_datetime(sddpl_df['Date'], errors='coerce')
        
        # Ensure BMC_ID is string
        sddpl_df['BMC_ID'] = sddpl_df['BMC_ID'].astype(str)


        st.success("SDDPL BMC data loaded!")
        return sddpl_df
    except FileNotFoundError:
        st.warning(f"SDDPL BMC file not found: {SDDPL_FILE_PATH}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading SDDPL BMC data: {e}")
        return pd.DataFrame()


# --- Existing Data Loading Function (MODIFIED) ---
@st.cache_data(show_spinner="Loading Ksheersagar data...")
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Attempts to load data from Excel files and combine BMC data,
    then falls back to embedded dummy CSV data.
    """
    farmer_df = pd.DataFrame()
    bmc_df = pd.DataFrame()
    field_team_df = pd.DataFrame()
    training_df = pd.DataFrame()
    summary_df = pd.DataFrame()

    try:
        # Load BMC data from Ksheersagar file if available
        if os.path.exists(EXCEL_FILE_PATH):
            all_data_df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None)
            
            farmer_sheet_name = None
            bmc_sheet_name = None
            field_team_sheet_name = None
            training_sheet_name = None
            
            for sheet_name, df_sheet in all_data_df.items():
                if any(FARMER_IDENTIFIER.lower() in str(col).lower() for col in df_sheet.columns):
                    farmer_sheet_name = sheet_name
                if any(BMC_IDENTIFIER.lower() in str(col).lower() for col in df_sheet.columns):
                    bmc_sheet_name = sheet_name
                if any(FIELD_TEAM_IDENTIFIER.lower() in str(col).lower() for col in df_sheet.columns):
                    field_team_sheet_name = sheet_name
                if any(TRAINING_IDENTIFIER.lower() in str(col).lower() for col in df_sheet.columns):
                    training_sheet_name = sheet_name
            
            farmer_df = all_data_df.get(farmer_sheet_name, pd.DataFrame())
            bmc_df = all_data_df.get(bmc_sheet_name, pd.DataFrame())
            field_team_df = all_data_df.get(field_team_sheet_name, pd.DataFrame())
            training_df = all_data_df.get(training_sheet_name, pd.DataFrame())
            
            if training_sheet_name:
                if 'Total_Training' in all_data_df[training_sheet_name].columns and 'No_of_Farmers' in all_data_df[training_sheet_name].columns:
                    summary_df = all_data_df[training_sheet_name]
            
            st.success("Ksheersagar data loaded!")
            
        # Load Govind and SDDPL BMC data
        govind_bmc_df = load_govind_bmc_data()
        sddpl_bmc_df = load_sddpl_bmc_data()

        # Combine all BMC dataframes
        # Identify all unique columns across all BMC dataframes to ensure consistent columns for concat
        all_bmc_cols = set(bmc_df.columns).union(set(govind_bmc_df.columns)).union(set(sddpl_bmc_df.columns))

        # Reindex each DataFrame to have all common columns, filling missing with pd.NA
        # This step is crucial to prevent Pandas from coercing mixed types (e.g., bool/int to object)
        # and to ensure proper alignment during concatenation.
        for df_in_list in [bmc_df, govind_bmc_df, sddpl_bmc_df]:
            for col in all_bmc_cols:
                if col not in df_in_list.columns:
                    df_in_list[col] = pd.NA 
            # Reorder columns to match 'all_bmc_cols' set for consistent schema
            df_in_list = df_in_list[list(all_bmc_cols)] 

        # Ensure 'Date' column is datetime before concatenation for proper sorting and latest entry selection
        for df_in_list in [bmc_df, govind_bmc_df, sddpl_bmc_df]:
            if 'Date' in df_in_list.columns:
                df_in_list['Date'] = pd.to_datetime(df_in_list['Date'], errors='coerce')

        # Concatenate all BMC data.
        combined_bmc_df = pd.concat([bmc_df, govind_bmc_df, sddpl_bmc_df], ignore_index=True)
        
        # Drop duplicates, keeping the latest entry for each BMC_ID based on 'Date'
        # Convert BMC_ID to string before dropping duplicates to ensure consistent type
        combined_bmc_df['BMC_ID'] = combined_bmc_df['BMC_ID'].astype(str)
        if 'Date' in combined_bmc_df.columns:
            # Sort by Date descending to keep the latest
            bmc_df = combined_bmc_df.sort_values(by='Date', ascending=False).drop_duplicates(subset='BMC_ID', keep='first')
        else:
            # If no date column, just drop duplicates based on BMC_ID
            bmc_df = combined_bmc_df.drop_duplicates(subset='BMC_ID', keep='first')
        

        return farmer_df, bmc_df, field_team_df, training_df, summary_df

    except Exception as e:
        st.error(f"Error loading and combining data from Excel files: {e}. Falling back to dummy data.")
        # Fallback to dummy data in case of any loading/processing error with real files
        try:
            farmer_df = pd.read_csv(StringIO(FALLBACK_FARMERS_CSV))
            bmc_df = pd.read_csv(StringIO(FALLBACK_BMCS_CSV))
            field_team_df = pd.read_csv(StringIO(FALLBACK_FIELD_TEAMS_CSV))
            training_df = pd.read_csv(StringIO(FALLBACK_TRAINING_DATA))
            summary_df = pd.read_csv(StringIO(SUMMARY_DATA))
            st.warning("Could not load real data; using fallback dummy data.")
            return farmer_df, bmc_df, field_team_df, training_df, summary_df
        except Exception as e_fallback:
            st.error(f"Critical error: Could not load even fallback dummy data. Error: {e_fallback}")
            st.stop()


# --- Workplan Data Handling Functions ---
def load_workplans() -> pd.DataFrame:
    """Loads daily workplans from a CSV file."""
    if os.path.exists(WORKPLAN_FILE_PATH):
        try:
            df = pd.read_csv(WORKPLAN_FILE_PATH)
            # Ensure 'Date' column is datetime
            df['Date'] = pd.to_datetime(df['Date']).dt.date # Store as date only
            return df
        except Exception as e:
            st.error(f"Error loading workplans: {e}")
            return pd.DataFrame(columns=['Date', 'Field Team Member', 'Activity', 'Target', 'Achieved'])
    return pd.DataFrame(columns=['Date', 'Field Team Member', 'Activity', 'Target', 'Achieved'])

def save_workplans(df: pd.DataFrame):
    """Saves daily workplans to a CSV file."""
    try:
        df.to_csv(WORKPLAN_FILE_PATH, index=False)
        st.success("Workplan saved successfully!")
    except Exception as e:
        st.error(f"Error saving workplan: {e}")

def get_admin_status():
    """Checks admin status based on session state."""
    return st.session_state.get('is_admin', False)

# --- Existing Analysis and Target Generation Functions (MODIFIED) ---
def analyze_bmcs(bmc_df: pd.DataFrame, farmer_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Analyzes BMC data against KPIs and identifies low-performing BMCs.
    Returns a dictionary of low-performing BMCs for each KPI.
    """
    if 'Date' in bmc_df.columns:
        bmc_df['Date'] = pd.to_datetime(bmc_df['Date'])
        # Get the latest entry for each BMC_ID
        latest_bmc_df = bmc_df.loc[bmc_df.groupby('BMC_ID')['Date'].idxmax()].copy() # .copy() to avoid SettingWithCopyWarning
    else:
        latest_bmc_df = bmc_df.copy()

    low_performing_bmcs = {
        'Volume': pd.DataFrame(), # New KPI for Volume
        'Utilization': pd.DataFrame(),
        'Quality_General': pd.DataFrame(), # General quality issues (Fat, SNF, Adulteration)
        'Quality_Alcohol': pd.DataFrame(),
        'Quality_MBRP': pd.DataFrame(),
        'Quality_Aflatoxins': pd.DataFrame(),
        'Quality_AB_Positive': pd.DataFrame(),
        'Quality_Sulpha': pd.DataFrame(),
        'Quality_Capa': pd.DataFrame(),
        'Animal_Welfare': pd.DataFrame(),
        'Women_Empowerment': pd.DataFrame()
    }

    # --- KPI THRESHOLDS (Adjust as needed) ---
    QUALITY_FAT_THRESHOLD = 3.5
    QUALITY_SNF_THRESHOLD = 7.8
    UTILIZATION_THRESHOLD = 70.0
    ANIMAL_WELFARE_THRESHOLD = 4.0
    WOMEN_EMPOWERMENT_THRESHOLD = 55.0
    VOLUME_THRESHOLD_LITERS = 500 # Example: BMCs collecting less than 500 liters daily
    
    # Quality specific thresholds (assuming 0 for negative results indicates good, >0 indicates issue)
    QUALITY_AB_POSITIVE_THRESHOLD = 0.0 # No positive tests allowed
    QUALITY_SULPHA_THRESHOLD = 0.0
    QUALITY_BETA_MBRP_THRESHOLD = 0.0 # Beta is used for MBRP in Govind, MBRP for SDDPL
    QUALITY_CAPA_THRESHOLD = 0.0
    QUALITY_AFLATOXINS_THRESHOLD = 0.0 # Often ppm or ppb, 0 indicates no detection
    QUALITY_ALCOHOL_POSITIVE_THRESHOLD = 0.0 # Often a flag (0 or 1), or a value

    # --- Volume Analysis ---
    if 'Daily_Collection_Liters' in latest_bmc_df.columns:
        # Ensure column is numeric before comparison
        latest_bmc_df['Daily_Collection_Liters'] = pd.to_numeric(latest_bmc_df['Daily_Collection_Liters'], errors='coerce')
        low_volume_bmcs = latest_bmc_df[latest_bmc_df['Daily_Collection_Liters'] < VOLUME_THRESHOLD_LITERS]
        if not low_volume_bmcs.empty:
            low_performing_bmcs['Volume'] = low_volume_bmcs.copy()
            low_performing_bmcs['Volume']['Reason'] = 'Low Milk Volume'

    # --- Utilization Analysis ---
    if 'Daily_Collection_Liters' in latest_bmc_df.columns and 'Capacity_Liters' in latest_bmc_df.columns:
        # Ensure columns are numeric
        latest_bmc_df['Daily_Collection_Liters'] = pd.to_numeric(latest_bmc_df['Daily_Collection_Liters'], errors='coerce')
        latest_bmc_df['Capacity_Liters'] = pd.to_numeric(latest_bmc_df['Capacity_Liters'], errors='coerce')

        # Calculate Utilization_Percentage_Calculated if not present or explicitly from Govind's 'Utilization'
        # Handle division by zero for Capacity_Liters
        latest_bmc_df['Calculated_Utilization'] = (
            latest_bmc_df['Daily_Collection_Liters'] / 
            latest_bmc_df['Capacity_Liters'].replace(0, pd.NA) # Replace 0 capacity with NA to avoid ZeroDivisionError
        ) * 100
        
        # Prefer the provided Utilization_Percentage_Calculated if it exists and is not NA
        # Otherwise, use the newly calculated one
        latest_bmc_df['Effective_Utilization'] = latest_bmc_df['Utilization_Percentage_Calculated'].fillna(
                                                 latest_bmc_df['Calculated_Utilization'])
        
        low_util_bmcs = latest_bmc_df[latest_bmc_df['Effective_Utilization'] < UTILIZATION_THRESHOLD]
        if not low_util_bmcs.empty:
            low_performing_bmcs['Utilization'] = low_util_bmcs.copy()
            low_performing_bmcs['Utilization']['Reason'] = 'Low Utilization'


    # --- Quality Analysis (General: Fat, SNF, Adulteration) ---
    low_quality_fat = pd.DataFrame()
    if 'Quality_Fat_Percentage' in latest_bmc_df.columns:
        latest_bmc_df['Quality_Fat_Percentage'] = pd.to_numeric(latest_bmc_df['Quality_Fat_Percentage'], errors='coerce')
        low_quality_fat = latest_bmc_df[latest_bmc_df['Quality_Fat_Percentage'] < QUALITY_FAT_THRESHOLD] 
    
    low_quality_snf = pd.DataFrame()
    if 'Quality_SNF_Percentage' in latest_bmc_df.columns:
        latest_bmc_df['Quality_SNF_Percentage'] = pd.to_numeric(latest_bmc_df['Quality_SNF_Percentage'], errors='coerce')
        low_quality_snf = latest_bmc_df[latest_bmc_df['Quality_SNF_Percentage'] < QUALITY_SNF_THRESHOLD] 
    
    adulteration_issues = pd.DataFrame()
    if 'Quality_Adulteration_Flag' in latest_bmc_df.columns:
        adulteration_issues = latest_bmc_df[latest_bmc_df['Quality_Adulteration_Flag'].astype(str).str.lower() == 'yes'] 

    general_quality_issues = pd.concat([low_quality_fat, low_quality_snf, adulteration_issues]).drop_duplicates(subset=['BMC_ID'])
    if not general_quality_issues.empty:
        low_performing_bmcs['Quality_General'] = general_quality_issues
        low_performing_bmcs['Quality_General']['Reason'] = 'Low Fat/SNF or Adulteration'

    # --- New Quality Analysis (Alcohol/MBRP/Aflatoxins/AB Positive/Sulfa/Capa) ---
    if 'Quality_Alcohol_Positive' in latest_bmc_df.columns:
        latest_bmc_df['Quality_Alcohol_Positive'] = pd.to_numeric(latest_bmc_df['Quality_Alcohol_Positive'], errors='coerce')
        low_alcohol = latest_bmc_df[latest_bmc_df['Quality_Alcohol_Positive'] > QUALITY_ALCOHOL_POSITIVE_THRESHOLD].copy()
        if not low_alcohol.empty:
            low_performing_bmcs['Quality_Alcohol'] = low_alcohol
            low_performing_bmcs['Quality_Alcohol']['Reason'] = 'Alcohol Positive'

    # MBRP (Beta from Govind, 4IN1 STRIP from SDDPL)
    mbrp_issues = pd.DataFrame()
    if 'Quality_Beta' in latest_bmc_df.columns: # From Govind
        latest_bmc_df['Quality_Beta'] = pd.to_numeric(latest_bmc_df['Quality_Beta'], errors='coerce')
        mbrp_issues = pd.concat([mbrp_issues, latest_bmc_df[latest_bmc_df['Quality_Beta'] > QUALITY_BETA_MBRP_THRESHOLD].copy()])
    if 'Quality_MBRP' in latest_bmc_df.columns: # From SDDPL
        latest_bmc_df['Quality_MBRP'] = pd.to_numeric(latest_bmc_df['Quality_MBRP'], errors='coerce')
        mbrp_issues = pd.concat([mbrp_issues, latest_bmc_df[latest_bmc_df['Quality_MBRP'] > QUALITY_BETA_MBRP_THRESHOLD].copy()])
    if not mbrp_issues.empty:
        low_performing_bmcs['Quality_MBRP'] = mbrp_issues.drop_duplicates(subset=['BMC_ID'])
        low_performing_bmcs['Quality_MBRP']['Reason'] = 'MBRP Positive'

    if 'Quality_Aflatoxins' in latest_bmc_df.columns:
        latest_bmc_df['Quality_Aflatoxins'] = pd.to_numeric(latest_bmc_df['Quality_Aflatoxins'], errors='coerce')
        low_aflatoxins = latest_bmc_df[latest_bmc_df['Quality_Aflatoxins'] > QUALITY_AFLATOXINS_THRESHOLD].copy()
        if not low_aflatoxins.empty:
            low_performing_bmcs['Quality_Aflatoxins'] = low_aflatoxins
            low_performing_bmcs['Quality_Aflatoxins']['Reason'] = 'Aflatoxins Positive'

    if 'Quality_AB_Positive' in latest_bmc_df.columns:
        latest_bmc_df['Quality_AB_Positive'] = pd.to_numeric(latest_bmc_df['Quality_AB_Positive'], errors='coerce')
        low_ab_positive = latest_bmc_df[latest_bmc_df['Quality_AB_Positive'] > QUALITY_AB_POSITIVE_THRESHOLD].copy()
        if not low_ab_positive.empty:
            low_performing_bmcs['Quality_AB_Positive'] = low_ab_positive
            low_performing_bmcs['Quality_AB_Positive']['Reason'] = 'Antibiotic Positive'

    if 'Quality_Sulpha' in latest_bmc_df.columns:
        latest_bmc_df['Quality_Sulpha'] = pd.to_numeric(latest_bmc_df['Quality_Sulpha'], errors='coerce')
        low_sulpha = latest_bmc_df[latest_bmc_df['Quality_Sulpha'] > QUALITY_SULPHA_THRESHOLD].copy()
        if not low_sulpha.empty:
            low_performing_bmcs['Quality_Sulpha'] = low_sulpha
            low_performing_bmcs['Quality_Sulpha']['Reason'] = 'Sulpha Positive'

    if 'Quality_Capa' in latest_bmc_df.columns:
        latest_bmc_df['Quality_Capa'] = pd.to_numeric(latest_bmc_df['Quality_Capa'], errors='coerce')
        low_capa = latest_bmc_df[latest_bmc_df['Quality_Capa'] > QUALITY_CAPA_THRESHOLD].copy()
        if not low_capa.empty:
            low_performing_bmcs['Quality_Capa'] = low_capa
            low_performing_bmcs['Quality_Capa']['Reason'] = 'Capa Positive'
            
    # --- Animal Welfare Analysis ---
    if 'Animal_Welfare_Compliance_Score_BMC' in latest_bmc_df.columns:
        latest_bmc_df['Animal_Welfare_Compliance_Score_BMC'] = pd.to_numeric(latest_bmc_df['Animal_Welfare_Compliance_Score_BMC'], errors='coerce')
        low_animal_welfare = latest_bmc_df[
            latest_bmc_df['Animal_Welfare_Compliance_Score_BMC'] < ANIMAL_WELFARE_THRESHOLD]
        if not low_animal_welfare.empty:
            low_performing_bmcs['Animal_Welfare'] = low_animal_welfare.copy()
            low_performing_bmcs['Animal_Welfare']['Reason'] = 'Low Animal Welfare Score'

    # --- Women Empowerment Analysis ---
    if 'Women_Empowerment_Participation_Rate_BMC' in latest_bmc_df.columns:
        latest_bmc_df['Women_Empowerment_Participation_Rate_BMC'] = pd.to_numeric(latest_bmc_df['Women_Empowerment_Participation_Rate_BMC'], errors='coerce')
        low_women_empowerment = latest_bmc_df[
            latest_bmc_df['Women_Empowerment_Participation_Rate_BMC'] < WOMEN_EMPOWERMENT_THRESHOLD]
        if not low_women_empowerment.empty:
            low_performing_bmcs['Women_Empowerment'] = low_women_empowerment.copy()
            low_performing_bmcs['Women_Empowerment']['Reason'] = 'Low Women Empowerment Rate'

    return low_performing_bmcs


def generate_actionable_targets(low_bmcs_dict: Dict[str, pd.DataFrame]) -> List[str]:
    """
    Generates actionable insights and suggested targets for low-performing BMCs.
    This is a simplified example. Real logic would be more complex.
    """
    action_items = []
    for kpi, df in low_bmcs_dict.items():
        if not df.empty:
            for index, row in df.iterrows():
                bmc_id = row['BMC_ID']
                bmc_name = row.get('BMC_Name', bmc_id) # Use name if available, else ID
                district = row.get('District', 'N/A')

                if kpi == 'Volume':
                    current_volume = row.get('Daily_Collection_Liters', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Low Milk Volume** ({current_volume} L). "
                        f"**Action:** Field team to assess local farmer engagement, improve milk procurement strategies, and optimize collection routes. "
                        f"**Target:** Increase daily collection by 15% within 2 months."
                    )
                elif kpi == 'Utilization':
                    current_util = row.get('Effective_Utilization', 'N/A') # Use Effective_Utilization
                    target_util = row.get('Utilization_Target_Percentage', '80')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Low Utilization** ({current_util:.2f}%). "
                        f"**Action:** Identify reasons for low collection, farmer mobilization campaigns, improve logistics and infrastructure utilization. "
                        f"**Target:** Increase utilization to {target_util}% (or +5% points) within 2 months."
                    )
                elif kpi == 'Quality_General':
                    current_fat = row.get('Quality_Fat_Percentage', 'N/A')
                    current_snf = row.get('Quality_SNF_Percentage', 'N/A')
                    adulteration = row.get('Quality_Adulteration_Flag', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **General Low Quality** (Fat: {current_fat}%, SNF: {current_snf}%, Adulteration: {adulteration}). "
                        f"**Action:** Field team to visit for comprehensive quality checks, farmer awareness on clean milk production, and proper testing protocols. "
                        f"**Target:** Increase Fat to >3.8% and SNF to >8.0%, and eliminate adulteration within 1 month."
                    )
                elif kpi == 'Quality_Alcohol':
                    current_value = row.get('Quality_Alcohol_Positive', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Alcohol Positive Milk Issues** (Value: {current_value}). "
                        f"**Action:** Immediate investigation into feed, water, and animal health for potential causes. Farmer training on avoiding fermentation and proper storage. "
                        f"**Target:** Eliminate alcohol positive results within 2 weeks."
                    )
                elif kpi == 'Quality_MBRP':
                    current_beta = row.get('Quality_Beta', 'N/A')
                    current_mbrp = row.get('Quality_MBRP', 'N/A')
                    value_str = f"Beta: {current_beta}, MBRP: {current_mbrp}" if current_beta != 'N/A' and current_mbrp != 'N/A' else str(current_beta if current_beta != 'N/A' else current_mbrp)
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **MBRP/Beta Positive Issues** (Values: {value_str}). "
                        f"**Action:** Focus on cleanliness, hygiene at farm level, and proper cooling of milk. Training on bacteria control. "
                        f"**Target:** Eliminate MBRP/Beta positive results within 2 weeks."
                    )
                elif kpi == 'Quality_Aflatoxins':
                    current_value = row.get('Quality_Aflatoxins', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Aflatoxins Positive Issues** (Value: {current_value}). "
                        f"**Action:** Urgent assessment of feed quality, storage conditions, and sourcing. Provide alternatives for contaminated feed. "
                        f"**Target:** Eliminate Aflatoxins positive results within 2 weeks."
                    )
                elif kpi == 'Quality_AB_Positive':
                    current_value = row.get('Quality_AB_Positive', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Antibiotic Positive Milk Issues** (Value: {current_value}). "
                        f"**Action:** Review animal health protocols, responsible antibiotic use, and milk withdrawal periods. Farmer education on proper veterinary practices. "
                        f"**Target:** Eliminate antibiotic positive results within 2 weeks."
                    )
                elif kpi == 'Quality_Sulpha':
                    current_value = row.get('Quality_Sulpha', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Sulpha Positive Issues** (Value: {current_value}). "
                        f"**Action:** Investigate potential sources of sulpha contamination, likely feed or incorrect medication practices. "
                        f"**Target:** Eliminate sulpha positive results within 2 weeks."
                    )
                elif kpi == 'Quality_Capa':
                    current_value = row.get('Quality_Capa', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Capa Positive Issues** (Value: {current_value}). "
                        f"**Action:** Address potential issues with cleaning agents, water quality, or external contaminants at the BMC or farm. "
                        f"**Target:** Eliminate Capa positive results within 2 weeks."
                    )
                elif kpi == 'Animal_Welfare':
                    current_score = row.get('Animal_Welfare_Compliance_Score_BMC', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Low Animal Welfare Score** ({current_score}). "
                        f"**Action:** Conduct farmer training on animal health, hygiene, proper housing, and ethical treatment. "
                        f"**Target:** Improve average animal welfare score to >4.5 within 3 months."
                    )
                elif kpi == 'Women_Empowerment':
                    current_rate = row.get('Women_Empowerment_Participation_Rate_BMC', 'N/A')
                    action_items.append(
                        f"BMC **{bmc_name}** ({bmc_id}, District: {district}) has **Low Women Empowerment Participation** ({current_rate:.2f}%). "
                        f"**Action:** Organize women's self-help group meetings, promote female farmer participation in dairy activities and decision-making. "
                        f"**Target:** Increase women empowerment participation rate to >65% within 3 months."
                    )
    return action_items


# --- Main Application Logic ---
# This is where the data is loaded and cached
farmer_df, bmc_df, field_team_df, training_df, summary_df = load_data()

# Initialize session state for workplans if not already present
if 'workplans_df' not in st.session_state:
    st.session_state.workplans_df = load_workplans()
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'admin_email_input' not in st.session_state:
    st.session_state.admin_email_input = ""


st.title("Ksheersagar Dairy Performance Dashboard & Workplan")
st.markdown("---")

# --- Admin Login Section ---
st.sidebar.header("Admin Login")
admin_email_input = st.sidebar.text_input("Enter your admin email", value=st.session_state.admin_email_input)

# Check if the input email is in the authorized list
if admin_email_input:
    st.session_state.admin_email_input = admin_email_input # Store in session state
    if admin_email_input.lower() in [email.lower() for email in AUTHORIZED_ADMIN_EMAILS]:
        st.session_state.is_admin = True
        st.sidebar.success(f"Admin access granted for {admin_email_input}!")
    else:
        st.session_state.is_admin = False
        st.sidebar.error("Unauthorized email address.")
else:
    st.session_state.is_admin = False


# --- Workplan Entry Section ---
st.header("Daily Workplan Entry")
st.markdown("---")

with st.form("daily_workplan_form"):
    col_date, col_member = st.columns(2)
    with col_date:
        workplan_date = st.date_input("Select Date", datetime.date.today())
    with col_member:
        selected_member = st.selectbox("Select Field Team Member", FIELD_TEAM_MEMBERS)

    st.subheader(f"Workplan for {selected_member} on {workplan_date.strftime('%Y-%m-%d')}")

    # Dictionary to store targets and achieved for each activity
    current_targets = {}
    current_achieved = {}

    for activity in ACTIVITIES:
        st.markdown(f"**{activity}**")
        col_target, col_achieved = st.columns(2)
        
        # Filter for existing data for this specific activity, member, and date
        existing_entry = st.session_state.workplans_df.loc[
            (st.session_state.workplans_df['Date'] == workplan_date) &
            (st.session_state.workplans_df['Field Team Member'] == selected_member) &
            (st.session_state.workplans_df['Activity'] == activity)
        ]

        with col_target:
            target_key = f"{selected_member}_{activity}_target_{workplan_date}"
            # Ensure default_target is an integer for number_input
            default_target = int(existing_entry['Target'].iloc[0]) if not existing_entry.empty and pd.notna(existing_entry['Target'].iloc[0]) else 0
            current_targets[activity] = st.number_input(f"Target for {activity}", min_value=0, value=default_target, key=target_key)
        
        with col_achieved:
            achieved_key = f"{selected_member}_{activity}_achieved_{workplan_date}"
            # Ensure default_achieved is an integer for number_input
            default_achieved = int(existing_entry['Achieved'].iloc[0]) if not existing_entry.empty and pd.notna(existing_entry['Achieved'].iloc[0]) else 0
            
            current_achieved[activity] = st.number_input(
                f"Achieved for {activity}",
                min_value=0,
                value=default_achieved,
                disabled=not get_admin_status(), # Disable if not admin
                key=achieved_key
            )
            if not get_admin_status():
                st.info("Admin login required to edit 'Achieved' values.")
    
    submitted = st.form_submit_button("Save Daily Workplan")
    if submitted:
        new_workplan_entries = []
        for activity in ACTIVITIES:
            new_workplan_entries.append({
                'Date': workplan_date,
                'Field Team Member': selected_member,
                'Activity': activity,
                'Target': current_targets[activity],
                'Achieved': current_achieved[activity]
            })
        
        new_workplan_df = pd.DataFrame(new_workplan_entries)

        # Remove existing entries for the selected member and date to update
        st.session_state.workplans_df = st.session_state.workplans_df[
            ~((st.session_state.workplans_df['Date'] == workplan_date) &
              (st.session_state.workplans_df['Field Team Member'] == selected_member))
        ]
        
        # Concatenate the updated/new entries
        st.session_state.workplans_df = pd.concat([st.session_state.workplans_df, new_workplan_df], ignore_index=True)
        save_workplans(st.session_state.workplans_df)
        st.rerun() # Rerun to refresh the display

st.markdown("---")
st.header("Workplan Tracking and Download")

# Filter and display workplans
display_date = st.date_input("View Workplans for Date", datetime.date.today(), key="display_date")

filtered_workplans = st.session_state.workplans_df[
    st.session_state.workplans_df['Date'] == display_date
].sort_values(by=['Field Team Member', 'Activity'])

if not filtered_workplans.empty:
    st.subheader(f"Workplans for {display_date.strftime('%Y-%m-%d')}")
    st.dataframe(filtered_workplans, use_container_width=True)
else:
    st.info(f"No workplans recorded for {display_date.strftime('%Y-%m-%d')}.")

# Download options
st.subheader("Download Workplan Data")

col_download_daily, col_download_weekly, col_download_monthly = st.columns(3)

with col_download_daily:
    st.download_button(
        label="Download Daily Workplans (CSV)",
        data=st.session_state.workplans_df.to_csv(index=False).encode('utf-8'),
        file_name="daily_workplans.csv",
        mime="text/csv",
    )

with col_download_weekly:
    st.markdown("#### Weekly Summary")
    selected_week = st.date_input("Select a date in the week for weekly download", datetime.date.today(), key="weekly_date")
    start_of_week = selected_week - datetime.timedelta(days=selected_week.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    
    weekly_data = st.session_state.workplans_df[
        (st.session_state.workplans_df['Date'] >= start_of_week) &
        (st.session_state.workplans_df['Date'] <= end_of_week)
    ]
    
    if not weekly_data.empty:
        weekly_summary = weekly_data.groupby(['Field Team Member', 'Activity']).agg(
            Total_Target=('Target', 'sum'),
            Total_Achieved=('Achieved', 'sum')
        ).reset_index()
        
        csv = weekly_summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Weekly Summary (CSV)",
            data=csv,
            file_name=f"weekly_workplan_summary_{start_of_week.strftime('%Y%m%d')}_to_{end_of_week.strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("No data for this week.")

with col_download_monthly:
    st.markdown("#### Monthly Summary")
    selected_month = st.date_input("Select a date in the month for monthly download", datetime.date.today(), key="monthly_date")
    
    # Ensure the 'Date' column is treated as datetime objects for month/year comparison
    monthly_data = st.session_state.workplans_df[
        (st.session_state.workplans_df['Date'].apply(lambda x: x.month) == selected_month.month) &
        (st.session_state.workplans_df['Date'].apply(lambda x: x.year) == selected_month.year)
    ]
    
    if not monthly_data.empty:
        monthly_summary = monthly_data.groupby(['Field Team Member', 'Activity']).agg(
            Total_Target=('Target', 'sum'),
            Total_Achieved=('Achieved', 'sum')
        ).reset_index()
        
        csv = monthly_summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Monthly Summary (CSV)",
            data=csv,
            file_name=f"monthly_workplan_summary_{selected_month.strftime('%Y%m')}.csv",
            mime="text/csv",
        )
    else:
        st.info("No data for this month.")

st.markdown("---")


# --- Existing Dashboard Sections ---
st.header("Training Performance")
st.markdown("---")

# --- Display Raw Tables ---
st.subheader("📊 Monthly Training Breakdown")
st.dataframe(training_df, use_container_width=True)

st.subheader("📈 Training Summary Totals")
st.dataframe(summary_df, use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    if st.checkbox("Show Total Trainings per Topic"):
        chart_data = summary_df.set_index("Training_Topic")["Total_Training"]
        st.bar_chart(chart_data)

with col2:
    if st.checkbox("Show Total Farmers Reached per Topic"):
        farmer_data = summary_df.set_index("Training_Topic")["No_of_Farmers"]
        st.bar_chart(farmer_data)


st.markdown("---")
st.header("Data Overview & KPI Analysis")

with st.expander("Show Raw Data Previews"):
    st.subheader("Farmer Data")
    st.dataframe(farmer_df.head())

    st.subheader("Combined BMC Data (including Govind & SDDPL)")
    # Display the BMC data after combining and deduplicating
    st.dataframe(bmc_df.head())
    st.write(f"Total BMC records loaded: {len(bmc_df)}")
    # Safely display sources, checking if the column exists
    st.write(f"BMC data sources: {bmc_df['Source'].unique().tolist() if 'Source' in bmc_df.columns else 'N/A'}")


    st.subheader("Field Team & Training Data")
    st.dataframe(field_team_df.head())

st.markdown("---")
st.header("KPI Performance Analysis")

# Call analyze_bmcs with the combined BMC data
low_performing_bmcs = analyze_bmcs(bmc_df, farmer_df)

if any(not df.empty for df in low_performing_bmcs.values()):
    st.subheader("Low Performing BMCs Identified:")
    for kpi, df in low_performing_bmcs.items():
        if not df.empty:
            st.write(f"#### {kpi.replace('_', ' ').title()} KPI Concerns:")
            # Define a base set of columns to display
            display_cols = ['BMC_ID', 'BMC_Name', 'District', 'Reason', 'Source']
            
            # Add specific columns based on the KPI
            if kpi == 'Volume':
                display_cols.append('Daily_Collection_Liters')
            elif kpi == 'Utilization':
                display_cols.append('Effective_Utilization')
            elif kpi == 'Quality_General':
                display_cols.extend(['Quality_Fat_Percentage', 'Quality_SNF_Percentage', 'Quality_Adulteration_Flag'])
            elif kpi == 'Quality_Alcohol':
                display_cols.append('Quality_Alcohol_Positive')
            elif kpi == 'Quality_MBRP':
                # Check for both possible column names
                if 'Quality_Beta' in df.columns:
                    display_cols.append('Quality_Beta')
                if 'Quality_MBRP' in df.columns:
                    display_cols.append('Quality_MBRP')
            elif kpi == 'Quality_Aflatoxins':
                display_cols.append('Quality_Aflatoxins')
            elif kpi == 'Quality_AB_Positive':
                display_cols.append('Quality_AB_Positive')
            elif kpi == 'Quality_Sulpha':
                display_cols.append('Quality_Sulpha')
            elif kpi == 'Quality_Capa':
                display_cols.append('Quality_Capa')
            elif kpi == 'Animal_Welfare':
                display_cols.append('Animal_Welfare_Compliance_Score_BMC')
            elif kpi == 'Women_Empowerment':
                display_cols.append('Women_Empowerment_Participation_Rate_BMC')

            # Filter display columns to only include those actually present in the DataFrame
            columns_to_show = [col for col in display_cols if col in df.columns]
            st.dataframe(df[columns_to_show].set_index('BMC_ID'))
            st.markdown("---")
else:
    st.success("All BMCs are performing well across the defined KPIs based on current data!")

st.header("Actionable Insights & Targets for Field Team")
action_items = generate_actionable_targets(low_performing_bmcs)

if action_items:
    for item in action_items:
        st.markdown(f"- {item}")
else:
    st.info("No specific actionable insights or targets to display as all BMCs are performing well.")
