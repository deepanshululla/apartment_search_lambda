from bs4 import BeautifulSoup
import requests
import json
import re
import datetime

APT_REGEX = "Residence (?P<apt_num>[0-9]+) in (?P<building_name>.*) on (?P<address>.*), (?P<unit_type>.*), (?P<area>[0-9]+) square feet, (?P<rent>\$.*), Available (?P<availability>.*)"



payload = {
    'bedrooms': [],
    'priceMin': 1000,
    'isDefaultMinPrice': True,
    'priceMax': 3000,
    'isDefaultMaxPrice': True,
    'buildings':'',
    'moveInDate': '03/05/2020',
    'page': 1,
    'lastNum': '',
    'sort': 'priceASC',
    'numberPerPage': 1000
}


def get_dates_array():
    today = datetime.datetime.today()
    one_month_later = today + datetime.timedelta(days=30)
    two_month_later = today + datetime.timedelta(days=60)

    return [x.strftime("%m/%d/%y") for x in [today, one_month_later, two_month_later]]

def make_requests():
    headers = {
        'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    session = requests.Session()
    pages = []
    for date in get_dates_array():
        payload['moveInDate'] = date
        for i in range(1,10):
            payload['page'] = i

            page = session.post(url="https://www.newportrentals.com/ajax/getunitlist.asp", headers=headers, data=payload)

            pages.append(page)
    return pages



def parse_string(apt_string):
    matches = list(re.finditer(APT_REGEX, apt_string, re.MULTILINE))
    return matches[0].groupdict()


def soup_parser(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    apartments = list(soup.children)
    apartments_list = []
    for apartment in apartments:

        try:
            apt_string = apartment.find('a')['aria-label']
            # print(apt_string)
            # 'Residence 2807 in Parkside East on 30 Newport Parkway, Studio 1 Bathroom, 482 square feet, $2,286, Available 4/1/2020'
            apartments_list.append(parse_string(apt_string))
        except Exception as err:
            pass
    return apartments_list

def save_to_file(data):
    with open('output_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def fetch_apartment_list():
    apartments_list = []
    for page in make_requests():

        # print(page.content)
        apts = soup_parser(page)

        for apt in apts:
            if apt:
                apartments_list.append(apt)
    # save_to_file(apartments_list)
    return apartments_list
