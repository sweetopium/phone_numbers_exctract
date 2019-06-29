import re
import requests
from requests.exceptions import ConnectionError

__phone_number_pattern = r'\+?\d[\( -]?\d{3}[\) -]?\d{3}[ -]?\d{2}[ -]?\d{2}'

def site_connection_error_handler(site_url):
    try:
        res = requests.get(site_url)
        if res.status_code != 200:
            return False
        else:
            return res.text
    except ConnectionError:
        return False

def extract_numbers_from_site(site_url, re_pattern):
    site_content = site_connection_error_handler(site_url)
    if site_content is not False:
        founded_results = re.findall(re_pattern, site_content)
        if len(founded_results) == 0:
            return False
        return founded_results
    else:
        return False


def normalize_numbers(numbers_list):
    normalized_numbers = []
    for number in numbers_list:
        number = number.replace(' ', '').replace('+', '').replace('-', '').replace('(', '').replace(')', '')
        normalized_numbers.append(number)
    return normalized_numbers


def validate_numbers(numbers_list):
    validated_numbers = set()
    for number in numbers_list:
        if len(number) < 7:
            pass
        elif len(number) == 11 and (number[0] == '7' or number[0] == '8'):
            number = number[0].replace('7', '8') + number[1:]
            validated_numbers.add(number)
        elif len(number) == 7:
            number = '8495' + number
            validated_numbers.add(number)
    if len(validated_numbers) == 0:
        return False
    return list(validated_numbers)



def validation_worker(site, re_pattern):
    numbers_list = extract_numbers_from_site(site, re_pattern)
    if numbers_list is not False:
        normalized_numbers = normalize_numbers(numbers_list)
        validated_numbers = validate_numbers(normalized_numbers)
        return validated_numbers
    else:
        return False

if __name__ == "__main__":
    print(validation_worker('http://applerem24.ru/contacts/', __phone_number_pattern))

