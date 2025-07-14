import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime
import base64
import plotly.express as px
from PIL import Image
import io

# --------------------------
# Configuration
# --------------------------
st.set_page_config(
    page_title="SITM AI Business Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# Utility Functions
# --------------------------
def send_bulk_emails(subject, message, contacts_df):
    """Send bulk emails to a list of contacts"""
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        email_address = os.getenv("EMAIL_ADDRESS", "your@email.com")
        email_password = os.getenv("EMAIL_PASSWORD", "yourpassword")
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        
        for _, contact in contacts_df.iterrows():
            personalized_msg = message.format(
                first_name=contact.get("first_name", ""),
                last_name=contact.get("last_name", ""),
                location=contact.get("location", ""),
                current_job=contact.get("current_job", "")
            )
            
            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = contact['email']
            msg['Subject'] = subject
            msg.attach(MIMEText(personalized_msg, 'plain'))
            server.send_message(msg)
        
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending emails: {e}")
        return False

def get_calendly_events():
    """Mock function to simulate fetching Calendly events"""
    return [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "555-123-4567",
            "date": "2023-12-15 14:30",
            "type": "Consultation",
            "notes": "Interested in AWS training"
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "555-987-6543",
            "date": "2023-12-16 10:00",
            "type": "Career Advice",
            "notes": "Recent graduate looking for guidance"
        }
    ]

def create_payment_link(amount, description, customer):
    """Mock function to simulate payment link creation"""
    return "https://checkout.stripe.com/pay/test_link"

def generate_audio(text):
    """Generate simple audio without external dependencies"""
    # In a real implementation, you would use a proper TTS service
    # This is just a placeholder that returns a sample audio
    audio_base64 = """
    UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU...
    """  # Truncated for brevity
    return io.BytesIO(base64.b64decode(audio_base64))

# --------------------------
# Page Functions
# --------------------------
def email_campaigns_page():
    st.title("📧 Email Campaign Manager")
    
    st.subheader("Target Audience")
    audience_options = {
        "College Students": pd.DataFrame({
            "email": ["student1@university.edu", "student2@college.edu"],
            "first_name": ["Alex", "Jamie"],
            "last_name": ["Johnson", "Smith"],
            "location": ["Atlanta", "Chicago"]
        }),
        "Recent Graduates": pd.DataFrame({
            "email": ["grad1@alumni.edu", "grad2@alumni.edu"],
            "first_name": ["Taylor", "Morgan"],
            "last_name": ["Williams", "Brown"],
            "location": ["New York", "Los Angeles"]
        })
    }
    
    selected_audiences = st.multiselect(
        "Select target groups:",
        list(audience_options.keys()),
        default=["College Students"]
    )
    
    st.subheader("Compose Your Message")
    subject = st.text_input("Subject:", "Kickstart Your 6-Figure IT Career in 90-120 Days")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        message = st.text_area("Email Body:", """Hi {first_name},

Are you ready to transform your career? SolidITMinds offers elite training programs that can get you to six figures in just 90-120 days!

Our programs in:
- Cloud Computing (AWS, Azure)
- Database Administration
- DevOps
- Operating Systems

Book a free consultation: [Insert Calendly Link]
""")
    
    with col2:
        st.markdown("**Personalization Tags**")
        st.code("{first_name}\n{last_name}\n{location}\n{current_job}")
    
    if st.button("Review & Send Campaign"):
        combined_df = pd.concat([audience_options[audience] for audience in selected_audiences])
        st.success(f"Ready to send to {len(combined_df)} contacts!")
        
        if st.button("Confirm Send"):
            if send_bulk_emails(subject, message, combined_df):
                st.success("Campaign sent successfully!")

def bookings_page():
    st.title("📅 Appointment Scheduling")
    
    st.subheader("Upcoming Appointments")
    appointments = get_calendly_events()
    
    if appointments:
        for appt in appointments:
            with st.expander(f"{appt['name']} - {appt['date']}"):
                st.write(f"**Email:** {appt['email']}")
                st.write(f"**Phone:** {appt['phone']}")
                st.write(f"**Type:** {appt['type']}")
                st.write(f"**Notes:** {appt['notes']}")
    else:
        st.info("No upcoming appointments found.")
    
    st.subheader("Book New Appointment")
    st.markdown("""
    ### Book with SITM
    [Schedule a free consultation on Calendly](https://calendly.com/soliditminds/30min)
    """)

