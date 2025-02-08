import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image, ImageFile
import sqlite3

# Prevent truncated image error
ImageFile.LOAD_TRUNCATED_IMAGES = True  

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    user_type TEXT,
    license_number TEXT
)
""")
conn.commit()

# Streamlit Page Config
st.set_page_config(
    page_title="Bone Health AI Suite",
    page_icon="🦴",
    layout="wide"
)

# Header Section
st.markdown(
    """
    <h1 style="text-align: center; color: #2E86C1;">🌌 Bone Health AI Suite</h1>
    <h4 style="text-align: center; color: #5D6D7E;">AI-powered analysis for bone fractures, osteoporosis, and more.</h4>
    <hr style="border: 1px solid #D5D8DC;">
    """,
    unsafe_allow_html=True
)

# Function to authenticate users
def authenticate(username, password):
    cursor.execute("SELECT user_type FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    return user[0] if user else None

# Function to register users
def register(username, password, user_type, license_number=None):
    try:
        cursor.execute("INSERT INTO users (username, password, user_type, license_number) VALUES (?, ?, ?, ?)",
                       (username, password, user_type, license_number))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Login/Signup System
st.sidebar.title("🔐 Login / Signup")
auth_option = st.sidebar.radio("Choose an option:", ["Login", "Signup"])

if auth_option == "Signup":
    st.sidebar.subheader("Create a new account")
    new_username = st.sidebar.text_input("Username")
    new_password = st.sidebar.text_input("Password", type="password")
    user_type = st.sidebar.radio("Select User Type:", ["Common User", "Doctor"])
    license_number = st.sidebar.text_input("Medical License Number (Only for Doctors)") if user_type == "Doctor" else None
    if st.sidebar.button("Signup"):
        if register(new_username, new_password, user_type, license_number):
            st.sidebar.success("✅ Account created successfully. Please login.")
        else:
            st.sidebar.error("❌ Username already exists!")

elif auth_option == "Login":
    st.sidebar.subheader("Login to your account")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user_role = authenticate(username, password)
        if user_role:
            st.session_state["logged_in"] = True
            st.session_state["user_type"] = user_role
            st.session_state["username"] = username
            st.sidebar.success(f"✅ Logged in as {user_role}")
        else:
            st.sidebar.error("❌ Invalid credentials!")

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠️ Please log in to access the AI analysis tool.")
    st.stop()

# Expertise Selection
st.subheader("🦴 Select the analysis you want to perform")
task = st.radio("Choose a task:", [
    "Bone Fracture Detection",
    "Bone Marrow Cell Classification",
    "Knee Joint Osteoarthritis Detection",
    "Osteoporosis Stage Prediction & BMD Score",
    "Bone Age Detection",
    "Cervical Spine Fracture Detection"
])

# Image uploader
uploaded_file = st.file_uploader("📤 Upload an X-ray or biopsy image...", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=350, use_container_width=False)

additional_input = st.text_area("📝 Provide additional details if necessary")
submit_button = st.button("🔍 Analyze")

# Function to get AI response
def get_gemini_response(task_prompt, user_type, image=None, additional_input=""):
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
    expertise_prompt = "Generate a response suitable for a " + ("common user" if user_type == "Common User" else "doctor")
    input_data = [task_prompt, expertise_prompt, additional_input]
    if image:
        input_data.insert(1, image[0])
    response = model.generate_content(input_data)
    return response.text

if submit_button:
    if not uploaded_file:
        st.warning("🚨 Please upload an image before analyzing.")
        st.stop()
    
    task_prompts = {
    "Bone Fracture Detection": (
        "Analyze the X-ray image for fractures and classify into different fracture types with detailed severity assessment. "
        "For common users: Provide healing measures, recommended nutrition, exercises, and prevention steps for faster recovery. "
        "For doctors: Suggest medical treatment options, possible surgeries, immobilization techniques, and follow-up care strategies."
    ),
    
    "Bone Marrow Cell Classification": (
        "Analyze the biopsy image and classify bone marrow cells into relevant categories, identifying concerning cells. "
        "For common users: Explain the significance of detected cell types and provide basic guidance on maintaining bone health. "
        "For doctors: Provide detailed insights into abnormal cell structures, possible diagnoses, and recommended medical interventions."
    ),
    
    "Knee Joint Osteoarthritis Detection": (
        "Analyze the knee X-ray and classify osteoarthritis severity based on clinical grading. "
        "For common users: Provide lifestyle modifications, exercises, diet, and pain management strategies. "
        "For doctors: Suggest advanced treatments, medications, physiotherapy plans, and surgical options such as knee replacement."
    ),
    
    "Osteoporosis Stage Prediction & BMD Score": (
        "Analyze the bone X-ray and determine osteoporosis stage with estimated Bone Mineral Density (BMD) score. "
        "For common users: Offer guidance on calcium-rich diet, supplements, exercise routines, and ways to prevent further bone loss. "
        "For doctors: Recommend specific medications, hormone therapy, and advanced treatments to manage and prevent complications."
    ),
    
    "Bone Age Detection": (
        "Analyze the X-ray of a child's hand and predict bone age with insights into growth patterns. "
        "For common users: Explain how bone age relates to growth, provide nutrition tips, and suggest exercises for optimal development. "
        "For doctors: Offer insights into growth abnormalities, hormonal imbalances, and necessary medical interventions if delayed growth is detected."
    ),
    
    "Cervical Spine Fracture Detection": (
        "Analyze the CT scan of the cervical spine for fractures and provide a severity assessment. "
        "For common users: Provide information on precautions, pain management, and recommended postural corrections. "
        "For doctors: Suggest medical treatment plans, possible surgical options, and rehabilitation strategies for full recovery."
    )
}

    
    image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
    response = get_gemini_response(task_prompts[task], st.session_state["user_type"], image_data, additional_input)
    
    st.markdown("<h4 style='color: #27AE60;'>📊 Analysis Result</h4>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background-color:#E8F5E9;padding:15px;border-radius:10px;font-size:16px;color:#1B2631;'>{response}</div>",
        unsafe_allow_html=True
    )
