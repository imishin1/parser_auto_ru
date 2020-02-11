from bs4 import BeautifulSoup
import requests
import csv

def find_page_number(html_text): # возвращает колличество страниц, которые нужно запарсить
    soup = BeautifulSoup(html_text, 'lxml')
    data = soup.find('span', class_='ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination-module__pages')
    page_number = data.find_all('span', class_='Button__text')[-1].text
    return int(page_number)

def find_html_page(url): # возвращает html код страницы в текстовом формате
    html_req = requests.get(url)
    html_req.encoding = 'utf-8'
    return html_req.text

def write_data(data_dict): # необходим, для записи словаря построчно в cvs формат
    with open('lexus.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data_dict['title'], data_dict['price'], data_dict['motor'], data_dict['year'], data_dict['kmage'], data_dict['ref']))

def find_data(html_text): # парсит страницу и создает словарь с полученными параметрами
    print('Опа, новая страничка пошла')
    soup = BeautifulSoup(html_text,'lxml')
    data = soup.find('div', class_ = 'ListingCars-module__container ListingCars-module__list')
    data_list = data.find_all('div', class_='ListingItem-module__description')
    for each_data in data_list:
        try:
            title = each_data.find('a', class_='Link ListingItemTitle-module__link').text.strip()
        except:
            titile = ''
        try:
            ref = each_data.find('a', class_='Link ListingItemTitle-module__link').get('href')
        except:
            ref = ''
        try:
            price = each_data.find('div', class_='ListingItemPrice-module__content').text.strip()
        except:
            price = ''
        try:
            year = each_data.find('div', class_='ListingItem-module__year').text.strip()
        except:
            year = ''
        try:
            kmage = each_data.find('div', class_='ListingItem-module__kmAge').text.strip()
        except:
            kmage = ''
        try:
            step_one = each_data.find('div', class_='ListingItemTechSummary-module__container ListingItem-module__techSummary')
            motor = step_one.find('div', class_='ListingItemTechSummary-module__cell').text.strip()
        except:
            motor = ''
        data_dict = {
            'title' : title,
            'price' : price,
            'motor' : motor,
            'year' : year,
            'kmage' : kmage,
            'ref' : ref
        }
        write_data(data_dict)

def main():
    base_url = 'https://auto.ru/moskva/cars/lexus/all/?sort=fresh_relevance_1-desc&output_type=list&page='
    page_number = find_page_number(find_html_page(base_url))
    for i in range(1, page_number + 1): # цикл нужен, чтобы запарсить все страницы в указанном диапозоне
        url = base_url + str(i)
        find_data(find_html_page(url))

if __name__ == '__main__':
    main()