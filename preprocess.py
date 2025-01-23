# import json
# from llm_helper import llm
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.exceptions import OutputParserException

# def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
#     enriched_post = []
#     with open(raw_file_path, encoding="utf-8", errors="ignore") as file:
#         posts = json.load(file)
#         for post in posts:
#             # Sanitize the text to handle invalid characters
#             post["text"] = post["text"].encode("utf-8", errors="ignore").decode("utf-8")
#             metadata = extract_metadata(post["text"])
#             post_with_metadata = post | metadata
#             enriched_post.append(post_with_metadata)

#         for epost in enriched_post:
#             print(epost)

# def extract_metadata(post):
#     template = '''You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
#     1. Return a valid JSON. No preamble. 
#     2. JSON object should have exactly three keys: line_count, language and tags. 
#     3. tags is an array of text tags. Extract maximum two tags.
#     4. Language should be English or Hinglish (Hinglish means Hindi + English)
    
#     Here is the actual post on which you need to perform this task:  {post}'''

#     pt = PromptTemplate.from_template(template)
#     chain = pt | llm
#     response = chain.invoke(input={"post": post})

#     try:
#         # Sanitize response content to handle invalid characters
#         response_content = response.content.encode("utf-8", errors="ignore").decode("utf-8")
#         json_parser = JsonOutputParser()
#         res = json_parser.parse(response_content)
#     except OutputParserException:
#         raise OutputParserException("Context too big. Unable to parse jobs.")
#     return res

# if __name__ == "__main__":
#     process_posts("data/raw_data.json", "data/processed_posts.json")

# import json
# import os
# from llm_helper import llm
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.exceptions import OutputParserException

# def process_posts(raw_file_path, processed_file_path=None):
#     # Check if the input file exists
#     if not os.path.exists(raw_file_path):
#         raise FileNotFoundError(f"Input file not found: {raw_file_path}")
    
#     with open(raw_file_path, encoding='utf-8', errors='ignore') as file:
#         posts = json.load(file)
#         enriched_posts = []
#         for post in posts:
#             post['text'] = post['text'].encode("utf-8", errors="ignore").decode("utf-8")
#             metadata = extract_metadata(post['text'])
#             post_with_metadata = post | metadata
#             enriched_posts.append(post_with_metadata)

#     unified_tags = get_unified_tags(enriched_posts)
#     for post in enriched_posts:
#         current_tags = post['tags']
#         new_tags = {unified_tags[tag] for tag in current_tags}
#         post['tags'] = list(new_tags)

#     with open(processed_file_path, encoding='utf-8', mode="w", errors='ignore') as outfile:
#         json.dump(enriched_posts, outfile, indent=4)

# def extract_metadata(post):
#     template = '''
#     You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
#     1. Return a valid JSON. No preamble. 
#     2. JSON object should have exactly three keys: line_count, language and tags. 
#     3. tags is an array of text tags. Extract maximum two tags.
#     4. Language should be English or Hinglish (Hinglish means hindi + english)
    
#     Here is the actual post on which you need to perform this task:  
#     {post}
#     '''

#     pt = PromptTemplate.from_template(template)
#     chain = pt | llm
#     response = chain.invoke(input={"post": post})

#     try:
#         json_parser = JsonOutputParser()
#         res = json_parser.parse(response.content)
#     except OutputParserException:
#         raise OutputParserException("Context too big. Unable to parse jobs.")
#     return res

# def get_unified_tags(posts_with_metadata):
#     unique_tags = set()
#     # Loop through each post and extract the tags
#     for post in posts_with_metadata:
#         unique_tags.update(post['tags'])  # Add the tags to the set

#     unique_tags_list = ','.join(unique_tags)

#     template = '''I will give you a list of tags. You need to unify tags with the following requirements,
#     1. Tags are unified and merged to create a shorter list. 
#        Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
#        Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
#        Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
#        Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
#     2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
#     3. Output should be a JSON object, No preamble
#     3. Output should have mapping of original tag and the unified tag. 
#        For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation"}}
    
#     Here is the list of tags: 
#     {tags}
#     '''
#     pt = PromptTemplate.from_template(template)
#     chain = pt | llm
#     response = chain.invoke(input={"tags": str(unique_tags_list)})
#     try:
#         json_parser = JsonOutputParser()
#         res = json_parser.parse(response.content)
#     except OutputParserException:
#         raise OutputParserException("Context too big. Unable to parse jobs.")
#     return res

# if __name__ == "__main__":
#     try:
#         process_posts("data/raw_data.json", "data/processed_posts.json")
#     except FileNotFoundError as e:
#         print(e)
#         # Optionally create a sample raw_data.json file for testing
#         os.makedirs("data", exist_ok=True)
#         sample_data = [
#             {"text": "This is a sample LinkedIn post about AI and machine learning.", "tags": []}
#         ]
#         with open("data/raw_data.json", "w", encoding="utf-8") as sample_file:
#             json.dump(sample_data, sample_file, indent=4)
#         print("Created a sample raw_data.json file. Run the script again.")



import json
import os
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def process_posts(raw_file_path, processed_file_path=None):
    # Check if the input file exists
    if not os.path.exists(raw_file_path):
        raise FileNotFoundError(f"Input file not found: {raw_file_path}")
    
    with open(raw_file_path, encoding='utf-8', errors='ignore') as file:
        posts = json.load(file)
        enriched_posts = []
        for post in posts:
            post['text'] = post['text'].encode("utf-8", errors="ignore").decode("utf-8")
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding='utf-8', mode="w", errors='ignore') as outfile:
        json.dump(enriched_posts, outfile, indent=4)

def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    # Loop through each post and extract the tags
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])  # Add the tags to the set

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation"}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res

if __name__ == "__main__":
    try:
        process_posts("data/raw_posts.json", "data/processed_posts.json")
    except FileNotFoundError as e:
        print(e)
        # Optionally create a sample raw_posts.json file for testing
        os.makedirs("data", exist_ok=True)
        sample_data = [
            {"text": "This is a sample LinkedIn post about AI and machine learning.", "tags": []}
        ]
        with open("data/raw_posts.json", "w", encoding="utf-8") as sample_file:
            json.dump(sample_data, sample_file, indent=4)
        print("Created a sample raw_posts.json file. Run the script again.")
