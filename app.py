import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import os

# Add custom CSS
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Center the title */
        .title {
            text-align: center;
            font-size: 2.5rem;
            color: #1f77b4;
            font-family: 'Arial', sans-serif;
        }
        /* Style the sidebar */
        .sidebar .sidebar-content {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
        }
        /* Style the buttons */
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            font-family: 'Arial', sans-serif;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        /* Style file upload box */
        .stFileUploader {
            border: 2px dashed #1f77b4;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Add styling
add_custom_css()

# PDF-to-Word Converter Functions
def pdf_to_text(file):
    """Extract text from PDF using PyPDF2."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def text_to_word(text, output_path):
    """Convert text to Word file using python-docx."""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_path)

# Image-to-PDF Converter Function
def image_to_pdf(image_file, output_path):
    """Convert an image to PDF using PIL."""
    image = Image.open(image_file)
    # Convert image mode to RGB if it's not already
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(output_path, "PDF")

# Streamlit UI
st.markdown("<h1 class='title'>File Converters</h1>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Choose a Converter")
converter_option = st.sidebar.radio("Select a converter:", ("PDF to Word", "Image to PDF"))

if converter_option == "PDF to Word":
    st.header("PDF to Word Converter")
    uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_pdf is not None:
        st.success("PDF file uploaded successfully!")

        # Button to process the file
        if st.button("Convert PDF to Word"):
            with st.spinner("Extracting text and converting to Word..."):
                extracted_text = pdf_to_text(uploaded_pdf)

            if extracted_text.strip():
                # Save as Word file
                output_filename = "converted_word_file.docx"
                text_to_word(extracted_text, output_filename)
                
                # Provide download link
                with open(output_filename, "rb") as word_file:
                    st.download_button(
                        label="Download Word File",
                        data=word_file,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                os.remove(output_filename)
            else:
                st.error("Failed to extract text from the PDF. Please try another file.")

elif converter_option == "Image to PDF":
    st.header("Image to PDF Converter")
    uploaded_image = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        st.success("Image file uploaded successfully!")

        # Button to process the image
        if st.button("Convert Image to PDF"):
            with st.spinner("Converting image to PDF..."):
                output_filename = "converted_image_file.pdf"
                image_to_pdf(uploaded_image, output_filename)
                
                # Provide download link
                with open(output_filename, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF File",
                        data=pdf_file,
                        file_name=output_filename,
                        mime="application/pdf"
                    )
                os.remove(output_filename)

st.caption("Built with ❤️ using Streamlit")
