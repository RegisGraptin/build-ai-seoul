from nearai.agents.environment import Environment

from actions import Actions
from events import Events
from prompt import prompt_choose_events, prompt_format_event_info
from utils import AiUtils, State

# load user's private key
utils = AiUtils(env, agent)
events = Events()

# 1. Get user information and events info
# 2. Adjust the selection based on the user preferences

LUMA_CITIES = ["bangkok", "hongkong", "manila", "seoul", "tel-aviv", "tokyo", "singapore", "melbourne", "honolulu", "bengaluru", "dubai", "jakarta", "mumbai", "sydney", "taipei", "new-delhi", "kuala-lumpur", "ho-chi-minh-city"]

def get_user_messages(chat_history):
    return [msg['content'] for msg in chat_history if msg.get('role') == 'user']

def agent(env: Environment, state: State):
    
    env.add_system_log("type of action " + state.action)

    print("state.action", state.action)

    # Get user input

    match Actions[state.action]:
        case Actions.FETCH_INFO:
            env.add_system_log("Discover new events")
            user_input = get_user_messages(env.list_messages())[-1]

            # Get user city
            target_city = None
            norm_user_input = user_input.lower()
            for city in LUMA_CITIES:
                if city in norm_user_input:
                    target_city = city
                    break
            
            if target_city is None:
                env.add_reply("Please choose one city from the following list: \n" \
                "bangkok, hongkong, manila, seoul, tel-aviv, tokyo, singapore, melbourne, honolulu, bengaluru, dubai, jakarta, mumbai, sydney, taipei, new-delhi, kuala-lumpur, ho-chi-minh-city.")
                return 

            list_events = events.discover(target_city)

            env.add_system_log("Number of events:" + str(len(list_events.keys())))
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
            
            prompt = {"role": "system", "content": prompt_choose_events([user_input], event_details)}
            result = env.completion([prompt])
            
            env.add_reply(result)

            # Move to the other phase
            state.action = Actions.FEEDBACK
        
        case Actions.FEEDBACK:
            user_inputs = get_user_messages(env.list_messages())
            prompt = {"role": "system", "content": prompt_choose_events(user_inputs, state.event_details)}
            result = env.completion([prompt])
            env.add_reply(result)



    # data = utils.parse_response(reply)
    utils.save_state(state)
    
env.add_system_log("Load state")
state = State(**utils.get_state())

env.add_system_log("Call agent")
agent(env, state)
