import json

from configs.model_config import compressor
from processing.data_cleaning import extract_info

from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

def retrieve_similar_info(applicant_json_data, prof_db):
    """
    Retrieves similar info from professor's database.
    [Optional] : Has setup for reranker as well.
    """

    # Flatten and format JSON as readable text
    applicant_text = json.dumps(applicant_json_data, indent=2)

    # Extracts specific features from applicant data
    extracted_applicant_features = extract_info(applicant_json_data)
    extracted_applicant_text = json.dumps(extracted_applicant_features,indent=2)

    query = (
        "Retrieve information such as professor's research topics, publications, current projects, and interests that match "
        "the applicant's data—especially academic background, research interests, skills, relevant experiences, publications or projects "
        "The aim is to find meaningful overlaps and similarities between them to write a cold email introducing the applicant, "
        "explaining interest in the professor’s work, and showing alignment in experience and goals."
    )

    query_context = f"{query}\n\nApplicant Data:\n{extracted_applicant_text}"
    
    retrieved_info = prof_db.invoke(query_context)


    # [OPTIONAL] : Use a reranker on retrieved_data   
    compression_retriever = ContextualCompressionRetriever(
        base_compressor = compressor,
        base_retriever = prof_db
    )
    compressed_docs = compression_retriever.invoke(query_context)

    """
    [OPTION 1]: Return applicant_text and retrived_info, if Reranker is NOT used
    [OPTION 2]: Return applicant_text and compressed_docs, if Reranker is used
    """
    return applicant_text, retrieved_info