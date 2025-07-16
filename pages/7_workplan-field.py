import streamlit as st
import pandas as pd
import os
from io import StringIO
from typing import Tuple, Dict, List
import datetime

# --- Configuration and File Paths ---
# This EXCEL_FILE_PATH is currently set to trigger fallback to embedded CSV data.
# If you eventually have a main Excel file with various sheets, you'd modify
# the load_data() function to parse it accordingly.
EXCEL_FILE_PATH = "KSHEERSAGAR LTD File.xlsx"

# This CSV file will be created and used for storing dynamic daily workplan inputs.
# It needs to be writable by the application.
DAILY_WORKPLAN_CSV = "daily_workplans.csv"

# Identifiers for different data sections (used in the hypothetical Excel loading,
# but kept here for context/potential future use).
FARMER_IDENTIFIER = "Farmer"
BMC_IDENTIFIER = "BMC"
FIELD_TEAM_IDENTIFIER = "FieldTeam"
TRAINING_IDENTIFIER = "Training"

# --- Fallback Data (as multi-line strings for easy embedding in the script) ---
# This data will be used if the main EXCEL_FILE_PATH is not found or cannot be processed.
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

# Define field team members (These names are used throughout the app for selection and display)
FT_MEMBERS = ["Dr. Sachin", "Bhushan Sananse", "Nilesh", "Subhrat", "Aniket"]
ADMIN_PASSWORD = "admin" # Simple password for demonstration. **Change this for a real application!**

# --- HARDCODED MONTHLY WORKPLAN DATA ---
# This dictionary stores the static monthly workplan for each field team member directly in code.
# This means you do NOT need to provide separate CSV files for these plans.
HARDCODED_MONTHLY_WORKPLANS: Dict[str, pd.DataFrame] = {}

# Define the common activities from your template
common_activities = [
    "Monitoring and validation : of farm and BMCs",
    "Training : DEOs, QIs, SS, MPOs, BCF and Lead Farmers",
    "Assessment : KS 1.0 endline and KS 2.0 baseline",
    "Governance : Weekly, Monthly"
]

# Initialize a dictionary to build the common DataFrame
common_monthly_plan_dict = {
    'Activity': common_activities
}

# Add columns for July dates (16 to 31)
for day in range(16, 32):
    common_monthly_plan_dict[f"July_{day}"] = [''] * len(common_activities)

# Add columns for August dates (1 to 31), padding single digits with a leading zero (e.g., Aug_01)
for day in range(1, 32):
    common_monthly_plan_dict[f"August_{str(day).zfill(2)}"] = [''] * len(common_activities)

# Set the specific text for the first activity's first date cell, as per your template
# "Monitoring and validation : of farm and BMCs" is at index 0 in common_activities
common_monthly_plan_dict["July_16"][0] = "Targets(input by FT) vs Achieved(input by Muskan)"

# Create a master DataFrame from this common structure
common_monthly_plan_df_template = pd.DataFrame(common_monthly_plan_dict)

# Assign a COPY of this common DataFrame to each field team member.
# Using .copy() is crucial so that if you ever wanted to modify a specific
# member's hardcoded plan later, it wouldn't affect others.
for member in FT_MEMBERS:
    HARDCODED_MONTHLY_WORKPLANS[member] = common_monthly_plan_df_template.copy()

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Ksheersagar Dairy Dashboard")

# --- Data Loading Functions ---

