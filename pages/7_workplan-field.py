import streamlit as st
import pandas as pd
import os
from io import StringIO
from typing import Tuple, Dict, List
import datetime

# --- Constants and Fallback Data (existing code) ---
EXCEL_FILE_PATH = "KSHEERSAGAR LTD File.xlsx"

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

# --- Existing Data Loading Functions ---
st.set_page_config(layout="wide")

@st.cache_data(show_spinner="Loading Ksheersagar data...")
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: # Corrected line
    """
    Attempts to load data from an Excel file and split it into DataFrames, then falls back to embedded dummy CSV data.
    """
    try:
        all_data_df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None) # Load all sheets
        
        # Determine which sheet contains which identifier
        farmer_sheet_name = None
        bmc_sheet_name = None
        field_team_sheet_name = None
        training_sheet_name = None
        
        for sheet_name, df_sheet in all_data_df.items():
            # Check for column names containing the identifier
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
        
        # Assuming summary data might be in the same training sheet or a separate one
        # For now, let's assume if 'Total_Training' and 'No_of_Farmers' columns exist, it's summary_df
        summary_df = pd.DataFrame()
        if training_sheet_name:
            if 'Total_Training' in all_data_df[training_sheet_name].columns and 'No_of_Farmers' in all_data_df[training_sheet_name].columns:
                summary_df = all_data_df[training_sheet_name]
            # If summary data is on a different sheet, you'd need to identify it similarly
            
        st.success("Data loaded and split from the Excel file!")
        return farmer_df, bmc_df, field_team_df, training_df, summary_df

    except FileNotFoundError:
        st.warning("Excel file not found. Falling back to dummy data.")
    except Exception as e:
        st.error(f"Error loading/splitting data from the Excel file: {e}. Falling back to dummy data.")

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

# --- Existing Analysis and Target Generation Functions ---
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


# --- Main Application Logic ---
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

# --- Admin Login Section (UPDATED) ---
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
            default_target = int(existing_entry['Target'].iloc[0]) if not existing_entry.empty else 0
            current_targets[activity] = st.number_input(f"Target for {activity}", min_value=0, value=default_target, key=target_key)
        
        with col_achieved:
            achieved_key = f"{selected_member}_{activity}_achieved_{workplan_date}"
            default_achieved = int(existing_entry['Achieved'].iloc[0]) if not existing_entry.empty else 0
            
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


# --- Existing Dashboard Sections (remaining code) ---
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
