
from bs4 import BeautifulSoup
import requests


class Events:

    def __init__(self):
        pass

    def extract_event_links(self, url):
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        events = soup.find_all("a", class_="event-link content-link")
        links = [event.get("href") for event in events]
        return links 

    def extract_event_content(self, url):
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        text_only = soup.get_text(separator=' ', strip=True)

        return text_only

    def discover(self, city):
        events = {}
        links = self.extract_event_links(f"https://lu.ma/{city}")
        for link in links:
            event_link = f"https://lu.ma/{link}"
            events[event_link] = self.extract_event_content(event_link)
        return events

    

if __name__ == "__main__":

    events = Events()

    print(events.discover("seoul"))
    # response = requests.get("https://lu.ma/seoul")
    # response.raise_for_status()
    
    # soup = BeautifulSoup(response.content, 'html.parser')
    # d = soup.find("div", class_=".weekday")
    # print(d)
    