@st.cache_data(show_spinner="Loading Ksheersagar main data...")
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Attempts to load general data. Currently, it always falls back to embedded CSV strings
    for consistency and to avoid external file dependencies for core data.
    """
    try:
        # This explicit `raise FileNotFoundError` ensures the fallback data is used.
        # Remove or modify this if you implement actual Excel file parsing in the future.
        raise FileNotFoundError 
    except FileNotFoundError:
        st.warning(f"Main Excel file '{EXCEL_FILE_PATH}' not found. Using embedded dummy data.")
    except Exception as e:
        st.error(f"Error loading/splitting data from the Excel file: {e}. Using embedded dummy data.")

    # Fallback to in-memory CSV data (these strings are defined at the top of the script)
    try:
        farmer_df = pd.read_csv(StringIO(FALLBACK_FARMERS_CSV))
        bmc_df = pd.read_csv(StringIO(FALLBACK_BMCS_CSV))
        field_team_df = pd.read_csv(StringIO(FALLBACK_FIELD_TEAMS_CSV))
        training_df = pd.read_csv(StringIO(FALLBACK_TRAINING_DATA))
        summary_df = pd.read_csv(StringIO(SUMMARY_DATA))
        return farmer_df, bmc_df, field_team_df, training_df, summary_df
    except Exception as e:
        st.error(f"Critical error: Could not load even fallback dummy data. Please check script. Error: {e}")
        st.stop() # Stop the app if essential fallback data cannot be loaded.

@st.cache_data(show_spinner="Retrieving monthly workplan data...")
def load_monthly_workplan_data(ft_member_name: str) -> pd.DataFrame:
    """
    Retrieves the static monthly workplan for a specific field team member directly from the hardcoded data.
    """
    if ft_member_name in HARDCODED_MONTHLY_WORKPLANS:
        # Return a copy to ensure that internal modifications within Streamlit's dataframe display
        # do not affect the original hardcoded data.
        return HARDCODED_MONTHLY_WORKPLANS[ft_member_name].copy()
    else:
        st.error(f"Error: Hardcoded monthly workplan for '{ft_member_name}' not found. Check FT_MEMBERS list.")
        return pd.DataFrame({"Activity": [f"No hardcoded monthly plan for {ft_member_name}."], "Details": ["-"]})

@st.cache_resource
def load_daily_workplans() -> pd.DataFrame:
    """
    Loads daily workplan entries from 'daily_workplans.csv'.
    If the file does not exist, it initializes it with appropriate headers.
    Uses @st.cache_resource to ensure the DataFrame is loaded once and persisted
    across Streamlit reruns, allowing in-memory modifications to be tracked.
    """
    if os.path.exists(DAILY_WORKPLAN_CSV):
        df = pd.read_csv(DAILY_WORKPLAN_CSV)
        # Ensure 'Date' column is parsed as datetime objects for proper sorting/filtering
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        # Define the schema for the daily workplan CSV
        columns = ["Date", "FT_Member", "Activity", "Target", "Achieved", "Timestamp"]
        df = pd.DataFrame(columns=columns)
        # Create the empty CSV file with headers
        df.to_csv(DAILY_WORKPLAN_CSV, index=False)
        return df

def save_daily_workplans(df: pd.DataFrame):
    """
    Saves the current state of the daily workplans DataFrame back to 'daily_workplans.csv'.
    """
    # Ensure 'Date' is in string format before saving to CSV for consistency
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df.to_csv(DAILY_WORKPLAN_CSV, index=False)
    # Reload the daily_workplans_df after saving to ensure consistency in cache
    # (This is handled by st.rerun() in form submissions, but good practice if called elsewhere)
    load_daily_workplans.clear()


# --- KPI Analysis Functions (Logic remains unchanged) ---
def analyze_bmcs(bmc_df: pd.DataFrame, farmer_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Analyzes BMC data against defined KPIs (Quality, Utilization, Animal Welfare, Women Empowerment)
    and identifies low-performing BMCs based on predefined thresholds.
    """
    # Ensure 'Date' column is datetime and get the latest entry for each BMC_ID
    if 'Date' in bmc_df.columns:
        bmc_df['Date'] = pd.to_datetime(bmc_df['Date'])
        latest_bmc_df = bmc_df.loc[bmc_df.groupby('BMC_ID')['Date'].idxmax()]
    else:
        latest_bmc_df = bmc_df.copy() # If no 'Date' column, use the entire BMC dataframe

    low_performing_bmcs = {
        'Quality': pd.DataFrame(),
        'Utilization': pd.DataFrame(),
        'Animal_Welfare': pd.DataFrame(),
        'Women_Empowerment': pd.DataFrame()
    }

    # Quality KPI: Check Fat, SNF, and Adulteration
    QUALITY_FAT_THRESHOLD = 3.5
    QUALITY_SNF_THRESHOLD = 7.8
    low_quality_fat = latest_bmc_df[latest_bmc_df['Quality_Fat_Percentage'] < QUALITY_FAT_THRESHOLD]
    low_quality_snf = latest_bmc_df[latest_bmc_df['Quality_SNF_Percentage'] < QUALITY_SNF_THRESHOLD]
    adulteration_issues = latest_bmc_df[latest_bmc_df['Quality_Adulteration_Flag'].astype(str).str.lower() == 'yes']
    # Combine and remove duplicates based on BMC_ID
    low_performing_bmcs['Quality'] = pd.concat([low_quality_fat, low_quality_snf, adulteration_issues]).drop_duplicates(
        subset=['BMC_ID'])
    if not low_performing_bmcs['Quality'].empty:
        low_performing_bmcs['Quality']['Reason'] = 'Low Fat/SNF or Adulteration'

    # Utilization KPI: Calculate utilization percentage and compare to threshold
    if 'Daily_Collection_Liters' in latest_bmc_df.columns and 'Capacity_Liters' in latest_bmc_df.columns:
        latest_bmc_df['Utilization_Percentage_Calculated'] = (
                                                                latest_bmc_df['Daily_Collection_Liters'] /
                                                                latest_bmc_df['Capacity_Liters']) * 100
        UTILIZATION_THRESHOLD = 70.0
        low_performing_bmcs['Utilization'] = latest_bmc_df[
            latest_bmc_df['Utilization_Percentage_Calculated'] < UTILIZATION_THRESHOLD]
        if not low_performing_bmcs['Utilization'].empty:
            low_performing_bmcs['Utilization']['Reason'] = 'Low Utilization'

    # Animal Welfare KPI: Check compliance score
    ANIMAL_WELFARE_THRESHOLD = 4.0
    if 'Animal_Welfare_Compliance_Score_BMC' in latest_bmc_df.columns:
        low_performing_bmcs['Animal_Welfare'] = latest_bmc_df[
            latest_bmc_df['Animal_Welfare_Compliance_Score_BMC'] < ANIMAL_WELFARE_THRESHOLD]
        if not low_performing_bmcs['Animal_Welfare'].empty:
            low_performing_bmcs['Animal_Welfare']['Reason'] = 'Low Animal Welfare Score'

    # Women Empowerment KPI: Check participation rate
    WOMEN_EMPOWERMENT_THRESHOLD = 55.0
    if 'Women_Empowerment_Participation_Rate_BMC' in latest_bmc_df.columns:
        low_performing_bmcs['Women_Empowerment'] = latest_bmc_df[
            latest_bmc_df['Women_Empowerment_Participation_Rate_BMC'] < WOMEN_EMPOWERMENT_THRESHOLD]
        if not low_performing_bmcs['Women_Empowerment'].empty:
            low_performing_bmcs['Women_Empowerment']['Reason'] = 'Low Women Empowerment Rate'

    return low_performing_bmcs


