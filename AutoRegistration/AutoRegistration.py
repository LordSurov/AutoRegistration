# -*- coding: cp1251 -*- 
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  # Импортируем Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Укажи путь к драйверу браузера
driver_path = "C:/Users/user/Downloads/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)

# Функция для чтения CSV-файла с кодировкой utf-8-sig
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:  # Используем utf-8-sig
        reader = csv.DictReader(csvfile, delimiter=';')  # Указываем разделитель ';'
        data = [row for row in reader]
    return data

# Загружаем данные из CSV
data = read_csv("C:\\Users\\user\\Downloads\\chromedriver-win64\\tadj1.csv")  # Укажи путь к файлу с данными

# Инициализируем драйвер с использованием Service
driver = webdriver.Chrome(service=service)
driver.get("https://job.cznmos.ru/anketa/irs-construction/")

# Ждем загрузки страницы
time.sleep(3)

# Цикл для обработки каждого человека из данных
for person in data:
    # Заполнение полей
    driver.find_element(By.NAME, "canlastname").send_keys(person['last_name'])  # Фамилия
    driver.find_element(By.NAME, "canfirstname").send_keys(person['first_name'])  # Имя
    driver.find_element(By.NAME, "cansurname").send_keys(person['surname'])  # Отчество

    # Заполнение поля "Дата рождения"
    dob_field = driver.find_element(By.CSS_SELECTOR, '.react-datepicker__input-container input')
    # Кликаем на поле, чтобы оно получило фокус
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(dob_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", dob_field)  # Прокручиваем страницу
    dob_field.click()

    # Даем немного времени, чтобы каретка установилась в нужное место
    time.sleep(1)  # Задержка 1 секунда
    dob_field.send_keys(person['dob'])
    dob_field.send_keys(Keys.TAB)

    # Ожидаем, что календарь закроется (или скрываем его через JavaScript)
    time.sleep(1)  # Дополнительная задержка
    driver.execute_script('document.querySelector(".react-datepicker").style.display = "none";')

    # Заполнение поля "Пол"
    gender_input = driver.find_element(By.ID, "react-select-2-input")
    gender_input.send_keys(person['gender'])
    gender_input.send_keys(Keys.ENTER)

    # Заполнение поля "Мобильный телефон"
    tel_field = driver.find_element(By.NAME, "ccmobtel")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(tel_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", tel_field)  # Прокручиваем страницу
    actions = ActionChains(driver)
    actions.move_to_element(tel_field).click().perform()

    time.sleep(1)  # Задержка 1 секунда
    tel_field.send_keys(person['phone'])
    tel_field.send_keys(Keys.TAB)

    # Заполнение поля "E-mail"
    driver.find_element(By.NAME, "ccemail").send_keys(person['email'])

    # Заполнение поля "Уровень образования" (по умолчанию 11)
    education_input = driver.find_element(By.ID, "react-select-3-input")
    education_input.send_keys("11")
    education_input.send_keys(Keys.ENTER)

    # Заполнение поля "Гражданство" (по умолчанию тад)
    country_input = driver.find_element(By.ID, "react-select-4-input")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(country_input))
    driver.execute_script("arguments[0].scrollIntoView(true);", country_input)  # Прокручиваем страницу
    country_input.send_keys(person['country_name'])  # Используем новое поле для страны
    country_input.send_keys(Keys.ENTER)

    # Заполнение поля "Программа обучения" (по умолчанию Водитель погрузчика)
    program_input = driver.find_element(By.ID, "react-select-5-input")
    program_input.send_keys(person['program'])
    program_input.send_keys(Keys.ENTER)

    # Заполнение поля "Старт обучения" (по умолчанию Январь)
    start_training_input = driver.find_element(By.ID, "react-select-6-input")
    start_training_input.send_keys(person['start_training'])
    start_training_input.send_keys(Keys.ENTER)

    # Заполнение поля "Наименование работы" (по умолчанию самолет)
    driver.find_element(By.NAME, "workName").send_keys("самолет")

    # Заполнение поля "Телефон для работы" (по умолчанию 926 717-73-12)
    work_tel_field = driver.find_element(By.NAME, "workTel")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(work_tel_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", work_tel_field)  # Прокручиваем страницу
    actions.move_to_element(work_tel_field).click().perform()

    time.sleep(1)  # Задержка 1 секунда
    work_tel_field.send_keys("926 717-73-12")

    # Заполнение поля "Согласие"
    checkbox = driver.find_element(By.ID, "agreement")
    if not checkbox.is_selected():  # Проверка, если галочка еще не выбрана
        checkbox.click()

    # Ожидаем появления кнопки "Зарегистрироваться"
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]"))
        )
        submit_button.click()  # Кликаем на кнопку отправки формы
        time.sleep(3)  # Небольшая задержка перед переходом к следующему человеку
    except Exception as e:
        print(f"Ошибка при клике на кнопку отправки: {e}")
        pass

    # Ждем появления кнопки "К форме регистрации"
    try:
        registration_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'К форме регистрации')]"))
        )
        registration_button.click()  # Кликаем на кнопку "К форме регистрации"
        time.sleep(3)  # Небольшая задержка перед переходом к следующему человеку
    except Exception as e:
        print(f"Ошибка при клике на кнопку 'К форме регистрации': {e}")
        pass

    # Ждем немного перед переходом к следующему человеку
    delay_time = random.randint(60, 180)  # Задержка в секундах от 60 (1 минута) до 180 (3 минуты)
    print(f"Ожидаем {delay_time} секунд перед отправкой следующей формы...")
    time.sleep(delay_time)  # Задержка перед переходом к следующему человеку


# Ждём, чтобы увидеть результат
time.sleep(50)
driver.quit()

