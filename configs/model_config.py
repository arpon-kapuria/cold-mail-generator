import os

from langchain_groq import ChatGroq
from langchain_cohere import CohereRerank
from langchain_community.embeddings import JinaEmbeddings

from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="meta-llama/llama-4-maverick-17b-128e-instruct"
)

embeddings = JinaEmbeddings(
    jina_api_key=os.getenv("JINA_API_TOKEN"),
    model_name="jina-embeddings-v3"
)

compressor = CohereRerank(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model="rerank-v3.5",
    top_n=10
)