def payments_page():
    st.title("💰 Payment Processing")
    
    st.subheader("Training Program Payment Plans")
    plan = st.radio("Select Payment Option:", [
        "💰 Full Payment ($3,500 - Save $500)",
        "💳 3-Month Installment ($1,500 + $1,000 x 2 = $3,500)",
        "📅 Custom Payment Plan"
    ])
    
    with st.form("payment_info"):
        st.subheader("Student Information")
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First Name")
        last_name = col2.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        course = st.selectbox("Select Course", [
            "AWS Cloud Practitioner",
            "Linux Administration",
            "Oracle DBA",
            "DevOps Engineering"
        ])
        
        submitted = st.form_submit_button("Generate Payment Link")
        
        if submitted:
            if plan == "💰 Full Payment ($3,500 - Save $500)":
                amount = 3500
                description = f"Full payment for {course}"
            elif plan == "💳 3-Month Installment ($1,500 + $1,000 x 2 = $3,500)":
                amount = 1500
                description = f"First installment for {course}"
            else:
                amount = st.number_input("Custom Amount", min_value=500, max_value=3500)
                description = f"Custom payment for {course}"
            
            payment_link = create_payment_link(amount, description, {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone
            })
            
            st.success("Payment link generated!")
            st.markdown(f"""
            ### Payment Instructions
            [Click here to complete your payment]({payment_link})
            """)

