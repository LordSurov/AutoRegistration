# -*- coding: cp1251 -*- 
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Specify the path to the Chrome WebDriver
driver_path = "C:/Users/user/Downloads/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)

# Function to read CSV file with utf-8-sig encoding
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = [row for row in reader]
    return data

# Load data from CSV
data = read_csv("C:\\Users\\user\\Downloads\\chromedriver-win64\\tadj1.csv")

# Initialize WebDriver
driver = webdriver.Chrome(service=service)
driver.get("https://job.cznmos.ru/anketa/irs-construction/")

# Wait for the page to load
time.sleep(3)

# Loop through each person in the dataset
for person in data:
    # Fill in personal information fields
    driver.find_element(By.NAME, "canlastname").send_keys(person['last_name'])  # Last name
    driver.find_element(By.NAME, "canfirstname").send_keys(person['first_name'])  # First name
    driver.find_element(By.NAME, "cansurname").send_keys(person['surname'])  # Middle name

    # Fill in the "Date of Birth" field
    dob_field = driver.find_element(By.CSS_SELECTOR, '.react-datepicker__input-container input')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(dob_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", dob_field)
    dob_field.click()
    time.sleep(1)  # Small delay
    dob_field.send_keys(person['dob'])
    dob_field.send_keys(Keys.TAB)
    time.sleep(1)  # Additional delay
    driver.execute_script('document.querySelector(".react-datepicker").style.display = "none";')

    # Fill in the "Gender" field
    gender_input = driver.find_element(By.ID, "react-select-2-input")
    gender_input.send_keys(person['gender'])
    gender_input.send_keys(Keys.ENTER)

    # Fill in the "Mobile Phone" field
    tel_field = driver.find_element(By.NAME, "ccmobtel")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(tel_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", tel_field)
    actions = ActionChains(driver)
    actions.move_to_element(tel_field).click().perform()
    time.sleep(1)
    tel_field.send_keys(person['phone'])
    tel_field.send_keys(Keys.TAB)

    # Fill in the "Email" field
    driver.find_element(By.NAME, "ccemail").send_keys(person['email'])

    # Fill in the "Education Level" field (default: 11)
    education_input = driver.find_element(By.ID, "react-select-3-input")
    education_input.send_keys("11")
    education_input.send_keys(Keys.ENTER)

    # Fill in the "Citizenship" field
    country_input = driver.find_element(By.ID, "react-select-4-input")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(country_input))
    driver.execute_script("arguments[0].scrollIntoView(true);", country_input)
    country_input.send_keys(person['country_name'])
    country_input.send_keys(Keys.ENTER)

    # Fill in the "Training Program" field
    program_input = driver.find_element(By.ID, "react-select-5-input")
    program_input.send_keys(person['program'])
    program_input.send_keys(Keys.ENTER)

    # Fill in the "Training Start Date" field
    start_training_input = driver.find_element(By.ID, "react-select-6-input")
    start_training_input.send_keys(person['start_training'])
    start_training_input.send_keys(Keys.ENTER)

    # Fill in the "Job Title" field (default: "самолет")
    driver.find_element(By.NAME, "workName").send_keys("самолет")

    # Fill in the "Work Phone" field (default: 926 717-73-12)
    work_tel_field = driver.find_element(By.NAME, "workTel")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(work_tel_field))
    driver.execute_script("arguments[0].scrollIntoView(true);", work_tel_field)
    actions.move_to_element(work_tel_field).click().perform()
    time.sleep(1)
    work_tel_field.send_keys("926 717-73-12")

    # Click the "Agreement" checkbox
    checkbox = driver.find_element(By.ID, "agreement")
    if not checkbox.is_selected():
        checkbox.click()

    # Click the "Register" button
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]"))
        )
        submit_button.click()
        time.sleep(3)
    except Exception as e:
        print(f"Error clicking the submit button: {e}")

    # Click the "Back to Registration Form" button
    try:
        registration_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'К форме регистрации')]"))
        )
        registration_button.click()
        time.sleep(3)
    except Exception as e:
        print(f"Error clicking the 'Back to Registration' button: {e}")

    # Delay before processing the next person
    delay_time = random.randint(60, 180)  # Delay between 1 to 3 minutes
    print(f"Waiting {delay_time} seconds before submitting the next form...")
    time.sleep(delay_time)

# Wait before closing the browser
time.sleep(50)
driver.quit()
