import os 
import requests
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool
from google.cloud import secretmanager
from dotenv import load_dotenv
import os

load_dotenv()


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
PROJECT_ID = "jira-project-465616"  # actual project ID for secrets
SECRET_ID = "jira_api_key"          # secret name in GCP
JIRA_EMAIL = "ethandemott@outlook.com"
JIRA_BASE_URL = "https://ethandemott.atlassian.net"
JIRA_PROJECT_KEY = "EM"

# # Hardcoded token for local testing only
# HARDCODED_JIRA_TOKEN = (
#     'ATATT3xFfGF0d4AE2fqqjFwnl3g50YLS42z3SMWLwkviyfkDKoVA3XNDxWS3Hhi7-rEDBdDppLSjcg72sONIbJuOsGYnJpr9uO0jFVtF_RxRiH8Tumv7NG4coBOC2smt3BUSdJmUaqUanx9NWySVcWYytJATSe8w0n5aViYL2jpMfoyDPCsLvMs=0D1E2012'
#     #"ATCTT3xFfGN0VvJyckeT-9t1cpHS-_p6FaTgew6R5_l6YKU03bn_jck6vsZLNDmhuTP9OzdEHYkA18jrvLCJdizVoAz6DqzM5cmiqC5scvqAAVpenWulZNwDi5cnhrOEcFKqOgBpTALmvW75sRUT4z6KAiFlObGtaFPC_-8Zg0FVwcN25l-GobE=1E0BB662"
# )

# # Toggle this flag to use hardcoded token instead of Secret Manager
# USE_HARDCODED_TOKEN = True

# # ------------------------------------------------------
# # Secure token retrieval (or fallback to hardcoded for testing)
# # ------------------------------------------------------
# def get_jira_token() -> str:
#     if USE_HARDCODED_TOKEN:
#         # 🚨 WARNING: Hardcoding secrets is insecure. Do this for local testing only.
#         return HARDCODED_JIRA_TOKEN
#     else:
#         client = secretmanager.SecretManagerServiceClient()
#         name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
#         response = client.access_secret_version(request={"name": name})
#         return response.payload.data.decode("UTF-8")
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
    priority = task.get("priority", "Medium")
    issue_type = task.get("type", "Task")

    data = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": f"Auto-created by AI agent.\nDue: {due_date}\nPriority: {priority}",
            "issuetype": {"name": issue_type},
            "priority": {"name": priority},
        }
    }

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

# to test run adk run tool_agent and type in somthing similar to this "'John, can you fix the login bug by Friday? It's urgent.'"