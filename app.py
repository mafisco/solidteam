import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import time
import json

# ======================
# 🧩 CORE FUNCTIONALITY
# ======================

class Faker:
    """Built-in data generator"""
    def __init__(self):
        self.first_names = ["Alex", "Jamie", "Taylor", "Casey", "Morgan", "Jordan"]
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
        self.companies = ["Tech", "Solutions", "Global", "Innovations", "Data"]
        self.jobs = ["Cloud Engineer", "DevOps", "DBA", "Solutions Architect"]
        self.cities = ["Atlanta", "New York", "Chicago", "Austin", "London", "Berlin"]
        
    def name(self):
        return f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
    
    def email(self, name=None):
        name = name or self.name().replace(" ", "").lower()
        return f"{name}{random.randint(10,99)}@example.com"
    
    def phone(self):
        return f"{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"
    
    def company(self):
        return f"{random.choice(self.companies)} {random.choice(['Inc', 'LLC', 'Corp'])}"
    
    def date(self, days=365):
        return (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, days))).strftime("%Y-%m-%d")

class SITM:
    """Main application class"""
    def __init__(self):
        self.fake = Faker()
        self.training_programs = {
            "AWS": {"price": 3500, "duration": "12 weeks", "placement": 0.92},
            "DevOps": {"price": 4000, "duration": "14 weeks", "placement": 0.89},
            "Database": {"price": 3200, "duration": "10 weeks", "placement": 0.85}
        }
        
    def generate_leads(self, n=1000, lead_type="student"):
        leads = []
        for _ in range(n):
            if lead_type == "student":
                leads.append({
                    "Name": self.fake.name(),
                    "Email": self.fake.email(),
                    "Phone": self.fake.phone(),
                    "Interest": random.choice(list(self.training_programs.keys())),
                    "Status": "New"
                })
            else:  # Corporate
                leads.append({
                    "Company": self.fake.company(),
                    "Contact": self.fake.name(),
                    "Email": self.fake.email(),
                    "Budget": f"${random.randint(5000, 50000)}"
                })
        return pd.DataFrame(leads)

# ======================
# 🖥️ STREAMLIT APP
# ======================

# Initialize
COMPANY_NAME = "SolidITMinds"
AGENT_NAME = "SITM (SaiTim)"
sitm = SITM()

if 'leads' not in st.session_state:
    st.session_state.leads = None

# App layout
st.set_page_config(layout="wide", page_title=f"{AGENT_NAME} | {COMPANY_NAME}")
st.title(f"🌟 {AGENT_NAME} - IT Training Platform")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    app_mode = st.selectbox("Choose Module", [
        "Lead Generator",
        "Training Programs", 
        "Payment Portal",
        "Placement Tracker"
    ])
    
    st.divider()
    st.write(f"**{COMPANY_NAME}**")
    st.caption("AI-Powered IT Training System")

# Lead Generator
if app_mode == "Lead Generator":
    st.header("📊 Lead Generation")
    
    col1, col2 = st.columns(2)
    with col1:
        lead_type = st.radio("Lead Type", ["Students", "Corporate"])
        num_leads = st.slider("Number of Leads", 100, 10000, 1000)
        
        if st.button("Generate Leads"):
            st.session_state.leads = sitm.generate_leads(num_leads, lead_type.lower())
            st.success(f"Generated {num_leads} {lead_type.lower()} leads!")
    
    with col2:
        if st.session_state.leads is not None:
            st.dataframe(st.session_state.leads.head(10))
            if st.button("Export Leads"):
                st.success("Leads exported to CSV")

# Training Programs
elif app_mode == "Training Programs":
    st.header("🎓 Training Programs")
    
    program = st.selectbox("Select Program", list(sitm.training_programs.keys()))
    program_data = sitm.training_programs[program]
    
    st.write(f"""
    ### {program} Training
    - **Duration:** {program_data['duration']}
    - **Price:** ${program_data['price']}
    - **Placement Rate:** {program_data['placement']*100}%
    """)
    
    if st.button("Enroll Now"):
        st.session_state.current_program = program
        st.success(f"Selected {program} program!")

# Payment Portal
elif app_mode == "Payment Portal":
    st.header("💳 Payment Processing")
    
    if 'current_program' not in st.session_state:
        st.warning("Please select a program first")
        st.stop()
    
    program = st.session_state.current_program
    price = sitm.training_programs[program]["price"]
    
    st.write(f"""
    ### {program} Program
    - **Total Cost:** ${price}
    - **Duration:** {sitm.training_programs[program]['duration']}
    """)
    
    payment_method = st.selectbox("Payment Method", [
        "Credit Card",
        "Installments (3 months)",
        "County Sponsorship"
    ])
    
    if st.button("Complete Enrollment"):
        receipt = {
            "Program": program,
            "Amount": price,
            "Method": payment_method,
            "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Status": "Confirmed"
        }
        st.json(receipt)
        st.balloons()
        st.success("Enrollment confirmed!")

# Placement Tracker
elif app_mode == "Placement Tracker":
    st.header("📈 Placement Analytics")
    
    # Generate sample data
    placements = []
    for _ in range(100):
        program = random.choice(list(sitm.training_programs.keys()))
        placements.append({
            "Name": sitm.fake.name(),
            "Program": program,
            "Company": sitm.fake.company(),
            "Salary": f"${random.randint(80, 180)}k",
            "Hired": sitm.fake.date(180)
        })
    
    df = pd.DataFrame(placements)
    
    # Filters
    program_filter = st.multiselect(
        "Filter by Program", 
        list(sitm.training_programs.keys()),
        default=list(sitm.training_programs.keys())
    )
    
    # Display
    filtered_df = df[df["Program"].isin(program_filter)]
    st.dataframe(filtered_df)
    
    # Simple metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Placements", len(filtered_df))
    with col2:
        avg_salary = np.mean([int(x.replace('k','').replace('$','')) for x in filtered_df["Salary"]])
        st.metric("Average Salary", f"${avg_salary:,.0f}k")

# Footer
st.divider()
st.caption(f"© {datetime.datetime.now().year} {COMPANY_NAME} | v1.0")
