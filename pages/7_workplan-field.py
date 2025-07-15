import streamlit as st
import pandas as pd
import os
from io import StringIO # Needed for fallback data

# --- Configuration ---
PROCESSED_DATA_DIR = "processed_data" # This directory must be in THIS repository
FARMERS_PARQUET_PATH = os.path.join(PROCESSED_DATA_DIR, "farmers.parquet")
BMCS_PARQUET_PATH = os.path.join(PROCESSED_DATA_DIR, "bmcs.parquet")
FIELD_TEAMS_PARQUET_PATH = os.path.join(PROCESSED_DATA_DIR, "field_teams.parquet")

# Set page configuration for wider layout
st.set_page_config(layout="wide")

# --- Fallback Dummy Data (Only used if processed_data is not found) ---
# This is a safety net so the app doesn't completely break during development/testing
# if the external data manager hasn't synced the files yet.
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


# --- Data Loading Function ---
@st.cache_data(show_spinner="Loading Ksheersagar data...")
def load_data():
    """
    Attempts to load data from pre-processed Parquet files.
    If not found, falls back to embedded dummy CSV data for testing.
    """
    # Check if processed data directory and files exist
    if (os.path.exists(FARMERS_PARQUET_PATH) and
        os.path.exists(BMCS_PARQUET_PATH) and
        os.path.exists(FIELD_TEAMS_PARQUET_PATH)):
        try:
            farmer_df = pd.read_parquet(FARMERS_PARQUET_PATH)
            bmc_df = pd.read_parquet(BMCS_PARQUET_PATH)
            field_team_df = pd.read_parquet(FIELD_TEAMS_PARQUET_PATH)
            st.success("Data loaded from Parquet files!")
            return farmer_df, bmc_df, field_team_df
        except Exception as e:
            st.error(f"Error loading data from Parquet files: {e}. Falling back to embedded dummy data.")
            # Fall through to load embedded data if Parquet fails
    else:
        st.warning("Processed Parquet data not found. Loading from embedded dummy data for prototype.")
        st.info("To use faster Parquet loading, please run `data_manager.py` locally and commit the `processed_data` folder to this repository.")


    # Fallback: Load from embedded CSV strings
    try:
        farmer_df = pd.read_csv(StringIO(FALLBACK_FARMERS_CSV))
        bmc_df = pd.read_csv(StringIO(FALLBACK_BMCS_CSV))
        field_team_df = pd.read_csv(StringIO(FALLBACK_FIELD_TEAMS_CSV))
        return farmer_df, bmc_df, field_team_df
    except Exception as e:
        st.error(f"Critical error: Could not load even fallback dummy data. Error: {e}")
        st.stop() # Stop the app if no data can be loaded


# --- KPI Calculation and Analysis Functions (remain the same) ---

def analyze_bmcs(bmc_df, farmer_df):
    """
    Analyzes BMC data against KPIs and identifies low-performing BMCs.
    Returns a dictionary of low-performing BMCs for each KPI.
    """
    # Ensure 'Date' column is datetime for filtering latest data
    if 'Date' in bmc_df.columns:
        bmc_df['Date'] = pd.to_datetime(bmc_df['Date'])
        # Get the latest data for each BMC
        latest_bmc_df = bmc_df.loc[bmc_df.groupby('BMC_ID')['Date'].idxmax()]
    else:
        latest_bmc_df = bmc_df.copy() # Use as is if no date column

    low_performing_bmcs = {
        'Quality': pd.DataFrame(),
        'Utilization': pd.DataFrame(),
        'Animal_Welfare': pd.DataFrame(),
        'Women_Empowerment': pd.DataFrame()
    }

    # --- KPI: Quality ---
    # Placeholder Thresholds - PLEASE ADJUST THESE VALUES BASED ON YOUR BUSINESS RULES
    QUALITY_FAT_THRESHOLD = 3.5
    QUALITY_SNF_THRESHOLD = 7.8

    low_quality_fat = latest_bmc_df[latest_bmc_df['Quality_Fat_Percentage'] < QUALITY_FAT_THRESHOLD]
    low_quality_snf = latest_bmc_df[latest_bmc_df['Quality_SNF_Percentage'] < QUALITY_SNF_THRESHOLD]
    adulteration_issues = latest_bmc_df[latest_bmc_df['Quality_Adulteration_Flag'].astype(str).str.lower() == 'yes']

    # Combine all quality issues
    low_performing_bmcs['Quality'] = pd.concat([low_quality_fat, low_quality_snf, adulteration_issues]).drop_duplicates(subset=['BMC_ID'])
    if not low_performing_bmcs['Quality'].empty:
        low_performing_bmcs['Quality']['Reason'] = 'Low Fat/SNF or Adulteration'


    # --- KPI: Utilization ---
    if 'Daily_Collection_Liters' in latest_bmc_df.columns and 'Capacity_Liters' in latest_bmc_df.columns:
        latest_bmc_df['Utilization_Percentage_Calculated'] = (latest_bmc_df['Daily_Collection_Liters'] / latest_bmc_df['Capacity_Liters']) * 100
        # Placeholder Threshold
        UTILIZATION_THRESHOLD = 70.0 # Below 70% is considered low
        low_performing_bmcs['Utilization'] = latest_bmc_df[latest_bmc_df['Utilization_Percentage_Calculated'] < UTILIZATION_THRESHOLD]
        if not low_performing_bmcs['Utilization'].empty:
            low_performing_bmcs['Utilization']['Reason'] = 'Low Utilization'

    # --- KPI: Animal Welfare Farms ---
    # Placeholder Threshold
    ANIMAL_WELFARE_THRESHOLD = 4.0 # Below 4.0 is considered low
    if 'Animal_Welfare_Compliance_Score_BMC' in latest_bmc_df.columns:
        low_performing_bmcs['Animal_Welfare'] = latest_bmc_df[latest_bmc_df['Animal_Welfare_Compliance_Score_BMC'] < ANIMAL_WELFARE_THRESHOLD]
        if not low_performing_bmcs['Animal_Welfare'].empty:
            low_performing_bmcs['Animal_Welfare']['Reason'] = 'Low Animal Welfare Score'

    # --- KPI: Women Empowerment ---
    # Placeholder Threshold
    WOMEN_EMPOWERMENT_THRESHOLD = 55.0 # Below 55% participation is considered low
    if 'Women_Empowerment_Participation_Rate_BMC' in latest_bmc_df.columns:
        low_performing_bmcs['Women_Empowerment'] = latest_bmc_df[latest_bmc_df['Women_Empowerment_Participation_Rate_BMC'] < WOMEN_EMPOWERMENT_THRESHOLD]
        if not low_performing_bmcs['Women_Empowerment'].empty:
            low_performing_bmcs['Women_Empowerment']['Reason'] = 'Low Women Empowerment Rate'

    return low_performing_bmcs


