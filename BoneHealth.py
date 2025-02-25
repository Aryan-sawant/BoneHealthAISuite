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

# --- UPDATED PREMIUM CSS STYLING WITH SIDEBAR ANIMATION & 3D EFFECTS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    body {
        background: linear-gradient(to bottom, #E6F7FF, #D0E8FA);
        color: #333;
        font-family: 'Roboto', sans-serif;
        overflow-x: hidden;
    }

    .stApp {
        max-width: 100vw;
        min-height: 100vh;
        margin: 0;
        padding: 35px 40px;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        background: transparent;
    }

    .highlight-box {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(5px);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 12px 12px 25px rgba(0,0,0,0.1), -8px -8px 15px rgba(255,255,255,0.6);
        animation: fadeIn 1.5s ease-out forwards;
        opacity: 0;
    }
    @keyframes fadeIn {
        to { opacity: 1; }
    }

    .highlight-box:hover {
        box-shadow: 15px 15px 30px rgba(0,0,0,0.12), -10px -10px 18px rgba(255,255,255,0.7);
        transform: scale(1.005);
    }

    .highlight-box h1 {
        color: #0B5394;
        font-size: 3.6em;
        margin-bottom: 12px;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.15), 0 0 10px rgba(255, 255, 255, 0.4);
        font-weight: 700;
        letter-spacing: -1.8px;
        animation: pulseTitle 3s infinite alternate, fadeInTitle 1.5s ease-out forwards 0.5s;
        opacity: 0;
        transition: text-shadow 0.3s ease;
    }

    @keyframes fadeInTitle {
        to { opacity: 1; }
    }

    @keyframes pulseTitle {
        0% { text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.15), 0 0 10px rgba(255, 255, 255, 0.4); transform: scale(1); }
        100% { text-shadow: 3px 3px 7px rgba(0, 0, 0, 0.2), 0 0 14px rgba(255, 255, 255, 0.6); transform: scale(1.02); }
    }

    .highlight-box h4 {
        color: #555;
        font-size: 1.2em;
        margin-bottom: 20px;
        text-shadow: 0.5px 0.5px 1px rgba(255, 255, 255, 0.5);
        font-style: normal;
        font-weight: 400;
        opacity: 0.9;
        line-height: 1.6;
    }

    .task-option-box {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(5px);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow:
            15px 15px 25px rgba(0,0,0,0.08),
            -10px -10px 18px rgba(255,255,255,0.7);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
        animation: fadeInUp 1s ease-out forwards 0.8s;
        transform: translateY(20px);
        opacity: 0;
        border: 1px solid #AED6F1;
    }

    @keyframes fadeInUp {
        to { transform: translateY(0); opacity: 1; }
    }

    .task-option-box:hover {
        box-shadow:
            18px 18px 30px rgba(0,0,0,0.1),
            -12px -12px 20px rgba(255,255,255,0.8);
        transform: scale(1.01);
    }

    .task-option-box h2 {
        color: #0B5394;
        font-size: 2.1em;
        margin-bottom: 15px;
        text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.7);
        font-weight: 600;
        opacity: 1;
        letter-spacing: -1px;
        animation: fadeInText 1s ease-out forwards 1.2s;
        opacity: 0;
    }
    @keyframes fadeInText {
        to { opacity: 1; }
    }

    .task-option-box p {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 15px;
        text-shadow: 0.4px 0.4px 0.8px rgba(255, 255, 255, 0.6);
        transform: translateY(0);
        opacity: 0.85;
        animation: fadeInParagraph 1s ease-out forwards 1.5s;
        opacity: 0;
        line-height: 1.5;
    }
    @keyframes fadeInParagraph {
        to { opacity: 0.85; }
    }

    /* Animated Sidebar */
    .stSidebar {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(8px);
        padding: 30px 25px;
        border-radius: 15px;
        border: none;
        box-shadow: 12px 12px 25px rgba(0,0,0,0.1), -8px -8px 15px rgba(255,255,255,0.6);
        position: fixed; /* Fixed position for animation */
        left: 0;
        top: 0;
        height: 100%;
        width: 280px; /* Adjust sidebar width as needed */
        transform: translateX(-280px); /* Initially hidden */
        transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out; /* Smooth animation */
        opacity: 0.95;
        z-index: 1000; /* Ensure sidebar is on top */
    }

    .stSidebar.expanded {
        transform: translateX(0); /* Slide in when expanded class is added */
    }

    .stSidebar:hover {
        box-shadow: 15px 15px 30px rgba(0,0,0,0.12), -10px -10px 18px rgba(255,255,255,0.75);
    }

    .stSidebar h2 {
        color: #0B5394;
        font-size: 1.8em;
        margin-bottom: 12px;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.6);
        font-weight: 600;
        opacity: 1;
    }

    .stSidebar .stButton > button, .stButton > button.st-ef {
        background: linear-gradient(to bottom, #0C69C6, #085394);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 500;
        width: auto;
        min-width: 110px;
        box-shadow: 5px 5px 12px rgba(0,0,0,0.15), -4px -4px 8px rgba(255,255,255,0.5);
        animation: none;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }

    .stSidebar .stButton > button:hover, .stButton > button.st-ef:hover {
        transform: translateY(-3px);
        box-shadow: 6px 6px 15px rgba(0,0,0,0.18), -5px -5px 10px rgba(255,255,255,0.6);
    }
    .stSidebar .stButton > button:active, .stButton > button.st-ef:active {
        transform: translateY(0);
        box-shadow: 3px 3px 7px rgba(0,0,0,0.2) inset, -2px -2px 4px rgba(255,255,255,0.5) inset;
    }

    .stTextInput > div > div > input, .stChatInputContainer > div > div > textarea {
        border-radius: 10px;
        border: 1px solid #AED6F1;
        padding: 12px;
        font-size: 1.05rem;
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.05), inset -2px -2px 4px rgba(255,255,255,0.4);
        opacity: 0.95;
        transform: translateY(0);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .stTextInput > div > div > input:focus, .stChatInputContainer > div > div > textarea:focus {
        border-color: #0C69C6;
        box-shadow: inset 4px 4px 8px rgba(0,0,0,0.07), inset -3px -3px 5px rgba(255,255,255,0.5), 0 0 0 0.2rem rgba(11, 105, 198, .2);
        outline: none;
    }

    .stRadio > div {
        gap: 2rem;
        display: flex;
        flex-direction: column;
        opacity: 1;
    }

    .stRadio > div > label {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        cursor: pointer;
        background-color: rgba(255, 255, 255, 0.95);
        padding: 10px 18px;
        border-radius: 20px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.04), -2px -2px 4px rgba(255,255,255,0.3);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, background-color 0.2s ease-in-out;
    }
    .stRadio > div > label:hover {
        transform: scale(1.01);
        box-shadow: 4px 4px 8px rgba(0,0,0,0.06), -3px -3px 5px rgba(255,255,255,0.35);
        background-color: rgba(255, 255, 255, 1);
    }

    .stRadio > div > label > div:first-child input[type="radio"] {
        appearance: none;
        -webkit-appearance: none;
        -moz-appearance: none;
        width: 22px;
        height: 22px;
        border: 2px solid #0C69C6;
        border-radius: 50%;
        background: linear-gradient(160deg, #ffffff, #f0f0f0);
        margin-right: 12px;
        position: relative;
        cursor: pointer;
        display: inline-block;
    }
    .stRadio > div > label > div:first-child input[type="radio"]:hover {
        border-color: #085394;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1), -2px -2px 3px rgba(255,255,255,0.35);
        transform: scale(1.03);
    }

    .stRadio > div > label > div:first-child input[type="radio"]:checked {
        background-color: #0C69C6 !important;
        border-color: #0C69C6 !important;
        box-shadow: inset 2px 2px 4px rgba(0,0,0,0.08) !important, inset -1px -1px 2px rgba(255,255,255,0.3) !important;
    }
    .stRadio > div > label > div:first-child input[type="radio"]:checked + span::before {
        content: '';
        display: block;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 12px;
        height: 12px;
        background-color: white !important;
        border-radius: 50%;
    }

    .stRadio > div > label > span {
        font-size: 1.15rem;
        color: #444;
        font-weight: 500;
        position: relative;
        text-shadow: 0.5px 0.5px 1px rgba(255, 255, 255, 0.5);
    }
    .stRadio > div > label > span:hover {
         text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.6);
    }

    .stChatMessage {
        border-radius: 15px;
        padding: 12px 20px;
        margin-bottom: 12px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.03), -1px -1px 3px rgba(255,255,255,0.2);
        transform: translateY(0);
        opacity: 0.98;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }

    .stChatMessage:hover {
        transform: scale(1.002);
        box-shadow: 3px 3px 6px rgba(0,0,0,0.05), -2px -2px 4px rgba(255,255,255,0.3);
    }

    .stChatMessage.user {
        background: rgba(228, 243, 255, 0.8);
        border: none;
        color: #444;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.02), -1px -1px 2px rgba(255,255,255,0.15);
    }
    .stChatMessage.assistant {
        background: rgba(245, 250, 255, 0.8);
        border: none;
        color: #444;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.02), -1px -1px 2px rgba(255,255,255,0.15);
    }

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #AED6F1, #D0E8FA, #AED6F1);
        margin-bottom: 35px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.03), -1px -1px 2px rgba(255,255,255,0.2);
        transform: scaleX(1);
        animation: growHorizontal 1s ease-out forwards 1.8s;
        transform-origin: left center;
        transform: scaleX(0);
    }
    @keyframes growHorizontal {
        to { transform: scaleX(1); }
    }

    div.stButton > button:first-child {
        background: linear-gradient(to bottom, #000080, #000060) !important;
        color: white !important;
        box-shadow: 5px 5px 12px rgba(0,0,0,0.2), -4px -4px 8px rgba(255,255,255,0.3) !important;
        border-color: transparent !important;
        animation: fadeInButton 1s ease-out forwards 2.1s;
        opacity: 0;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    @keyframes fadeInButton {
        to { opacity: 1; }
    }

    div.stButton > button:first-child:hover {
        box-shadow: 6px 6px 15px rgba(0,0,0,0.25), -5px -5px 10px rgba(255,255,255,0.4) !important;
        transform: translateY(-2px);
    }
    div.stButton > button:first-child:active {
        box-shadow: 3px 3px 7px rgba(0,0,0,0.25) inset, -2px -2px 4px rgba(255,255,255,0.3) inset !important;
        transform: translateY(0);
    }

    .stImage > div > div > img {
        border: 10px solid #f8f8f8;
        border-radius: 15px;
        box-shadow: 8px 8px 15px rgba(0,0,0,0.1), -5px -5px 10px rgba(255,255,255,0.4);
        animation: zoomInImage 1s ease-out forwards 2.4s;
        transform: scale(0.8);
        opacity: 0;
    }
    @keyframes zoomInImage {
        to { transform: scale(1); opacity: 1; }
    }

    .stApp h3 {
        color: #0B5394;
        font-size: 2.3em;
        margin-bottom: 20px;
        text-shadow: 1.5px 1.5px 3px rgba(255, 255, 255, 0.6);
        font-weight: 600;
        letter-spacing: -1.2px;
        opacity: 1;
        animation: fadeInSectionTitle 1s ease-out forwards 2.7s;
        opacity: 0;
    }
    @keyframes fadeInSectionTitle {
        to { opacity: 1; }
    }

    .stApp h3 i {
        margin-right: 8px;
        font-size: 1.1em;
        vertical-align: middle;
        color: #0B5394;
        opacity: 0.9;
    }

    .stApp p[style*="color: #4D5656;"] {
        color: #666 !important;
        line-height: 1.6;
        animation: fadeInParagraphs 1s ease-out forwards 3s;
        opacity: 0;
    }
     @keyframes fadeInParagraphs {
        to { opacity: 0.85; }
    }

    .task-option-box .stRadio > div > label > span {
        font-size: 1.2rem;
        color: #444;
        font-weight: 500;
        text-shadow: 0.5px 0.5px 1px rgba(255, 255, 255, 0.5);
    }
    .task-option-box .stRadio > div > label {
        background-color: rgba(255, 255, 255, 0.98);
        padding: 12px 20px;
        margin-bottom: 15px;
        border-radius: 22px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.05), -2px -2px 4px rgba(255,255,255,0.3);
    }
    .task-option-box .stRadio > div > label:hover {
         box-shadow: 4px 4px 8px rgba(0,0,0,0.07), -3px -3px 5px rgba(255,255,255,0.35);
         background-color: rgba(255, 255, 255, 1);
    }

    .stChatContainer {
        padding-top: 20px;
    }

    /* Hamburger Menu Button for Sidebar Toggle */
    .sidebar-toggle-button {
        position: fixed; /* Fixed button position */
        top: 15px;
        left: 15px;
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(5px);
        border: none;
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
        z-index: 1001; /* Above sidebar */
        box-shadow: 3px 3px 6px rgba(0,0,0,0.08), -2px -2px 4px rgba(255,255,255,0.3);
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }
    .sidebar-toggle-button:hover {
        background-color: rgba(255, 255, 255, 0.95);
        box-shadow: 4px 4px 8px rgba(0,0,0,0.1), -3px -3px 5px rgba(255,255,255,0.4);
    }
    .sidebar-toggle-button:active {
        box-shadow: inset 2px 2px 4px rgba(0,0,0,0.1), inset -1px -1px 2px rgba(255,255,255,0.3);
    }
    .sidebar-toggle-button i {
        font-size: 1.4em;
        color: #0B5394;
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
            <h1 style="color: #0B5394; font-size: 3.2em; margin-bottom: 10px; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); transition: text-shadow 0.3s ease;">
                <i class="fas fa-hospital-symbol"></i> 🦴 Bone Health AI Suite 🌌
            </h1>
            <h4 style="color: #555; font-weight: 400; font-style: italic; font-size: 1.1em; text-shadow: 0.5px 0.5px 1px rgba(255, 255, 255, 0.3); transition: text-shadow 0.3s ease; line-height: 1.6;">
                ✨ Empowering Bone Health with Advanced AI Analysis ✨
            </h4>
        </div>
    </div>
    <hr style="margin-bottom: 35px;">
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

# Sidebar State Management
if "sidebar_expanded" not in st.session_state:
    st.session_state.sidebar_expanded = False

def toggle_sidebar():
    st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded

# Hamburger Menu Button (Outside Sidebar)
st.button("☰ Menu", on_click=toggle_sidebar, key="sidebar_toggle_button", type="primary", use_container_width=False) # Changed to st.button instead of markdown for button functionality
# Premium Sidebar for Login/Signup
with st.sidebar:
    st.markdown(f"## 🔑 **Account Access**", unsafe_allow_html=True) # Title with Key Emoji
    auth_option = st.radio("**Choose an option:**", ["Login", "Signup"])

    if auth_option == "Signup":
        st.markdown("### 📝 Create Account", unsafe_allow_html=True) # Title with Writing Hand Emoji
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password", )
        user_type = st.radio("User Type:", ["Common User", "Doctor"])
        license_number = st.text_input("Medical License Number (Doctors only)", disabled=user_type == "Common User")

        # Doctor Specific Fields
        if user_type == "Doctor":
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
            st.markdown("#### 🩺 Doctor Credentials", unsafe_allow_html=True) # Title with Stethoscope Emoji
            specialization = st.text_input("Specialization (e.g., Orthopedics)")
            affiliation = st.text_input("Hospital/Clinic Affiliation")
        else:
            specialization = None
            affiliation = None

        if st.button("Signup"):
            if user_type == "Doctor" and (not specialization or not affiliation or not license_number):
                st.error("❌ Doctors must provide Specialization, Affiliation, and License Number.")
            elif register(new_username, new_password, user_type, license_number, specialization, affiliation):
                st.success("✅ Account created successfully. Please login.")
            else:
                st.error("❌ Username already exists!")

    elif auth_option == "Login":
        st.markdown("### 🚪 Login", unsafe_allow_html=True) # Title with Door Emoji
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

# Apply sidebar expanded class based on state
if st.session_state.sidebar_expanded:
    st.markdown(
        """
        <style>
            .stSidebar {
                transform: translateX(0); /* Slide in */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
            .stSidebar {
                transform: translateX(-280px); /* Slide out */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
