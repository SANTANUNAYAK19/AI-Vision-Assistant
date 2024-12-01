import streamlit as st
from PIL import Image
import os
import pyttsx3
import pytesseract
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize Google Generative AI with API Key
API_KEY = 'AIzaSyArOEt0GNyxnd6-h1i4V-Ur0O7iiEh53V8'  # Replace with your valid API key
os.environ["GOOGLE_API_KEY"] = API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Styling
st.markdown(
    """
    <style>
        body {
            background-color: #f9f9f9;
            font-family: 'Arial', sans-serif;
        }
        .main-header {
            background: linear-gradient(90deg, #1d3557, #457b9d);
            color: white;
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .subheading {
            font-size: 18px;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .feature-header {
            font-size: 24px;
            color: #34495e;
            font-weight: bold;
            margin-top: 40px;
        }
        .sidebar {
            font-size: 16px;
            color: #2c3e50;
            padding: 10px;
        }
        .sidebar-header {
            font-size: 20px;
            color: #1d3557;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .button {
            background-color: #457b9d;
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 5px;
            width: 100%;
        }
        .button:hover {
            background-color: #1d3557;
        }
        .spinner {
            color: #1d3557;
        }
          footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #1d3557;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 2px solid #457b9d;
            z-index: 1000;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Title with Background
st.markdown('<div class="main-header">AI Vision Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subheading">Empowering visually impaired individuals with AI-powered tools</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown(
    """
    <div class="sidebar">
        <h3 class="sidebar-header">Features</h3>
        <ul>
            <li><b>Describe Scene</b>: Get AI insights about the image, including objects and suggestions.</li>
            <li><b>Extract Text</b>: Extract visible text using OCR.</li>
            <li><b>Text-to-Speech</b>: Hear the extracted text aloud.</li>
        </ul>
        <p><b>AI Vision Assistant</b>: Helps visually impaired users by providing scene descriptions, text extraction, and speech.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Upload Image Section
st.markdown("<h3 class='feature-header'>Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Buttons Section
st.markdown("<h3 class='feature-header'>Features</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🖼️ Describe Scene", key="scene", help="Generate scene description from the image.")
ocr_button = col2.button("🔍 Extract Text", key="ocr", help="Extract text from the image using OCR.")
tts_button = col3.button("🔊 Text-to-Speech", key="tts", help="Convert the extracted text to speech.")

# Functions for functionality
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

# Process user interactions
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            response = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='feature-header'>Scene Description</h3>", unsafe_allow_html=True)
            st.write(response)

    if ocr_button:
        with st.spinner("Extracting text from the image..."):
            text = extract_text_from_image(image)
            st.markdown("<h3 class='feature-header'>Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", text, height=150)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            text = extract_text_from_image(image)
            if text.strip():
                text_to_speech(text)
                st.success("Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text found to convert.")

# Footer
st.markdown(
    """
    <footer>
        <p>Created by <strong>Santanu Prasad Nayak</strong>.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
