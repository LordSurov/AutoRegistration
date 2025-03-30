# -*- coding: cp1251 -*- 
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  # ����������� Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# ����� ���� � �������� ��������
driver_path = "C:/Users/user/Downloads/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)

# ������� ��� ������ CSV-����� � ���������� utf-8-sig
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:  # ���������� utf-8-sig
        reader = csv.DictReader(csvfile, delimiter=';')  # ��������� ����������� ';'
        data = [row for row in reader]
    return data

# ��������� ������ �� CSV
data = read_csv("C:\\Users\\user\\Downloads\\chromedriver-win64\\tadj1.csv")  # ����� ���� � ����� � �������

# �������������� ������� � �������������� Service
driver = webdriver.Chrome(service=service)
driver.get("https://job.cznmos.ru/anketa/irs-construction/")

# ���� �������� ��������
time.sleep(3)

# ���� ��� ��������� ������� �������� �� ������
for person in data:
    # ���������� �����
    driver.find_element(By.NAME, "canlastname").send_keys(person['last_name'])  # �������
    driver.find_element(By.NAME, "canfirstname").send_keys(person['first_name'])  # ���
    driver.find_element(By.NAME, "cansurname").send_keys(person['surname'])  # ��������

    # ���������� ���� "���� ��������"
    dob_field = driver.find_element(By.CSS_SELECTOR, '.react-datepicker__input-container input')
    # ������� �� ����, ����� ��� �������� �����
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(dob_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", dob_field)  # ������������ ��������
    dob_field.click()

    # ���� ������� �������, ����� ������� ������������ � ������ �����
    time.sleep(1)  # �������� 1 �������
    dob_field.send_keys(person['dob'])
    dob_field.send_keys(Keys.TAB)

    # �������, ��� ��������� ��������� (��� �������� ��� ����� JavaScript)
    time.sleep(1)  # �������������� ��������
    driver.execute_script('document.querySelector(".react-datepicker").style.display = "none";')

    # ���������� ���� "���"
    gender_input = driver.find_element(By.ID, "react-select-2-input")
    gender_input.send_keys(person['gender'])
    gender_input.send_keys(Keys.ENTER)

    # ���������� ���� "��������� �������"
    tel_field = driver.find_element(By.NAME, "ccmobtel")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(tel_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", tel_field)  # ������������ ��������
    actions = ActionChains(driver)
    actions.move_to_element(tel_field).click().perform()

    time.sleep(1)  # �������� 1 �������
    tel_field.send_keys(person['phone'])
    tel_field.send_keys(Keys.TAB)

    # ���������� ���� "E-mail"
    driver.find_element(By.NAME, "ccemail").send_keys(person['email'])

    # ���������� ���� "������� �����������" (�� ��������� 11)
    education_input = driver.find_element(By.ID, "react-select-3-input")
    education_input.send_keys("11")
    education_input.send_keys(Keys.ENTER)

    # ���������� ���� "�����������" (�� ��������� ���)
    country_input = driver.find_element(By.ID, "react-select-4-input")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(country_input))
    driver.execute_script("arguments[0].scrollIntoView(true);", country_input)  # ������������ ��������
    country_input.send_keys(person['country_name'])  # ���������� ����� ���� ��� ������
    country_input.send_keys(Keys.ENTER)

    # ���������� ���� "��������� ��������" (�� ��������� �������� ����������)
    program_input = driver.find_element(By.ID, "react-select-5-input")
    program_input.send_keys(person['program'])
    program_input.send_keys(Keys.ENTER)

    # ���������� ���� "����� ��������" (�� ��������� ������)
    start_training_input = driver.find_element(By.ID, "react-select-6-input")
    start_training_input.send_keys(person['start_training'])
    start_training_input.send_keys(Keys.ENTER)

    # ���������� ���� "������������ ������" (�� ��������� �������)
    driver.find_element(By.NAME, "workName").send_keys("�������")

    # ���������� ���� "������� ��� ������" (�� ��������� 926 717-73-12)
    work_tel_field = driver.find_element(By.NAME, "workTel")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(work_tel_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", work_tel_field)  # ������������ ��������
    actions.move_to_element(work_tel_field).click().perform()

    time.sleep(1)  # �������� 1 �������
    work_tel_field.send_keys("926 717-73-12")

    # ���������� ���� "��������"
    checkbox = driver.find_element(By.ID, "agreement")
    if not checkbox.is_selected():  # ��������, ���� ������� ��� �� �������
        checkbox.click()

    # ������� ��������� ������ "������������������"
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '������������������')]"))
        )
        submit_button.click()  # ������� �� ������ �������� �����
        time.sleep(3)  # ��������� �������� ����� ��������� � ���������� ��������
    except Exception as e:
        print(f"������ ��� ����� �� ������ ��������: {e}")
        pass

    # ���� ��������� ������ "� ����� �����������"
    try:
        registration_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '� ����� �����������')]"))
        )
        registration_button.click()  # ������� �� ������ "� ����� �����������"
        time.sleep(3)  # ��������� �������� ����� ��������� � ���������� ��������
    except Exception as e:
        print(f"������ ��� ����� �� ������ '� ����� �����������': {e}")
        pass

    # ���� ������� ����� ��������� � ���������� ��������
    delay_time = random.randint(60, 180)  # �������� � �������� �� 60 (1 ������) �� 180 (3 ������)
    print(f"������� {delay_time} ������ ����� ��������� ��������� �����...")
    time.sleep(delay_time)  # �������� ����� ��������� � ���������� ��������


# ���, ����� ������� ���������
time.sleep(50)
driver.quit()

