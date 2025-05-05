from scraping.scrape_prof import getProfessorData
from scraping.scrape_user import getApplicantData

from composer.draft_mail import generate_mail
from processing.database import setup_database
from processing.retrieval import retrieve_similar_info

import streamlit as st
import tempfile
import time


# 
#   Input setup 

#   Applicant's data :
#       - url link / links [optional]
#       - pdf file (single) [mandatory]

#   Professor's data :
#       - url link / links [mandatory]
#       - papers read (single/multiple) [optional]
#


st.set_page_config(page_title="Cold Email Generator", layout="centered")

# --- Sidebar ---
st.sidebar.title("📌 About This Project")
st.sidebar.markdown("""
**Cold Email Generator** is an AI-powered app that helps students generate personalized emails to professors by analyzing their resumes and the professor’s research interests.

### 🎯 Who is this for?
- Prospective **PhD** or **Master's** students
- Anyone emailing professors for **research opportunities**

### 📚 What does it do?
- Scrapes your resume and online profile
- Analyzes the professor’s research website
- Matches your background with their work
- Generates a custom cold email

### 🚀 How to use?
1. Paste the **professor’s website** URL.
2. Add your **portfolio URLs** *(optional)*.
3. Upload your **PDF resume** *(mandatory)*.
4. Mention **papers you've read** *(optional)*.
5. Choose your **target degree**.
6. Click **Generate Email** and copy your output!
                    
### 🌐 Explore More -

- 🔗 [**GitHub**](https://github.com/arpon-kapuria/cold-mail-generator) — Star it if you find it useful !
- 🔗 [**Author**](https://arpon-kapuria.github.io/) — Know more about me, my work & thoughts !

""")

# --- Main Content ---
st.title("📧 RAG Powered Cold Email Generator")
st.markdown("Generate personalized, research-specific emails for professors using your resume and their research pages.")

with st.form("input_form"):

    prof_url = st.text_input("🔗 Professor's Website URL (mandatory)")

    applicant_urls = st.text_area(
        "🌐 Applicant's Website URLs (optional, comma-separated)",
        placeholder="https://yourportfolio.com, https://yourblog.com"
    )

    pdf_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])
    
    paper_titles = st.text_area(
        "📚 Papers you've read (optional)", 
        placeholder="e.g., Deconstructing denoising diffusion models, MoCo for SSL"
    )

    degree = st.selectbox("🎓 Degree Seeking", ["PhD", "Master's"])

    submit = st.form_submit_button("🚀 Generate Email")

if submit:
    if not pdf_file or not prof_url:
        st.error("Please upload your resume and provide the professor's website.")
    else:
        with st.spinner("Processing and generating email..."):
            try:
                # Process URLs
                applicant_url_list = [url.strip() for url in applicant_urls.split(",") if url.strip()]
                paper_list = [paper.strip() for paper in paper_titles.split(",") if paper.strip()]

                time.sleep(2)

                if not paper_list:
                    st.write("Ah you haven't read any paper. You just made my work harder :(")

                # Save PDF temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(pdf_file.read())
                    pdf_path = tmp.name

                # Scrape data
                applicant_json_data = getApplicantData(url=applicant_url_list, pdf_path=pdf_path)
                prof_json_data, read_papers = getProfessorData(url=prof_url, papers=paper_list)

                st.write("Sorry If I am taking too long. Data is too large for me, but I am almost there . . ")

                # Setup vector DB and retrieve info
                database = setup_database(prof_json_data)
                applicant_info, retrieved_info = retrieve_similar_info(applicant_json_data, database)

                # Generate final email
                email = generate_mail(applicant_info, retrieved_info, read_papers, degree=degree)

                st.success("✅ Here is your Email. As it's AI generated, it's prone to mistakes. Feel free to modify the content . . . ")

                st.text_area("📬 Your Generated Email", email, height=500)

            except Exception as e:
                st.error(f"❌ Error: {e}")




