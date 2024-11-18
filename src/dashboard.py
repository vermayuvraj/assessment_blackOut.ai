import streamlit as st

st.title("AI Agent Project Dashboard")
st.write("Upload a CSV file or connect to Google Sheets to start data processing.")


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Display the uploaded file's content
    st.write("Uploaded CSV file:")
    st.write(uploaded_file.name)


import pandas as pd

if uploaded_file is not None:
    # Read CSV file into a DataFrame
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(data.head())  # Display the first few rows


from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from JSON file
credentials = service_account.Credentials.from_service_account_file("AI-Agent-Project/src/client_secret.json")
scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/spreadsheets.readonly"])

# Initialize Google Sheets API
service = build("sheets", "v4", credentials=scoped_credentials)


sheet_url = st.text_input("Enter Google Sheets URL")
if sheet_url:
    sheet_id = sheet_url.split("/d/")[1].split("/")[0]  # Extract Sheet ID from the URL


if sheet_url:
    sheet_range = "Sheet1"  # Adjust to match your sheet name and range if necessary
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get("values", [])

    if values:
        data = pd.DataFrame(values[1:], columns=values[0])  # Assuming first row is header
        st.write("Google Sheets Data Preview:")
        st.dataframe(data)
    else:
        st.write("No data found in the specified Google Sheet.")


if uploaded_file or sheet_url:
    columns = data.columns
    main_column = st.selectbox("Select the primary column (e.g., company names)", columns)


if main_column:
    st.write("Selected Column Data Preview:")
    st.write(data[main_column].head())  # Display first few entries in the selected column


# Add a custom query input
query_template = st.text_input("Enter your query template", 
                               value="Get me the email address of {company}")

st.write("Query Template Preview:")
st.write(query_template)


# Example entity to preview how the query template will be formatted
if main_column:
    example_entity = data[main_column].iloc[0]  # Use the first entity as a sample
    sample_query = query_template.format(company=example_entity)
    st.write("Sample Query for Preview:")
    st.write(sample_query)


# Generate queries for each entity
queries = []
if main_column:
    for entity in data[main_column]:
        query = query_template.format(company=entity)
        queries.append(query)

    # Display a preview of the generated queries
    st.write("Generated Queries:")
    st.write(queries[:5])  # Show only the first 5 queries for preview


from utils.search_api import search_web

if queries:
    st.write("Testing Web Search:")
    sample_search_results = search_web(queries[0])  # Test with the first generated query
    st.write(sample_search_results)


all_search_results = []

if queries:
    for query in queries:
        # Perform the search and store the results
        results = search_web(query)
        all_search_results.append({
            "query": query,
            "results": results
        })

    # Display a sample of the collected results
    st.write("Sample of Search Results:")
    st.write(all_search_results[:5])  # Show only the first 5 for preview


import pandas as pd

# Convert search results into a DataFrame for easier processing in the next phase
results_df = pd.DataFrame([
    {"Entity": entity, "Query": query, "Results": results}
    for entity, query, results in zip(data[main_column], queries, all_search_results)
])

# Display structured results
st.write("Structured Search Results:")
st.dataframe(results_df.head())

results_df.to_csv("search_results.csv", index=False)

import time

for query in queries:
    results = search_web(query)
    all_search_results.append({"query": query, "results": results})
    time.sleep(1)  # Pause to avoid hitting rate limits

for query in queries:
    try:
        results = search_web(query)
        all_search_results.append({"query": query, "results": results})
    except Exception as e:
        st.error(f"Error with query '{query}': {e}")
    time.sleep(1)


from utils.llm_integration import extract_information_with_llm

extracted_data = []

if queries:
    for i, query in enumerate(queries):
        entity = data[main_column].iloc[i]
        search_results = all_search_results[i]["results"]

        # Extract specific information with LLM...
        extracted_info = extract_information_with_llm(entity, search_results, query_template)

        # Store extracted data in a structured format
        extracted_data.append({
            "Entity": entity,
            "Query": query,
            "Extracted Information": extracted_info
        })

    # Display extracted data preview
    st.write("Extracted Data:")
    st.write(extracted_data[:5])  # Show only the first 5 results for preview

extracted_df = pd.DataFrame(extracted_data)

# Display extracted information in a table
st.write("Final Extracted Information:")
st.dataframe(extracted_df)

# Download button for extracted information
st.download_button(
    label="Download Extracted Data as CSV",
    data=extracted_df.to_csv(index=False).encode('utf-8'),
    file_name="extracted_data.csv",
    mime="text/csv"
)

def extract_information_with_llm(entity, search_results, query_template):
    try:
        prompt = f"Extract the requested information for '{entity}' from the following search results based on the prompt: '{query_template}'.\n\n"
        for result in search_results:
            prompt += f"Title: {result['title']}\nURL: {result['link']}\nSnippet: {result['snippet']}\n\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0
        )

        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error extracting information for {entity}: {e}")
        return "Extraction failed"


# Display the extracted information in a table format
if not extracted_df.empty:
    st.write("Final Extracted Information:")
    st.dataframe(extracted_df)
else:
    st.write("No data to display.")


# Download button for the extracted data
if not extracted_df.empty:
    st.download_button(
        label="Download Extracted Data as CSV",
        data=extracted_df.to_csv(index=False).encode('utf-8'),
        file_name="extracted_data.csv",
        mime="text/csv"
    )


if not extracted_df.empty:
    update_google_sheet = st.button("Update Google Sheet with Extracted Data")

from googleapiclient.discovery import build

def write_to_google_sheet(sheet_id, data):
    # Authenticate and build service
    credentials = service_account.Credentials.from_service_account_file("path/to/client_secret.json")
    scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=scoped_credentials)

    # Convert DataFrame to a list of lists for Google Sheets
    values = [data.columns.tolist()] + data.values.tolist()

    # Update Google Sheet
    request = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Sheet1",  # Adjust range if needed
        valueInputOption="RAW",
        body={"values": values}
    )
    response = request.execute()
    return response

# Trigger the Google Sheet update when the button is clicked
if update_google_sheet:
    try:
        response = write_to_google_sheet(sheet_id, extracted_df)
        st.success("Google Sheet successfully updated.")
    except Exception as e:
        st.error(f"Failed to update Google Sheet: {e}")
