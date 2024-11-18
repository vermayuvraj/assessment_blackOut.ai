import os
from serpapi import GoogleSearch

# Load API key from environment variables
SERP_API_KEY = os.getenv("SERP_API_KEY")

def search_web(query):
    params = {
        "q": query,
        "hl": "en",  # Language
        "gl": "us",  # Country
        "api_key": SERP_API_KEY
    }
    
    # Initialize SerpAPI client
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract URLs and snippets (limit to top 3 results for simplicity)
    search_results = []
    for result in results.get("organic_results", [])[:3]:
        search_results.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet")
        })
    
    return search_results
