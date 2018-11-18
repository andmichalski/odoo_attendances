import os
import time
from datetime import date, datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CURRENT_PATH = os.getcwd()
LOGIN_FILE_PATH = CURRENT_PATH + "/login.txt"
CHROMEDRIVER_PATH = CURRENT_PATH + "/chromedriver"


class FillAttendances():

    def __init__(self):
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 2)
        self.login = None
        self.password = None
        self.name = None
        self.surname = None
        self.check_in_hours = None
        self.check_out_hours = None

    def parse_base_user_data(self):
        with open(LOGIN_FILE_PATH, "r") as file:
            data = [line.replace('\n', '').split(" ")[1] for line in
                    file.readlines()]
            self.login = data[0]
            self.password = data[1]
            self.name = data[2]
            self.surname = data[3]
            self.check_in_hours = data[4]
            self.check_out_hours = data[5]

    def login_user(self):
        self.driver.get("https://odoo.servocode.com/web#menu_id=386&action=542")

        login_element = self.driver.find_element_by_id("login")
        login_element.send_keys(self.login)

        password_element = self.driver.find_element_by_id("password")
        password_element.send_keys(self.password)
        password_element.send_keys(Keys.RETURN)

        time.sleep(1)
        elements = self.driver.find_elements_by_link_text("Attendances")
        locs = [el.location['y'] for el in elements]
        max_y = max(locs)
        index = locs.index(max_y)
        attendance_button = elements[index]
        attendance_button.click()

    def find_last_filled_date(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    "/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div[2]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    "/html/body/div[1]/div[2]/div[1]/div[1]/div/input"))).send_keys(
            self.surname, Keys.ENTER)
        time.sleep(1)
        last_record = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                  "/html/body/div[1]/div[2]/div[2]/div/div/div/table/tbody/tr[1]/td[3]")))
        last_date = last_record.text.split(" ")[0]
        return last_date

    def create_new_attendance(self, attendance_date="11/07/2018"):
        check_in_time = attendance_date + " " + self.check_in_hours
        check_out_time = attendance_date + " " + self.check_out_hours

        try:
            self.short_wait.until(EC.element_to_be_clickable((By.XPATH,
                                                              "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[2]"))).click()
        except TimeoutException:
            self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                        "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/button[1]"))).click()

        self.wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "o_main_content")))

        self.driver.implicitly_wait(2)

        check_out = self.driver.find_element_by_name("check_out")
        check_out.click()
        check_out.clear()
        check_out.send_keys(check_out_time)
        check_out.click()

        check_in = self.driver.find_element_by_name("check_in")
        check_in.click()
        check_in.clear()
        check_in.send_keys(check_in_time)
        check_in.click()

        employee_name = self.driver.find_element_by_css_selector(
            "input[id*='o_field_input']")
        employee_name.click()
        employee_name_input = self.name + " " + self.surname
        employee_name.send_keys(employee_name_input)

        time.sleep(1)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/button[1]").click()


class FindWorkDays():

    def find_work_days(self, last_flled_date_str="11/01/2018"):
        today_date = datetime.now().date()

        last_filled_values = last_flled_date_str.split("/")
        last_filled_date = date(int(last_filled_values[2]),
                                int(last_filled_values[0]),
                                int(last_filled_values[1]))

        begin_date = last_filled_date + timedelta(days=1)
        dates_delta = today_date - begin_date

        days = []
        for day in range(dates_delta.days + 1):
            temp_date = begin_date + timedelta(day)
            if temp_date.weekday() < 5:
                days.append(temp_date.strftime('%m/%d/%Y'))

        return days


if __name__ == "__main__":
    fa = FillAttendances()
    fwd = FindWorkDays()
    fa.parse_base_user_data()
    fa.login_user()
    last_filled_date = fa.find_last_filled_date()
    days = fwd.find_work_days(last_filled_date)
    for day in days:
        fa.create_new_attendance(day)
