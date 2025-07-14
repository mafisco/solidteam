import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="SolidITMinds AI Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample data - in a real app, you'd load from files/database
def get_courses():
    return {
        "Operating Systems": [
            {
                "id": "os-001",
                "name": "Linux Administration",
                "duration": "6 weeks",
                "level": "Intermediate",
                "format": "Online Instructor-led",
                "price": "$1,800",
                "next_start": "2023-12-01",
                "description": "Comprehensive training on Linux system administration.",
                "skills": ["Linux installation", "User management", "Security"]
            }
        ],
        "Databases": [
            {
                "id": "db-001",
                "name": "Oracle DBA",
                "duration": "8 weeks",
                "level": "Advanced",
                "format": "Online Instructor-led",
                "price": "$2,500",
                "next_start": "2023-12-01",
                "description": "Comprehensive Oracle Database Administration training.",
                "skills": ["Oracle architecture", "Installation", "Performance tuning"]
            }
        ],
        "Monitoring": [
            {
                "id": "mon-001",
                "name": "Dynatrace Monitoring",
                "duration": "5 weeks",
                "level": "Intermediate",
                "format": "Online Instructor-led",
                "price": "$2,200",
                "next_start": "2023-12-15",
                "description": "Master Dynatrace monitoring platform.",
                "skills": ["Real-time monitoring", "Smart alerting", "Root cause analysis"]
            },
            {
                "id": "mon-002",
                "name": "Prometheus & Grafana",
                "duration": "4 weeks",
                "level": "Intermediate",
                "format": "Online Instructor-led",
                "price": "$1,900",
                "next_start": "2023-12-10",
                "description": "Hands-on training on Prometheus and Grafana.",
                "skills": ["Prometheus setup", "Grafana dashboards", "Alert management"]
            }
        ]
    }

def get_contacts():
    return pd.DataFrame({
        "first_name": ["John", "Jane", "Mike"],
        "last_name": ["Doe", "Smith", "Johnson"],
        "email": ["john@example.com", "jane@example.com", "mike@example.com"],
        "phone": ["555-1234", "555-5678", "555-9012"],
        "type": ["student", "grad", "it_pro"],
        "location": ["Chicago", "New York", "Atlanta"]
    })

def get_payments():
    return pd.DataFrame([
        {"amount": 1500, "description": "AWS Course", "customer": "John Doe", "date": "2023-11-01", "status": "Paid"},
        {"amount": 1000, "description": "Linux Course", "customer": "Jane Smith", "date": "2023-11-05", "status": "Paid"},
        {"amount": 2000, "description": "Oracle DBA", "customer": "Mike Johnson", "date": "2023-11-10", "status": "Pending"}
    ])

# Load data
courses = get_courses()
contacts = get_contacts()
payments = get_payments()

# Navigation
st.sidebar.title("SolidITMinds")
page = st.sidebar.radio("Menu", [
    "🏠 Home",
    "📚 Training",
    "💼 Consulting",
    "👔 Recruiting",
    "📊 Monitoring",
    "📅 Appointments",
    "📧 Campaigns",
    "💰 Payments"
])

