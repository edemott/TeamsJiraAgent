# Jira Agent MS Teams Integration

This repositiroy contains code for an AI agent that integrates with Microsoft Teams to automatically create and assign Jira issues from Teams messages



## Getting Started

### Setup Environment


```bash
# Create virtual environment in the root directory
python -m venv .venv

# Activate 
# macOS/Linux:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```


## Setting Up API Keys

### Google API Setup

1. Create an account in Google Cloud https://cloud.google.com/?hl=en
2. Create a new project
3. Go to https://aistudio.google.com/apikey
4. Create an API key
5. Assign key to the project
6. Connect to a billing account

### Jira API Setup

1.	Log in to the Atlassian account that has access to your Jira site.
2.	Go to Manage API Tokens.
3.	Click Create API token, give it a label, and copy the generated token.
4.	Use that email/token pair in your environment or secret storage.


1. Create an enviroment file to place api key
2. Open the `.env` file and replace the placeholder with your API key:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_api_key_here
   JIRA_API_KEY=your_api_key_here
   ```



