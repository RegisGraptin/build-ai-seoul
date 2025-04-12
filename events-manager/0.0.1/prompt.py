import json


event_template_json = json.load(open("./template/event.json"))

def prompt_format_event_info(data: str) -> str:
    return f"""Your job is to extract the information from the data and set it to a JSON format.

Here is the JSON format:
{event_template_json}

Here is the data:
{data}
"""

def prompt_choose_events(events) -> str:

    details = [event_detail for event_detail in events.values()]

    return "Here a list of event, based on the user preferences and availability, you will be in charge to propose and manage" \
    "a list of events. Here are the events, you need to pick the most relevant and interesting. The user will have the possibility later on" \
    "to give you some feedbacks:" \
    "".join(details)