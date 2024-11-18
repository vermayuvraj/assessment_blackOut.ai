# **assessment blackout.ai**

This project is a comprehensive **AI Toll** that processes datasets, performs web searches, and uses a Language Model (LLM) to extract user-defined information. Designed with a user-friendly interface, it streamlines the workflow for data extraction, query generation, and information retrieval. 

---

## **Table of Contents**

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Workflow](#workflow)
  - [Phase 1: Initial Setup](#phase-1-initial-setup)
  - [Phase 2: File Upload and Google Sheets Integration](#phase-2-file-upload-and-google-sheets-integration)
  - [Phase 3: Dynamic Query Input and Prompt Template](#phase-3-dynamic-query-input-and-prompt-template)
  - [Phase 4: Automated Web Search](#phase-4-automated-web-search)
  - [Phase 5: Information Extraction Using LLM](#phase-5-information-extraction-using-llm)
  - [Phase 6: Display and Store Extracted Information](#phase-6-display-and-store-extracted-information)
- [API Keys and Environment Variables](#api-keys-and-environment-variables)


---

## **Project Overview**

This **Project** enables users to:
1. Upload a **CSV file** or connect to a **Google Sheet**.
2. Select the main data column (e.g., company names or entities).
3. Enter a **custom query template** to retrieve specific information (e.g., "Find the email address for {company}").
4. Automate **web searches** and process the results using an **LLM** to extract the desired data.
5. Display, download, or update the extracted data in the Google Sheet.

---

## **Features**

1. **File Upload**:
   - Upload CSV files or connect to Google Sheets for seamless integration.

2. **Dynamic Query Input**:
   - Create custom queries with placeholders to extract entity-specific information.

3. **Automated Web Search**:
   - Perform automated searches using APIs like SerpAPI or ScraperAPI.

4. **Information Extraction**:
   - Use OpenAI's GPT API to parse and extract relevant data from web search results.

5. **Data Display and Download**:
   - View the extracted data in a clean, tabular format and download it as a CSV.

6. **Google Sheets Integration**:
   - Update extracted data directly in a connected Google Sheet.

---

## **Technologies Used**

- **Frontend**: Streamlit
- **Backend**: Python
- **APIs**:
  - OpenAI GPT API
  - Google Sheets API
  - SerpAPI (or alternative web search APIs)
- **Libraries**:
  - `pandas`: Data handling and manipulation.
  - `google-api-python-client`: Google Sheets integration.
  - `streamlit`: Dashboard and UI.
  - `openai`: Integration with GPT API.
  - `python-dotenv`: Manage environment variables securely.

---


**Dashboard**

![image alt](https://github.com/vermayuvraj/assessment_blackOut.ai/blob/bdcceb1efb97b785b6c9a89c8977211023bd47db/2.jpg)

**Data Priview**

![image alt](https://github.com/vermayuvraj/assessment_blackOut.ai/blob/bdcceb1efb97b785b6c9a89c8977211023bd47db/1.jpg)

