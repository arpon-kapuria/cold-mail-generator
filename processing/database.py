import json

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from configs.model_config import embeddings


def setup_database(prof_json_data):
    """
    Gets the professor's data and initializes the vector database
    """

    json_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30
    )

    # Split prof data and get texts
    prof_data_str = json.dumps(prof_json_data)
    prof_json_chunks = json_splitter.split_text(prof_data_str)

    # Get embeddings from professor's data
    text_embeddings = embeddings.embed_documents(texts=prof_json_chunks)
    text_embeddings_pair = list(zip(prof_json_chunks, text_embeddings))

    # Initialize the database
    prof_db = FAISS.from_embeddings(text_embeddings_pair, embeddings).as_retriever(search="similarity", search_kwargs={"k": 30})

    return prof_db