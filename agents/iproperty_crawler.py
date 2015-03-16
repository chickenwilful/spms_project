import logging
import re
from lxml import etree

logger = logging.getLogger("agents_crawler")
logger.setLevel(logging.DEBUG)

# create file handler
file_handler = logging.FileHandler('iproperty_crawler.log')
file_handler.setLevel(logging.ERROR)

# create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s")
formatter.datefmt = "%d/%b/%Y %H:%M:%S"
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

from _elementtree import tostring
import os
import string
import sys
from lxml import html
import time
import csv


sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spms_site.settings")
import django
django.setup()

import requests
from requests import exceptions
from agents.models import AgentIProperty

DOMAIN = "http://www.stproperty.sg"
SEARCH_URL = "http://www.iproperty.com.sg/realestate/findanagent.aspx?ty=al&ak=%c&rk=&p=%d&s=%d"
AGENT_CSV_FILENAME = "agents_stproperty.csv"

MIN_ID = 0
RESULT_PER_PAGE = 100


def get_page(url):
    response = requests.get(url)
    return response


def get_phone_number(html):
    pattern = r"65(\d*)"
    if not pattern:
        return None
    else:
        return re.search(pattern, tostring(html), re.I).group(1)


def get_agent_by_html(html):
    # print tostring(html)
    name = html.cssselect('a')[0].get('title')
    agent_url = html.cssselect('a')[0].get('href')
    estate_name = html.cssselect('a')
    estate_name = estate_name[len(estate_name)-1].get('title')
    try:
        reg_number = re.search(re.escape(r'CEA Registration Number :') + '\s(.{8})', tostring(html), re.I).group(1)
    except AttributeError:
        reg_number = None
    try:
        lic_number = re.search(re.escape(r'Agency Licence Number :') + '\s(.{9})', tostring(html), re.I).group(1)
    except AttributeError:
        lic_number = None
    phone_number = html.cssselect('span a')
    if phone_number:
        phone_number = get_phone_number(phone_number[0])
    agent = AgentIProperty(name=name, phone_number=phone_number, estate_name=estate_name, reg_number=reg_number, lic_number=lic_number, url=agent_url)
    print agent
    return agent


def get_agents_by_url(url):
    logger.info("Get agent list, url = %s" % url)
    agents = []
    try:
        response = get_page(url)
        tree = html.fromstring(response.text)
        tables = tree.cssselect('div.SGmiddleColsub2 table table td.morelistingtext')[::2]
        for table in tables:
            agent = get_agent_by_html(table)
            agents.append(agent)
        # print agents
        return agents
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP Error: " + str(e))
        return []


def get_num_page(first_letter):
    url = SEARCH_URL % (first_letter, 1, RESULT_PER_PAGE)
    response = get_page(url)
    tree = html.fromstring(response.text)
    list = tree.cssselect('div.totalfound')[1].text.split(' ')
    num_page = (int(list[0]) - 1) / RESULT_PER_PAGE + 1
    logger.info("get num page, first_letter=%c --> %d" % (first_letter, num_page))
    return num_page


def write_agents_csv(filename):
    with open(filename, "wb") as csvfile:
        field_names = ["Agent Name", "Estate Agents Name", "Phone Number", "Estate Agents License Number", "Agent Registration Number"]
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(field_names)
        agents = AgentIProperty.objects.filter(name__isnull=False)
        for agent in agents:
            if agent.estate_name:
                agent.estate_name = agent.estate_name.encode('ascii', 'ignore').decode('ascii')
            while agent.lic_number and agent.lic_number[0] != 'L':
                agent.lic_number = agent.lic_number[1:]
                agent.save()
            # print agent.url
            # print agent.name, agent.estate_name, agent.lic_number, agent.reg_number
            writer.writerow([agent.name, agent.estate_name, str(agent.phone_number)[3:], agent.lic_number, agent.reg_number])


def get_all_agent_info():
    for first_letter in string.ascii_uppercase:
        num_page = get_num_page(first_letter)
        for page in range(1, num_page + 1):
            url = SEARCH_URL % (first_letter, page, RESULT_PER_PAGE)
            get_agents_by_url(url)


if __name__ == "__main__":
    get_all_agent_info()