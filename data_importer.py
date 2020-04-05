from bs4 import BeautifulSoup
import requests
import json
import re
import datetime


from config import APT_REGEX, BUILDINGS_WITH_WD


class ApartmentData:
    def __init__(self, apt_num, building_name, address,
                 unit_type, area, rent, availability,
                 price_per_sq_ft,
                 has_washer_dryer):
        self.has_washer_dryer = has_washer_dryer
        self.price_per_sq_ft = price_per_sq_ft
        self.availability = availability
        self.rent = rent
        self.area = area
        self.unit_type = unit_type
        self.address = address
        self.building_name = building_name
        self.apt_num = apt_num

    @classmethod
    def from_dict(self, apt_dict):
        return ApartmentData(**apt_dict)

    @classmethod
    def _parse_string(self, apt_string):
        matches = list(re.finditer(APT_REGEX, apt_string, re.MULTILINE))
        parsed_dict = dict(**matches[0].groupdict())
        parsed_dict['price_per_sq_ft'] = float(parsed_dict['rent'].replace("$", "").replace(',', '')) / float(
            parsed_dict['area'])
        if parsed_dict['building_name'] in BUILDINGS_WITH_WD:
            parsed_dict['has_washer_dryer'] = True
        else:
            parsed_dict['has_washer_dryer'] = False
        return parsed_dict

    @classmethod
    def from_string(self, apt_string):
        return self.from_dict(self._parse_string(apt_string))

    def __eq__(self, other):
        return f"{self.apt_num} {self.building_name}"

    def __repr__(self):
        return f"{self.apt_num} {self.building_name} {self.area} " \
               f"{self.unit_type} {self.rent} {self.has_washer_dryer}"

    def __hash__(self):
        return hash(f"{self.apt_num} {self.building_name}")

    def to_dict(self):
        return {
            'apt_num': self.apt_num,
            'building_name': self.building_name,
            'address': self.address,
            'unit_type': self.unit_type,
            'area': self.area,
            'rent': self.rent,
            'availability': self.availability,
            'price_per_sq_ft': self.price_per_sq_ft,
            'has_washer_dryer': self.has_washer_dryer
        }


payload = {
    'bedrooms': [],
    'priceMin': 1000,
    'isDefaultMinPrice': True,
    'priceMax': 10000,
    'isDefaultMaxPrice': True,
    'buildings': '',
    'moveInDate': '04/05/2020',
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
        for i in range(1, 10):
            payload['page'] = i

            page = session.post(url="https://www.newportrentals.com/ajax/getunitlist.asp", headers=headers,
                                data=payload)

            pages.append(page)
    return pages


def page_parser(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    apartments = list(soup.children)
    apartments_list = []
    for apartment in apartments:

        try:
            apt_string = apartment.find('a')['aria-label']
            # print(apt_string)
            # 'Residence 2807 in Parkside East on 30 Newport Parkway, Studio 1 Bathroom, 482 square feet, $2,286, Available 4/1/2020'
            apartments_list.append(ApartmentData.from_string(apt_string))
        except Exception as err:
            pass
    return apartments_list


def save_to_file(data):
    with open('output_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def fetch_apartment_list():
    apartments_set = set()
    for page in make_requests():
        apts = page_parser(page)
        for apt in apts:
            if apt:
                apartments_set.add(apt)
    apartments_list = list(apartments_set)
    apartments_list.sort(key=lambda x: (x.price_per_sq_ft, x.availability, x.rent))
    return apartments_list


# if __name__ == '__main__':
#     from pprint import PrettyPrinter
#     pp = PrettyPrinter(indent=4)
#     pp.pprint(fetch_apartment_list())
