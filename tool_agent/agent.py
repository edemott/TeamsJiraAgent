import os 
import requests
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool
from google.cloud import secretmanager
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
SECRET_ID = os.getenv("SECRET_ID")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")


# Interprets Messages for Jira Format
def extract_task_fields(message: str) -> dict:
    """
    Extracts task fields from an informal message.
    Returns a dictionary with: summary, assignee, due_date, priority, type.
    """
    # This is a placeholder – Gemini will fill in the values based on instruction.
    return {
        "summary": "",
        "assignee": "",
        "due_date": "",
        "priority": "",
        "type": ""
    }
extract_tool = FunctionTool(func=extract_task_fields)


def extract_task_fields(message: str) -> dict:
    """
    Extracts task fields from an informal message.
    Returns a dictionary with: summary, assignee, due_date, priority, type.
    """
    # This is a placeholder – Gemini will fill in the values based on instruction.
    return {
        "summary": "",
        "assignee": "",
        "due_date": "",
        "priority": "",
        "type": ""
    }
extract_tool = FunctionTool(func=extract_task_fields)


# ------------------------------------------------------
# Jira configuration
# ------------------------------------------------------


def get_jira_token() -> str:
    token = os.getenv("JIRA_API_TOKEN")
    if not token:
        raise ValueError("Missing JIRA_API_TOKEN in environment.")
    return token
# ------------------------------------------------------
# Create Jira issue from task fields
# ------------------------------------------------------
def create_jira_ticket(task: dict) -> dict:
    token = get_jira_token()
    auth = (JIRA_EMAIL, token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Provide default values in case task dict is missing fields
    summary = task.get("summary", "No summary provided")
    due_date = task.get("due_date", "N/A")
    issue_type = task.get("type", "Task")
    epic_key = task.get("epic")        
    sprint_id = task.get("sprint_id") 

    description_adf = {
    "type": "doc",
    "version": 1,
    "content": [
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": f"Auto-created by AI agent. Due: {due_date}."}
            ]
        }
    ]
}

    fields = {
    "project": {"key": JIRA_PROJECT_KEY},
    "summary": summary,
    "description": description_adf,
    "issuetype": {"name": issue_type},
    }

    # Optional Epic link
    if epic_key:
        fields["customfield_10008"] = epic_key  

    # Optional Sprint
    if sprint_id:
        fields["customfield_10020"] = sprint_id  

    data = { "fields": fields }

    response = requests.post(
        f"{JIRA_BASE_URL}/rest/api/3/issue",
        json=data,
        headers=headers,
        auth=auth
    )

    if response.status_code == 201:
        issue_key = response.json().get("key")
        return {"status": "success", "issue_key": issue_key}
    else:
        return {
            "status": "error",
            "details": response.text
        }

create_ticket_tool = FunctionTool(func=create_jira_ticket)




root_agent = Agent(
    name="jira_agent",
    model="gemini-2.0-flash",
    description="Extract task fields from informal chat messages.",
    instruction="""
You are an agent that helps with task management. First, extract task fields from the user message using the appropriate tool.
Then, if the task looks actionable, use another tool to create a Jira ticket using the extracted information.
""",
    tools=[extract_tool,create_ticket_tool]
)

# To test "run adk run tool_agent" and type in somthing similar to this: 'John, can you fix the login bug by Friday? It's urgent.'