def generate_actionable_targets(low_bmcs_dict: Dict[str, pd.DataFrame]) -> List[str]:
    """
    Generates actionable insights and suggested targets for field teams based on identified low-performing BMCs.
    """
    action_items = []
    for kpi, df in low_bmcs_dict.items():
        if not df.empty:
            for index, row in df.iterrows():
                bmc_id = row['BMC_ID']
                district = row['District']

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
                    target_util = row.get('Utilization_Target_Percentage', '80')
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


# --- Streamlit UI Layout and Application Flow ---

# Load main dashboard data and the persistent daily workplans DataFrame when the app starts
farmer_df, bmc_df, field_team_df, training_df, summary_df = load_data()
daily_workplans_df = load_daily_workplans() # This will load from daily_workplans.csv or create it

st.title("Ksheersagar Dairy Performance Dashboard & Workplan")
st.markdown("---")

# --- User Role Selection (Simplified Authentication) ---
# Allows switching between Field Team Member view (input daily plans) and Admin view (update 'Achieved')
st.sidebar.header("User Role Selection")
user_role = st.sidebar.radio("Select your role:", ("Field Team Member", "Admin"))

is_admin = False
if user_role == "Admin":
    password = st.sidebar.text_input("Admin Password:", type="password")
    if password == ADMIN_PASSWORD:
        is_admin = True
        st.sidebar.success("Admin logged in.")
    else:
        st.sidebar.error("Incorrect password. Access denied.")
        is_admin = False # Ensure admin privileges are revoked if password is wrong

