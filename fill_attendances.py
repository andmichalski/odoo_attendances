import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_FILE_PATH = "/home/amich/odoo_attendances/login_data.txt"
with open(LOGIN_FILE_PATH, "r") as file:
    data = [line.replace('\n', '').split(" ")[1] for line in file.readlines()]
    LOGIN = data[0]
    PASSWORD = data[1]

NAME = "Andrzej"
SURNAME = "Michalski"
CHECK_IN = "09:00:00"
CHECK_OUT = "16:20:00"

driver = webdriver.Chrome()
driver.get("https://odoo.servocode.com/web#menu_id=386&action=542")

login_element = driver.find_element_by_id("login")
login_element.send_keys(LOGIN)

password_element = driver.find_element_by_id("password")
password_element.send_keys(PASSWORD)
password_element.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 10)

attendance_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[11]/ul/li[1]/a/span")))
attendance_button.click()

def find_last_date():
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div[2]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/input"))).send_keys(SURNAME, Keys.ENTER)
    last_record = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div/table/tbody/tr[1]/td[3]")))
    last_date = last_record.text.split(" ")[0]
    return last_date

last_date = "11/07/2018"
test_date_1 = last_date + " 09:00:00"
test_date_2 = last_date + " 16:20:00"

# Create new Attendance
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/button[1]"))).click()
main_content = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "o_main_content")))

driver.implicitly_wait(2)

check_out= driver.find_element_by_name("check_out")
check_out.click()
check_out.clear()
check_out.send_keys(test_date_2)
check_out.click()

check_in = driver.find_element_by_name("check_in")
check_in.click()
check_in.clear()
check_in.send_keys(test_date_1)
check_in.click()

employee_name = driver.find_element_by_css_selector("input[id*='o_field_input']")
employee_name.click()
employee_name_input = NAME + " " + SURNAME
employee_name.send_keys(employee_name_input)

time.sleep(1)

driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/button[1]").click()

