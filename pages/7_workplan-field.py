import streamlit as st
import pandas as pd
import os
from io import StringIO
from typing import Tuple, Dict, List
import datetime

# --- Configuration and Fallback Data ---
# Path to your main Excel file (currently set to trigger fallback for CSV consistency)
EXCEL_FILE_PATH = "KSHEERSAGAR LTD File.xlsx"
# CSV file for storing dynamic daily workplan inputs
DAILY_WORKPLAN_CSV = "daily_workplans.csv"

# Identifiers for different data sections within a hypothetical larger Excel file
FARMER_IDENTIFIER = "Farmer"
BMC_IDENTIFIER = "BMC"
FIELD_TEAM_IDENTIFIER = "FieldTeam"
TRAINING_IDENTIFIER = "Training"

# Fallback CSV data for various sections if Excel file is not found or fails to load
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

# Define field team members (ensure these names match your file naming convention for static workplans)
FT_MEMBERS = ["Dr. Sachin", "Bhushan Sananse", "Nilesh", "Subhrat", "Aniket"]
ADMIN_PASSWORD = "admin" # Simple admin password for demonstration purposes

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide")

# --- Data Loading Functions ---

@st.cache_data(show_spinner="Loading Ksheersagar main data...")
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Attempts to load data from an Excel file. If not found or error, falls back to embedded dummy CSV data.
    """
    try:
        # This section is commented out/modified to consistently use fallback CSVs
        # as per previous interactions, ensuring the app runs without a specific Excel file.
        # If you have a specific KSHEERSAGAR LTD File.xlsx with these sections,
        # you'll need to adapt this parsing to read from its sheets/ranges.
        # For now, we force the fallback:
        raise FileNotFoundError # Forces the app to use the FALLBACK_..._CSV data
        
        # Example of how you might load from an actual Excel with multiple sheets:
        # all_excel_data = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None)
        # farmer_df = all_excel_data.get("Farmers_Sheet_Name", pd.DataFrame()) # Replace "Farmers_Sheet_Name"
        # bmc_df = all_excel_data.get("BMCs_Sheet_Name", pd.DataFrame())
        # field_team_df = all_excel_data.get("FieldTeams_Sheet_Name", pd.DataFrame())
        # training_df = all_excel_data.get("Training_Sheet_Name", pd.DataFrame())
        # summary_df = all_excel_data.get("Summary_Sheet_Name", pd.DataFrame())
        # st.success("Data loaded and split from the Excel file!")
        # return farmer_df, bmc_df, field_team_df, training_df, summary_df

    except FileNotFoundError:
        st.warning(f"Main Excel file '{EXCEL_FILE_PATH}' not found. Falling back to dummy data.")
    except Exception as e:
        st.error(f"Error loading/splitting data from the Excel file: {e}. Falling back to dummy data.")

    # Fallback to in-memory CSV data if Excel loading fails or is skipped
    try:
        farmer_df = pd.read_csv(StringIO(FALLBACK_FARMERS_CSV))
        bmc_df = pd.read_csv(StringIO(FALLBACK_BMCS_CSV))
        field_team_df = pd.read_csv(StringIO(FALLBACK_FIELD_TEAMS_CSV))
        training_df = pd.read_csv(StringIO(FALLBACK_TRAINING_DATA))
        summary_df = pd.read_csv(StringIO(SUMMARY_DATA))
        return farmer_df, bmc_df, field_team_df, training_df, summary_df
    except Exception as e:
        st.error(f"Critical error: Could not load even fallback dummy data. Error: {e}")
        st.stop()

@st.cache_data(show_spinner="Loading monthly workplan data...")
def load_monthly_workplan_data(ft_member_name: str) -> pd.DataFrame:
    """
    Loads the monthly workplan data for a given field team member from their respective CSV file.
    It expects the CSVs to be named 'Plan till 31st August 2025.xlsx - [Member Name].csv'.
    Handles the multi-level header structure (e.g., 'July' over '16', '17').
    Returns a DataFrame with 'Activity' and flattened date columns (e.g., 'July_16', 'August_01').
    """
    # Standardize the member name to match the file naming convention
    # Adjusting for "Dr. Sachin" and "Bhushan Sananse" as per provided file names
    if ft_member_name == "Dr. Sachin":
        file_suffix = "Dr. Sachin"
    elif ft_member_name == "Bhushan Sananse":
        file_suffix = "Bhushan" # Based on 'Plan till 31st August 2025.xlsx - Bhushan.csv'
    else:
        file_suffix = ft_member_name

    file_name = f"Plan till 31st August 2025.xlsx - {file_suffix}.csv"

    try:
        # Read the first two rows as headers (0-indexed: row 2 and row 3 in the CSV)
        df = pd.read_csv(file_name, header=[2, 3])

        # Clean up columns: Remove the initial 'S.No.' column which often becomes Unnamed
        # and flatten multi-index columns for easier access.
        if isinstance(df.columns, pd.MultiIndex):
            new_columns = []
            for col_idx, (level0, level1) in enumerate(df.columns):
                # Skip the first column if it's 'Unnamed' at both levels (likely 'S.No.')
                if col_idx == 0 and (level0.startswith('Unnamed') or pd.isna(level0)) and (level1.startswith('Unnamed') or pd.isna(level1)):
                    continue
                
                # Clean up month and day names
                month = str(level0).strip().replace(',', '').replace(' ', '_') if pd.notna(level0) else ''
                day = str(level1).strip() if pd.notna(level1) else ''

                if month and day:
                    # Format day with leading zero if single digit for August for consistency
                    if month.lower() == 'august' and day.isdigit():
                        day = str(int(day)).zfill(2)
                    new_columns.append(f"{month}_{day}")
                elif day: # This might be the 'Activities' column if it didn't get a top-level header
                    new_columns.append(day)
                else: # Fallback for unexpected empty or strange multi-index parts
                    new_columns.append(f"col_{col_idx}") # Unique name to avoid conflicts

            df.columns = new_columns
        else: # Handle case where it might not be multi-index (e.g., if skiprows was different)
            if df.columns[0].startswith('Unnamed'):
                df = df.iloc[:, 1:] # Drop the first column if it's unnamed

        # Rename 'Activities' column to 'Activity' for consistency
        if 'Activities' in df.columns:
            df = df.rename(columns={'Activities': 'Activity'})
        
        # Ensure 'Activity' is the first column if it exists
        if 'Activity' in df.columns:
            cols = ['Activity'] + [col for col in df.columns if col != 'Activity']
            df = df[cols]

        return df
    except FileNotFoundError:
        st.warning(f"Monthly workplan for {ft_member_name} not found: '{file_name}'. Displaying a placeholder.")
        return pd.DataFrame({"Activity": ["No monthly workplan data found for this member."], "Details": ["-"]})
    except pd.errors.EmptyDataError:
        st.warning(f"Monthly workplan for {ft_member_name} is empty: '{file_name}'. Displaying a placeholder.")
        return pd.DataFrame({"Activity": ["Monthly workplan file is empty."], "Details": ["-"]})
    except Exception as e:
        st.error(f"Error loading monthly workplan for {ft_member_name} from '{file_name}': {e}")
        return pd.DataFrame({"Activity": ["Error loading monthly workplan."], "Details": [f"Error: {e}"]})

@st.cache_resource
def load_daily_workplans() -> pd.DataFrame:
    """Loads or initializes the daily workplans CSV."""
    if os.path.exists(DAILY_WORKPLAN_CSV):
        df = pd.read_csv(DAILY_WORKPLAN_CSV)
        # Ensure 'Date' column is datetime object for proper handling
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        # Create an empty DataFrame with required columns if file doesn't exist
        df = pd.DataFrame(columns=["Date", "FT_Member", "Activity", "Target", "Achieved", "Timestamp"])
        # Save the empty DataFrame to create the CSV file
        df.to_csv(DAILY_WORKPLAN_CSV, index=False)
        return df

def save_daily_workplans(df: pd.DataFrame):
    """Saves the daily workplans DataFrame to CSV."""
    df.to_csv(DAILY_WORKPLAN_CSV, index=False)


# --- Analysis Functions (Unchanged from previous versions) ---
def analyze_bmcs(bmc_df: pd.DataFrame, farmer_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Analyzes BMC data against KPIs and identifies low-performing BMCs.
    Returns a dictionary of low-performing BMCs for each KPI.
    """
    if 'Date' in bmc_df.columns:
        bmc_df['Date'] = pd.to_datetime(bmc_df['Date'])
        latest_bmc_df = bmc_df.loc[bmc_df.groupby('BMC_ID')['Date'].idxmax()]
    else:
        latest_bmc_df = bmc_df.copy()

    low_performing_bmcs = {
        'Quality': pd.DataFrame(),
        'Utilization': pd.DataFrame(),
        'Animal_Welfare': pd.DataFrame(),
        'Women_Empowerment': pd.DataFrame()
    }

    QUALITY_FAT_THRESHOLD = 3.5
    QUALITY_SNF_THRESHOLD = 7.8

    low_quality_fat = latest_bmc_df[latest_bmc_df['Quality_Fat_Percentage'] < QUALITY_FAT_THRESHOLD]
    low_quality_snf = latest_bmc_df[latest_bmc_df['Quality_SNF_Percentage'] < QUALITY_SNF_THRESHOLD]
    adulteration_issues = latest_bmc_df[latest_bmc_df['Quality_Adulteration_Flag'].astype(str).str.lower() == 'yes']

    low_performing_bmcs['Quality'] = pd.concat([low_quality_fat, low_quality_snf, adulteration_issues]).drop_duplicates(
        subset=['BMC_ID'])
    if not low_performing_bmcs['Quality'].empty:
        low_performing_bmcs['Quality']['Reason'] = 'Low Fat/SNF or Adulteration'

    if 'Daily_Collection_Liters' in latest_bmc_df.columns and 'Capacity_Liters' in latest_bmc_df.columns:
        latest_bmc_df['Utilization_Percentage_Calculated'] = (
                                                                latest_bmc_df['Daily_Collection_Liters'] /
                                                                latest_bmc_df['Capacity_Liters']) * 100

        UTILIZATION_THRESHOLD = 70.0
        low_performing_bmcs['Utilization'] = latest_bmc_df[
            latest_bmc_df['Utilization_Percentage_Calculated'] < UTILIZATION_THRESHOLD]
        if not low_performing_bmcs['Utilization'].empty:
            low_performing_bmcs['Utilization']['Reason'] = 'Low Utilization'


    ANIMAL_WELFARE_THRESHOLD = 4.0
    if 'Animal_Welfare_Compliance_Score_BMC' in latest_bmc_df.columns:
        low_performing_bmcs['Animal_Welfare'] = latest_bmc_df[
            latest_bmc_df['Animal_Welfare_Compliance_Score_BMC'] < ANIMAL_WELFARE_THRESHOLD]
        if not low_performing_bmcs['Animal_Welfare'].empty:
            low_performing_bmcs['Animal_Welfare']['Reason'] = 'Low Animal Welfare Score'


    WOMEN_EMPOWERMENT_THRESHOLD = 55.0
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


