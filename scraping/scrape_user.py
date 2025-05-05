import sys
from typing import List, Union, Literal
from collections import defaultdict

from langchain_community.document_loaders import WebBaseLoader, PyMuPDFLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

from configs.model_config import llm
from processing.data_cleaning import clean_text, remove_empty_values
from composer.prompts import prompt_extract_user, combined_data_template

import streamlit as st


def load_data(source: Union[str, List[str]], source_type: Literal['url', 'pdf']):
    """
    Load text either from a URL or a PDF using LangChain.
    """

    if source_type == "url":
        if isinstance(source, list):
            loader = WebBaseLoader(source)
        else:
            loader = WebBaseLoader([source])
    elif source_type == "pdf":
        loader = PyMuPDFLoader(source)
    else:
        raise ValueError("Invalid source type. Use only 'url' or 'pdf'.")
        sys.exit()
    
    documents = loader.load()
    data = " ".join([doc.page_content for doc in documents])
    
    return data


def json_data_using_chunking(chain, data):
    """
    Chunk the Applicant data, then pass it to an LLM
    """

    json_parser = JsonOutputParser()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_text(data)
    final_output = defaultdict(list)

    for i, chunk in enumerate(chunks):
        try:
            res = chain.invoke({"page_data" : chunk})
            parsed_json = json_parser.parse(res.content)

            for key, value in parsed_json.items():
                if isinstance(value, list):
                    final_output[key].extend(value)
                elif isinstance(value, str) and value and not final_output[key]:
                    final_output[key] = value
        except Exception as e:
            st.write("Server Error. Try again after some time...")
            sys.exit()
            # print(f"Chunk {i+1} failed:", e)
            # continue

    return dict(final_output)


def getJsonData(data: str):
    """
    Send Applicant's data to an LLM to convert it into JSON
    """
    
    chain_extract = prompt_extract_user | llm
    json_parser = JsonOutputParser()
    
    try:
        res = chain_extract.invoke(input={'page_data' : data})
        return json_parser.parse(res.content)
    
    except Exception as e:
        # print("Full input failed. Falling back to chunks...")
    
        return json_data_using_chunking(chain_extract, data) 

'''
WHEN COMBINING DATA, FOCUS - 

skills from pdf data only
research interest from pdf data only
project description from pdf_data more
'''

def getCombinedJsonData(url_data : str, pdf_data : str):
    """
    Combine Applicant data from URL and PDF, returns JSON
    """

    chain_combined_data = combined_data_template | llm
    json_parser = JsonOutputParser()

    combined_res = chain_combined_data.invoke(input={'url_data' : url_data, 'pdf_data' : pdf_data})

    try:
        json_data = json_parser.parse(combined_res.content)
    except Exception as e:
        st.write("Parsing Error. Please try again...")
        # print("❌ JSON parsing error:", e)
        # print("Please try again !")
        # return {}
        sys.exit()

    return json_data


def getApplicantData(url: Union[str , list] = None, pdf_path: str = None):
    """
    Process Applicant data from a URL or PDF (or both), clean it, and returns JSON data.
    """
    url_data = None
    pdf_data = None

    # Handle URL
    if url:
        scraped_url_data = load_data(url, "url")
        clean_url_data = clean_text(scraped_url_data)
        url_data = getJsonData(clean_url_data)
    
    # Handle PDF
    if pdf_path:
        scraped_pdf_data = load_data(pdf_path, "pdf")
        clean_pdf_data = clean_text(scraped_pdf_data)
        pdf_data = getJsonData(clean_pdf_data)
    
    # Merge data if both provided
    if url_data and pdf_data:
        final_json_data = getCombinedJsonData(url_data, pdf_data)  
    elif url_data:
        final_json_data = url_data
    elif pdf_data:
        final_json_data = pdf_data

    return remove_empty_values(final_json_data)

    # save_applicant_data(applicant_id, final_json_data)

