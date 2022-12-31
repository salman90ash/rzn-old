import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import json
from rzn.models import TasksData, TasksKey, TasksNotice
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

RZN_DOMAIN = 'https://roszdravnadzor.gov.ru'
RZN_TYPES = [(1, 'РУ'), (2, 'Ввоз'), (3, 'Обращение', 'по вх.'), (4, 'ВИРД'), (5, 'Дубликат'),
             (6, 'Обращение', 'по исх.')]

mark_PY_negative = 'об отказе в регистрации'
mark_PY_positive = 'ыдано Регистрационное удостоверение'

# Принято решение об отказе во внесении изменений в документы
# Принято решение о внесении изменений в документы
mark_VIRD = 'Принято решение'

# Принято решение о выдаче дубликата регистрационного
mark_duplicate = 'Принято решение'

mark_zamena_blanka = 'Принято решение'

mark_le = ' от '


def set_url_for_py(rzn_number: str, rzn_date: str) -> str:
    return RZN_DOMAIN + '/services/cab_mi?type_search=1&letters=0&in_doc_num=' + rzn_number + '&in_doc_dt=' + rzn_date


def set_url_for_vird(rzn_number: str, rzn_date: str) -> str:
    return RZN_DOMAIN + '/services/cab_mi?type_search=1&letters=0&in_doc_num=' + rzn_number + '&in_doc_dt=' + rzn_date


def set_url_for_duplicate(rzn_number: str, rzn_date: str) -> str:
    return RZN_DOMAIN + '/services/cab_mi?type_search=4&letters=0&in_doc_num=' + rzn_number + '&in_doc_dt=' + rzn_date


# doc_type=1 - входящий
# doc_type=2 - исходящий
def set_url_for_letters(number: str, date: str, rzn_requisites: bool = False) -> str:
    if rzn_requisites:
        return RZN_DOMAIN + '/services/le?&doc_type=1&doc_num=' + number + '&doc_dt=' + date
    return RZN_DOMAIN + '/services/le?&doc_type=2&doc_num=' + number + '&doc_dt=' + date


# 1	РУ
# 2	Ввоз
# 3	Обращения по вх.
# 4	ВИРД
# 5	Дубликат
# 6	Обращения по исх.


def get_type_title(type_id):
    global RZN_TYPES
    for type_ in RZN_TYPES:
        if type_[0] == type_id:
            return type_[1]
    return False


def set_url(number: str, date: str, rzn_type: int) -> str:
    url = ''
    if rzn_type == 1:
        url = set_url_for_py(number, date)
    elif rzn_type == 2 or rzn_type == 3:
        url = set_url_for_letters(number, date, rzn_requisites=True)
    elif rzn_type == 4:
        url = set_url_for_vird(number, date)
    elif rzn_type == 5:
        url = set_url_for_duplicate(number, date)
    elif rzn_type == 6:
        url = set_url_for_letters(number, date)
    return url


# def get_page(url: str, proxy: dict = {}) -> str:
#     HEADERS = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
#     requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#     r = requests.get(url, headers=HEADERS, proxies=proxy, verify=False)
#     return r.text

def get_page(url: str) -> str:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(url=url)
        return driver.page_source
    except Exception as e:
        print(e)


