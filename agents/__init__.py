import requests
from bs4 import BeautifulSoup

ITEM_PER_PAGES = 1000


def get_agent_url_list_from_url(url):
    pass


def get_agent_by_url(url):
    source_code = requests.get(url)
    plain_text = source_code.text

    with open("text.txt", "w") as file:
        file.write(plain_text.encode('utf-8'))

    soup = BeautifulSoup(plain_text)


    agent_summary = soup.findAll("div", {"class": "agent_summary"})
    print agent_summary

    summary1 = soup.findAll('div', {'class': 'summary1'})
    print summary1
    # Get detail information about the agent
    pass


def get_all_agents():
    pass


if __name__ == "__main__":
    get_agent_by_url("http://www.propertyguru.com.sg/agent/a-balaji-12016")