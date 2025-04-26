# 📧 RAG Powered Cold Email Generator 

This is a Retrieval-Augmented Generation (RAG) project that automates the creation of personalized cold emails for prospective Master's or PhD students reaching out to professors. It leverages vector search and large language models to craft highly tailored emails based on both the applicant’s and professor’s information.

---

### ✨ Features

1. **Generates emails based on:**
   - Applicant's profile and academic background
   - Professor's research interests and works
   - Papers read (or smart matching if no papers are read)
2. **Smart fallback:**  
   If no papers have been read, the system automatically matches professor's papers to the applicant's research experience.
3. **Human-like personalization:**  
   Emails are crafted to feel genuine, motivated, and thoughtful.
4. **Auto-save:**  
   Generated emails are saved neatly with timestamps for easy later editing.

> **Note:**  
> Please review and edit the email slightly before sending. While the LLM does a good job, small personal tweaks make it even better.

---

### 🧰 Tech Stack 

- **Core Programming Language:** Python 
- **LLM Framework:** LangChain
- **Vector Database:** FAISS
- **Web Scraping:** BeautifulSoup4
- **Chat Model:** llama-4-maverick-17b-128e-instruct (Groq AI)
- **Embedding Model:** jina-embeddings-v3 (Jina AI)
- **Reranking Model:** rerank-v3.5 (Cohere AI)

---

## 🗂️ Project Structure

```
cold-mail-generator/
├── composer/
│   ├── draft_mail.py       # Generates and formats the email draft
│   └── prompts.py          # Contains prompt templates for the LLM
│
├── configs/
│   └── model_config.py     # Configuration settings for the models (language, embedding, reranking)
│
├── env/                    # Virtual environment directory
│
├── outputs/                # Stores generated emails with timestamps
│
├── processing/
│   ├── data_cleaning.py    # Cleans and preprocesses scraped data and features
│   ├── database.py         # Handles data storage and embeddings
│   └── retrieval.py        # Extracts relevant information from database
│
├── scraping/
│   ├── scrape_prof.py      # Scrapes professor's information
│   └── scrape_user.py      # Processes applicant's information
│
├── .env                    # Environment variables (e.g., API keys)
├── .gitignore              # Specifies files and folders to ignore in Git
├── main.py                 # Main script to run the application
├── README.md               # Project documentation
└── requirements.txt        # Dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 
- Git installed on your system

---

### 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/arpon-kapuria/cold-mail-generator.git
   cd cold-email-generator
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3.9 -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install project dependencies**

   ```bash
   pip3.9 install -r requirements.txt
   
   # If the above doesn't work, try:
   pip install -r requirements.txt 
   ```
   

4. **Set up environment variables**

   Create a `.env` file in the root directory and add necessary environment variables:

   ```
   GROQ_API_KEY=<groq_api_key>
   JINA_API_TOKEN=<jina_api_token>
   COHERE_API_KEY=<cohere_api_key>
   ```

---

### 📝 How to Run

1. **Provide the required inputs in main.py**

   - Your applicant profile.
   - Professor's website URL.
   - List of papers you have read (optional).
   - Degree you are applying for (`masters` or `phd`).

2. **Execute the main script**

   ```bash
   python3.9 main.py
   ```

2. **Result**

   - Your generated cold email will be printed on the screen AND saved automatically as a .txt file with the current date and time inside the `outputs/` folder.
   - The email file will be named like:  
     ```
     Email_YYYY-MM-DD_HH-MM-SS.txt
     ```

---

### ⚙️ Customization

- **Prompt Template**  
  Modify `composer/prompts.py` to customize the tone, structure, or content of the generated emails.

- **Model Settings**  
  Adjust `configs/model_config.py` to change LLM parameters such as model name, temperature, etc.

- **Data Cleaning & Retrieval**  
  Enhance or change data processing logic inside the `processing/` directory.

- **Reranking**
  Use reranker in `preprocessing/retrival.py` to retrieve more specific information. Currently this project doesn't use Reranker but it has reranking support.

---

### 📋 Notes

- `.env` must be configured properly with the required keys.
- Internet connection is required for scraping professor data and calling the language model API.
- Use responsibly and ethically while contacting professors.

---

### 🤝 Contributing

Contributions are always welcome. Potential areas to work on -

- **Data Formatting & Chunking:**  
  Enhance how data is preprocessed before storing it into the database for better retrieval efficiency.

- **Improved Retrieval:**  
  Implement smarter techniques to fetch more relevant and similar information from the vector database.

- **Advanced Reranking:**  
  Integrate reranker models more effectively to prioritize the most contextually relevant results.

- **Prompt Engineering:**  
  Design even better prompts to guide the LLM into generating more precise, context-aware, and impactful emails.