# Home Page
if page == "🏠 Home":
    st.title("SolidITMinds AI Platform")
    st.subheader("Your Complete IT Solutions Partner")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        ### Transform Your IT Career or Business
        
        We provide:
        - **Training**: Cutting-edge IT courses
        - **Consulting**: Expert infrastructure solutions
        - **Recruiting**: Top tech talent placement
        """)
        
        st.markdown("""
        ### Popular Courses
        - Dynatrace Monitoring
        - Prometheus & Grafana
        - Oracle DBA
        - Linux Administration
        """)
    
    with col2:
        st.metric("Active Students", "142")
        st.metric("Clients Served", "58")
        st.metric("Job Placements", "43")
        
        with st.expander("Quick Contact"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            if st.button("Submit"):
                st.success("We'll contact you soon!")

# Training Page
elif page == "📚 Training":
    st.title("IT Training Programs")
    
    # Category filter
    category = st.selectbox("Category", list(courses.keys()))
    
    # Display courses
    for course in courses[category]:
        with st.expander(f"{course['name']} - {course['price']}"):
            st.markdown(f"""
            **Duration**: {course['duration']}  
            **Level**: {course['level']}  
            **Next Start**: {course['next_start']}
            """)
            st.markdown(course['description'])
            st.markdown(f"**Skills**: {', '.join(course['skills'])}")
            
            if st.button("Enroll", key=course['id']):
                st.session_state['course'] = course
                st.experimental_rerun()
    
    if 'course' in st.session_state:
        st.subheader(f"Enroll in {st.session_state['course']['name']}")
        with st.form("enroll_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            if st.form_submit_button("Complete Enrollment"):
                st.success("Enrollment submitted!")
                del st.session_state['course']

# Consulting Page
elif page == "💼 Consulting":
    st.title("IT Consulting Services")
    
    tab1, tab2, tab3 = st.tabs(["Database", "OS", "Cloud"])
    
    with tab1:
        st.markdown("""
        ### Database Consulting
        - Design & Implementation
        - Performance Tuning
        - Migration Services
        """)
    
    with tab2:
        st.markdown("""
        ### OS Consulting
        - Linux/Unix Administration
        - Windows Server
        - Security Hardening
        """)
    
    with tab3:
        st.markdown("""
        ### Cloud Consulting
        - AWS Architecture
        - Azure Migration
        - Cost Optimization
        """)
    
    with st.form("consulting_form"):
        st.subheader("Request Consultation")
        name = st.text_input("Name")
        company = st.text_input("Company")
        service = st.selectbox("Service Needed", ["Database", "OS", "Cloud"])
        if st.form_submit_button("Submit Request"):
            st.success("Request received!")

# Recruiting Page
elif page == "👔 Recruiting":
    st.title("Recruiting Solutions")
    
    tab1, tab2 = st.tabs(["For Candidates", "For Employers"])
    
    with tab1:
        st.markdown("""
        ### Job Search Assistance
        - Resume Optimization
        - Interview Coaching
        - Career Counseling
        """)
        
        with st.expander("Current Openings"):
            st.table(pd.DataFrame({
                "Position": ["Linux Admin", "Cloud Engineer", "DBA"],
                "Location": ["Chicago", "Remote", "Atlanta"],
                "Experience": ["3+ years", "2+ years", "5+ years"]
            }))
    
    with tab2:
        st.markdown("""
        ### Hiring Solutions
        - Candidate Screening
        - Technical Assessments
        - Placement Services
        """)
        
        with st.form("employer_form"):
            company = st.text_input("Company Name")
            positions = st.text_area("Positions Needed")
            if st.form_submit_button("Request Talent"):
                st.success("We'll contact you!")

# Monitoring Page
elif page == "📊 Monitoring":
    st.title("Monitoring Dashboard")
    
    st.subheader("Training Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Students", "142", "8+")
    col2.metric("Completion Rate", "87%", "5%")
    col3.metric("Certification Rate", "92%", "3%")
    
    # Progress chart
    progress = pd.DataFrame({
        "Week": [1, 2, 3, 4, 5, 6],
        "Completion": [15, 30, 45, 60, 75, 90]
    })
    st.plotly_chart(px.line(progress, x="Week", y="Completion"))
    
    st.subheader("Monitoring Tools")
    tool = st.selectbox("Select Tool", ["Dynatrace", "Prometheus/Grafana"])
    
    if tool == "Dynatrace":
        st.image("https://www.dynatrace.com/news/wp-content/uploads/2020/10/code-level-metrics-dashboard.png", 
                caption="Dynatrace Dashboard")
    else:
        st.image("https://grafana.com/static/assets/img/grafana/screenshots/grafana-dashboard.png",
                caption="Grafana Dashboard")

# Appointments Page
elif page == "📅 Appointments":
    st.title("Appointment Scheduling")
    
    with st.form("appointment_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        date = st.date_input("Date")
        time = st.time_input("Time")
        if st.form_submit_button("Schedule"):
            st.success(f"Appointment scheduled for {date} at {time}")

# Campaigns Page
elif page == "📧 Campaigns":
    st.title("Email Campaigns")
    
    audience = st.multiselect("Audience", ["Students", "Grads", "IT Pros"])
    subject = st.text_input("Subject", "IT Career Opportunity")
    message = st.text_area("Message")
    
    if st.button("Send Campaign"):
        st.success(f"Campaign sent to {len(audience)} groups")

# Payments Page
elif page == "💰 Payments":
    st.title("Payment Processing")
    
    st.table(payments)
    
    with st.form("payment_form"):
        name = st.text_input("Customer Name")
        amount = st.number_input("Amount", min_value=100)
        course = st.selectbox("Course", ["AWS", "Linux", "Oracle"])
        if st.form_submit_button("Create Invoice"):
            st.success(f"Invoice for ${amount} created")

# Footer
st.markdown("---")
st.markdown("""
**Contact Us**  
📞 (404) 969-6618  
📧 soliditminds@gmail.com  
🌐 www.soliditminds.com
""")
