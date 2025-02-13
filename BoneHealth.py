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

# Function to get AI response
def get_gemini_response(task_prompt, user_type, image=None, additional_input=""):
    """Generates AI response using Google's Gemini model"""
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

    # Expertise level prompt based on user type
    expertise_prompt = f"Generate a response suitable for a {'common user' if user_type == 'Common User' else 'doctor'}"

    input_data = [task_prompt, expertise_prompt, additional_input]

    # Include image if provided
    if image:
        input_data.insert(1, image[0])

    response = model.generate_content(input_data)
    return response.text

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

# Authentication Functions
def authenticate(username, password):
    cursor.execute("SELECT user_type FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    return user[0] if user else None

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
            # Account switch handling: Clear session state if username changed
            if "username" in st.session_state and st.session_state["username"] != username:
                st.session_state.pop('message_log', None)
                st.session_state.pop('analysis_context', None)
                st.session_state.pop('uploaded_image', None)
                st.session_state.pop('selected_task', None) # Optionally clear selected task as well

            st.session_state["logged_in"] = True
            st.session_state["user_type"] = user_role
            st.session_state["username"] = username
            if "message_log" not in st.session_state:
                st.session_state.message_log = [{"role": "ai", "content": "👋 Welcome to Bone Health AI Suite! How can I help you today?"}] # Initial message for new login
            st.sidebar.success(f"✅ Logged in as {user_role}")
        else:
            st.sidebar.error("❌ Invalid credentials!")

# Initialize message_log if not present (for first login)
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "👋 Welcome to Bone Health AI Suite! Please log in to start."}]

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠️ Please log in to access the AI analysis tool.")
    st.stop()

# Task Selection
st.subheader("🦴 Select the analysis you want to perform")
task = st.radio("Choose a task:", [
    "Bone Fracture Detection",
    "Bone Marrow Cell Classification",
    "Knee Joint Osteoarthritis Detection",
    "Osteoporosis Stage Prediction & BMD Score",
    "Bone Age Detection",
    "Cervical Spine Fracture Detection",
    "Bone Tumor/Cancer Detection",
    "Bone Infection (Osteomyelitis) Detection"
])

# Define task prompts
task_prompts = {
    "Bone Fracture Detection": (
        "Analyze the X-ray, MRI, or CT scan image for fractures only and classify into different fracture types with detailed severity assessment. "
        "For common users: The image will be analyzed to check for fractures, identifying the affected bone and the type of break. "
        "You will receive an easy-to-understand explanation of the fracture, including its severity and possible effects on movement, provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Suggest medical treatment options, possible surgeries, immobilization techniques, and follow-up care strategies,provide nutrition plan,steps to recover like remedies and exercises if required. "
    ),

    "Bone Marrow Cell Classification": (
        "Analyze the biopsy or MRI image and classify bone marrow cells only into relevant categories, identifying concerning cells. "
        "For common users: The image will be analyzed to check for abnormalities in bone marrow cells. "
        "You will receive a simple explanation of the findings, including whether there are unusual cell changes and what they might indicate,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Provide detailed insights into abnormal cell structures, possible diagnoses, and recommended medical interventions,provide nutrition plan,steps to recover like remedies and exercises if required. "
    ),

    "Knee Joint Osteoarthritis Detection": (
        "Analyze the knee X-ray or MRI and classify osteoarthritis severity only based on clinical grading. "
        "For common users: The image will be assessed for signs of knee osteoarthritis, including joint space narrowing and bone changes. "
        "You will get an easy-to-understand report on whether osteoarthritis is present and its severity level, along with its impact on knee function,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Suggest advanced treatments, medications, physiotherapy plans, and surgical options such as knee replacement,provide nutrition plan,steps to recover like remedies and exercises if required."

    ),

    "Osteoporosis Stage Prediction & BMD Score": (
        "Analyze the bone X-ray and determine osteoporosis stage only with estimated Bone Mineral Density (BMD) score. "
        "For common users: The scan will be analyzed to determine how strong or weak the bones are and whether osteoporosis is present. "
        "You will receive a simple explanation of the results, including whether bone density is lower than normal and what it means for bone health,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Recommend specific medications, hormone therapy, and advanced treatments to manage and prevent complications,provide nutrition plan,steps to recover like remedies and exercises if required."
    ),

    "Bone Age Detection": (
        "Analyze the X-ray of a child's hand and predict bone age only with insights into growth patterns. "
        "For common users: The scan will be assessed to check how well the bones are developing compared to the expected growth pattern for the child’s age. "
        "You will receive an easy-to-understand result explaining whether the bone growth is normal, advanced, or delayed,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Offer insights into growth abnormalities, hormonal imbalances, and necessary medical interventions if delayed growth is detected,provide nutrition plan,steps to recover like remedies and exercises if required."
    ),

    "Cervical Spine Fracture Detection": (
        "Analyze the X-ray, MRI, or CT scan of the cervical spine only for fractures and provide a severity assessment. "
        "For common users: The scan will be analyzed for fractures in the neck bones, and you will receive an explanation of the findings. "
        "The report will describe whether a fracture is present, its severity, and how it may affect movement or pain levels,provide nutrition plan,steps to recover like remedies and exercises if required"
        "For doctors: Suggest medical treatment plans, possible surgical options, and rehabilitation strategies for full recovery,provide nutrition plan,steps to recover like remedies and exercises if required"
    ),

    "Bone Tumor/Cancer Detection": (
        "Analyze the X-ray, MRI, CT scan, or biopsy image for possible bone tumors or cancerous growths only. "
        "For common users: The image will be checked for any unusual growths or masses in the bone, and you will receive a simple explanation of the findings. "
        "If any suspicious areas are detected, the report will describe their size, location, and whether they appear concerning,provide nutrition plan,steps to recover like remedies and exercises if required."
        "For doctors: Provide detailed insights into tumor classification, possible malignancy assessment, and treatment options,provide nutrition plan,steps to recover like remedies and exercises if required. "
    ),

    "Bone Infection (Osteomyelitis) Detection": (
        "Analyze the X-ray, MRI, CT scan, or biopsy image for signs of bone infection (osteomyelitis) only. "
        "For common users: The image will be checked for any signs of infection in the bone, such as swelling, bone damage, or abscess formation. "
        "You will receive an easy-to-understand explanation of whether an infection is present and how it may be affecting the bone,provide nutrition plan,steps to recover like remedies and exercises if required."
        "For doctors: Provide insights on infection severity, possible antibiotic treatments, and surgical recommendations if needed,provide nutrition plan,steps to recover like remedies and exercises if required."
    )
}

