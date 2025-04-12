import asyncio
import enum

from nearai.agents.environment import Environment
from py_near.account import Account
from py_near.dapps.core import NEAR

from actions import Actions
from events import Events
from prompt import prompt_choose_events, prompt_format_event_info
from utils import AiUtils, State

# load user's private key
utils = AiUtils(env, agent)
events = Events()

# 1. Get user information and events info
# 2. Adjust the selection based on the user preferences

def agent(env: Environment, state: State):
    
    env.add_system_log("type of action " + state.action)
    state.action = Actions.EVENT_SEARCH_INFO
    

    if not state.action:
        state.action = Actions.EVENT_SEARCH_INFO

    match state.action:
        # case Actions.
        case Actions.FETCH_USER_INFO:
            pass

        case Actions.EVENT_SEARCH_INFO:
            
            env.add_system_log("Discover new events")

            list_events = events.discover()
            n_events = 0
            event_details = {}
            for link, event_detail in list_events.items():
                
                prompt = {"role": "system", "content": prompt_format_event_info(event_detail)}
                result = env.completion([prompt])
                event_details[link] = result
                n_events += 1

            env.add_system_log("Number of extracted events: " + str(n_events))

            # Save the extracted data
            state.event_details = event_details

            prompt = {"role": "system", "content": prompt_choose_events(event_details)}
            result = env.completion([prompt])
            
            env.add_reply(result)
        
        case Actions.PROPOSE_EVENTS:
            prompt = {"role": "system", "content": prompt_choose_events(state.event_details)}
            result = env.completion([prompt])
                
            env.add_reply(result)



    # data = utils.parse_response(reply)
    state.action = Actions.PROPOSE_EVENTS
    utils.save_state(state)
    




state = State(**utils.get_state())

agent(env, state)