st.markdown("---") # Visual separator in the main content area

# --- Daily Workplan Input Section (Visible to Field Team Members) ---
if user_role == "Field Team Member":
    st.header("Daily Workplan Input")
    st.markdown("Use this section to record your daily activities and set targets.")

    with st.form("daily_workplan_submission_form"): # Unique key for the form
        ft_member_selected = st.selectbox("Select Your Name:", FT_MEMBERS, key="ft_member_input_daily")
        
        # Set default date to today's date in Pune, Maharashtra timezone
        pune_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        current_pune_date = datetime.datetime.now(pune_timezone).date()
        plan_date_input = st.date_input("Date of Activity:", current_pune_date, key="plan_date_input_daily")
        
        activity_description = st.text_area("Activity Description:", 
                                            placeholder="e.g., Visited BMC001 for quality check; Conducted farmer training on AW for 10 farmers.", 
                                            key="activity_input_daily")
        target_value = st.text_input("Target:", 
                                      placeholder="e.g., Check quality of 500L milk; Train 10 farmers.", 
                                      key="target_input_daily")

        submitted_daily_workplan = st.form_submit_button("Submit Daily Workplan")

        if submitted_daily_workplan:
            if ft_member_selected and plan_date_input and activity_description and target_value:
                # Create a new entry dictionary
                new_daily_entry = {
                    "Date": plan_date_input.strftime('%Y-%m-%d'), # Store date as string for CSV consistency
                    "FT_Member": ft_member_selected,
                    "Activity": activity_description,
                    "Target": target_value,
                    "Achieved": "", # 'Achieved' is initially empty for field team submissions
                    "Timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Record submission timestamp
                }
                # Append the new entry to the global DataFrame and save it
                global daily_workplans_df # Declare to modify the DataFrame in cache
                daily_workplans_df = pd.concat([daily_workplans_df, pd.DataFrame([new_daily_entry])], ignore_index=True)
                save_daily_workplans(daily_workplans_df) # Save the updated DataFrame to CSV
                st.success("Daily workplan submitted successfully!")
                st.rerun() # Rerun the app to update the displayed tables immediately
            else:
                st.error("Please fill in all fields (Name, Date, Activity, Target) to submit your daily workplan.")

