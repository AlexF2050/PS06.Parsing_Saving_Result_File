import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook

# Путь к вашему драйверу Chrome
driver = webdriver.Chrome()
# URL страницы для парсинга
url = 'https://www.divan.ru/novosibirsk/category/odeala'
driver.get(url)
# Даем странице время на загрузку
time.sleep(5)
# Находим все элементы с товарами
products = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-card"]')
# Список для хранения данных
data = []
# Извлекаем данные о каждом товаре
for product in products:
    name_element = product.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]')
    price_element = product.find_element(By.CLASS_NAME, 'ui-LD-ZU')
    image_element = product.find_element(By.TAG_NAME, 'img')
    name = name_element.text
    price = price_element.text
    image_src = image_element.get_attribute('src')
    data.append({
        'Наименование товара': name,
        'Цена товара': price,
        'Ссылка на картинку': image_src
    })
# Закрываем драйвер
driver.quit()

# Сохраняем данные в CSV файл
with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
print("Данные успешно сохранены в products.csv")

# Сохраняем данные в XLSX файл
workbook = Workbook()
sheet = workbook.active
sheet.title = "Товары"

# Записываем заголовки
sheet.append(['Наименование товара', 'Цена товара', 'Ссылка на картинку'])

# Записываем данные
for item in data:
    sheet.append([item['Наименование товара'], item['Цена товара'], item['Ссылка на картинку']])

# Сохраняем файл
workbook.save('products.xlsx')
print("Данные успешно сохранены в products.xlsx")