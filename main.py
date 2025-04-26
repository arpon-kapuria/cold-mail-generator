from scraping.scrape_prof import getProfessorData
from scraping.scrape_user import getApplicantData

from composer.draft_mail import generate_mail
from processing.database import setup_database
from processing.retrieval import retrieve_similar_info


"""
@ Input setup 

    Applicant's data :
        - url link / links [optional]
        - pdf file (single) [mandatory]

    Professor's data :
        - url link / links [mandatory]
        - papers read (single/multiple) [optional]

"""

if __name__== "__main__":

    # link to the applicant's portfolio website [OPTIONAL]
    applicant_url = [
        "https://arpon-kapuria.github.io/index.html",
        "https://arpon-kapuria.github.io/experience.html",
        "https://arpon-kapuria.github.io/blogs.html"
    ]

    # path to applicant's resume (.pdf)
    pdf_path = "resume.pdf"

    # link to the professor's website
    prof_url = "https://www.sainingxie.com/"

    # name of the papers, you have read any [OPTIONAL]
    papers_read = [
        "Deconstructing denoising diffusion models for self-supervised learning",
        "Momentum Contrast for Unsupervised Visual Representation Learning"
    ]

    # Degree seeking [Master's / PhD]
    degree = "PhD"


    # Scrape applicant's data and return JSON data
    applicant_json_data = getApplicantData(url=applicant_url, pdf_path=pdf_path)

    print("Information scraping")

    # Scrape professor's data and return JSON data
    prof_json_data, read_papers = getProfessorData(url=prof_url, papers=papers_read)

    print("Vector database being setup")

    # Setup vector db on professor data
    database = setup_database(prof_json_data)

    # Retrives data similar to the applicant's background
    applicant_info, retrieved_info = retrieve_similar_info(applicant_json_data, database)

    print("Generating mail...")
    
    # Finally Generate the mail
    generate_mail(applicant_info, retrieved_info, read_papers, degree=degree)