# --- Main Streamlit App Execution ---

# Load main data and daily workplans on app start
farmer_df, bmc_df, field_team_df, training_df, summary_df = load_data()
daily_workplans_df = load_daily_workplans()

st.title("Ksheersagar Dairy Performance Dashboard & Workplan")
st.markdown("---")


# --- User Role Selection (Simplified Authentication) ---
st.sidebar.header("User Role Selection")
user_role = st.sidebar.radio("Select your role:", ("Field Team Member", "Admin"))

is_admin = False
if user_role == "Admin":
    password = st.sidebar.text_input("Admin Password:", type="password")
    if password == ADMIN_PASSWORD:
        is_admin = True
        st.sidebar.success("Admin logged in.")
    else:
        st.sidebar.error("Incorrect password.")
        is_admin = False # Ensure it's false if password is wrong

st.markdown("---") # Visual separator

# --- Daily Workplan Input Section (for Field Team Members) ---
if user_role == "Field Team Member":
    st.header("Daily Workplan Input")
    st.markdown("Enter your daily activities and targets.")

    with st.form("daily_workplan_form"):
        ft_member = st.selectbox("Select Your Name:", FT_MEMBERS, key="ft_member_input")
        plan_date = st.date_input("Date:", datetime.date.today(), key="plan_date_input")
        activity = st.text_area("Activity Description (e.g., 'Visited BMC001 for quality check', 'Conducted farmer training on AW for 10 farmers'):", key="activity_input")
        target = st.text_input("Target (e.g., 'Check quality of 500L milk', 'Train 10 farmers'):", key="target_input")

        submitted_workplan = st.form_submit_button("Submit Daily Workplan")

        if submitted_workplan:
            if ft_member and plan_date and activity and target:
                new_entry = {
                    "Date": plan_date.strftime('%Y-%m-%d'), # Store date as string for CSV persistence
                    "FT_Member": ft_member,
                    "Activity": activity,
                    "Target": target,
                    "Achieved": "", # Initially empty, to be filled by admin
                    "Timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Record submission time
                }
                # Add the new entry to the DataFrame
                global daily_workplans_df
                daily_workplans_df = pd.concat([daily_workplans_df, pd.DataFrame([new_entry])], ignore_index=True)
                save_daily_workplans(daily_workplans_df) # Save changes to CSV
                st.success("Daily workplan submitted successfully!")
                st.rerun() # Rerun to refresh the displayed data immediately
            else:
                st.error("Please fill in all fields for the daily workplan.")

