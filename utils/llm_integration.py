import os
import openai
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_information_with_llm(entity, search_results, query_template):
    # Construct the prompt
    prompt = f"Extract the requested information for '{entity}' from the following search results based on the prompt: '{query_template}'.\n\n"
    for result in search_results:
        prompt += f"Title: {result['title']}\nURL: {result['link']}\nSnippet: {result['snippet']}\n\n"

    # Send the prompt to OpenAI's API
    response = openai.Completion.create(
        engine="text-davinci-003",  # Replace with the LLM model you want to use
        prompt=prompt,
        max_tokens=100,            # Adjust based on the required response length
        temperature=0              # Low temperature for focused results
    )

    # Return the extracted information
    return response.choices[0].text.strip()