# --- Admin Input for Achieved Values (Visible only to Admin) ---
if is_admin:
    st.header("Admin: Update Achieved Values")
    st.markdown("Review submitted daily workplans and enter the 'Achieved' results.")

    # Filter for entries where 'Achieved' is still empty (or an empty string)
    # Use .copy() to avoid SettingWithCopyWarning when modifying later
    unachieved_entries_for_admin = daily_workplans_df[daily_workplans_df['Achieved'] == ""].copy()

    if unachieved_entries_for_admin.empty:
        st.info("No unachieved daily workplan entries to update at this time.")
    else:
        st.subheader("Pending Achieved Updates:")
        # Display the pending entries in a read-only format for review
        st.dataframe(
            unachieved_entries_for_admin,
            column_config={
                "Date": st.column_config.DatetimeColumn("Date", format="YYYY-MM-DD"),
                "FT_Member": "Field Team Member",
                "Activity": "Activity Description",
                "Target": "Target Set",
                "Achieved": st.column_config.TextColumn("Achieved (Pending)"), 
                "Timestamp": st.column_config.DatetimeColumn("Submitted On", format="YYYY-MM-DD HH:mm:ss")
            },
            hide_row_index=True,
            use_container_width=True,
            key="admin_pending_workplans_display" # Unique key for this dataframe widget
        )

        st.warning("To update an entry, select it from the dropdown below and enter the achieved value.")

        # Admin update form for specific entry
        with st.form("admin_achieved_update_form"): # Unique key for the admin update form
            # Create a user-friendly string for selecting each pending entry
            unachieved_entries_for_admin['Display_String'] = unachieved_entries_for_admin.apply(
                lambda row: f"{row['Date'].strftime('%Y-%m-%d')} | {row['FT_Member']} | {row['Activity'][:70]}...", axis=1
            )
            selected_entry_for_update = st.selectbox(
                "Select the daily workplan entry to update 'Achieved':",
                options=unachieved_entries_for_admin['Display_String'].tolist(),
                key="admin_select_entry_to_update"
            )

            if selected_entry_for_update:
                # Find the corresponding row in the pending entries DataFrame
                selected_row_data = unachieved_entries_for_admin[
                    unachieved_entries_for_admin['Display_String'] == selected_entry_for_update
                ].iloc[0]
                
                # Pre-fill input with current (empty) achieved value
                current_achieved_val_for_input = selected_row_data['Achieved'] if pd.notna(selected_row_data['Achieved']) else ""
                
                new_achieved_value_input = st.text_input(
                    f"Enter Achieved for Activity: '{selected_row_data['Activity']}' (Target: '{selected_row_data['Target']}')",
                    value=current_achieved_val_for_input,
                    key="new_achieved_value_text_input"
                )
                
                submit_achieved_update = st.form_submit_button("Update Achieved Value")

                if submit_achieved_update:
                    # Find the exact row in the global daily_workplans_df to modify
                    # Convert Date column to string for robust comparison (as stored in CSV)
                    temp_df_for_matching = daily_workplans_df.copy()
                    temp_df_for_matching['Date_Str'] = temp_df_for_matching['Date'].dt.strftime('%Y-%m-%d')
                    
                    # Match based on all original unique identifying fields (Date, Member, Activity, Target, Timestamp)
                    match_criteria = (
                        (temp_df_for_matching['Date_Str'] == selected_row_data['Date'].strftime('%Y-%m-%d')) &
                        (temp_df_for_matching['FT_Member'] == selected_row_data['FT_Member']) &
                        (temp_df_for_matching['Activity'] == selected_row_data['Activity']) &
                        (temp_df_for_matching['Target'] == selected_row_data['Target']) &
                        (temp_df_for_matching['Timestamp'] == selected_row_data['Timestamp']) 
                    )
                    
                    matching_index = temp_df_for_matching[match_criteria].index

                    if not matching_index.empty:
                        # Update the 'Achieved' value and record the new timestamp of update
                        daily_workplans_df.loc[matching_index[0], 'Achieved'] = new_achieved_value_input
                        daily_workplans_df.loc[matching_index[0], 'Timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        save_daily_workplans(daily_workplans_df) # Save changes to the CSV file
                        st.success("Achieved value updated successfully!")
                        st.rerun() # Rerun the app to refresh the UI and tables
                    else:
                        st.error("Error: Could not find the original daily workplan entry to update. It might have been altered or deleted. Please refresh the page.")
            else:
                st.info("Select a daily workplan entry to begin updating its achieved value.")

# --- General Dashboard Sections ---

st.markdown("---")
st.header("Training Performance Overview")
st.markdown("This section provides a summary of various training activities and farmer outreach.")

st.subheader("📊 Monthly Training Breakdown")
st.dataframe(training_df, use_container_width=True)

st.subheader("📈 Training Summary Totals")
st.dataframe(summary_df, use_container_width=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    if st.checkbox("Show Total Trainings per Topic Chart", key="chart_trainings"):
        chart_data_trainings = summary_df.set_index("Training_Topic")["Total_Training"]
        st.bar_chart(chart_data_trainings)

with col_chart2:
    if st.checkbox("Show Total Farmers Reached per Topic Chart", key="chart_farmers"):
        chart_data_farmers = summary_df.set_index("Training_Topic")["No_of_Farmers"]
        st.bar_chart(chart_data_farmers)

st.markdown("---")
st.header("Data Overview & KPI Analysis")
st.markdown("Review raw data snapshots and identify key performance areas.")

with st.expander("Show Raw Data Previews"):
    st.subheader("Farmer Data Snapshot")
    st.dataframe(farmer_df.head())

    st.subheader("BMC Data Snapshot")
    st.dataframe(bmc_df.head())

    st.subheader("Field Team & Training Data Snapshot")
    st.dataframe(field_team_df.head())

st.markdown("---")
st.header("KPI Performance Analysis")
st.markdown("Identifies BMCs that are currently underperforming based on predefined Key Performance Indicators (KPIs).")

low_performing_bmcs = analyze_bmcs(bmc_df, farmer_df)

if any(not df.empty for df in low_performing_bmcs.values()):
    st.subheader("Identified Low Performing BMCs:")
    for kpi_name, kpi_df in low_performing_bmcs.items():
        if not kpi_df.empty:
            st.write(f"#### {kpi_name.replace('_', ' ').title()} KPI Concerns:")
            # Display relevant columns for the identified low-performing BMCs
            display_cols = ['BMC_ID', 'BMC_Name', 'District', 'Reason']
            # Add specific KPI columns if they exist in the dataframe for more detail
            if kpi_name == 'Quality' and 'Quality_Fat_Percentage' in kpi_df.columns:
                display_cols.extend(['Quality_Fat_Percentage', 'Quality_SNF_Percentage', 'Quality_Adulteration_Flag'])
            if kpi_name == 'Utilization' and 'Utilization_Percentage_Calculated' in kpi_df.columns:
                display_cols.append('Utilization_Percentage_Calculated')
            if kpi_name == 'Animal_Welfare' and 'Animal_Welfare_Compliance_Score_BMC' in kpi_df.columns:
                display_cols.append('Animal_Welfare_Compliance_Score_BMC')
            if kpi_name == 'Women_Empowerment' and 'Women_Empowerment_Participation_Rate_BMC' in kpi_df.columns:
                display_cols.append('Women_Empowerment_Participation_Rate_BMC')
            
            # Filter columns to only those actually present in the DataFrame
            display_cols_actual = [col for col in display_cols if col in kpi_df.columns]
            st.dataframe(kpi_df[display_cols_actual].set_index('BMC_ID'), use_container_width=True)
            st.markdown("---")
else:
    st.success("All BMCs are performing well across the defined KPIs based on current data! No immediate concerns identified.")

st.header("Actionable Insights & Suggested Targets for Field Team")
st.markdown("Based on KPI analysis, here are specific action items and suggested targets for the field teams.")
action_items_list = generate_actionable_targets(low_performing_bmcs)

if action_items_list:
    for item in action_items_list:
        st.markdown(f"- {item}")
else:
    st.info("No specific actionable insights or targets to display as all BMCs are performing well, or no low-performing BMCs were identified.")

# --- Month-wise Static Workplans Section (Data is now HARDCODED) ---
st.markdown("---")
st.header("Static Monthly Workplans (July & August 2025) - Overview")
st.markdown("This section provides a consolidated view of the pre-defined monthly workplans for all field team members for July and August 2025.")

# Load all monthly workplans from the hardcoded dictionary
all_monthly_workplans_loaded_data = {}
for member_name in FT_MEMBERS:
    df_monthly = load_monthly_workplan_data(member_name)
    if not df_monthly.empty:
        all_monthly_workplans_loaded_data[member_name] = df_monthly

# Display July Workplan Section
st.subheader("📅 July 2025 Workplans")
if not all_monthly_workplans_loaded_data:
    st.info("No static monthly workplan data loaded for any member.")
else:
    july_combined_data_frames = []
    # Define expected column names for July dates based on the hardcoded structure
    expected_july_date_columns = [f"July_{d}" for d in range(16, 32)] # July 16 to July 31

    for member_name_key, member_monthly_df in all_monthly_workplans_loaded_data.items():
        if 'Activity' in member_monthly_df.columns:
            # Select 'Activity' and only the July date columns that are actually present in this DataFrame
            member_july_specific_cols = ['Activity'] + [col for col in expected_july_date_columns if col in member_monthly_df.columns]
            member_july_filtered_df = member_monthly_df[member_july_specific_cols].copy()
            member_july_filtered_df.insert(1, 'Field Team Member', member_name_key) # Add member's name
            july_combined_data_frames.append(member_july_filtered_df)

    if july_combined_data_frames:
        # Concatenate all July DataFrames into one
        combined_july_overview_df = pd.concat(july_combined_data_frames, ignore_index=True)
        # Reorder columns for display: Member, Activity, then July dates
        final_july_display_order = ['Field Team Member', 'Activity'] + \
                                   [col for col in combined_july_overview_df.columns if col.startswith('July_')]
        combined_july_overview_df = combined_july_overview_df[final_july_display_order]

        st.dataframe(combined_july_overview_df, use_container_width=True)
    else:
        st.info("No July workplan data to display after processing from hardcoded templates.")

st.markdown("---")

# Display August Workplan Section
st.subheader("📅 August 2025 Workplans")
if not all_monthly_workplans_loaded_data:
    st.info("No static monthly workplan data loaded for any member.")
else:
    august_combined_data_frames = []
    # Define expected column names for August dates (e.g., August_01 to August_31)
    expected_august_date_columns = [f"August_{str(day).zfill(2)}" for day in range(1, 32)]

    for member_name_key, member_monthly_df in all_monthly_workplans_loaded_data.items():
        if 'Activity' in member_monthly_df.columns:
            # Select 'Activity' and only the August date columns that are actually present in this DataFrame
            member_august_specific_cols = ['Activity'] + [col for col in expected_august_date_columns if col in member_monthly_df.columns]
            member_august_filtered_df = member_monthly_df[member_august_specific_cols].copy()
            member_august_filtered_df.insert(1, 'Field Team Member', member_name_key) # Add member's name
            august_combined_data_frames.append(member_august_filtered_df)

    if august_combined_data_frames:
        # Concatenate all August DataFrames into one
        combined_august_overview_df = pd.concat(august_combined_data_frames, ignore_index=True)
        # Reorder columns for display: Member, Activity, then August dates
        final_august_display_order = ['Field Team Member', 'Activity'] + \
                                     [col for col in combined_august_overview_df.columns if col.startswith('August_')]
        combined_august_overview_df = combined_august_overview_df[final_august_display_order]

        st.dataframe(combined_august_overview_df, use_container_width=True)
    else:
        st.info("No August workplan data to display after processing from hardcoded templates.")

st.markdown("---")

# --- Daily Workplan Entries Section (Dynamic User Inputs) ---
st.header("Daily Workplan Entries (Targets & Achieved)")
st.markdown("This table provides a comprehensive log of all daily workplan submissions, including set targets and achieved results. Entries for today and future dates (relative to Pune, Maharashtra time) are highlighted for quick review.")
if not daily_workplans_df.empty:
    # Convert 'Date' column to datetime objects for accurate sorting and comparison
    display_daily_workplans_sorted_df = daily_workplans_df.copy()
    display_daily_workplans_sorted_df['Date'] = pd.to_datetime(display_daily_workplans_sorted_df['Date'])
    
    # Sort by date (most recent first) and then by field team member for better readability
    display_daily_workplans_sorted_df = display_daily_workplans_sorted_df.sort_values(
        by=['Date', 'FT_Member'], ascending=[False, True]
    ).reset_index(drop=True)

    # Get the current date in Pune, Maharashtra timezone for highlighting
    pune_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    current_pune_date_only = datetime.datetime.now(pune_timezone).date()
    
    # Function to apply row highlighting based on date
    def highlight_current_or_future_dates(row):
        row_date_as_date_obj = row['Date'].date() # Extract date part for comparison
        if row_date_as_date_obj >= current_pune_date_only:
            # Return a list of styles, one for each column, to apply background color
            return ['background-color: #e6e6fa'] * len(row) # Light lavender background
        return [''] * len(row) # No special style

    # Display the DataFrame with conditional styling
    st.dataframe(
        display_daily_workplans_sorted_df.style.apply(highlight_current_or_future_dates, axis=1),
        column_config={
            "Date": st.column_config.DatetimeColumn("Date", format="YYYY-MM-DD"),
            "FT_Member": "Field Team Member",
            "Activity": "Activity Description",
            "Target": "Target Set",
            "Achieved": "Achieved Result",
            "Timestamp": st.column_config.DatetimeColumn("Last Updated", format="YYYY-MM-DD HH:mm:ss")
        },
        hide_row_index=True,
        use_container_width=True
    )
else:
    st.info("No daily workplan entries have been recorded yet.")
