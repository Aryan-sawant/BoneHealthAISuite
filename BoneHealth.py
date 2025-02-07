import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image, ImageFile

# Prevent truncated image error
ImageFile.LOAD_TRUNCATED_IMAGES = True  

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

# Function to get AI response
def get_gemini_response(task_prompt, image=None, additional_input=""):
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
    input_data = [task_prompt, additional_input]
    if image:
        input_data.insert(1, image[0])  # Add image if provided
    response = model.generate_content(input_data)
    return response.text

# Function to process image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            image.load()
        except OSError:
            st.error("🚨 The uploaded image is corrupted. Please upload a valid image.")
            return None, None
        
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        
        return image_parts, image
    return None, None

# Task Selection
st.subheader("🦴 Select the analysis you want to perform")
task = st.radio("Choose a task:", [
    "Bone Fracture Detection",
    "Bone Marrow Cell Classification",
    "Knee Joint Osteoarthritis Detection",
    "Osteoporosis Stage Prediction & BMD Score",
    "Bone Age Detection",
    "Cervical Spine Fracture Detection"
])

# Image uploader (common for all tasks)
uploaded_file = st.file_uploader("📤 Upload an X-ray or biopsy image...", type=["jpg", "jpeg", "png"])
additional_input = st.text_area("📝 Provide additional details if necessary")
submit_button = st.button("🔍 Analyze")

# Run AI Analysis on Button Click
if submit_button:
    try:
        image_data, image = input_image_setup(uploaded_file)
        if not uploaded_file:
            st.warning("🚨 Please upload an image before analyzing.")
            st.stop()

        # Task prompts
        if task == "Bone Fracture Detection":
            task_prompt = "Analyze the X-ray image for fractures and classify into: avulsion fracture, comminuted fracture, hairline fracture, impacted fracture, oblique fracture, spiral fracture, pathological fracture, or no fracture. Provide healing measures, nutrition, lifestyle changes, and whether to consult a doctor."
        
        elif task == "Bone Marrow Cell Classification":
            task_prompt = "Analyze the biopsy image and classify bone marrow cells into categories such as abnormal eosinophil, basophil, blast, erythroblast, eosinophil, lymphocyte, metamyelocyte, monocyte, plasma cell, etc. Identify concerning cells linked to cancer risk."
        
        elif task == "Knee Joint Osteoarthritis Detection":
            task_prompt = "Analyze the knee X-ray and classify the osteoarthritis severity: Grade 0 (Healthy), Grade 1 (Doubtful joint narrowing), Grade 2 (Minimal osteophytes), Grade 3 (Moderate joint space narrowing and sclerosis), or Grade 4 (Severe osteoarthritis). Provide management and lifestyle recommendations."
        
        elif task == "Osteoporosis Stage Prediction & BMD Score":
            task_prompt = (
                "Analyze the uploaded bone X-ray and determine the osteoporosis stage (Normal, Osteopenia, or Osteoporosis). "
                "Additionally, predict an estimated Bone Mineral Density (BMD) score based on the image. "
                "Offer insights on bone health and possible lifestyle changes."
            )
        
        elif task == "Bone Age Detection":
            task_prompt = "Analyze the X-ray of a child's hand and accurately predict the bone age. Provide insights into growth patterns."
        
        elif task == "Cervical Spine Fracture Detection":
            task_prompt = "Analyze the CT scan image of the cervical spine for fractures. Identify the location, type (compression, burst, flexion teardrop, etc.), severity, and potential risks. Provide recommendations on medical evaluation and treatment approaches."
        
        # Get AI response
        response = get_gemini_response(task_prompt, image_data, additional_input)

        # Display Input Image
        st.markdown("<h4 style='color: #2E86C1;'>📸 Uploaded Image</h4>", unsafe_allow_html=True)
        st.image(image, caption="Uploaded Image", width=350, use_container_width=False)

        # Display AI Response
        st.markdown("<h4 style='color: #27AE60;'>📊 Analysis Result</h4>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='background-color:#E8F5E9;padding:15px;border-radius:10px;font-size:16px;color:#1B2631;'>{response}</div>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"🚨 Error: {e}")
