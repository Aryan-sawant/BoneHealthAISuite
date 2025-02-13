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
    license_number TEXT,
    specialization TEXT,
    affiliation TEXT
)
""")
conn.commit()

# Streamlit Page Config - Landscape and Wide Layout
st.set_page_config(
    page_title="Bone Health AI Suite",
    page_icon="🦴",
    layout="wide"
)

# Premium CSS Styling with Cobalt Blue Theme
st.markdown(
    """
    <style>
    body {
        /* background-color: #f0f2f6;  Old background */
        background: linear-gradient(to bottom, #E6F7FF, #C0E0FF); /* Light Cobalt Blue gradient background */
        color: #2E4053; /* Darker text for better contrast on light blue */
        font-family: 'Helvetica Neue', sans-serif;
        overflow: hidden;
    }

    .stApp {
        max-width: 100vw;
        min-height: 100vh;
        margin: 0;
        padding: 25px 30px;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        background: transparent; /* Make stApp background transparent */
    }

    .highlight-box {
        background: linear-gradient(135deg, #A9CCE3, #D4E6F1); /* Cobalt Blue highlight box gradient */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 8px 8px 15px rgba(0,0,0,0.15), -5px -5px 10px rgba(255,255,255,0.6);
        animation: fadeIn 1.5s ease-out forwards; /* Added Fade-in Animation */
        opacity: 0;
    }
    @keyframes fadeIn {
        to { opacity: 1; }
    }


    .highlight-box:hover {
        box-shadow: 10px 10px 20px rgba(0,0,0,0.18), -7px -7px 12px rgba(255,255,255,0.7);
        transform: scale(1.005);
    }

    .highlight-box h1 { /* Enhanced Main Title Styling */
        color: #0B5394; /* Darker Cobalt Blue for heading */
        font-size: 3.2em; /* Increased size */
        margin-bottom: 8px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 255, 255, 0.5); /* Enhanced shadow & glow */
        font-weight: 700; /* Bold font weight */
        letter-spacing: -1.5px; /* Tighter letter spacing */
        animation: pulseTitle 3s infinite alternate, fadeInTitle 1.5s ease-out forwards 0.5s; /* Pulse animation and staggered fade-in */
        opacity: 0;
        transition: text-shadow 0.3s ease;
    }

    @keyframes fadeInTitle {
        to { opacity: 1; }
    }

    @keyframes pulseTitle {
        0% { text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 255, 255, 0.5); transform: scale(1); }
        100% { text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.25), 0 0 12px rgba(255, 255, 255, 0.7); transform: scale(1.02); }
    }


    .highlight-box h4 {
        color: #4D5656; /* Slightly darker paragraph text */
        font-size: 1.1em;
        margin-bottom: 15px;
        text-shadow: 0.5px 0.5px 1px rgba(255, 255, 255, 0.5);
        font-style: normal; /* Removed italic style */
        font-weight: 500; /* Adjusted font weight */
        opacity: 0.9;
    }

    /* Task Option Box Styling - Cobalt Blue Gradient Background */
    .task-option-box {
        background: linear-gradient(135deg, #A9CCE3, #D4E6F1); /* Cobalt Blue task box gradient - More Saturated */
        padding: 20px;
        border-radius: 15px; /* More rounded corners */
        margin-bottom: 25px;
        box-shadow:
            12px 12px 20px rgba(0,0,0,0.1), /* Stronger primary shadow */
            -8px -8px 15px rgba(255,255,255,0.7); /* Softer highlight shadow */
        transition: box-shadow 0.3s ease, transform 0.3s ease;
        animation: fadeInUp 1s ease-out forwards 0.8s; /* Fade-in up animation for task box */
        transform: translateY(20px);
        opacity: 0;
        border: 2px solid #85C1E9; /* Added border for better definition */
    }

    @keyframes fadeInUp {
        to { transform: translateY(0); opacity: 1; }
    }


    .task-option-box:hover {
        box-shadow:
            15px 15px 25px rgba(0,0,0,0.12), /* Slightly stronger hover shadow */
            -10px -10px 18px rgba(255,255,255,0.8); /* Brighter hover highlight */
        transform: scale(1.01); /* Gentle scale up on hover */
    }

    .task-option-box h2 { /* Style inside the task box if needed */
        color: #0B5394; /* Darker Cobalt Blue for task box heading */
        font-size: 1.9em; /* Slightly larger than highlight-box h2 */
        margin-bottom: 10px;
        text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.8); /* Refined text shadow */
        font-weight: bold;
        opacity: 1;
        letter-spacing: -0.8px; /* Slightly tighter letter spacing */
        animation: fadeInText 1s ease-out forwards 1.2s; /* Fade-in animation with delay */
        opacity: 0;
    }
    @keyframes fadeInText {
        to { opacity: 1; }
    }


    .task-option-box p { /* Style paragraphs inside task box */
        color: #4D5656; /* Slightly darker text */
        font-size: 1.0em;
        margin-bottom: 12px;
        text-shadow: 0.4px 0.4px 0.8px rgba(255, 255, 255, 0.6); /* Softer text shadow */
        transform: translateY(0);
        opacity: 0.9;
        animation: fadeInParagraph 1s ease-out forwards 1.5s; /* Fade-in animation with delay */
        opacity: 0;
    }
    @keyframes fadeInParagraph {
        to { opacity: 0.9; }
    }


    .stSidebar {
        background: linear-gradient(to bottom, #D4E6F1, #A9CCE3); /* Cobalt Blue sidebar gradient */
        padding: 25px 20px;
        border-radius: 10px;
        border: none;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.18), -7px -7px 12px rgba(255,255,255,0.6);
        animation: slideInSidebar 1s ease-out forwards 0.3s; /* Slide-in animation for sidebar */
        transform: translateX(-50px);
        opacity: 0;
    }

    @keyframes slideInSidebar {
        to { transform: translateX(0); opacity: 1; }
    }


    .stSidebar:hover {
        box-shadow: 12px 12px 25px rgba(0,0,0,0.22), -10px -10px 20px rgba(255,255,255,0.75);
        transform: scale(1.003);
    }

    .stSidebar h2 {
        color: #0B5394; /* Darker Cobalt Blue for sidebar heading */
        font-size: 1.7em;
        margin-bottom: 10px;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.6);
        font-weight: bold;
        opacity: 1;
    }


    .stSidebar .stButton > button, .stButton > button.st-ef {
        background: linear-gradient(to bottom, #0B5394, #08457E); /* Cobalt Blue button gradient */
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        width: auto;
        min-width: 100px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.18), -3px -3px 6px rgba(255,255,255,0.5);
        animation: none;
    }


    .stSidebar .stButton > button:hover, .stButton > button.st-ef:hover {
        transform: translateY(-2px);
        box-shadow: 5px 5px 12px rgba(0,0,0,0.22), -4px -4px 8px rgba(255,255,255,0.6);
    }
    .stSidebar .stButton > button:active, .stButton > button.st-ef:active {
        transform: translateY(1px);
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2) inset, -1px -1px 3px rgba(255,255,255,0.5) inset;
    }

    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #85C1E9; /* Light Cobalt Blue border for input */
        padding: 10px;
        font-size: 1.0rem;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.08), inset -2px -2px 4px rgba(255,255,255,0.5);
        opacity: 1;
        transform: translateY(0);
    }


    /* Radio Buttons - Cobalt Blue Highlight and Compact Spacing */
    .stRadio > div {
        gap: 1.5rem;
        display: flex;
        flex-direction: column;
        opacity: 1;
    }


    .stRadio > div > label {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        cursor: pointer;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 8px 14px;
        border-radius: 15px;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.05), -1px -1px 2px rgba(255,255,255,0.3);
    }
    .stRadio > div > label:hover {
        transform: scale(1.01);
        box-shadow: 3px 3px 6px rgba(0,0,0,0.08), -2px -2px 4px rgba(255,255,255,0.4);
        background-color: rgba(255, 255, 255, 0.9);
    }

    /* Target the input element directly when checked */
    .stRadio > div > label > div:first-child input[type="radio"] {
        appearance: none; /* Remove default radio button appearance */
        -webkit-appearance: none; /* For Safari */
        -moz-appearance: none; /* For Firefox */
        width: 20px;
        height: 20px;
        border: 1.5px solid #0B5394; /* Cobalt Blue border */
        border-radius: 50%;
        background: linear-gradient(160deg, #ffffff, #f0f0f0);
        margin-right: 10px;
        position: relative;
        cursor: pointer;
        display: inline-block; /* Ensure it's inline for label alignment */
    }
    .stRadio > div > label > div:first-child input[type="radio"]:hover {
        border-color: #08457E; /* Darker Cobalt Blue hover border */
        box-shadow: 2px 2px 5px rgba(0,0,0,0.15), -2px -2px 3px rgba(255,255,255,0.4);
        transform: scale(1.03);
    }

    /* Style the "inner dot" when checked - Cobalt Blue */
    .stRadio > div > label > div:first-child input[type="radio"]:checked {
        background-color: #0B5394 !important; /* Solid Cobalt Blue Background when checked */
        border-color: #0B5394 !important;     /* Cobalt Blue Border when checked */
        box-shadow: inset 2px 2px 4px rgba(0,0,0,0.1) !important, inset -1px -1px 2px rgba(255,255,255,0.3) !important;
    }
    .stRadio > div > label > div:first-child input[type="radio"]:checked + span::before { /* Using a pseudo-element for the inner dot */
        content: '';
        display: block;
        position: absolute; /* Position relative to the input */
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 10px;
        height: 10px;
        background-color: white !important; /* White inner dot for Cobalt Blue */
        border-radius: 50%;
    }


    .stRadio > div > label > span {
        font-size: 1.0rem;
        color: #2E4053; /* Darker text for radio labels */
        font-weight: 500;
        position: relative; /* Needed for pseudo-element positioning */
    }
    .stRadio > div > label > span:hover {
         text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.6);
    }


    .stChatMessage {
        border-radius: 10px;
        padding: 10px 18px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05), -1px -1px 3px rgba(255,255,255,0.3);
        transform: translateY(0);
        opacity: 1;
    }


    .stChatMessage:hover {
        transform: scale(1.002);
        box-shadow: 3px 3px 6px rgba(0,0,0,0.08), -2px -2px 4px rgba(255,255,255,0.4);
    }

    .stChatMessage.user {
        background: linear-gradient(to right, #D4E6F1, #EAF2F8); /* User chat Cobalt Blue */
        border: none;
        color: #2E4053; /* Darker user text */
        box-shadow: 1px 1px 3px rgba(0,0,0,0.03), -1px -1px 2px rgba(255,255,255,0.2);
    }
    .stChatMessage.assistant {
        background: linear-gradient(to left, #EAF2F8, #F5FBFF); /* Assistant chat Light Cobalt Blue */
        border: none;
        color: #2E4053; /* Darker assistant text */
        box-shadow: 1px 1px 3px rgba(0,0,0,0.03), -1px -1px 2px rgba(255,255,255,0.2);
    }

    .stChatInputContainer > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #85C1E9; /* Light Cobalt Blue border for chat input */
        padding: 8px;
        font-size: 0.95rem;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.08), inset -2px -2px 4px rgba(255,255,255,0.5);
        opacity: 1;
        transform: translateY(0);
    }
     .stChatInputContainer > div > div > textarea:focus {
        border-color: #0B5394; /* Cobalt Blue focus border for chat input */
        box-shadow: inset 3px 3px 7px rgba(0,0,0,0.09), inset -3px -3px 5px rgba(255,255,255,0.6), 0 0 0 0.2rem rgba(11, 83, 148, .25); /* Cobalt Blue focus shadow */
        outline: 0;
    }

    hr {
        border: none;
        height: 1.5px;
        background: linear-gradient(to right, #85C1E9, #D4E6F1, #85C1E9); /* Cobalt Blue hr gradient */
        margin-bottom: 25px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.05), -1px -1px 2px rgba(255,255,255,0.3);
        transform: scaleX(1);
        animation: growHorizontal 1s ease-out forwards 1.8s; /* Horizontal grow animation for hr */
        transform-origin: left center;
        transform: scaleX(0);
    }
    @keyframes growHorizontal {
        to { transform: scaleX(1); }
    }


    /* Analyze Image Button - Navy Blue - FORCED */
    div.stButton > button:first-child { /* More specific selector */
        background: linear-gradient(to bottom, #000080, #000050) !important; /* Navy Blue Button Gradient - Forced */
        color: white !important;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.25), -3px -3px 6px rgba(255,255,255,0.4) !important;
        border-color: transparent !important; /* Remove any default border */
        animation: fadeInButton 1s ease-out forwards 2.1s; /* Fade-in for Analyze Button */
        opacity: 0;
    }
    @keyframes fadeInButton {
        to { opacity: 1; }
    }


    div.stButton > button:first-child:hover {
        box-shadow: 5px 5px 12px rgba(0,0,0,0.3), -4px -4px 8px rgba(255,255,255,0.5) !important;
    }
    div.stButton > button:first-child:active {
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3) inset, -1px -1px 3px rgba(255,255,255,0.4) inset !important;
    }

    /* Uploaded Image 3D Border */
    .stImage > div > div > img {
        border: 8px solid #f0f0f0;
        border-radius: 12px;
        box-shadow: 6px 6px 12px rgba(0,0,0,0.15), -4px -4px 8px rgba(255,255,255,0.5);
        animation: zoomInImage 1s ease-out forwards 2.4s; /* Zoom-in animation for image */
        transform: scale(0.8);
        opacity: 0;
    }
    @keyframes zoomInImage {
        to { transform: scale(1); opacity: 1; }
    }


    /* Section Title Styling - Select Task and Upload Image */
    .stApp h3 {
        color: #0B5394; /* Darker Cobalt Blue for section headings */
        font-size: 2.1em; /* Increased size */
        margin-bottom: 15px;
        text-shadow: 1.5px 1.5px 3px rgba(255, 255, 255, 0.7); /* Enhanced text shadow */
        font-weight: 700; /* Bold font weight */
        letter-spacing: -1px; /* Tighter letter spacing */
        opacity: 1;
        animation: fadeInSectionTitle 1s ease-out forwards 2.7s; /* Fade-in animation for section titles */
        opacity: 0;
    }
    @keyframes fadeInSectionTitle {
        to { opacity: 1; }
    }


    .stApp h3 i { /* Style for the bone icon in section titles */
        margin-right: 5px; /* Add some spacing after the icon */
        font-size: 1.1em; /* Slightly adjust icon size if needed */
        vertical-align: middle; /* Vertically align the icon with the text */
        color: #0B5394; /* Icon color same as title */
    }


    .stApp p[style*="color: #4D5656;"] { /* Targeting styled paragraphs */
        animation: fadeInParagraphs 1s ease-out forwards 3s; /* Fade-in animation for paragraphs */
        opacity: 0;
    }
     @keyframes fadeInParagraphs {
        to { opacity: 0.9; }
    }


    </style>
    """,
    unsafe_allow_html=True,
)

# Premium Header Section with Highlight Box
st.markdown(
    """
    <div class="highlight-box">
        <div style="text-align: center; margin-bottom: 15px;">
            <h1 style="color: #0B5394; font-size: 2.8em; margin-bottom: 8px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); transition: text-shadow 0.3s ease;">
                <i class="fas fa-hospital-symbol"></i> 🦴 Bone Health AI Suite 🌌
            </h1>
            <h4 style="color: #4D5656; font-weight: 500; font-style: italic; font-size: 1.0em; text-shadow: 0.5px 0.5px 1px rgba(255, 255, 255, 0.3); transition: text-shadow 0.3s ease;">
                ✨ Empowering Bone Health with Advanced AI Analysis ✨
            </h4>
        </div>
    </div>
    <hr style="margin-bottom: 30px;">
    """,
    unsafe_allow_html=True
)

# Authentication Functions (No change in logic except for register function)
def authenticate(username, password):
    cursor.execute("SELECT user_type FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    return user[0] if user else None

def register(username, password, user_type, license_number=None, specialization=None, affiliation=None): # Added specialization and affiliation
    try:
        cursor.execute("INSERT INTO users (username, password, user_type, license_number, specialization, affiliation) VALUES (?, ?, ?, ?, ?, ?)", # Added specialization and affiliation
                       (username, password, user_type, license_number, specialization, affiliation)) # Added specialization and affiliation
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Premium Sidebar for Login/Signup
with st.sidebar:
    st.markdown("## 🔑 **Account Access**", unsafe_allow_html=True)
    auth_option = st.radio("**Choose an option:**", ["Login", "Signup"])

    if auth_option == "Signup":
        st.markdown("### 📝 Create Account", unsafe_allow_html=True)
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password", )
        user_type = st.radio("User Type:", ["Common User", "Doctor"])
        license_number = st.text_input("Medical License Number (Doctors only)", disabled=user_type == "Common User")

        # Doctor Specific Fields
        if user_type == "Doctor":
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True) # Separator line
            st.markdown("#### 🩺 Doctor Credentials", unsafe_allow_html=True) # Subheader
            specialization = st.text_input("Specialization (e.g., Orthopedics)")
            affiliation = st.text_input("Hospital/Clinic Affiliation")
        else:
            specialization = None
            affiliation = None

        if st.button("Signup"):
            if user_type == "Doctor" and (not specialization or not affiliation or not license_number):
                st.error("❌ Doctors must provide Specialization, Affiliation, and License Number.")
            elif register(new_username, new_password, user_type, license_number, specialization, affiliation): # Passing new fields to register
                st.success("✅ Account created successfully. Please login.")
            else:
                st.error("❌ Username already exists!")

    elif auth_option == "Login":
        st.markdown("### 🚪 Login", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_role = authenticate(username, password)
            if user_role:
                # Account switch handling
                if "username" in st.session_state and st.session_state["username"] != username:
                    st.session_state.pop('message_log', None)
                    st.session_state.pop('analysis_context', None)
                    st.session_state.pop('uploaded_image', None)
                    st.session_state.pop('selected_task', None)

                st.session_state["logged_in"] = True
                st.session_state["user_type"] = user_role
                st.session_state["username"] = username
                if "message_log" not in st.session_state:
                    st.session_state.message_log = [{"role": "ai", "content": "👋 Welcome to Bone Health AI Suite! How can I help you today?"}]
                st.success(f"✅ Logged in as **{user_role}**")
            else:
                st.error("❌ Invalid credentials!")

# Initialize message_log if not present
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "👋 Welcome to Bone Health AI Suite! Please log in to start."}]

# Check login status
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("⚠️ Please log in to access the AI analysis tool.")
    st.stop()

# Task Selection with 3D Box
st.markdown('<div class="task-option-box">', unsafe_allow_html=True) # Apply task-option-box class
st.markdown(f"<h3><i class='fas fa-tasks'></i> 🦴 <b>Select Analysis Task</b></h3>", unsafe_allow_html=True) # Enhanced Section Title
st.markdown("<p style='color: #4D5656;'>Choose the type of bone health analysis you want to perform:</p>", unsafe_allow_html=True) # Styled paragraph
task_options = [
        "Bone Fracture Detection",
        "Bone Marrow Cell Classification",
        "Knee Joint Osteoarthritis Detection",
        "Osteoporosis Stage Prediction & BMD Score",
        "Bone Age Detection",
        "Cervical Spine Fracture Detection",
        "Bone Tumor/Cancer Detection",
        "Bone Infection (Osteomyelitis) Detection"
    ]
task_radio = st.radio( # Assign radio to a variable to style labels
    "",
    task_options,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True) # Close task-option-box

# Apply premium style to radio button labels within task-option-box
st.markdown(
    """
    <style>
        .task-option-box .stRadio > div > label > span {
            font-size: 1.1rem; /* Increased font size */
            color: #2E4053;
            font-weight: 600; /* Bold font weight */
            text-shadow: 0.6px 0.6px 1px rgba(255, 255, 255, 0.5); /* Refined text shadow */
        }
        .task-option-box .stRadio > div > label {
            background-color: rgba(255, 255, 255, 0.9); /* Slightly more opaque background */
            padding: 10px 18px; /* Increased padding */
            margin-bottom: 12px; /* Increased margin */
            border-radius: 18px; /* More rounded labels */
            box-shadow: 3px 3px 6px rgba(0,0,0,0.06), -2px -2px 4px rgba(255,255,255,0.35); /* Refined shadow */
        }
        .task-option-box .stRadio > div > label:hover {
             box-shadow: 4px 4px 8px rgba(0,0,0,0.09), -3px -3px 5px rgba(255,255,255,0.4); /* Hover shadow stronger */
             background-color: rgba(255, 255, 255, 0.95); /* Slightly lighter on hover */
             transform: scale(1.005); /* Gentle scale on hover */
        }


    </style>
    """,
    unsafe_allow_html=True
)


task = task_radio # Use the assigned variable for task value

# Task Prompts (No change in content)
task_prompts = {
    "Bone Fracture Detection": (
        "Analyze the X-ray, MRI, or CT scan image for fractures and classify into different fracture types with detailed severity assessment. "
        "For common users: The image will be analyzed to check for fractures, identifying the affected bone and the type of break. "
        "You will receive an easy-to-understand explanation of the fracture, including its severity and possible effects on movement, provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Suggest medical treatment options, possible surgeries, immobilization techniques, and follow-up care strategies,provide nutrition plan,steps to recover like remedies and exercises if required. "
    ),

    "Bone Marrow Cell Classification": (
        "Analyze the biopsy or MRI image and classify bone marrow cells into relevant categories, identifying concerning cells. "
        "For common users: The image will be analyzed to check for abnormalities in bone marrow cells. "
        "You will receive a simple explanation of the findings, including whether there are unusual cell changes and what they might indicate,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Provide detailed insights into abnormal cell structures, possible diagnoses, and recommended medical interventions,provide nutrition plan,steps to recover like remedies and exercises if required. "
    ),

    "Knee Joint Osteoarthritis Detection": (
        "Analyze the knee X-ray or MRI and classify osteoarthritis severity based on clinical grading. "
        "For common users: The image will be assessed for signs of knee osteoarthritis, including joint space narrowing and bone changes. "
        "You will get an easy-to-understand report on whether osteoarthritis is present and its severity level, along with its impact on knee function,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Suggest advanced treatments, medications, physiotherapy plans, and surgical options such as knee replacement,provide nutrition plan,steps to recover like remedies and exercises if required."
        
    ),

    "Osteoporosis Stage Prediction & BMD Score": (
        "Analyze the bone X-ray and determine osteoporosis stage with estimated Bone Mineral Density (BMD) score. "
        "For common users: The scan will be analyzed to determine how strong or weak the bones are and whether osteoporosis is present. "
        "You will receive a simple explanation of the results, including whether bone density is lower than normal and what it means for bone health,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Recommend specific medications, hormone therapy, and advanced treatments to manage and prevent complications,provide nutrition plan,steps to recover like remedies and exercises if required."
    ),

    "Bone Age Detection": (
        "Analyze the X-ray of a child's hand and predict bone age with insights into growth patterns. "
        "For common users: The scan will be assessed to check how well the bones are developing compared to the expected growth pattern for the child’s age. "
        "You will receive an easy-to-understand result explaining whether the bone growth is normal, advanced, or delayed,provide nutrition plan,steps to recover like remedies and exercises if required. "
        "For doctors: Offer insights into growth abnormalities, hormonal imbalances, and necessary medical interventions if delayed growth is detected,provide nutrition plan,steps to recover like remedies and exercises if required."
    ),

    "Cervical Spine Fracture Detection": (
        "Analyze the X-ray, MRI, or CT scan of the cervical spine for fractures and provide a severity assessment. "
        "For common users: The scan will be analyzed for fractures in the neck bones, and you will receive an explanation of the findings. "
        "The report will describe whether a fracture is present, its severity, and how it may affect movement or pain levels,provide nutrition plan,steps to recover like remedies and exercises if required."
        "For doctors: Suggest medical treatment plans, possible surgical options, and rehabilitation strategies for full recovery,provide nutrition plan,steps to recover like remedies and exercises if required"
    ),

    "Bone Tumor/Cancer Detection": (
        "Analyze the X-ray, MRI, CT scan, or biopsy image for possible bone tumors or cancerous growths. "
        "For common users: The image will be checked for any unusual growths or masses in the bone, and you will receive a simple explanation of the findings. "
        "If any suspicious areas are detected, the report will describe their size, location, and whether they appear concerning,provide nutrition plan,steps to recover like remedies and exercises if required."
        "For doctors: Provide detailed insights into tumor classification, possible malignancy assessment, and treatment options,provide nutrition plan,steps to recover like remedies and exercises if required. "
    ),

    "Bone Infection (Osteomyelitis) Detection": (
        "Analyze the X-ray, MRI, CT scan, or biopsy image for signs of bone infection (osteomyelitis). "
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
    st.session_state.message_log = [{"role": "ai", "content": f"📢 Analyzing **{task}**. Upload an image and ask questions. 🚀"}]
    st.session_state.pop("uploaded_image", None)

# Image uploader
st.markdown(f"<h3><i class='fas fa-upload'></i> 📤 <b>Upload Medical Image</b></h3>", unsafe_allow_html=True) # Enhanced Section Title
st.markdown("<p style='color: #4D5656;'>Supported formats: JPG, JPEG, PNG</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)
if uploaded_file:
    st.session_state.uploaded_image = uploaded_file
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image Preview 🖼️", width=350, use_container_width=False)

# Analyze button
if st.button("🔍 **Analyze Image**", type="primary"):
    if uploaded_file:
        with st.spinner("🧠 AI is analyzing your image... Please wait"):
            image_data = [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
            ai_analysis = get_gemini_response(task_prompt, st.session_state["user_type"], image_data)

            st.session_state["analysis_context"] = ai_analysis
            st.session_state.message_log.append({"role": "ai", "content": ai_analysis})
            st.success("✅ Analysis Complete! Scroll down to see results. ✨")
    else:
        st.warning("⚠️ Please upload an image before analyzing. 📤")

# Chat Container
st.markdown("---")
st.markdown("## 💬 **Analysis & Chat**", unsafe_allow_html=True)
chat_container = st.container()
with chat_container:
    for message in st.session_state.message_log:
        if message["role"] == "ai":
            with st.chat_message("assistant"):
                st.markdown(f"**AI Assistant:** {message['content']} 🤖")
        else:
            with st.chat_message("user"):
                st.markdown(f"**You:** {message['content']} 🧑‍⚕️")

# Chat input
irrelevant_keywords = ["pm", "president", "capital", "weather", "politics", "sports"]
greeting_keywords = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
appreciation_keywords = ["thank you", "thanks", "great work", "well done", "appreciate", "good job"]

user_query = st.chat_input("Ask follow-up questions or request more details... ℹ️")

if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})

    response_text = ""

    if any(word.lower() == user_query.lower().strip() for word in greeting_keywords):
        response_text = "😊 Hello! How can I assist you further today?"

    elif any(word in user_query.lower() for word in appreciation_keywords):
        response_text = "🙏 You're very welcome! I'm here to help. Is there anything else I can assist you with?"

    elif any(word in user_query.lower() for word in irrelevant_keywords):
        response_text = "⚠️ Please ask questions related to the medical image analysis for the best results. 🩺"

    else:
        analysis_context = st.session_state.get("analysis_context", None)
        if analysis_context:
            response_text = get_gemini_response(
                task_prompt="Answer the follow-up question based on the previous context.",
                user_type=st.session_state["user_type"],
                additional_input=f"Context: {analysis_context}\nUser Query: {user_query}"
            )
        else:
            response_text = "⚠️ I don't have the previous analysis context. Please ensure you have analyzed an image first, or rephrase your question. 🖼️"

    st.session_state.message_log.append({"role": "ai", "content": response_text})
    st.rerun()
