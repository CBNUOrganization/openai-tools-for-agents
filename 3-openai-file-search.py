from openai import OpenAI
import requests
from io import BytesIO

client = OpenAI()

# Upload file into OpenAI server
def create_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print(result.id)
    return result.id

# Function to create vector store in OpenAI
def create_vector_store(file_id):
    vector_store = client.vector_stores.create(
        name = "knowledge_base"
    )
    print(vector_store.id)
    client.vector_stores.files.create(
        vector_store_id = vector_store.id,
        file_id = file_id
    )
    
    result = client.vector_stores.files.list(
        vector_store_id=vector_store.id
    )
    print(result)
    return vector_store.id

import os

file_path = "./files/deep_research_blog.pdf"
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found.")
else:
    print(f"File found: {file_path}")

# Replace with your own file path or URL, you can upload file locally or using site.
file_id = create_file(client, file_path)

# Create Vector Store
vector_store_id = create_vector_store(file_id)

# Create File Search response
response = client.responses.create(
    model="gpt-4o-mini",
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store_id],
        "max_num_results" : 3,    # Limiting the number of retrieval results
        "filters": {              # Attribute filtering helps narrow down results by applying criteria
            "type": "eq",
            "key": "title",  # filename, type, etc.
            "value": "deep research"
        }
    }]
)
print("raw result: ", response)

# Get only the content
response_text = next(
    (content.text for output in response.output if output.type == "message"
     for content in output.content if content.type == "output_text"),
    "No response text found"
)
print(response_text)