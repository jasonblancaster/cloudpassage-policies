#!/usr/bin/env python2.7
# Generate log messages with CCN in log entry
# Logs to/var/log/web_app.log

import requests, time
from random import randint
from bs4 import BeautifulSoup

def get_test_ccn_list():

    ccn_url = 'https://www.paypalobjects.com/en_US/vhelp/paypalmanager_help/credit_card_numbers.htm'
    res = requests.get(ccn_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    return soup

def parse_cct(soup):

    credit_card_type = []
    credit_card_types = soup.findAll("td", {"class":"whs4"})[1:]
    for ccts in credit_card_types:
        cct = ccts.find("p", {"class": "CellBody"}).text
        credit_card_type.append(cct)
    return credit_card_type

def parse_ccn(soup):

    credit_card_number = []
    credit_card_numbers = soup.findAll("td", {"class":"whs5"})[1:]
    for ccns in credit_card_numbers:
        ccn = ccns.find("p", {"class": "CellBody"}).text
        credit_card_number.append(ccn)
    return credit_card_number


def main():

    filename = '/var/log/web_app.log'

    while True:
        card_data = get_test_ccn_list()

        cct_list = parse_cct(card_data)
        ccn_list = parse_ccn(card_data)

        rand = randint(0,len(cct_list)-1)
        #print cct_list[rand], ccn_list[rand]

        with open(filename, 'a') as f:
            f.write("Credit Card Type: %s \tCredit Card Number: %s  Note: This is only test card data.\n" % (cct_list[rand], ccn_list[rand]))
        time.sleep(300)


if __name__ == "__main__":

    main()
