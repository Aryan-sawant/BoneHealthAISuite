# 🦴 Bone Health AI Suite 🌌

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-orange?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

## ✨ Empowering Bone Health with Advanced AI Analysis ✨

This application is a Streamlit-based web tool designed to analyze medical images for various bone health conditions using Google's Gemini AI model. It provides insights tailored for both common users and medical professionals (doctors).

**Please Note:** This application is for demonstration and informational purposes only and should **not** be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for any health concerns or before making any decisions related to your health or treatment.

## 🚀 Features

*   **Multiple Bone Health Analysis Tasks:**
    *   Bone Fracture Detection
    *   Bone Marrow Cell Classification
    *   Knee Joint Osteoarthritis Detection
    *   Osteoporosis Stage Prediction & BMD Score
    *   Bone Age Detection
    *   Cervical Spine Fracture Detection
    *   Bone Tumor/Cancer Detection
    *   Bone Infection (Osteomyelitis) Detection
*   **User-Specific Responses:** AI responses are tailored for either "Common User" (easy-to-understand explanations) or "Doctor" (detailed medical insights and treatment options).
*   **Interactive Chat Interface:**  Allows users to ask follow-up questions and engage in a conversation with the AI about the analysis results.
*   **User Authentication:** Basic login/signup system to manage user types and access.
*   **Visually Pleasing UI:**  Clean and professional user interface built with Streamlit and custom CSS styling.
*   **Animated Sidebar:** Slide-in/slide-out sidebar for account access (login/signup).
*   **Image Upload:** Supports JPG, JPEG, and PNG image formats for analysis.

## ⚙️ Setup and Installation

Follow these steps to set up and run the Bone Health AI Suite application locally:

### Prerequisites

*   **Python 3.8 or higher:**  Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).
*   **pip:**  Python's package installer. It usually comes bundled with Python installations.

### Installation Steps

1.  **Clone the Repository:**

    ```bash
    git clone [repository URL]
    cd [repository-name]
    ```
    Replace `[repository URL]` with the actual URL of your GitHub repository and `[repository-name]` with the name of the cloned directory.

2.  **Set up Environment Variables:**

    *   **Create a `.env` file** in the root directory of your project (if you haven't already).
    *   **Obtain a Google Cloud API Key:** You need to get an API key from Google Cloud to use the Gemini AI model.
        *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
        *   Create a project or select an existing one.
        *   Enable the "Generative Language API" for your project.
        *   Go to "Credentials" and create an API key.
    *   **Add your API key to the `.env` file:**

        ```
        GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
        ```
        **Important:** Replace `YOUR_GOOGLE_API_KEY` with your actual Google Cloud API key. **Do not commit your `.env` file with your API key to GitHub if it's a public repository!** Consider adding `.env` to your `.gitignore` file.

3.  **Install Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    This command will install all the necessary Python packages listed in the `requirements.txt` file, including Streamlit, `google-generativeai`, and other dependencies. **It's highly recommended to do this within a virtual environment** to keep your project dependencies isolated. You can create and activate a virtual environment like this:

    ```bash
    # (Optional) Create a virtual environment (recommended)
    python -m venv venv
    # Activate the virtual environment
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application:**

    ```bash
    streamlit run BoneHealth.py
    ```
    This command will start the Streamlit server and open the Bone Health AI Suite application in your default web browser.

## 🧑‍⚕️ Usage

1.  **Access the Application:** Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).
2.  **Account Access:**
    *   **Login or Signup:** Use the sidebar on the left to either log in with existing credentials or create a new account. Choose between "Common User" or "Doctor" user types during signup. Doctors will need to provide additional credentials (License Number, Specialization, Affiliation).
3.  **Select Analysis Task:** Choose the type of bone health analysis you want to perform from the "Select Analysis Task" section.
4.  **Upload Medical Image:** Upload a medical image (X-ray, MRI, CT scan, biopsy image) in JPG, JPEG, or PNG format using the "Upload Medical Image" section.
5.  **Analyze Image:** Click the "🔍 **Analyze Image**" button. The AI will process the image based on the selected task.
6.  **View Analysis Results:** The AI's analysis will be displayed in the chat interface under "Analysis & Chat".
7.  **Interactive Chat:** Ask follow-up questions or request more details in the chat input box at the bottom. The AI will respond based on the analysis context and your user type.

## ⚠️ Disclaimer

**Important:** This application is intended for educational and demonstration purposes only. It is **not a medical device** and should not be used for clinical diagnosis or treatment decisions. The AI's analysis is based on the provided image and may not be accurate or complete. Always consult with a qualified medical professional for any health concerns, diagnoses, or treatment plans.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please feel free to open an issue or submit a pull request.

## ✉️ Contact

For questions or feedback, please contact [Your Name/Email or GitHub Profile Link].

---

**Enjoy using the Bone Health AI Suite!** 🦴🌌