def training_page():
    st.title("📚 Training Programs")
    
    courses = {
        "Operating Systems": [
            {"name": "Linux Administration", "duration": "6 weeks", "level": "Intermediate", "price": "$1,200"},
            {"name": "Windows Server", "duration": "4 weeks", "level": "Beginner", "price": "$950"}
        ],
        "Databases": [
            {"name": "Oracle DBA", "duration": "8 weeks", "level": "Advanced", "price": "$1,800"},
            {"name": "MySQL Fundamentals", "duration": "4 weeks", "level": "Beginner", "price": "$850"}
        ],
        "DevOps": [
            {"name": "Docker & Kubernetes", "duration": "6 weeks", "level": "Intermediate", "price": "$1,500"},
            {"name": "Terraform & Ansible", "duration": "5 weeks", "level": "Intermediate", "price": "$1,350"}
        ]
    }
    
    selected_category = st.sidebar.selectbox("Category", ["All"] + list(courses.keys()))
    search_query = st.sidebar.text_input("Search Courses")
    
    if selected_category == "All":
        for category, items in courses.items():
            st.subheader(category)
            for course in items:
                if not search_query or search_query.lower() in course["name"].lower():
                    with st.expander(f"🎯 {course['name']} - {course['duration']}"):
                        st.markdown(f"""
                        **Level:** {course['level']}  
                        **Price:** {course['price']}
                        """)
                        if st.button("Enroll Now", key=f"enroll_{course['name']}"):
                            st.session_state['selected_course'] = course
    
    else:
        st.subheader(selected_category)
        for course in courses[selected_category]:
            if not search_query or search_query.lower() in course["name"].lower():
                with st.expander(f"🎯 {course['name']} - {course['duration']}"):
                    st.markdown(f"""
                    **Level:** {course['level']}  
                    **Price:** {course['price']}
                    """)
                    if st.button("Enroll Now", key=f"enroll_{course['name']}"):
                        st.session_state['selected_course'] = course
    
    if 'selected_course' in st.session_state:
        st.subheader(f"Enroll in {st.session_state['selected_course']['name']}")
        with st.form("enrollment_form"):
            col1, col2 = st.columns(2)
            first_name = col1.text_input("First Name")
            last_name = col2.text_input("Last Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            
            if st.form_submit_button("Submit Enrollment"):
                st.success("Enrollment submitted! Our team will contact you shortly.")
                del st.session_state['selected_course']

def social_media_page():
    st.title("📢 Social Media Content Generator")
    
    platforms = {
        "LinkedIn": {"max_chars": 1300},
        "Twitter/X": {"max_chars": 280},
        "Facebook": {"max_chars": 8000},
        "Instagram": {"max_chars": 2200}
    }
    
    selected_platform = st.selectbox("Select Platform", list(platforms.keys()))
    topic = st.text_input("Post Topic", "How to start a six-figure IT career")
    tone = st.selectbox("Tone", ["Professional", "Motivational", "George Carlin-style"])
    
    if st.button("Generate Post"):
        sample_post = f"""🚀 {topic} with SolidITMinds!

We can train you for a six-figure IT career in just 90-120 days. No fluff, just results.

✅ Hands-on training
✅ Expert instructors
✅ Job placement support

Ready to transform your career? DM us or visit soliditminds.com"""

        st.text_area("Generated Post", sample_post, height=200)
        st.markdown("**Suggested Hashtags:**")
        st.code("#ITCareer #TechJobs #CloudComputing #DevOps #SixFigureSalary")
        
        if st.button("Generate Voiceover"):
            audio_file = generate_audio(sample_post)
            st.audio(audio_file, format="audio/wav")

def monitoring_page():
    st.title("📊 Performance Monitoring Dashboard")
    
    st.subheader("Monitoring Tools")
    tools = st.multiselect("Select Tools", ["Prometheus & Grafana", "Dynatrace"], default=["Prometheus & Grafana"])
    
    st.subheader("Student Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Students", "142", "+8 this week")
    col2.metric("Completion Rate", "87%", "+5%")
    col3.metric("Certification Rate", "92%", "3% above avg")
    
    progress_data = pd.DataFrame({
        "Week": [1, 2, 3, 4, 5, 6, 7, 8],
        "Avg Progress": [10, 25, 40, 55, 70, 80, 90, 95]
    })
    
    fig = px.line(progress_data, x="Week", y="Avg Progress", title="8-Week Training Progress")
    st.plotly_chart(fig)
    
    if "Prometheus & Grafana" in tools:
        st.subheader("Prometheus & Grafana Metrics")
        st.image("https://grafana.com/static/assets/img/blog/mixed_styles.png", caption="Sample Monitoring Dashboard")

def crm_page():
    st.title("🤝 CRM Dashboard")
    
    st.subheader("Lead Management")
    tab1, tab2, tab3 = st.tabs(["All Leads", "New", "Converted"])
    
    with tab1:
        st.dataframe(pd.DataFrame({
            "Name": ["John Doe", "Jane Smith"],
            "Email": ["john@example.com", "jane@example.com"],
            "Status": ["Contacted", "New"],
            "Source": ["Website", "Referral"]
        }))
    
    st.subheader("Student Tracking")
    student = st.selectbox("Select Student", ["John Doe", "Jane Smith"])
    
    if student:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **Course:** AWS Cloud Practitioner  
            **Progress:** 65%  
            **Last Active:** 2 days ago
            """)
            st.progress(65)
        
        with col2:
            st.markdown("""
            **Assessment Scores:**  
            - Week 1: 92%  
            - Week 2: 88%  
            - Week 3: 95%
            """)

# --------------------------
# Main App
# --------------------------
def main():
    # Sidebar navigation
    st.sidebar.title("SITM Navigation")
    page = st.sidebar.radio("Choose a module:", [
        "🏠 Dashboard",
        "📧 Email Campaigns",
        "📅 Book Appointments",
        "💰 Payment Processing",
        "📚 Training Programs",
        "📢 Social Media",
        "📊 Performance Monitoring",
        "🤝 CRM Dashboard"
    ])
    
    # Main content
    if page == "🏠 Dashboard":
        st.title("🤖 SITM AI Business Agent")
        st.subheader("Your 24/7 Consulting, Training & Recruiting Assistant")
        
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("""
            ## Welcome to SITM (SaiTim)
            
            **Smart Consulting | Elite Training | Targeted Recruiting**
            
            SITM is your AI-powered business partner that automates:
            - 📧 Email campaigns
            - 📅 Appointment booking
            - 💰 Payment processing
            - 📢 Social media
            - 📊 Performance tracking
            """)
        
        with col2:
            st.video("https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4")
        
        st.markdown("---")
        st.subheader("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Active Students", "142")
        col2.metric("Revenue", "$48,750")
        col3.metric("Open Positions", "23")
        col4.metric("Social Reach", "12.4K")
    
    elif page == "📧 Email Campaigns":
        email_campaigns_page()
    elif page == "📅 Book Appointments":
        bookings_page()
    elif page == "💰 Payment Processing":
        payments_page()
    elif page == "📚 Training Programs":
        training_page()
    elif page == "📢 Social Media":
        social_media_page()
    elif page == "📊 Performance Monitoring":
        monitoring_page()
    elif page == "🤝 CRM Dashboard":
        crm_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Contact SITM Support**  
    📞 IL: (224) 622-4202 | GA: (404) 969-6618  
    📧 soliditminds@gmail.com | mafany27@msn.com  
    🌐 [www.soliditminds.com](https://www.soliditminds.com)
    """)

if __name__ == "__main__":
    main()
