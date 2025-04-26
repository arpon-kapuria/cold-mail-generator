import os
import sys
from datetime import datetime
from langchain_core.output_parsers import StrOutputParser

from configs.model_config import llm
from composer.prompts import prompt_mail


def save_generated_mail(res):
    """
    Write the generated mail to a .TXT file in Outputs folder.
    """

    # Directory setup
    base_dir = os.path.dirname(__file__)
    DATA_DIR = os.path.join(base_dir, "..", "outputs")
    os.makedirs(DATA_DIR, exist_ok=True)

    # Create filename with current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"Email_{timestamp}.txt"

    path = os.path.join(DATA_DIR, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(res.strip())

def generate_mail(applicant_text, prof_text, read_papers, degree):
    """
    Gets the applicant and professors's data and generate mail
    """
    
    prof_data = "\n".join([doc.page_content for doc in prof_text])
    applicant_data = applicant_text
    papers = read_papers
    degree_seeking = degree

    parser = StrOutputParser()

    chain_email = prompt_mail | llm | parser

    try :
        res = chain_email.invoke(input={
            'applicant_info' : applicant_data,
            'professor_info' : prof_data,
            'read_papers': papers,
            'degree' : degree_seeking
        })
        if not papers:
            print("As you haven't read any paper, I will pick a random paper close to your background. ")
        
        print("\n📧 Here is your Email. As it's AI generated, it's prone to mistakes. Feel free to modify the content - \n")
        print(res)

        # Writes the generated mail to a file
        save_generated_mail(res)

    except Exception as e:
        print("Server Error. Try again after some time...")
        # print("Exact error: ", e)
        sys.exit()

        
