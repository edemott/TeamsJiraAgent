from google.adk.tools import FunctionTool


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
