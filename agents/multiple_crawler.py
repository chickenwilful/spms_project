import os
import sys
import threading
import requests

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spms_site.settings")
import django
django.setup()


import logging
from agents.models import Agent, BadNum

logger = logging.getLogger("cea_crawler")
logger.setLevel(logging.DEBUG)

# create file handler
file_handler = logging.FileHandler('crawler.log')
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


from requests import Session, ConnectionError
import time
from lxml import html


CEA_DOMAIN = "https://www.cea.gov.sg"
HEADER_URL = "https://www.cea.gov.sg/cea/app/newimplpublicregister/publicregister.jspa"
SEARCH_URL = "https://www.cea.gov.sg/cea/app/newimplpublicregister/searchPublicRegister.jspa"

LAST_NUM = '90015276'
LEN = 8


def get_agent_html_by_phone_number(phone_number):
    logger.info("get agent by phone number = %s" % phone_number)
    if phone_number > LAST_NUM:
        with open("multi_crawler_last_num.txt", "w") as f:
            f.write(phone_number)

    try:
        session = Session()
        session.head(HEADER_URL)
        response = session.post(
            url=SEARCH_URL,
            data={
                'type': 'searchSls',
                'slsName': '',
                'slsEaName': '',
                'slsRegNo': '',
                'slsMblNum': phone_number,
                'answer': ''
            },
            headers={
                'Referer': HEADER_URL,
                # 'Cookie':'gov.sg=!jHc4h/lIwbRPs3HIqxNfqRUjNuyoiGmYP6IYVwWywlWBxDn5rK7l2rUcHzPC0S9P+xE61chFxwmrNx4=; __atuvc=2%7C10; __utmt=1; __utma=135192814.1580995594.1425746596.1426138225.1426141926.8; __utmb=135192814.2.10.1426141926; __utmc=135192814; __utmz=135192814.1425930869.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); JSESSIONID=hrvBVBxJcCqqyqn3T9nLJBTQrnFfhL6wKtBHRr2ycvZ2wHl3y8yf!-1793834817!1426141492644'
            })
        if "Invalid captcha" in response.text:
            raise ConnectionError
        return response.text
    except ConnectionError as e:
        logger.error("Connection Error with phonenumber = %s" % phone_number + str(e))
        logger.info('Try to resume...')
        time.sleep(3)
        return get_agent_html_by_phone_number(phone_number)


def get_agents_by_html(source_code):  # care only about 1st page of results
    tree = html.fromstring(source_code)
    rows = tree.xpath('//tbody/tr')
    agents = []
    for row in rows:
        agents.append(Agent(reg_number=row.xpath('td/a/text()')[0], name=row.xpath('td/span/text()')[0]))
    logger.info("get %d agents." % len(agents))
    if len(agents) > 0:
        logger.info(agents[0])
    return agents


def get_agents_by_phone_number(phone_number):
    source_code = get_agent_html_by_phone_number(phone_number)
    return get_agents_by_html(source_code)


def update_agents(agents, phone_number):
    logger.info("update agents with phonenumber = %s" % phone_number)
    if len(agents) == 0 or len(phone_number) != 8:
        return
    try:
        print agents
        with open("update_agent.txt", "a") as f:
            f.write(agents[0].name + ",")
            f.write(agents[0].reg_number + ",")
            f.write(phone_number + "\n")

        if len(agents) > 1:
            raise ValueError("More than 1 matched agent")
        agent_list = Agent.objects.filter(reg_number=agents[0].reg_number)
        if len(agent_list) == 0:
            raise ValueError("No matched agent found!")
        agent = agent_list[0]
        agent.phone_number = phone_number
        agent.save()
        logger.info("save agent = " + str(agent) + "phonenumber = %s" % phone_number + "reg num = %s" % agents[0].reg_number)
    except ValueError as e:
        logger.error(phone_number + " " + str(agents[0].name) + str(e))


def get_all_sub_sequences(input_string):
    length = len(input_string)
    return [input_string[i:j+1] for i in xrange(length) for j in xrange(i, length)]


def already_finished(input_string):
    last_num = str(LAST_NUM)
    l = 8 - len(last_num)
    last_num += (" " * l)

    l = 8 - len(input_string)
    input_string += ("9" * l)
    return input_string < last_num


def is_valid(num):
    if already_finished(num):
        return False
    strings = get_all_sub_sequences(num)
    for string in strings:
        if BadNum.objects.filter(numstr=string).count() > 0:
            return False
    return True


def update_badnum(new_num):
    # Update new_num as a bad number
    logger.info("update badnumber = " + new_num)
    if BadNum.objects.filter(numstr=new_num).count() == 0:
        BadNum.objects.create(numstr=new_num)
    print len(BadNum.objects.all())


def update_all_agents(num, i, o_len):
    # with open("multi_crawler_last_num.txt", "w") as f:
    #     f.write(num)

    if o_len >= 20:
        o_len = 33000

    if i > LEN:
        return

    old_len = o_len

    for d in range(0, 10):
        new_num = num + str(d)
        if is_valid(new_num):
            if old_len == 0:
                if (i < 8):
                    update_badnum(new_num)
            else:
                agents = get_agents_by_phone_number(new_num)
                old_len -= len(agents)
                if i == 8:
                    update_agents(agents, new_num)
                    continue

                if len(agents) > 0:
                    update_all_agents(new_num, i + 1, len(agents))
                else:
                    update_badnum(new_num)



class CrawlerThread(threading.Thread):

    def __init__(self, binarySemaphore, url):
        self.binarySemaphore = binarySemaphore
        self.theadId = hash(self)
        threading.Thread.__init__(self)

    def run(self):
        pass


if __name__ == "__main__":

    with open("multi_crawler_last_num.txt", "r") as f:
        LAST_NUM = f.read()
    print "LAST NUM = %s" % LAST_NUM

    update_all_agents("9", 2, 33000)
    # print len(Agent.objects.filter(phone_number__isnull=False))


