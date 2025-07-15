import streamlit as st
import pandas as pd
import os
from io import StringIO  # Needed for fallback data
from typing import Tuple, Dict, List

# --- Configuration ---
# Excel File Configuration
EXCEL_FILE_PATH = "path/to/your/LTD_9Litres_per_day.xlsx"  # Replace with your actual path

# Identifiers for splitting the data (Adjust these based on your Excel structure)
FARMER_IDENTIFIER = "Farmer"  # Example:  If Farmer data has a column with "Farmer" in it
BMC_IDENTIFIER = "BMC"  # Example: If BMC data has a column with "BMC" in it
FIELD_TEAM_IDENTIFIER = "FieldTeam"  # Example: If Field Team data has a column with "FieldTeam" in it
TRAINING_IDENTIFIER = "Training" # Example: If Training data has a column with "Training" in it

# Fallback Dummy Data (Only used if Excel file is not found)
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

# Set page configuration for wider layout
st.set_page_config(layout="wide")

# --- Data Loading Function ---
@st.cache_data(show_spinner="Loading Ksheersagar data...")
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Attempts to load data from an Excel file and split it into DataFrames, then falls back to embedded dummy CSV data.
    """

    # 1. Try loading and splitting from the Excel file
    try:
        all_data_df = pd.read_excel(EXCEL_FILE_PATH)

        # --- Split the DataFrame based on identifiers ---
        farmer_df = all_data_df[all_data_df.apply(lambda row: any(str(FARMER_IDENTIFIER).lower() in str(x).lower() for x in row), axis=1)]
        bmc_df = all_data_df[all_data_df.apply(lambda row: any(str(BMC_IDENTIFIER).lower() in str(x).lower() for x in row), axis=1)]
        field_team_df = all_data_df[all_data_df.apply(lambda row: any(str(FIELD_TEAM_IDENTIFIER).lower() in str(x).lower() for x in row), axis=1)]
        training_df = all_data_df[all_data_df.apply(lambda row: any(str(TRAINING_IDENTIFIER).lower() in str(x).lower() for x in row), axis=1)]
        summary_df = all_data_df[all_data_df.apply(lambda row: any(str(TRAINING_IDENTIFIER).lower() in str(x).lower() for x in row), axis=1)]

        st.success("Data loaded and split from the Excel file!")
        return farmer_df, bmc_df, field_team_df, training_df, summary_df

    except FileNotFoundError:
        st.warning("Excel file not found. Falling back to dummy data.")
    except Exception as e:
        st.error(f"Error loading/splitting data from the Excel file: {e}. Falling back to dummy data.")

    # 2. Fallback: Load from embedded CSV strings
    try:
        farmer_df = pd.read_csv(StringIO(FALLBACK_FARMERS_CSV))
        bmc_df = pd.read_csv(StringIO(FALLBACK_BMCS_CSV))
        field_team_df = pd.read_csv(StringIO(FALLBACK_FIELD_TEAMS_CSV))
        training_df = pd.read_csv(StringIO(FALLBACK_TRAINING_DATA))
        summary_df = pd.read_csv(StringIO(SUMMARY_DATA))
        return farmer_df, bmc_df, field_team_df, training_df, summary_df
    except Exception as e:
        st.error(f"Critical error: Could not load even fallback dummy data. Error: {e}")
        st.stop()  # Stop the app if no data can be loaded

# --- KPI Calculation and Analysis Functions ---

def analyze_bmcs(bmc_df: pd.DataFrame, farmer_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
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
        latest_bmc_df = bmc_df.copy()  # Use as is if no date column

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
    low_performing_bmcs['Quality'] = pd.concat([low_quality_fat, low_quality_snf, adulteration_issues]).drop_duplicates(
        subset=['BMC_ID'])
    if not low_performing_bmcs['Quality'].empty:
        low_performing_bmcs['Quality']['Reason'] = 'Low Fat/SNF or Adulteration'

    # --- KPI: Utilization ---
    if 'Daily_Collection_Liters' in latest_bmc_df.columns and 'Capacity_Liters' in latest_bmc_df.columns:
        latest_bmc_df['Utilization_Percentage_Calculated'] = (
                                                                       latest_bmc_df['Daily_Collection_Liters'] /
                                                                       latest_bmc_df['Capacity_Liters']) * 100
        # Placeholder Threshold
        UTILIZATION_THRESHOLD = 70.0  # Below 70% is considered low
        low_performing_bmcs['Utilization'] = latest_bmc_df[
            latest_bmc_df['Utilization_Percentage_Calculated'] < UTILIZATION_THRESHOLD]
        if not low_performing_bmcs['Utilization'].empty:
            low_performing_bmcs['Utilization']['Reason'] = 'Low Utilization'

    # --- KPI: Animal Welfare Farms ---
    # Placeholder Threshold
    ANIMAL_WELFARE_THRESHOLD = 4.0  # Below 4.0 is considered low
    if 'Animal_Welfare_Compliance_Score_BMC' in latest_bmc_df.columns:
        low_performing_bmcs['Animal_Welfare'] = latest_bmc_df[
            latest_bmc_df['Animal_Welfare_Compliance_Score_BMC'] < ANIMAL_WELFARE_THRESHOLD]
        if not low_performing_bmcs['Animal_Welfare'].empty:
            low_performing_bmcs['Animal_Welfare']['Reason'] = 'Low Animal Welfare Score'

    # --- KPI: Women Empowerment ---
    # Placeholder Threshold
    WOMEN_EMPOWERMENT_THRESHOLD = 55.0  # Below 55% participation is considered low
    if 'Women_Empowerment_Participation_Rate_BMC' in latest_bmc_df.columns:
        low_performing_bmcs['Women_Empowerment'] = latest_bmc_df[
            latest_bmc_df['Women_Empowerment_Participation_Rate_BMC'] < WOMEN_EMPOWERMENT_THRESHOLD]
        if not low_performing_bmcs['Women_Empowerment'].empty:
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
                district = row['District']  # Assuming District is always available

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
                    target_util = row.get('Utilization_Target_Percentage', '80')  # Default for targets
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
farmer_df, bmc_df, field_team_df, training_df, summary_df = load_data()

# --- Streamlit Page Layout ---

st.title("Ksheersagar Dairy Performance Dashboard & Workplan")
st.markdown("---")

# --- Training Performance Dashboard Integration ---
st.header("Training Performance")
st.markdown("---")

# --- Display Raw Tables ---
st.subheader("📊 Monthly Training Breakdown")
st.dataframe(training_df, use_container_width=True)

st.subheader("📈 Training Summary Totals")
st.dataframe(summary_df, use_container_width=True)

# --- Optional Visualizations ---
col1, col2 = st.columns(2)

with col1:
    if st.checkbox("Show Total Trainings per Topic"):
        chart_data = summary_df.set_index("Training_Topic")["Total_Training"]
        st.bar_chart(chart_data)

with col2:
    if st.checkbox("Show Total Farmers Reached per Topic"):
        farmer_data = summary_df.set_index("Training_Topic")["No_of_Farmers"]
        st.bar_chart(farmer_data)

# --- End of training_summary module ---

st.markdown("---")
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
