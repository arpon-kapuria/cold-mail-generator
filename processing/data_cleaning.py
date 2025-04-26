import re

def clean_text(text: str) -> str:
    """
    Clean and normalize scrapped or extracted text.
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters (excluding some punctuation if necessary)
    text = re.sub(r'[^\w\s.,!?\'\"-]', '', text)  # Keep common punctuation
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())

    return text


def remove_empty_values(data):
    """
    Removes any empty key-value pair from the json data.
    """
    if isinstance(data, dict):
        return {k: remove_empty_values(v) for k, v in data.items() if v not in ("", [], {}, None)}
    elif isinstance(data, list):
        return [remove_empty_values(item) for item in data if item not in ("", [], {}, None)]
    else:
        return data
    

def extract_info(data):
    """
    Extracts some key specific values from json data
    """
    research_interests = data.get("research_interests", [])
    skills = data.get("skills", [])

    # Get all projects
    projects = [value for key, value in data.items() if key.startswith("project")]

    # Get all experiences
    experience = [value for key, value in data.items() if key.startswith("experience")]

    # Get all publications
    publications = [value for key, value in data.items() if key.startswith("all_publications")]

    return {
        "research_interests": research_interests,
        "projects": projects,
        "experience": experience,
        "publications": publications,
        "skills": skills
    }