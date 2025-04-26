from langchain_core.prompts import PromptTemplate

prompt_extract_user = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM APPLICANT'S WEBSITE:
    {page_data}

    ### YOUR TASK:
    You are an intelligent assistant helping a PhD/Master’s applicant organize their academic profile. Extract and summarize all useful information from the given portfolio website content and return it in a **well-formatted JSON object** with the following structure:

    {{
        "name": "",
        "email": "",

        "education 1": {{
            "degree": "",
            "department": "",
            "institute": "",
            "location": "",
            "Year": ""
        }},
        "education 2": {{
            "degree": "",
            "department": "",
            "institute": "",
            "location": "",
            "Year": ""
        }},
        ...

        "experience 1": {{
            "title": "",
            "organization": "",
            "location": "",
            "duration": "",
            "advisor": "",
            "description": ""
        }},
        "experience 2": {{
            "title": "",
            "organization": "",
            "location": "",
            "duration": "",
            "advisor": "",
            "description": ""
        }},
        ...

        "project 1": {{
            "title": "",
            "duration / year": "",
            "description": "",
            "tech_stack": []
        }},
        "project 2": {{
            "title": "",
            "duration / year": "",
            "description": "",
            "tech_stack": []
        }},
        ...
        "all_publications": [],
        "research_interests": [],
        "skills": [],
        "goals": ""
    }}

    ### INSTRUCTIONS:
    - Fill all fields only with the information present in the input text.
    - If a field is not found, return an empty string or skip it.
    - For projects description, extract all the information you can get.
    - Use brief, clear language.
    - Do not make up or hallucinate any data.
    - Avoid duplicates or redundant entries.
    - Ensure all field names match **exactly** and return **valid JSON only**.
    - Give a final check and if you find any key that has no value, then remove that key from the json_format_data (Don't keep any empty key-value pair)

    ### OUTPUT FORMAT:
    Return only the JSON object as per the structure above. No preamble, no commentary, no markdown.
    """
)

combined_data_template = PromptTemplate.from_template(
    """
    ### URL DATA:
    {url_data}
    
    ### PDF DATA:
    {pdf_data}
    
    ### TASK:
    You are an intelligent assistant helping a PhD/Master’s applicant organize their academic profile. Integrate and prioritize the best data from both URL and PDF. Return the combined result in JSON format.

    ## INSTRUCTIONS:
    - Don't combine skills and research interests from {url_data} and {pdf_data}, take informations only from {pdf_data}
    - Handle missing or incomplete fields by using information from the other source.
    - Prioritize essential data from both sources.
    - Return only valid JSON.

    ### OUTPUT FORMAT:
    Return only the JSON object as per the structure above. No preamble, no commentary, no markdown.
    """
)

prompt_extract_prof = PromptTemplate.from_template(
    """
    ### PROFESSOR PROFILE TEXT:
    {page_data}

    ### TASK:
    You are an intelligent academic assistant. From the given professor profile, extract as much structured information as possible. Return your output in the following JSON format:

    {{
        "name": "",                           // Full name
        "email": "",                          // Email address if available
        "university": "",                     // University or institution name
        "department": "",                     // Department, school, or lab name
        "position": "",                       // Academic or professional title
        "homepage": "",                       // Full homepage URL if found
        "google_scholar": "",                 // Google Scholar link, if available
        "linkedin": "",                       // LinkedIn URL if available
        "lab_website": "",                    // Personal/Lab website if mentioned
        "research_interests": [],            // List of research topics or focus areas
        "keywords": [],                      // Technical terms, methods, subfields, tools, etc.
        "bio": "",                            // Biography or overview paragraph
        "education": [],                     // List of degrees, institutions, and years
        "positions_held": [],               // Previous academic/professional roles
        "awards": [],                        // Awards, fellowships, honors
        "grants": [],                        // Grants or funding received
        "teaching": [],                      // Courses taught or teaching experience
        "students": [],                      // List of current or former PhD/Postdoc students (if any)
        "collaborators": [],                 // List of notable collaborators (if mentioned)
        "recent_publications": [],           // Up to 10 recent publications with full titles
        "all_publications": [],              // All publication titles found (can be longer list)
        "projects": [],                      // List of research projects with short descriptions
        "service": [],                       // Editorial boards, conferences, committees served on 
        "contact": "",                       // Physical office address or phone (if listed)
        "extra_links": []                    // Any extra URLs mentioned (DBLP, ORCID, CV, etc.)
    }}

    ### INSTRUCTIONS:
    - Try to extract everything.
    - Fill each field with **only what is explicitly found** in the profile text.
    - Do not make assumptions or hallucinate. If something is not mentioned, leave it empty or as an empty list.
    - Keep the JSON structure exactly as shown above.
    - Use bullet points or short descriptions where appropriate.
    - For publication titles, use exact formatting and punctuation from the profile.
    - Maintain valid JSON syntax. Do not include any explanatory text before or after the JSON.
    - Give a final check and if you find any key that has no value, then remove that key from the json_format_data (Don't keep any empty key-value pair)

    ### OUTPUT FORMAT:
    Valid JSON only.
    """
)

prompt_mail = PromptTemplate(
    input_variables=["applicant_info", "professor_info", "read_papers", "degree"],
    template = """
        This is year 2025. You are a highly motivated {degree} applicant reaching out to a professor whose work aligns closely with your academic interests and background. Write a cold email that clearly expresses interest in joining the professor’s research group, demonstrates alignment in research goals, and highlights relevant experiences or skills.

        Based on the applicant's profile:
        {applicant_info}

        And the professor's information:
        {professor_info}

        Name of the papers read by applicant:
        {read_papers}

        ***INSTRUCTIONS***
        - Write a concise, well-structured, and compelling cold email with a tone that is respectful, enthusiastic, and intellectually curious.
        - Keep it human written mail, as much as possible.
        - For Subject, write "Prospective {{degree.capitalize()}} Student - ", then keep empty space for the user to write their session, like this : `[Insert your intended session]`

        - OPENING PARAGRAPH:
            - Mention your name, your completed highest degree (with institute and year), and your country.
            - Clearly state your intent to apply for a {degree} position under the professor’s supervision.

        - MIDDLE PARAGRAPH(S):
            - WRITE MAXIMUM 3-4 LINES HERE.
            - Briefly state what aspect of the professor’s work attracts you and how your previous experiences  at any institution/skills/projects/research, related to the professor's work, align with the professor’s interests.
            - Include specific areas, problems, or approaches you find exciting in their work.
            - For read papers, use the names provided in {read_papers} and briefly explain one in a sentence.
            - If {read_papers} seems unspecified or unavailable, find paper(s) from the professor’s profile that align with the applicant's past research or projects and include them naturally.
            - Never mention that you didn’t read any papers — always reference at least one specific paper that fits the applicant’s interests.

        - CLOSING PARAGRAPH:
            - Politely express your hope for future discussion or feedback.
            - Mention that your CV, transcript, and portfolio are available for reference.

        - DO NOT include preambles like “Hope this email finds you well.”
        - DO NOT sound generic or overly formal — write like a real, thoughtful student reaching out.
        - Finish with [Sincerely, You name]
        - NO PREAMBLE
    """
)