# --- Admin Input for Achieved Values ---
if is_admin:
    st.header("Admin: Update Achieved Values")
    st.markdown("Select a workplan entry and input the achieved value.")

    # Filter for entries where 'Achieved' is not yet filled (or is an empty string)
    unachieved_entries = daily_workplans_df[daily_workplans_df['Achieved'] == ""].copy()

    if unachieved_entries.empty:
        st.info("No unachieved daily workplan entries to update.")
    else:
        # Display the unachieved entries in a read-only table for context
        st.dataframe(
            unachieved_entries,
            column_config={
                "Date": st.column_config.DatetimeColumn("Date", format="YYYY-MM-DD"),
                "FT_Member": "Field Team Member",
                "Activity": "Activity",
                "Target": "Target",
                "Achieved": st.column_config.TextColumn("Achieved (Current)"), # Show current empty state
                "Timestamp": st.column_config.DatetimeColumn("Submitted On", format="YYYY-MM-DD HH:mm:ss")
            },
            hide_row_index=True,
            use_container_width=True,
            key="admin_unachieved_display" # Use a distinct key
        )

        st.warning("Note: Use the dropdown below to select an entry and update its 'Achieved' value.")

        # Admin selection and update form
        with st.form("admin_achieved_form"):
            # Create a unique identifiable string for each entry to display in the selectbox
            unachieved_entries['Display'] = unachieved_entries.apply(
                lambda row: f"{row['Date'].strftime('%Y-%m-%d')} - {row['FT_Member']} - {row['Activity'][:70]}...", axis=1
            )
            selected_entry_display = st.selectbox(
                "Select entry to update 'Achieved' value:",
                options=unachieved_entries['Display'].tolist(),
                key="admin_select_entry"
            )

            if selected_entry_display:
                # Retrieve the original row from the unachieved_entries DataFrame
                selected_row = unachieved_entries[unachieved_entries['Display'] == selected_entry_display].iloc[0]
                
                # Get the current achieved value (will likely be empty string)
                current_achieved_value = selected_row['Achieved'] if pd.notna(selected_row['Achieved']) else ""
                
                new_achieved_input = st.text_input(
                    f"Enter Achieved for: '{selected_row['Activity']}' (Target: '{selected_row['Target']}')",
                    value=current_achieved_value,
                    key="new_achieved_input"
                )
                
                update_button = st.form_submit_button("Update Achieved")

                if update_button:
                    # Find the corresponding row in the global daily_workplans_df
                    # Convert 'Date' column in daily_workplans_df to string for direct comparison
                    temp_df_for_match = daily_workplans_df.copy()
                    temp_df_for_match['Date_Str'] = temp_df_for_match['Date'].dt.strftime('%Y-%m-%d') if pd.api.types.is_datetime64_any_dtype(temp_df_for_match['Date']) else temp_df_for_match['Date']

                    # Match based on key fields, including the string formatted date
                    match_index = temp_df_for_match[
                        (temp_df_for_match['Date_Str'] == selected_row['Date'].strftime('%Y-%m-%d')) &
                        (temp_df_for_match['FT_Member'] == selected_row['FT_Member']) &
                        (temp_df_for_match['Activity'] == selected_row['Activity']) &
                        (temp_df_for_match['Target'] == selected_row['Target']) &
                        (temp_df_for_match['Timestamp'] == selected_row['Timestamp']) # Also match timestamp for uniqueness
                    ].index

                    if not match_index.empty:
                        # Update the 'Achieved' value and Timestamp in the global DataFrame
                        daily_workplans_df.loc[match_index[0], 'Achieved'] = new_achieved_input
                        daily_workplans_df.loc[match_index[0], 'Timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        save_daily_workplans(daily_workplans_df) # Save updated DataFrame to CSV
                        st.success("Achieved value updated successfully!")
                        st.rerun() # Rerun to refresh the displayed data
                    else:
                        st.error("Could not find the original entry to update. It might have been updated or removed. Please refresh.")
            else:
                st.info("Select an entry from the dropdown above to update its achieved value.")

# --- General Dashboard Sections ---
st.markdown("---")
st.header("Training Performance")
st.markdown("---")

st.subheader("📊 Monthly Training Breakdown")
st.dataframe(training_df, use_container_width=True)

st.subheader("📈 Training Summary Totals")
st.dataframe(summary_df, use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    if st.checkbox("Show Total Trainings per Topic", key="chart_trainings"):
        chart_data = summary_df.set_index("Training_Topic")["Total_Training"]
        st.bar_chart(chart_data)

with col2:
    if st.checkbox("Show Total Farmers Reached per Topic", key="chart_farmers"):
        farmer_data = summary_df.set_index("Training_Topic")["No_of_Farmers"]
        st.bar_chart(farmer_data)


st.markdown("---")
st.header("Data Overview & KPI Analysis")

with st.expander("Show Raw Data Previews"):
    st.subheader("Farmer Data")
    st.dataframe(farmer_df.head())

    st.subheader("BMC Data")
    st.dataframe(bmc_df.head())

    st.subheader("Field Team & Training Data")
    st.dataframe(field_team_df.head())

st.markdown("---")
st.header("KPI Performance Analysis")

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

# --- NEW: Month-wise Static Workplans (Refined Display) ---
st.markdown("---")
st.header("Static Monthly Workplans (July & August 2025) - Overview")
st.markdown("Displays the planned activities for each field team member, consolidated by month.")

# Load all monthly workplans once for efficient display
all_monthly_workplans_data = {}
for member in FT_MEMBERS:
    df = load_monthly_workplan_data(member)
    if not df.empty:
        all_monthly_workplans_data[member] = df

# Display July Workplan
st.subheader("📅 July 2025 Workplans")
if not all_monthly_workplans_data:
    st.info("No monthly workplan data loaded for any member.")
else:
    july_data_frames = []
    # Columns expected for July from the CSV structure
    expected_july_date_cols = [f"July_{d}" for d in range(16, 32)] # July 16 to July 31

    for member, df in all_monthly_workplans_data.items():
        # Ensure 'Activity' column exists before proceeding
        if 'Activity' in df.columns:
            # Select 'Activity' and only the actual July date columns present in this DF
            member_july_cols = ['Activity'] + [col for col in expected_july_date_cols if col in df.columns]
            member_july_df = df[member_july_cols].copy()
            member_july_df.insert(1, 'Field Team Member', member) # Add member name
            july_data_frames.append(member_july_df)

    if july_data_frames:
        combined_july_df = pd.concat(july_data_frames, ignore_index=True)
        # Reorder columns: Field Team Member, Activity, then July dates
        final_july_cols_order = ['Field Team Member', 'Activity'] + [col for col in combined_july_df.columns if col.startswith('July')]
        combined_july_df = combined_july_df[final_july_cols_order]

        st.dataframe(combined_july_df, use_container_width=True)
    else:
        st.info("No July workplan data to display after processing.")

st.markdown("---")

# Display August Workplan
st.subheader("📅 August 2025 Workplans")
if not all_monthly_workplans_data:
    st.info("No monthly workplan data loaded for any member.")
else:
    august_data_frames = []
    # Columns expected for August from the CSV structure (e.g., August_01 to August_31)
    expected_august_date_cols = [f"August_{str(d).zfill(2)}" for d in range(1, 32)] # August 1 to 31

    for member, df in all_monthly_workplans_data.items():
        if 'Activity' in df.columns:
            # Select 'Activity' and only the actual August date columns present in this DF
            member_august_cols = ['Activity'] + [col for col in expected_august_date_cols if col in df.columns]
            member_august_df = df[member_august_cols].copy()
            member_august_df.insert(1, 'Field Team Member', member) # Add member name
            august_data_frames.append(member_august_df)

    if august_data_frames:
        combined_august_df = pd.concat(august_data_frames, ignore_index=True)
        # Reorder columns: Field Team Member, Activity, then August dates
        final_august_cols_order = ['Field Team Member', 'Activity'] + [col for col in combined_august_df.columns if col.startswith('August')]
        combined_august_df = combined_august_df[final_august_cols_order]

        st.dataframe(combined_august_df, use_container_width=True)
    else:
        st.info("No August workplan data to display after processing.")

st.markdown("---")

# --- Daily Workplan Entries (Current and Historical Daily Submissions) ---
st.header("Daily Workplan Entries (Targets & Achieved)")
st.markdown("View all daily workplan submissions and their current status.")
if not daily_workplans_df.empty:
    # Sort by date (descending) and then member for better readability
    display_daily_df = daily_workplans_df.sort_values(by=['Date', 'FT_Member'], ascending=[False, True]).reset_index(drop=True)
    
    st.dataframe(
        display_daily_df,
        column_config={
            "Date": st.column_config.DatetimeColumn("Date", format="YYYY-MM-DD"),
            "FT_Member": "Field Team Member",
            "Activity": "Activity",
            "Target": "Target",
            "Achieved": "Achieved",
            "Timestamp": st.column_config.DatetimeColumn("Last Updated", format="YYYY-MM-DD HH:mm:ss")
        },
        hide_row_index=True,
        use_container_width=True
    )
else:
    st.info("No daily workplan entries recorded yet.")
