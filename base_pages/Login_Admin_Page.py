from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Login_Admin_Page:
    textbox_username_id = "//input[@name='userName']"
    textbox_password_id = "Password"
    btn_login_xpath = "//button[contains(.,'Login')]"
    captcha_box = "//input[contains(@placeholder,'Captcha')]"
    login_here_btn_xpath = "//button[contains(@class,'swal2-confirm') and normalize-space()='Login Here']"


    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        usernaam = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.textbox_username_id))
        )
        usernaam.clear()
        usernaam.send_keys(username)

    def enter_password(self, password):
        paasward = self.driver.find_element(By.ID, self.textbox_password_id)
        paasward.clear()
        paasward.send_keys(password)


    def enter_captcha(self):

        captcha_element = self.driver.find_element(By.XPATH, self.captcha_box)

        print("Please enter CAPTCHA manually...")

        while True:

            captcha_value = captcha_element.get_attribute("value")

            captcha_value = captcha_value.strip()

            if len(captcha_value) == 5:
                print("Captcha entered:", captcha_value)
                break

            time.sleep(1)

    def click_login_btn(self):
        self.driver.find_element(By.XPATH, self.btn_login_xpath).click()

        try:
            login_here_btn = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.login_here_btn_xpath)
                )
            )

            print("Login Here popup displayed. Clicking it...")
            login_here_btn.click()

        except:
            print("Login Here popup not displayed. Continuing...")


    def hover_user_icon(self):
        # Hover over user menu
        user_menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(@class,'dropdown-toggle') and @data-hover='Pages']")
            )
        )

        ActionChains(self.driver).move_to_element(user_menu).perform()

        # Click Logout
        logout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[normalize-space()='Logout']")
            )
        )

        logout.click()




