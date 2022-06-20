import requests
from bs4 import BeautifulSoup
from config import URL, COUNT_HOST
import time
from logger_app import get_logger

# Configure logging
logger = get_logger(__name__)


def stock_parser():
    """Returns a string with information about the stocks from clubs website"""
    try:
        url = "https://youplay24.ru/akczii-kluba/"
        headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) " +
                          "AppleWebKit/537.36 (HTML, like Gecko) Chrome/1 01.0.4951.67 Mobile Safari/537.36"
        }
        req = requests.get(url, timeout=30, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")

        stock_heading = soup.find_all(class_="elementor-price-table__heading")
        stock_price = soup.find_all(class_="elementor-price-table__integer-part")
        stock_description = soup.find_all(class_="elementor-price-table__feature-inner")

        stock_info = []

        for i in range(len(stock_heading)):
            stock_info.append(
                {
                    "Title": stock_heading[i].text.strip().replace('\xa0', ' ').replace('  ', ' '),
                    "Description": stock_description[i].text.strip().replace('\xa0', ' ').replace('  ', ' '),
                    "Price": stock_price[i].text.strip().replace('\xa0', ' ').replace('  ', ' ')
                }
            )

        mess = ''
        for txt in stock_info:
            mess += f"<b>{txt['Title']}</b>\n{txt['Description']}\n₽<b>{txt['Price']}</b>\n\n"
        return mess
    except Exception as ex:
        logger.error(ex)
        return -1


def get_hosts(host_sort):
    """Returns all hosts sorted by ascending"""
    try:
        response = requests.get(f'{URL}/hosts')
        host = response.json()['result']
        for i in range(len(host)):
            if host[i]['number'] < 100:
                host_sort[(host[i]['number'])] = host[i]['id']
        return host_sort
    except ConnectionError as ex:
        logger.error(ex)
        return 500


def get_free_hosts():
    """Returns a string with information about the status of all PCs"""
    try:
        occupied_host = [None] * COUNT_HOST
        host_sort = [None] * COUNT_HOST
        host_sort = get_hosts(host_sort)
        if host_sort == -1:
            return -1
        response = requests.get(f'{URL}/usersessions/activeinfo')
        host = response.json()['result']
        av_time = [None]*len(host)
        mess = ''
        for i in range(len(host)):
            userid = str(host[i]['userId'])
            response = requests.get(f'{URL}/users/{userid}/balance')
            av_time[i] = time.strftime('%H:%M', time.gmtime(response.json()['result']['availableTime']))
            occupied_host[i] = host[i]['hostId']
        for i in range(1, COUNT_HOST):
            if int(host_sort[i]) in occupied_host:
                index = occupied_host.index(host_sort[i])
                mess += f"{i} - {av_time[index]}\n\n"
            else:
                mess += f"{i} - Свободен\n\n"
        return mess
    except Exception as ex:
        logger.error(ex)
        return -1


def authorization(user_info):
    """Returns 1 if user data is valid and 0 if is not"""
    try:
        username = user_info['login']
        password = user_info['password']
        response = requests.get(f'{URL}/users/{username}/{password}/valid')
        response = response.json()['result']['result']
        # Response by default returns 0 if user data is valid
        return not response
    except Exception as ex:
        logger.error(ex)
        return -1


def get_user_balance(login):
    """Returns user balance by login"""
    try:
        response = requests.get(f'{URL}/users/{login}/userid')
        user_api_id = str(response.json()['result'])
        response = requests.get(f'{URL}/users/{user_api_id}/balance')
        user_deposit = response.json()['result']['deposits']
        user_point = response.json()['result']['points']
        mess = str(f'У вас на аккаунте <b>{user_deposit}</b> рублей и <b>{user_point}</b> баллов')
        return mess
    except Exception as ex:
        logger.error(ex)
        return -1
