import pyautogui
import pytest
from selenium import webdriver
import time


from selenium.common.exceptions import TimeoutException
from base_pages.Login_Admin_Page import Login_Admin_Page
from base_pages.Patient_Register_page import Patient_Register_Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import LogGen
from utilities.screenshot import Screenshot
from test_data.test_patient_data import Testdata, TestDataGenerator
import random
import string
from selenium.webdriver.common.keys import Keys

@pytest.mark.usefixtures("login")
class Test_Emergency_Patient_Register:
    logger = LogGen.loggen()
    driver = None
    patient_reg = None
    generated_crn = None
    selected_department = None
    selected_unit = None
    opd_unit_name = None


    @pytest.mark.emergency_flow
    def test_emergency_brought_dead_registration(self):

        emg_department_name = Testdata.EMERGENCY_NAME
        patient_name = Testdata.PATIENT_NAME
        mobile_number = TestDataGenerator.generate_mobile_number()

        self.logger.info(
            "========== EMERGENCY BROUGHT DEAD TEST STARTED =========="
        )

        self.logger.info(
            f"Test Data | Patient: {patient_name} | "
            f"Department: {emg_department_name} | "
            f"Mobile: {mobile_number}"
        )

        try:

            # ==========================
            # CREATE BROUGHT DEAD PATIENT
            # ==========================

            self.logger.info(
                "Opening patient registration module"
            )

            self.patient_reg.click_registration_module()

            self.patient_reg.click_patient_registration_option()

            self.patient_reg.click_new_registration_btn()

            time.sleep(3)

            self.logger.info(
                f"Selecting Emergency Department: {emg_department_name}"
            )

            self.patient_reg.select_visiting_dpt(
                emg_department_name
            )

            self.logger.info(
                "Emergency department selected"
            )

            self.logger.info(
                "Selecting Brought Dead option"
            )

            self.patient_reg.click_brought_dead_radio_btn()

            self.logger.info(
                "Entering brought dead patient details"
            )

            self.patient_reg.enter_patient_name(
                patient_name
            )

            self.patient_reg.enter_patient_age(
                "20"
            )

            self.patient_reg.select_gender(
                "Male"
            )

            self.patient_reg.enter_patient_mobile_no(
                mobile_number
            )

            self.patient_reg.enter_patient_father(
                "Automation father"
            )

            self.patient_reg.enter_patient_mother(
                "Automation mother"
            )

            self.patient_reg.enter_patient_city(
                "Automation city s"
            )

            self.patient_reg.enter_patient_post_office(
                "Automation post office"
            )

            self.patient_reg.enter_patient_house_number(
                "2922"
            )

            self.patient_reg.enter_patient_street(
                "Automation street s"
            )

            self.patient_reg.enter_patient_pincode(
                "301201"
            )

            self.logger.info(
                "Patient address details entered"
            )

            self.patient_reg.select_brought_by(
                "Other"
            )

            self.patient_reg.enter_brought_by_name(
                "Test"
            )

            self.patient_reg.enter_brought_by_mobile(
                "9998887778"
            )

            self.patient_reg.enter_brought_by_address(
                "Test address"
            )

            selected_declared_by = (
                self.patient_reg
                .select_random_brought_dead_declared_by()
            )

            self.logger.info(
                f"Brought Dead Declared By selected: "
                f"{selected_declared_by}"
            )

            time.sleep(3)

            self.patient_reg.click_save_btn()

            self.logger.info(
                "Brought dead registration saved"
            )

            time.sleep(10)

            pyautogui.press('esc')

            # ==========================
            # PDF VERIFICATION
            # ==========================

            self.logger.info(
                "Starting PDF verification"
            )

            time.sleep(2)

            pdf_text = (
                self.patient_reg.get_blob_pdf_text()
            )

            assert "CRN :" in pdf_text, (
                "CRN not found in PDF"
            )

            crn_number = (
                pdf_text.split("CRN :")[1]
                .split("NAME :")[0]
                .strip()
            )

            self.logger.info(
                f"PDF verification passed | CRN: {crn_number}"
            )

            self.patient_reg.click_close_btn()

            # ==========================
            # BARCODE VERIFICATION
            # ==========================

            self.logger.info(
                "Starting barcode verification"
            )

            time.sleep(3)

            self.patient_reg.get_barcode_blob()

            self.logger.info(
                "Barcode fetched successfully"
            )

            self.patient_reg.click_close_btn()

            # ==========================
            # SEARCH PATIENT
            # ==========================

            self.logger.info(
                f"Searching patient using CRN: {crn_number}"
            )

            self.patient_reg.click_home_tab()

            self.patient_reg.click_patient_registration_option()

            self.patient_reg.enter_search_value(
                crn_number
            )

            WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//tbody//tr"
                    )
                )
            )

            self.logger.info(
                "Patient search results loaded"
            )

            # ==========================
            # DEAD ICON VERIFICATION
            # ==========================

            self.logger.info(
                "Checking brought dead status icon"
            )
            time.sleep(5)

            dead_button = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//button[contains(@class,'status-dead')]"
                    )
                )
            )

            assert dead_button.is_displayed(), (
                "Dead button is not visible"
            )

            self.logger.info(
                "Brought Dead skull icon verified successfully"
            )

            self.logger.info(
                "========== TEST PASSED =========="
            )



        except Exception as e:

            Screenshot.capture(
                self.driver,
                "test_emergency_brought_dead_registration_failed"
            )

            self.logger.error(
                "========== TEST FAILED =========="
            )

            self.logger.error(
                f"Failure Reason: {str(e)}",
                exc_info=True
            )

            raise

    @pytest.mark.emergency_flow
    def test_emergency_is_trauma_registration(self):

        emg_department_name = Testdata.EMERGENCY_NAME
        patient_name = Testdata.PATIENT_NAME
        mobile_number = TestDataGenerator.generate_mobile_number()

        self.logger.info(
            "========== EMERGENCY TRAUMA REGISTRATION TEST STARTED =========="
        )

        self.logger.info(
            f"Test Data | Patient: {patient_name} | "
            f"Department: {emg_department_name} | "
            f"Mobile: {mobile_number}"
        )

        try:

            # ==========================
            # CREATE TRAUMA PATIENT
            # ==========================

            self.logger.info(
                "Opening patient registration module"
            )



            self.patient_reg.click_new_registration_btn()

            time.sleep(3)

            self.logger.info(
                f"Selecting emergency department: {emg_department_name}"
            )

            self.patient_reg.select_visiting_dpt(
                emg_department_name
            )

            self.logger.info(
                "Emergency department selected"
            )

            self.logger.info(
                "Selecting IS Trauma option"
            )

            self.patient_reg.click_is_trauma_radio_btn()

            self.logger.info(
                "Filling trauma patient details"
            )

            self.patient_reg.enter_patient_name(
                patient_name
            )

            self.patient_reg.enter_patient_age(
                "18"
            )

            self.patient_reg.select_gender(
                "Male"
            )

            self.patient_reg.enter_patient_mobile_no(
                mobile_number
            )

            self.patient_reg.enter_patient_father(
                "Automation father"
            )

            self.patient_reg.enter_patient_mother(
                "Automation mother"
            )

            self.patient_reg.enter_patient_city(
                "Automation city"
            )

            self.patient_reg.enter_patient_post_office(
                "Automation post office"
            )

            self.patient_reg.enter_patient_house_number(
                "292"
            )

            self.patient_reg.enter_patient_street(
                "Automation street"
            )

            self.patient_reg.enter_patient_pincode(
                "777538"
            )

            self.logger.info(
                "Trauma patient details entered successfully"
            )

            self.patient_reg.click_save_btn()

            self.logger.info(
                "Trauma patient registration saved"
            )

            time.sleep(5)

            pyautogui.press('esc')

            # ==========================
            # PDF VERIFICATION
            # ==========================

            self.logger.info(
                "Starting PDF verification"
            )

            time.sleep(2)

            pdf_text = (
                self.patient_reg.get_blob_pdf_text()
            )

            assert "CRN :" in pdf_text, (
                "CRN not found in PDF"
            )

            crn_number = (
                pdf_text.split("CRN :")[1]
                .split("NAME :")[0]
                .strip()
            )

            self.logger.info(
                f"PDF verification passed | CRN: {crn_number}"
            )

            self.patient_reg.click_close_btn()

            # ==========================
            # BARCODE VERIFICATION
            # ==========================

            self.logger.info(
                "Starting barcode verification"
            )

            time.sleep(3)

            self.patient_reg.get_barcode_blob()

            self.logger.info(
                "Barcode fetched successfully"
            )

            self.patient_reg.click_close_btn()

            # ==========================
            # SEARCH PATIENT
            # ==========================

            self.logger.info(
                f"Searching trauma patient using CRN: {crn_number}"
            )

            self.patient_reg.click_home_tab()

            self.patient_reg.click_patient_registration_option()

            self.patient_reg.enter_search_value(
                crn_number
            )

            time.sleep(5)

            WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//tbody//tr"
                    )
                )
            )

            self.logger.info(
                "Patient search results loaded"
            )

            # ==========================
            # CRN VALIDATION
            # ==========================

            crn_element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//td[contains(@class,'ant-table-cell-fix-left')]"
                        f"//span[normalize-space()='{crn_number}']"
                    )
                )
            )

            assert crn_element.is_displayed(), (
                f"CRN {crn_number} not visible in table"
            )

            self.logger.info(
                f"CRN verified successfully: {crn_number}"
            )

            self.logger.info(
                "========== TEST PASSED =========="
            )



        except Exception as e:

            Screenshot.capture(
                self.driver,
                "test_emergency_trauma_registration_failed"
            )

            self.logger.error(
                "========== TEST FAILED =========="
            )

            self.logger.error(
                f"Failure Reason: {str(e)}",
                exc_info=True
            )

            raise

    @pytest.mark.emergency_flow
    def test_emergency_unknown_registration(self):

        emg_department_name = Testdata.EMERGENCY_NAME
        mobile_number = TestDataGenerator.generate_mobile_number()
        patient_name = "Unknown"

        self.logger.info(
            "********** Test Emergency Unknown Registration Started **********"
        )

        try:

            # ==========================
            # CREATE UNKNOWN PATIENT
            # ==========================

            self.patient_reg.click_new_registration_btn()

            time.sleep(3)

            self.patient_reg.select_visiting_dpt(
                emg_department_name
            )

            self.patient_reg.click_unknown_radio_btn()

            self.patient_reg.select_gender("Male")

            self.patient_reg.enter_identification_mark(
                "Mole on Left cheek"
            )

            self.patient_reg.select_brought_by(
                "Other"
            )

            self.patient_reg.enter_brought_by_name(
                "Test"
            )

            self.patient_reg.enter_brought_by_mobile(
                mobile_number
            )

            self.patient_reg.enter_brought_by_address(
                "Test address"
            )

            self.patient_reg.click_save_btn()

            time.sleep(5)

            # ==========================
            # VALIDATION CHECK
            # ==========================

            validation_elements = self.driver.find_elements(
                By.XPATH,
                "//*[contains(@class,'d-block') and contains(@class,'invalid-feedback')]"
            )

            validation_messages = [
                element.text.strip()
                for element in validation_elements
                if element.is_displayed()
                   and element.text.strip()
            ]

            assert not validation_messages, (
                f"Validation messages found: {validation_messages}"
            )

            popup = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container']"
                    )
                )
            )

            popup_text = popup.text.strip()

            assert (
                    "success" in popup_text.lower()
                    or "registered" in popup_text.lower()
            ), (
                f"Unexpected popup message: {popup_text}"
            )

            self.logger.info(
                f"Emergency Unknown Registration successful: {popup_text}"
            )

            # ==========================
            # CLOSE PRINT PREVIEW
            # ==========================

            pyautogui.press('esc')
            time.sleep(3)

            self.patient_reg.click_close_btn()

            time.sleep(3)

            pyautogui.press('esc')

            time.sleep(3)
            self.patient_reg.click_close_btn()
            time.sleep(5)
            # ==========================
            # SEARCH VERIFICATION
            # ==========================

            self.patient_reg.click_home_tab()

            self.patient_reg.click_patient_registration_option()

            self.patient_reg.enter_search_value(
                patient_name
            )

            element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//td[contains(@class,'ant-table-cell-fix-left-last')]"
                        f"//span[translate(normalize-space(text()),"
                        f"'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')="
                        f"'{patient_name.upper()}']"
                    )
                )
            )

            actual_name = element.text.strip()

            assert actual_name.lower() == patient_name.lower(), (
                f"Patient mismatch. Expected {patient_name}, Actual {actual_name}"
            )

            self.logger.info(
                "Unknown patient found successfully"
            )

            # ==========================
            # OPD VERIFICATION
            # ==========================

            self.patient_reg.click_opd_module()

            self.patient_reg.click_opd_dr_desk()

            self.patient_reg.select_opd_dr_desk_department(
                emg_department_name
            )

            self.patient_reg.enter_search_name_in_opd(
                patient_name
            )

            opd_element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//tbody//tr//td[3]//div["
                        f"translate(normalize-space(),"
                        f"'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')="
                        f"'{patient_name.upper()}'"
                        f"]"
                    )
                )
            )

            assert opd_element.is_displayed(), (
                f"{patient_name} not found in OPD"
            )

            self.logger.info(
                "********** Test Emergency Unknown Registration Passed **********"
            )


        except Exception as e:

            Screenshot.capture(
                self.driver,
                "test_emergency_unknown_registration"
            )

            self.logger.error(
                f"********** Test Failed ********** Error: {str(e)}"
            )

            raise