import json
from typing import List


event_template_json = json.load(open("./template/event.json"))

def prompt_format_event_info(data: str) -> str:
    return f"""Your job is to extract the information from the data and set it to a JSON format.

Here is the JSON format:
{event_template_json}

Here is the data:
{data}
"""

def prompt_choose_events(user_preferences: List[str], events) -> str:
    details = "\n".join(events.values())
    user_details = "\n".join(user_preferences)

    return (
        "You are responsible for selecting and managing a list of events based on the user's preferences and availability. "
        "Below is the list of available events. Your task is to identify and propose the most relevant and engaging options. "
        "The user will have the opportunity to provide feedback afterwards. You have to list them in a specific format: "
        "#id - date - event name - relevant information / description.\n\n"
        f"User Preferences: {user_details}\n\n"
        f"Available Events:\n{details}"
    )
