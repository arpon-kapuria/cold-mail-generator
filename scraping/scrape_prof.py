import sys
from typing import List, Union
from collections import defaultdict

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

from configs.model_config import llm
from processing.data_cleaning import clean_text, remove_empty_values
from composer.prompts import prompt_extract_prof

def load_data(source: Union[str, List[str]]):
    """
    Load text either from a URL / URLs using LangChain.
    """

    if isinstance(source, list):
        loader = WebBaseLoader(source)
    else:
        loader = WebBaseLoader([source])

    documents = loader.load()
    data = " ".join([doc.page_content for doc in documents])
    
    return data


def getJsonData(data: str, token_limit=6000):
    """
    Sends professor's scrapped data to an llm to convert it into a JSON format, through API calls and custom prompt.
    Only splits the text into chunks if the token limit is exceeded.
    """
    
    chain = prompt_extract_prof | llm 
    json_parser = JsonOutputParser()

    try:
        res = chain.invoke({"page_data" : data})
        return json_parser.parse(res.content)
    
    except Exception as e:
        # print("Full input failed. Falling back to chunks...")
        print("I see... you've passed a huge amount of data. I might take some extra time. Stay there!")

        # Fallback: split and process in chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 3000,
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
                print("Server Error. Try again after some time...")
                # print(f"Chunk {i+1} failed:", e)
                sys.exit()

        return dict(final_output)


def getProfessorData(url: Union[str , List[str]] = None, papers: Union[str, List[str]] = None):
    """
    Process Professor data from a URL, clean it, and returns JSON data.
    """
        
    scraped_data = load_data(url)
    formatted_data = clean_text(scraped_data)
    
    json_data = getJsonData(formatted_data)

    if papers:
        return remove_empty_values(json_data), papers
    else:
        return remove_empty_values(json_data), ""
