import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация драйвера
driver = webdriver.Chrome()
url = 'https://www.divan.ru/chelyabinsk/category/podvesnye-svetilniki'

# Переход на сайт
driver.get(url)

# Ожидание загрузки элементов
try:
    light_divans = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.LlPhw'))
    )
except Exception as e:
    print(f'Ошибка при загрузке страницы: {e}')
    driver.quit()
    exit()

parsed_data = []

# Парсинг данных
for light_divan in light_divans:
    try:
        name = light_divan.find_element(By.CSS_SELECTOR, 'div.lsooF').text.splitlines()[0].strip()
        price = light_divan.find_element(By.CSS_SELECTOR, 'div.pY3d2').text.splitlines()[0].strip()
        price = price[:-4].strip()
        url_light = light_divan.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    except Exception as e:
        print(f'Произошла ошибка при парсинге сайта: {e}')
        continue

    parsed_data.append([name, price, url_light])

# Завершение работы драйвера
driver.quit()

# Запись данных в CSV файл
with open('Price_lights_divan.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название светильника', 'Цена, руб.', 'Ссылка на сайт'])
    writer.writerows(parsed_data)

