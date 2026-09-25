import pytest
from selenium import webdriver
import time
from base_pages.Login_Admin_Page import Login_Admin_Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import LogGen
from utilities.screenshot import Screenshot
from selenium.common.exceptions import TimeoutException
import pytest

@pytest.mark.usefixtures("setup")
class Test_Admin_Login:
    username = "USER_RAHUL"
    password = "Cdac@2026"
    invalid_username = "ASDF"
    invalid_password = "ADCDS"

    logger = LogGen.loggen()


    @pytest.mark.login
    def test_title_verification(self):

        self.logger.info(
            "********** Test Title Verification Started **********"
        )

        act_title = self.driver.title
        exp_title = "eShushrut - HMIS"

        self.logger.info(
            f"Actual Title: {act_title}"
        )

        self.logger.info(
            f"Expected Title: {exp_title}"
        )

        assert act_title == exp_title

        self.logger.info(
            "Title Verification Passed"
        )


    @pytest.mark.login
    def test_invalid_login(self):

        self.logger.info(
            "********** Test Invalid Login Started **********"
        )

        self.admin_lp = Login_Admin_Page(
            self.driver
        )

        self.logger.info(
            "Entering invalid credentials"
        )

        self.admin_lp.enter_username(
            self.invalid_username
        )

        self.admin_lp.enter_password(
            self.invalid_password
        )

        self.admin_lp.enter_captcha()

        self.admin_lp.click_login_btn()

        try:

            WebDriverWait(
                self.driver,
                3
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//a[contains(@class,'dropdown-toggle')]"
                    )
                )
            )

            pytest.fail(
                "Invalid login succeeded."
            )

        except TimeoutException:

            self.logger.info(
                "Invalid Login Passed"
            )

        # Clear username/password if required
        # or refresh page


    @pytest.mark.login
    def test_valid_login(self):

        self.logger.info(
            "********** Test Valid Login Started **********"
        )

        self.admin_lp = Login_Admin_Page(
            self.driver
        )

        self.admin_lp.enter_username(self.username)

        self.admin_lp.enter_password(
            self.password
        )

        self.admin_lp.enter_captcha()

        self.admin_lp.click_login_btn()

        act_username = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(@class,'dropdown-toggle')]"
                )
            )
        ).text.strip().upper()

        expected_parts = (
            self.username.upper()
            .replace("USER_", "")
            .replace("_USER", "")
            .split("_")
        )

        assert any(
            part and part in act_username
            for part in expected_parts
        ), (
            f"Username mismatch. "
            f"Login Username: {self.username}, "
            f"Displayed Username: {act_username}"
        )

        self.logger.info(
            "Valid Login Passed"
        )











