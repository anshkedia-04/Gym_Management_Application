import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import GymDatabase
from email_service import EmailService

# Page configuration
st.set_page_config(
    page_title="Gym Management System",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db = GymDatabase()

# Professional Custom CSS with Dark Blue/Navy theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #1a2332 0%, #2d3e50 100%);
        padding: 2rem;
    }
    
    .block-container {
        background: #ffffff;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2332 0%, #0f1419 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] .css-1d391kg, [data-testid="stSidebar"] .st-emotion-cache-1d391kg {
        color: white;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: rgba(255,255,255,0.9) !important;
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255,255,255,0.03);
        padding: 0.875rem 1.25rem;
        border-radius: 8px;
        margin: 0.4rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(59, 130, 246, 0.3);
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] [data-checked="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        font-weight: 500;
        border-color: #3b82f6;
    }
    
    /* Headers */
    h1 {
        color: #1e293b;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.75rem;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #3b82f6;
        padding-left: 1rem;
    }
    
    h3 {
        color: #334155;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(30, 64, 175, 0.35);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255,255,255,0.95) !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: rgba(255,255,255,0.85) !important;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(30, 64, 175, 0.3);
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(30, 64, 175, 0.4);
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background: white !important;
        color: #1e293b !important;
    }
    
    /* Input labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stDateInput label {
        color: #1e293b !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Date inputs */
    .stDateInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        background: white !important;
        color: #1e293b !important;
    }
    
    /* Selectbox text */
    .stSelectbox div[data-baseweb="select"] > div {
        background: white !important;
        color: #1e293b !important;
    }
    
    /* Dropdown menu */
    [data-baseweb="menu"] {
        background: white !important;
    }
    
    [data-baseweb="menu"] li {
        color: #1e293b !important;
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        font-weight: 600;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        color: #1e293b !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #3b82f6;
        background: #f1f5f9;
    }
    
    /* Expander content text */
    .streamlit-expanderContent {
        background: #f8fafc;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        border-top: none;
    }
    
    .streamlit-expanderContent p,
    .streamlit-expanderContent div {
        color: #1e293b !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 1rem 1.25rem;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Success message */
    .stSuccess {
        background: #f0fdf4;
        border-left-color: #10b981;
        color: #065f46;
    }
    
    /* Info message */
    .stInfo {
        background: #eff6ff;
        border-left-color: #3b82f6;
        color: #1e40af;
    }
    
    /* Warning message */
    .stWarning {
        background: #fffbeb;
        border-left-color: #f59e0b;
        color: #92400e;
    }
    
    /* Error message */
    .stError {
        background: #fef2f2;
        border-left-color: #ef4444;
        color: #991b1b;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }
    
    /* Form submit button special styling */
    .stForm button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.3);
    }
    
    .stForm button[kind="primaryFormSubmit"]:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%);
        box-shadow: 0 4px 16px rgba(5, 150, 105, 0.4);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    }
    
    /* Custom badge */
    .status-badge {
        display: inline-block;
        padding: 0.375rem 0.875rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-active {
        background: #d1fae5;
        color: #065f46;
        border: 1px solid #10b981;
    }
    
    .status-expired {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #ef4444;
    }
    
    /* Info boxes */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box p {
        margin: 0;
        color: #1e40af;
        font-weight: 500;
    }
    
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1.25rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .success-box h3 {
        margin: 0;
        color: #065f46;
    }
    
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box p {
        margin: 0;
        color: #92400e;
        font-weight: 600;
    }
    
    .danger-box {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .danger-box p {
        margin: 0;
        color: #991b1b;
        font-weight: 600;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stat-card p {
        margin: 0;
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-card h2 {
        margin: 0.5rem 0 0 0;
        color: #1e293b;
        border: none;
        padding: 0;
        font-size: 1.5rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    }
    
    /* Member card hover effect */
    .streamlit-expanderContent {
        background: #f8fafc;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        border-top: none;
    }
    
    .streamlit-expanderContent p,
    .streamlit-expanderContent div {
        color: #1e293b !important;
    }
    
    /* All paragraph and div text */
    p, div {
        color: #1e293b;
    }
    
    /* Strong/bold text */
    strong {
        color: #0f172a;
    }
    
    /* DataFrames text visibility */
    [data-testid="stDataFrame"] * {
        color: #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("""
    <h1>🏋️ Gym Management</h1>
""", unsafe_allow_html=True)
st.sidebar.image("assets/logo.png", width=200)

menu = st.sidebar.radio(
    "",
    ["📊 Dashboard", "➕ Register Member", "👥 View Members", "📧 Send Reminders", "⚙️ Settings"],
    label_visibility="collapsed"
)

# Main title
st.markdown("""
    <h1>💪 Swoldier Fitness</h1>
""", unsafe_allow_html=True)

# ==================== DASHBOARD ====================
if menu == "📊 Dashboard":
    st.markdown("<h2>📊 Live Dashboard</h2>", unsafe_allow_html=True)
    
    # Update all member statuses
    db.update_all_statuses()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_members = db.get_active_members_count()
        st.metric(
            label="Active Members",
            value=active_members,
            delta="Currently Active"
        )
    
    with col2:
        expiring_7_days = len(db.get_expiring_members(7))
        st.metric(
            label="Expiring in 7 Days",
            value=expiring_7_days,
            delta="Need Attention",
            delta_color="inverse"
        )
    
    with col3:
        expiring_30_days = len(db.get_expiring_members(30))
        st.metric(
            label="Expiring in 30 Days",
            value=expiring_30_days,
            delta="Plan Ahead"
        )
    
    with col4:
        all_members = db.get_all_members()
        total_members = len(all_members)
        st.metric(
            label="Total Members",
            value=total_members,
            delta="All Time"
        )
    
    st.markdown("---")
    
    # Expiring members details
    st.markdown("<h2>⚠️ Members Expiring in Next 7 Days</h2>", unsafe_allow_html=True)
    expiring_df = db.get_expiring_members(7)
    
    if not expiring_df.empty:
        expiring_df['Days Left'] = (expiring_df['Membership End Date'] - datetime.now()).dt.days + 1
        display_df = expiring_df[['Member ID', 'Name', 'Phone', 'Email', 'Membership End Date', 'Days Left']]
        st.dataframe(display_df, use_container_width=True, height=300)
    else:
        st.success("✅ No memberships expiring in the next 7 days!")
    
    st.markdown("---")
    
    # Recent registrations
    st.markdown("<h2>📋 Recent Registrations</h2>", unsafe_allow_html=True)
    all_members = db.get_all_members()
    if not all_members.empty:
        all_members['Joining Date'] = pd.to_datetime(all_members['Joining Date'])
        recent_members = all_members.sort_values('Joining Date', ascending=False).head(5)
        st.dataframe(recent_members[['Member ID', 'Name', 'Phone', 'Joining Date', 'Status']], use_container_width=True, height=250)
    else:
        st.info("📭 No members registered yet.")

# ==================== REGISTER MEMBER ====================
elif menu == "➕ Register Member":
    st.markdown("<h2>➕ Register New Member</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-box">
            <p>ℹ️ Fill in all required fields marked with * to register a new member</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👤 Personal Information")
            name = st.text_input("Full Name *", placeholder="Enter member name")
            phone = st.text_input("Phone Number *", placeholder="e.g., +91-9876543210")
            email = st.text_input("Email Address *", placeholder="member@example.com")
            joining_date = st.date_input("Joining Date *", value=datetime.now())
        
        with col2:
            st.markdown("### 💳 Membership Details")
            membership_duration = st.selectbox(
                "Membership Duration",
                ["1 Month", "3 Months", "6 Months", "1 Year", "Custom"]
            )
            
            if membership_duration == "Custom":
                end_date = st.date_input("Membership End Date *", value=datetime.now() + timedelta(days=30))
            else:
                duration_days = {
                    "1 Month": 30,
                    "3 Months": 90,
                    "6 Months": 180,
                    "1 Year": 365
                }
                end_date = joining_date + timedelta(days=duration_days[membership_duration])
                st.date_input("Membership End Date *", value=end_date, disabled=True)
            
            amount = st.number_input("Amount Paid (₹) *", min_value=0.0, step=100.0, value=1000.0)
            payment_mode = st.selectbox("Payment Mode *", ["Cash", "UPI", "Card", "Net Banking", "Cheque"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ Register Member", use_container_width=True)
        
        if submitted:
            if name and phone and email:
                member_id = db.add_member(
                    name=name,
                    phone=phone,
                    email=email,
                    joining_date=str(joining_date),
                    end_date=str(end_date),
                    amount=amount,
                    payment_mode=payment_mode
                )
                st.success(f"✅ Member registered successfully! Member ID: {member_id}")
                st.balloons()
            else:
                st.error("❌ Please fill all required fields!")

# ==================== VIEW MEMBERS ====================
elif menu == "👥 View Members":
    st.markdown("<h2>👥 All Members</h2>", unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Expired"])
    
    with col2:
        search_term = st.text_input("🔍 Search by Name/ID/Phone", placeholder="Type to search...")
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Get all members
    db.update_all_statuses()
    all_members = db.get_all_members()
    
    if not all_members.empty:
        # Apply filters
        if status_filter != "All":
            all_members = all_members[all_members['Status'] == status_filter]
        
        if search_term:
            all_members = all_members[
                all_members['Name'].str.contains(search_term, case=False, na=False) |
                all_members['Member ID'].str.contains(search_term, case=False, na=False) |
                all_members['Phone'].astype(str).str.contains(search_term, case=False, na=False)
            ]
        
        st.markdown(f"""
            <div class="info-box">
                <p>📊 Showing {len(all_members)} members</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display members
        for idx, member in all_members.iterrows():
            status_class = "status-active" if member['Status'] == "Active" else "status-expired"
            
            with st.expander(f"👤 {member['Name']} - {member['Member ID']} • {member['Status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📞 Contact Information")
                    st.write(f"**Phone:** {member['Phone']}")
                    st.write(f"**Email:** {member['Email']}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📅 Membership Period")
                    st.write(f"**Joining Date:** {member['Joining Date']}")
                    st.write(f"**Membership End:** {member['Membership End Date']}")
                
                with col2:
                    st.markdown("### 💰 Payment Information")
                    st.write(f"**Amount Paid:** ₹{member['Amount Paid']}")
                    st.write(f"**Payment Mode:** {member['Payment Mode']}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📊 Status")
                    st.markdown(f"<span class='status-badge {status_class}'>{member['Status']}</span>", unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{member['Member ID']}", use_container_width=True):
                        st.session_state[f"edit_mode_{member['Member ID']}"] = True
                
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{member['Member ID']}", use_container_width=True):
                        db.delete_member(member['Member ID'])
                        st.success(f"✅ Deleted {member['Name']}")
                        st.rerun()
                
                # Edit mode
                if st.session_state.get(f"edit_mode_{member['Member ID']}", False):
                    st.markdown("---")
                    st.markdown("<h3>✏️ Edit Member Details</h3>", unsafe_allow_html=True)
                    
                    with st.form(f"edit_form_{member['Member ID']}"):
                        edit_col1, edit_col2 = st.columns(2)
                        
                        with edit_col1:
                            edit_name = st.text_input("Name", value=member['Name'])
                            edit_phone = st.text_input("Phone", value=member['Phone'])
                            edit_email = st.text_input("Email", value=member['Email'])
                        
                        with edit_col2:
                            edit_joining = st.date_input("Joining Date", value=pd.to_datetime(member['Joining Date']))
                            edit_end = st.date_input("End Date", value=pd.to_datetime(member['Membership End Date']))
                            edit_amount = st.number_input("Amount", value=float(member['Amount Paid']))
                            edit_payment = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "Net Banking", "Cheque"], 
                                                       index=["Cash", "UPI", "Card", "Net Banking", "Cheque"].index(member['Payment Mode']))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            save_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                        with col2:
                            cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
                        
                        if save_edit:
                            db.update_member(
                                member['Member ID'],
                                edit_name, edit_phone, edit_email,
                                str(edit_joining), str(edit_end),
                                edit_amount, edit_payment
                            )
                            st.session_state[f"edit_mode_{member['Member ID']}"] = False
                            st.success("✅ Member updated successfully!")
                            st.rerun()
                        
                        if cancel_edit:
                            st.session_state[f"edit_mode_{member['Member ID']}"] = False
                            st.rerun()
    else:
        st.info("📭 No members found. Start by registering new members!")

# ==================== SEND REMINDERS ====================
elif menu == "📧 Send Reminders":
    st.markdown("<h2>📧 Send Membership Renewal Reminders</h2>", unsafe_allow_html=True)
    
    # Email configuration
    with st.expander("⚙️ Email Configuration (Gmail)", expanded=False):
        st.markdown("""
            <div class="warning-box">
                <h4 style='margin: 0 0 0.75rem 0; color: #92400e;'>📝 Gmail Setup Instructions</h4>
                <ol style='margin: 0; color: #92400e; line-height: 1.8;'>
                    <li>Enable 2-Step Verification in your Google Account</li>
                    <li>Generate an App Password: Google Account → Security → 2-Step Verification → App passwords</li>
                    <li>Use the generated 16-character password below</li>
                </ol>
                <p style='margin: 0.75rem 0 0 0; color: #92400e; font-weight: 600;'>
                    ⚠️ Note: Regular Gmail password won't work if 2FA is enabled.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        sender_email = st.text_input("Your Gmail Address", placeholder="your.email@gmail.com")
        sender_password = st.text_input("App Password", type="password", placeholder="16-character app password")
        
        if st.button("💾 Save Email Configuration", use_container_width=True):
            if sender_email and sender_password:
                st.session_state['sender_email'] = sender_email
                st.session_state['sender_password'] = sender_password
                st.success("✅ Email configuration saved!")
            else:
                st.error("❌ Please provide both email and password")
    
    st.markdown("---")
    
    # Get expiring members
    days_ahead = st.slider("📅 Select expiry window (days)", min_value=1, max_value=30, value=7)
    expiring_members = db.get_expiring_members(days_ahead)
    
    if not expiring_members.empty:
        st.markdown(f"""
            <div class="warning-box">
                <h3 style='margin: 0; color: #92400e;'>
                    📋 Members expiring in next {days_ahead} days: {len(expiring_members)}
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Show members
        st.dataframe(
            expiring_members[['Member ID', 'Name', 'Email', 'Phone', 'Membership End Date']],
            use_container_width=True,
            height=300
        )
        
        # Send emails
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📧 Send Renewal Reminders to All", type="primary", use_container_width=True):
            if 'sender_email' not in st.session_state or 'sender_password' not in st.session_state:
                st.error("❌ Please configure email settings first!")
            else:
                with st.spinner("📨 Sending emails..."):
                    email_service = EmailService(
                        sender_email=st.session_state['sender_email'],
                        sender_password=st.session_state['sender_password']
                    )
                    
                    results = email_service.send_bulk_renewal_reminders(expiring_members)
                    
                    # Display results
                    st.markdown("<h3>📊 Email Sending Results</h3>", unsafe_allow_html=True)
                    for result in results:
                        if result['Status'] == 'Sent':
                            st.success(f"✅ {result['Member']} ({result['Email']}): {result['Message']}")
                        else:
                            st.error(f"❌ {result['Member']} ({result['Email']}): {result['Message']}")
    else:
        st.markdown(f"""
            <div class="success-box">
                <h3>✅ No members expiring in the next {days_ahead} days!</h3>
            </div>
        """, unsafe_allow_html=True)

# ==================== SETTINGS ====================
elif menu == "⚙️ Settings":
    st.markdown("<h2>⚙️ System Settings</h2>", unsafe_allow_html=True)
    
    st.markdown("<h3>📊 Database Information</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        all_members = db.get_all_members()
        st.markdown("""
            <div class="stat-card">
                <p>DATABASE FILE</p>
                <h2>gym_members.xlsx</h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="stat-card">
                <p>TOTAL RECORDS</p>
                <h2>{len(all_members)}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-card">
                <p>LOCATION</p>
                <h2 style="font-size: 1.2rem;">Current Directory</h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="stat-card">
                <p>LAST UPDATED</p>
                <h2 style="font-size: 1.1rem;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Download backup
    st.markdown("<h3>💾 Backup & Export</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-box">
            <p>💡 Download a backup copy of your database to keep your data safe</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📥 Download Excel Backup", use_container_width=True):
        try:
            with open('gym_members.xlsx', 'rb') as file:
                st.download_button(
                    label="⬇️ Click to Download",
                    data=file,
                    file_name=f"gym_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Danger zone
    st.markdown("<h3>⚠️ Danger Zone</h3>", unsafe_allow_html=True)
    with st.expander("🗑️ Clear All Data (Irreversible!)", expanded=False):
        st.markdown("""
            <div class="danger-box">
                <p>⚠️ WARNING: This will permanently delete all member records!</p>
            </div>
        """, unsafe_allow_html=True)
        
        confirm = st.text_input("Type 'DELETE ALL' to confirm", key="delete_confirm")
        if st.button("🗑️ Delete All Data", type="secondary", use_container_width=True):
            if confirm == "DELETE ALL":
                import os
                if os.path.exists('gym_members.xlsx'):
                    os.remove('gym_members.xlsx')
                    db.initialize_database()
                    st.success("✅ All data deleted and database reset!")
                    st.rerun()
            else:
                st.error("❌ Confirmation text doesn't match!")

# Professional Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.03); 
                border-radius: 8px; margin-top: 2rem; border: 1px solid rgba(255,255,255,0.1);'>
        <h3 style='color: white; margin: 0 0 0.5rem 0; font-weight: 600;'>💪 Gym Management</h3>
        <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.875rem;'>Professional Edition v2.0</p>
        <p style='color: rgba(255,255,255,0.6); margin: 0.5rem 0 0 0; font-size: 0.8rem;'>
            📅 {}</p>
    </div>
""".format(datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)