def get_table_of_cab_mi(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('div', class_='m-cabinet-results-table').text.strip()


def empty_check_table_cam_mi(html: str) -> bool:
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find('div', {"class": "form-additional"})
    if page is None:
        return False
    return True


def empty_check_table_le(html: str) -> bool:
    soup = BeautifulSoup(html, 'lxml')
    # le = 'По вашему запросу ничего не найдено'
    page = soup.find('div', {"class": "form-additional"}).find('span')
    if page is None:
        return False
    return True


def get_table_of_le(html: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('div', class_='m-cabinet-results-table').text.strip()
    # return soup.find('div', class_='m-cabinet-results-table')


def parse_table_cab_mi(table: str) -> list:
    rows = table.split('\n\n')
    list_rows = [row[1:].split('\n') for row in rows if row != '' or row.find('\n') != -1]
    return list_rows


def parse_table_le(table: str) -> list:
    return [row for row in table.split('\n') if row != '' or row.find('\n') != -1]


def get_key_cab_mi(html: str):
    if empty_check_table_cam_mi(html):
        return ''
    else:
        table = get_table_of_cab_mi(html)
        return parse_table_cab_mi(table)
        # rows = table.split('\n\n')
        # list_rows = [row[1:].split('\n') for row in rows if row != '' or row.find('\n') != -1]
        # return list_rows


def get_key_le(html: str):
    if empty_check_table_le(html):
        return ''
    else:
        table = get_table_of_le(html)
        return parse_table_le(table)


def check_cab_mi(type_id: int) -> bool:
    if type_id == 2 or type_id == 3 or type_id == 6:
        return False
    return True


def check_type_le(type_id: int) -> bool:
    if type_id == 3:
        return True  # Обращение по вх.
    return False


def check_rzn_details(type_id: int) -> bool:
    if type_id == 6:
        return False
    return True


def get_key(number: str, date: str, type_id: int):
    url = set_url(number, date, type_id)
    html = get_page(url)
    if check_cab_mi(type_id):
        return get_key_cab_mi(html)
    else:
        return get_key_le(html)
    # if type_id == 2 or type_id == 3 or type_id == 6:
    #     return get_key_le(html)
    # else:
    #     return get_key_cab_mi(html)


def get_updates():
    objs = TasksData.objects.filter(is_active=True, completed=False, notice=1)
    for obj in objs:
        key = TasksKey.objects.get(is_active=True, data=obj.pk)
        print(obj)
        new_key: TasksKey = TasksKey()
        if check_cab_mi(obj.type.pk):
            new_key.value = get_key(obj.rzn_number, obj.rzn_date, obj.type.pk)
        else:
            # print(f"{obj.dec_number=}, {obj.dec_date=}")
            if check_type_le(obj.type.pk):
                new_key.value = get_key(obj.rzn_number, obj.rzn_date, obj.type.pk)
            else:
                new_key.value = get_key(obj.dec_number, obj.dec_date, obj.type.pk)
        notice_id = new_key.compare(key)
        # print(notice_id)
        if notice_id > 1:
            key.is_active = False
            key.save()
            new_key.data = obj
            new_key.save()
            notice = TasksNotice.objects.get(pk=notice_id)
            # print(notice)
            obj.notice = notice
            obj.save()
            # print(f"{new_key.pk=}")
            # print(obj)
        time.sleep(2)


def get_last_row_cam_mi(data: list):
    return data[len(data) - 1]


def get_last_row_le(data: list):
    return data[len(data) - 1]


def validate_last_row_cab_mi(row: list):
    for txt in row:
        if mark_PY_positive in txt or mark_PY_negative in txt:
            return True  # Задача завершена
    return False  # Задача в работе


def validate_last_row_le(row: str):
    if mark_le in row:
        return True  # Задача завершена
    return False  # Задача в работе


def completeness_check_cab_mi(obj: TasksKey):
    data = obj.value

    last_row = get_last_row_cam_mi(data)
    return validate_last_row_cab_mi(last_row)


def completeness_check_le(obj: TasksKey):
    data = obj.value
    last_row = get_last_row_le(data)
    return validate_last_row_le(last_row)


def completeness_check(obj: TasksKey, type_id: int):
    if check_cab_mi(type_id):
        return completeness_check_cab_mi(obj)
    return completeness_check_le(obj)


def completeness_check_all():
    objs = TasksData.objects.filter(is_active=True, completed=False, notice_id__gte=2)
    for obj in objs:
        type_id = obj.type.pk
        key = TasksKey.objects.get(is_active=True, data_id=obj.pk)
        if completeness_check(key, type_id):
            notice = TasksNotice.objects.get(pk=1)
            obj.notice_id = notice
            obj.completed = True
            obj.is_active = False
            obj.save()
    print('Проверка выполнена')


def get_title_task_details(title, task_type_id, task_type_title, number, date):
    if task_type_id == 6:
        return f"{title} ({task_type_title} | Исх. № {number} от {date})"
    return f"{title} ({task_type_title} | Вх. № {number} от {date})"


def update_tasks():
    get_updates()
    # completeness_check_all()