def generate_actionable_targets(low_bmcs_dict):
    """
    Generates actionable insights and suggested targets for low-performing BMCs.
    This is a simplified example. Real logic would be more complex.
    """
    action_items = []
    for kpi, df in low_bmcs_dict.items():
        if not df.empty:
            for index, row in df.iterrows():
                bmc_id = row['BMC_ID']
                district = row['District'] # Assuming District is always available

                if kpi == 'Quality':
                    current_fat = row.get('Quality_Fat_Percentage', 'N/A')
                    current_snf = row.get('Quality_SNF_Percentage', 'N/A')
                    adulteration = row.get('Quality_Adulteration_Flag', 'N/A')
                    action_items.append(
                        f"BMC {bmc_id} (District: {district}) has **Low Quality** (Fat: {current_fat}%, SNF: {current_snf}%, Adulteration: {adulteration}). "
                        f"**Action:** Field team to visit for quality checks, farmer awareness on clean milk production. "
                        f"**Target:** Increase Fat to >3.8% and SNF to >8.0% within 1 month."
                    )
                elif kpi == 'Utilization':
                    current_util = row.get('Utilization_Percentage_Calculated', 'N/A')
                    target_util = row.get('Utilization_Target_Percentage', '80') # Default for targets
                    action_items.append(
                        f"BMC {bmc_id} (District: {district}) has **Low Utilization** ({current_util:.2f}%). "
                        f"**Action:** Identify reasons for low collection, farmer mobilization, improve logistics. "
                        f"**Target:** Increase utilization to {target_util}% (or +5% points) within 2 months."
                    )
                elif kpi == 'Animal_Welfare':
                    current_score = row.get('Animal_Welfare_Compliance_Score_BMC', 'N/A')
                    action_items.append(
                        f"BMC {bmc_id} (District: {district}) has **Low Animal Welfare Score** ({current_score}). "
                        f"**Action:** Conduct farmer training on animal health, hygiene, and shelter. "
                        f"**Target:** Improve average animal welfare score to >4.5 within 3 months."
                    )
                elif kpi == 'Women_Empowerment':
                    current_rate = row.get('Women_Empowerment_Participation_Rate_BMC', 'N/A')
                    action_items.append(
                        f"BMC {bmc_id} (District: {district}) has **Low Women Empowerment Participation** ({current_rate:.2f}%). "
                        f"**Action:** Organize women's self-help group meetings, promote female farmer participation. "
                        f"**Target:** Increase women empowerment participation rate to >65% within 3 months."
                    )
    return action_items

# --- Load Data (The Page's Entry Point) ---
farmer_df, bmc_df, field_team_df = load_data()

# --- Streamlit Page Layout ---

st.title("Ksheersagar Dairy Performance Dashboard & Workplan")
st.markdown("---")

# Main content area
st.header("Data Overview & KPI Analysis")

# Display loaded dataframes (optional, for verification)
with st.expander("Show Raw Data Previews"):
    st.subheader("Farmer Data")
    st.dataframe(farmer_df.head())

    st.subheader("BMC Data")
    st.dataframe(bmc_df.head())

    st.subheader("Field Team & Training Data")
    st.dataframe(field_team_df.head())

st.markdown("---")
st.header("KPI Performance Analysis")

# Run analysis instantly
low_performing_bmcs = analyze_bmcs(bmc_df, farmer_df)

if any(not df.empty for df in low_performing_bmcs.values()):
    st.subheader("Low Performing BMCs Identified:")
    for kpi, df in low_performing_bmcs.items():
        if not df.empty:
            st.write(f"#### {kpi.replace('_', ' ').title()} KPI Concerns:")
            st.dataframe(df[['BMC_ID', 'BMC_Name', 'District', 'Reason']].set_index('BMC_ID'))
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
