from agent import create_jira_ticket

task = {
    "summary": "Fix login bug",
    "assignee": "John",
    "due_date": "Friday",
    "priority": "High",
    "type": "Bug"
}

result = create_jira_ticket(task)
print(result)

#run gcloud services enable secretmanager.googleapis.com in terminal to get access