# Store the task prompt
task_prompt = task_prompts.get(task, "Perform the selected medical imaging analysis.")

# Clear previous responses and uploaded image when switching tasks
if "selected_task" not in st.session_state or st.session_state.selected_task != task:
    st.session_state.selected_task = task
    st.session_state.message_log = [{"role": "ai", "content": f"📢 You are now analyzing: **{task}**. Please upload an image and ask questions."}]
    st.session_state.pop("uploaded_image", None)

# Image uploader
uploaded_file = st.file_uploader("📤 Upload an X-ray, CT scan, MRI, or biopsy image...", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.session_state.uploaded_image = uploaded_file
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=350, use_container_width=False)

# Analyze button
if st.button("🔍 Analyze"):
    if uploaded_file:
        with st.spinner("🧠 Analyzing..."):
            image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
            ai_analysis = get_gemini_response(task_prompt, st.session_state["user_type"], image_data)

            # Store the analysis context in session_state for later use
            st.session_state["analysis_context"] = ai_analysis

            # Add analysis result to message log
            st.session_state.message_log.append({"role": "ai", "content": ai_analysis})
            st.success("✅ Analysis Complete! See results below.")
    else:
        st.warning("⚠️ Please upload an image before analyzing.")

# Chat container
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# Chat input
irrelevant_keywords = ["pm", "president", "capital", "weather", "politics", "sports"]
greeting_keywords = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
appreciation_keywords = ["thank you", "thanks", "great work", "well done", "appreciate", "good job"]

user_query = st.chat_input("Ask follow-up questions or request detailed analysis...")

if user_query:
    # Display user query in chat
    st.session_state.message_log.append({"role": "user", "content": user_query})

    response_text = ""

    # Respond to greetings (ensure it only matches standalone greetings)
    if any(word.lower() == user_query.lower().strip() for word in greeting_keywords):
        response_text = "😊 Hello! How can I assist you today?"

    # Respond to appreciation
    elif any(word in user_query.lower() for word in appreciation_keywords):
        response_text = "🙏 You're very welcome! I'm glad I could help. Let me know if there's anything else I can do for you. 😊"

    # Check for irrelevant keywords
    elif any(word in user_query.lower() for word in irrelevant_keywords):
        response_text = "⚠️ Please ask relevant questions related to the selected analysis."

    # Process normal queries
    else:
        # Generate a response using the analysis context
        analysis_context = st.session_state.get("analysis_context", None)
        if analysis_context:
            response_text = get_gemini_response(
                task_prompt="Answer the follow-up question based on the previous context.",
                user_type=st.session_state["user_type"],
                additional_input=f"Context: {analysis_context}\nUser Query: {user_query}"
            )
        else:
            response_text = "⚠️ I don't have any analysis context to refer to. Please analyze an image first or provide more details about your question."

    # Display AI response
    st.session_state.message_log.append({"role": "ai", "content": response_text})
    st.rerun()
