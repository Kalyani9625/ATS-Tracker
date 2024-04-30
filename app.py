import streamlit as st
import os
import google.generativeai as genai
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

input_prompt1 = """
Hey, Act like a skilled or very experience ATS (Applicable Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst and big data engineer.
Your task is to evaluate the resine based on the given job description
You must consider the job market is very competitive and you should provide
best assistance for improving the resumes. Assign the percentage Matching based
on Jd and
the missing keywords with high accuracy
resume: {text}
description: {jd}
I want the response in one single string having the structure
{{"JD Match":"%", "MissingKeywords: []", "Profile Summary":""}}
"""
## Streamlit App
st.title("Smart ATS")
st.text("Let's Analyse your Resume 😉")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload Your Resume", type='pdf', help= "Please upload the resume")

submit1 = st.button("Get Your Answer")

if submit1:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt1)
        st.subheader(response)

