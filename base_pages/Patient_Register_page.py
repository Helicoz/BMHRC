import re
import base64
from io import BytesIO
from datetime import datetime, timedelta
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pyautogui
import random
from PyPDF2 import PdfReader
from selenium.webdriver.support.ui import Select
from utilities.logger import LogGen

class Patient_Register_Page:
    sidebar_open_xpath = "//div[contains(@class,'sidebarClose')]//span[contains(@class,'navbtn_bar')]"
    registration_module_xpath = "//li[@title='Registration']"
    patient_registration_xpath = "//li[contains(@class,'menu-level-1')]//a[text()='Patient Registration']"
    new_registration_btn = "//button[@title='New Registration']"
    visiting_dpt_xpath = "//select[@id='deptCode']"
    visiting_reason_id = "visitReason"
    patient_name_id = "firstName"
    dob_id = "AgeDOBCompAge"
    gender_xpath = "//select[@id='genderCode']"
    mobile_number_id = "mobileNumber"
    patient_father_name_id = "fatherName"
    patient_mother_name_id = "motherName"
    patient_spouse_name_id = "spouseName"
    patient_guardian_name_id = "guardianName"
    city_id = "city"
    post_office_id = "postOffice"
    pincode_id = "pincode"
    house_number_id = "addressLine1"
    street_id = "subLocality1"
    save_id = "save"
    close_btn_xpath = "//button[@aria-label='Close']"
    home_btn_xpath = "//span[contains(@class,'tab-with-close')]//div[contains(.,'Home')]"
    search_xpath = "//input[@name='searchValue']"
    row_name = "//td[contains(@class,'ant-table-cell-fix-left-last')]//span[text()='AUTOMATION']"
    continue_with_new_patient = "//button[text()='Yes']"
    revisit_btn = "//button[contains(@class,'btn-revisit')]"
    new_department_revisit = "//button[normalize-space()='New Department Visit']"
    revisit_department = "//select[contains(@id,'department')]"
    patient_revisit_save_btn = "//button[contains(@class,'blue-button') and normalize-space()='Patient Revisit']"
    opd_module_xpath = "//li[@title='OPD']"
    opd_dr_desk_xpath = "//li[contains(@class,'menu-level-1')]//a[normalize-space()='OPD DrDesk']"
    opd_dr_desk_department = "//select[@title='Select Department/Unit']"
    patient_cancellation_xpath = "//li[contains(@class,'menu-level-1')]//a[text()='Registration  Cancellation']"
    cancel_process_btn_xpath  = "//button[@class='add-blue-button btn btn-primary']"
    cancel_radio_btn_xpath = "//span[@class='ant-radio-inner']"
    cancel_reason_xpath = "//input[@name='cancelReason']"
    cancel_save_xpath = "//button[contains(text(),'Save')]"
    search_after_cancel = "//input[@name='searchValue']"
    refresh_btn_xpath = "//button[@title='Refresh']"
    emergency_unknown_radio_btn = "//input[@id='isUnknown']"
    identification_1_id = "identificationMark1"
    brought_by_xpath = "//select[@id='isRelative']"
    brought_by_name = "//input[@name='broughtByName']"
    brought_by_phone = "//input[@name='broughtByPhone']"
    brought_by_address = "//textarea[@name='broughtByAddress']"
    opd_rx_btn_xpath = "//button[contains(@class,'btn-rx')]"
    chief_complaint_textbox = "//input[@name='complainId']"
    number_of_days_in_cm_xpath = "//input[@name='noOfDays']"
    diagnosis_selection_xpath = "//input[@name='diagnosisCode']"
    investigation_medication_tab_xpath = "//h6[normalize-space()='Investigation & Medication']"
    test_name_xpath = "//input[@name='testCode' and @placeholder='Search Test Name']"
    clinical_history_and_exm_xpath = "//div[@data-placeholder='Clinical History & Examination']"
    drug_name_xpath = "//input[@name='drugCode']"
    drug_instruction_xpath = "//input[@name='drugInstruction']"
    rx_revisit_days = "//input[@name='visitDays']"
    rx_preview_save_xpath = "//button[normalize-space()='PREVIEW & SAVE']"
    followup_tab_xpath = "//h6[normalize-space()='Follow Up & Referral']"
    three_dot_in_listing_page = "//span[contains(@class,'ant-dropdown-trigger') and contains(@class,'table-dropdown')]"
    change_patient_category = "//span[contains(@class,'ant-dropdown-menu-title-content') and normalize-space()='Change Patient Category']"
    patient_category = "//select[@name='categoryCode']"
    category_verification = "//input[@name = 'patIdNo']"
    recommended_by_xpath = "//select[contains(@class,'form-select') and @name='recommendedBy']"
    approved_by_xpath = "//select[@required and @name='newCatApprovedBy']"
    change_category_save_btn = "//button[contains(@class,'blue-button') and normalize-space()='Change Patient Category']"
    print_duplicate_opd_xpath = "//span[contains(@class,'ant-dropdown-menu-title-content') and normalize-space()='Duplicate OPD Card']"
    duplicate_opd_btn_xpath = "//button[contains(@class,'btn-print') and contains(.,'OPD Card')]"
    print_barcode_xpath = "//span[contains(@class,'ant-dropdown-menu-title-content') and normalize-space()='Print Bar Code / QR Code']"
    barcode_btn = "//button[contains(normalize-space(),'Bar Code')]"
    mobile_number_modification = "//span[contains(@class,'ant-dropdown-menu-title-content') and normalize-space()='Mobile Number Modification']"
    mobile_number_field_xpath = "//input[@type='text' and @name='mobileNumber']"
    modify_btn_xpath = "//button[contains(@class,'blue-button') and normalize-space()='Modify']"
    brought_dead_declared_by_xpath = "//select[@name='broughtDeadDeclaredBy']"
    patient_detail_mod = "//span[contains(@class,'ant-dropdown-menu-title-content') and normalize-space()='Patient Details Modification']"
    patient_audit_trail_xpath = "//li[contains(@class,'menu-level-1')]//a[normalize-space()='Patient Audit Trail']"
    adt_module_xpath = "//li[@title='ADT']"
    single_window_xpath = "//li[contains(@class,'menu-level-1')]//a[text()='Single Window Admission Desk']"
    new_admission_btn_xpath = "//button[contains(@class,'white-button') and normalize-space()='New Admission']"
    ipd_module_xpath  = "//li[@title='IPD']"
    ipd_nursing_xpath = "//li[contains(@class,'menu-level-1')]//a[text()='IPD Nursing Desk']"
    patient_acceptance_btn_xpath = "//button[contains(@class,'blue-button') and @title='Patient Acceptance']"
    baby_admission_xpath = "//li[contains(@class,'menu-level-1')]//a[text()='Baby Admission']"
    logger = LogGen.loggen()

    def __init__(self, driver):
        self.driver = driver


    def click_registration_module(self):
        registration = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.registration_module_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            registration
        )

        self.driver.execute_script(
            "arguments[0].click();",
            registration
        )

    def click_patient_registration_option(self):
        patient_registration = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.patient_registration_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_registration
        )

    def click_patient_mobile_modification_option(self):
        patient_mobile = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Mobile Number Modification']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_mobile
        )

    def click_new_registration_btn(self):
        new_registration = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.new_registration_btn)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            new_registration
        )

        self.driver.execute_script(
            "arguments[0].click();",
            new_registration
        )

    def enter_search_cr_no_value(self, value):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='crNo']")
            )
        )
        search_box.clear()
        search_box.send_keys(value)
        time.sleep(3)
        search_box.send_keys(Keys.ENTER)

    def enter_patient_id(self, patient_id):
        patient_id_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@name='attendentId']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            patient_id_field
        )

        patient_id_field.click()
        patient_id_field.clear()
        patient_id_field.send_keys(patient_id)

    def select_visiting_dpt(self, department_name):
        visiting_department = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.visiting_dpt_xpath)
            )
        )

        select = Select(visiting_department)

        for option in select.options:
            option_label = option.get_attribute("label").strip()

            if option_label.casefold() == department_name.strip().casefold():
                time.sleep(5)
                option.click()
                return

        raise Exception(f"Department '{department_name}' not found in dropdown")

    def enter_patient_name(self, patient_name):
        patient_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.patient_name_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_name_field
        )
        patient_name_field.clear()
        patient_name_field.send_keys(patient_name)


    def select_random_payment_mode(self):
        dropdown = Select(
            self.driver.find_element(
                By.XPATH, "//select[@id='paymentMode']"
            )
        )

        options = dropdown.options[1:]  # Skip "Select"

        random_option = random.choice(options)

        dropdown.select_by_value(
            random_option.get_attribute("value")
        )

        self.logger.info(
            f"Selected random payment mode: "
            f"{random_option.get_attribute('label')}"
        )

    def enter_patient_age(self, patient_age):
        patient_age_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.dob_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_age_field
        )
        patient_age_field.send_keys(patient_age)

    def select_gender(self, gender_name):
        gender_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.gender_xpath)
            )
        )

        select = Select(gender_dropdown)

        for option in select.options:
            if option.get_attribute("label") == gender_name:
                option.click()
                return

        raise Exception(f"Gender '{gender_name}' not found in dropdown")



    def enter_patient_mobile_no(self, patient_number):
        patient_number_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.mobile_number_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_number_field
        )
        patient_number_field.send_keys(patient_number)

    def enter_patient_father(self, patient_father_name):
        patient_father_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.patient_father_name_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_father_field
        )
        patient_father_field.send_keys(patient_father_name)

    def enter_patient_mother(self, patient_mother_name):
        patient_mother_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.patient_mother_name_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_mother_field
        )
        patient_mother_field.send_keys(patient_mother_name)

    def enter_patient_spouse(self, patient_spouse_name):
        patient_spouse_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.patient_spouse_name_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_spouse_field
        )
        patient_spouse_field.send_keys(patient_spouse_name)


    def enter_patient_guardian(self, patient_guardian_name):
        patient_guardian_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.patient_guardian_name_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_guardian_field
        )
        patient_guardian_field.send_keys(patient_guardian_name)

    def enter_patient_city(self, patient_city_name):
        patient_city_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.city_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_city_field
        )
        patient_city_field.send_keys(patient_city_name)

    def enter_patient_post_office(self, patient_post_office_name):
        patient_post_office_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.post_office_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_post_office_field
        )
        patient_post_office_field.send_keys(patient_post_office_name)

    def enter_patient_house_number(self, patient_house_number):
        patient_house_number_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.house_number_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_house_number_field
        )
        patient_house_number_field.send_keys(patient_house_number)


    def enter_patient_street(self, patient_street_name):
        patient_street_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.street_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_street_name_field
        )
        patient_street_name_field.send_keys(patient_street_name)

    def enter_patient_pincode(self, patient_pincode):
        patient_street_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.pincode_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_street_name_field
        )
        patient_street_name_field.send_keys(patient_pincode)

    def click_save_btn(self):
        new_registration_save = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.save_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            new_registration_save
        )

        self.driver.execute_script(
            "arguments[0].click();",
            new_registration_save
        )

    def close_print_preview(self):

        WebDriverWait(self.driver, 20).until(
            lambda driver: len(driver.window_handles) > 0
        )

        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def click_close_btn(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.close_btn_xpath)
            )
        ).click()

    def click_home_tab(self):
        home_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.home_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            home_tab
        )

    def enter_search_value(self, value):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.search_xpath)
            )
        )
        search_box.clear()
        search_box.send_keys(value)
        time.sleep(3)
        search_box.send_keys(Keys.ENTER)

    def click_yes_btn(self):
        yes_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Yes']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            yes_btn
        )

    def click_revisit_btn(self):
        revisit_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.revisit_btn)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            revisit_btn
        )

    def click_new_department_revisit_btn(self):
        new_department_revisit = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.new_department_revisit)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            new_department_revisit
        )

    def select_revisit_department(self, department_name):

        dropdowns = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH, self.revisit_department
                )
            )
        )

        dropdown = dropdowns[-1]  # latest/newly added row

        select = Select(dropdown)

        for option in select.options:
            if option.get_attribute("label") == department_name:
                option.click()
                return

        raise Exception(
            f"Department '{department_name}' not found in dropdown"
        )

    def click_revisit_save_btn(self):
        revisit_save_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.patient_revisit_save_btn)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            revisit_save_btn
        )

    def click_opd_module(self):
        opd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.opd_module_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            opd
        )

        self.driver.execute_script(
            "arguments[0].click();",
            opd
        )

    def click_opd_dr_desk(self):
        dr_desk = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.opd_dr_desk_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            dr_desk
        )

    def select_opd_dr_desk_department(self, department_name):

        dropdowns = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH, self.opd_dr_desk_department
                )
            )
        )

        dropdown = dropdowns[-1]  # latest/newly added row

        select = Select(dropdown)

        # Normalize the department we need to find
        expected_department = department_name.strip().casefold()

        self.logger.info(
            f"Looking for OPD Department/Unit: "
            f"'{department_name}'"
        )

        for option in select.options:

            # Actual value is inside the option text
            option_text = option.text.strip()

            self.logger.info(
                f"Checking dropdown option: '{option_text}'"
            )

            # Case-insensitive comparison
            if option_text.casefold() == expected_department:
                self.logger.info(
                    f"OPD Department/Unit matched: "
                    f"'{option_text}'"
                )

                option.click()

                time.sleep(2)

                return

        # Log all available options if no match is found
        available_options = [
            option.text.strip()
            for option in select.options
        ]

        self.logger.error(
            f"Department '{department_name}' not found."
        )

        self.logger.error(
            f"Available departments: {available_options}"
        )

        raise Exception(
            f"Department '{department_name}' not found in dropdown"
        )

    def close_revisit_print_preview(self):

        WebDriverWait(self.driver, 20).until(
            lambda d: len(d.window_handles) == 2
        )

        self.driver.switch_to.window(self.driver.window_handles[-1])

        time.sleep(2)

        pyautogui.press("esc")

        time.sleep(2)

        self.driver.switch_to.window(self.driver.window_handles[0])

    def click_patient_cancellation_option(self):
        patient_cancellation = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.patient_cancellation_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_cancellation
        )

    def click_cancel_proceed_btn(self):
        cancel_proc_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.cancel_process_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            cancel_proc_btn
        )

    def click_cancel_radio_btn(self):
        cancel_radio_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.cancel_radio_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            cancel_radio_btn
        )


    def click_cancellation_radio_btn(self):
        cancel_radio_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='refundOrCancellation' and @value='1']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            cancel_radio_btn
        )

    def enter_cancellation_reason(self, reason):
        cancellation_reason = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.cancel_reason_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            cancellation_reason
        )
        cancellation_reason.send_keys(reason)

    def click_save_cancel_btn(self):
        cancel_save = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.cancel_save_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            cancel_save
        )
        self.driver.execute_script(
        "arguments[0].click();",
        cancel_save
        )

    def enter_search_after_cancel(self, cancel_value):

        search_cancel_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.search_after_cancel))
        )

        self.driver.execute_script("""
            arguments[0].value = '';
            arguments[0].focus();
        """, search_cancel_box)

        search_cancel_box.send_keys(cancel_value)
        search_cancel_box.send_keys(Keys.ENTER)

    def click_refresh_btn(self):
        refresh_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.refresh_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            refresh_btn
        )
        self.driver.execute_script(
        "arguments[0].click();",
        refresh_btn
        )

    def click_unknown_radio_btn(self):
        unknown_radio_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.emergency_unknown_radio_btn)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            unknown_radio_btn
        )

    def enter_identification_mark(self, mark):
        identification_mark = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.identification_1_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            identification_mark
        )
        identification_mark.send_keys(mark)

    def select_brought_by(self, brought_by):
        brought_by_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.brought_by_xpath)
            )
        )

        select = Select(brought_by_dropdown)

        for option in select.options:
            if option.get_attribute("label") == brought_by:
                option.click()
                return

        raise Exception(f"Brought By '{brought_by}' not found in dropdown")

    def enter_brought_by_name(self, brought_name):
        brought_by_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.brought_by_name)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            brought_by_name
        )
        brought_by_name.send_keys(brought_name)

    def enter_brought_by_mobile(self, brought_mobile):
        brought_by_mobile = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.brought_by_phone)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            brought_by_mobile
        )
        brought_by_mobile.send_keys(brought_mobile)

    def enter_brought_by_address(self, brought_address):
        brought_by_address = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.brought_by_address)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            brought_by_address
        )
        brought_by_address.send_keys(brought_address)

    def select_random_visiting_dpt(self, exclude_departments=None):

        if exclude_departments is None:
            exclude_departments = ["PAEDIATRICS" , "OBSTETRICS AND GYNAECOLOGY", "RADIATION ONCOLOGY" , "SURGICAL ONCOLOGY"]

        visiting_department = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.visiting_dpt_xpath))
        )

        select = Select(visiting_department)

        # 🔥 get clean valid options
        valid_options = [
            option for option in select.options
            if option.get_attribute("label")
               and option.get_attribute("label").strip()
               and option.get_attribute("label").strip().upper() != "SELECT"
               and option.get_attribute("label").strip() not in exclude_departments
        ]

        if not valid_options:
            raise Exception("No more unique departments available in dropdown")

        # 🔥 pick random department
        random_option = random.choice(valid_options)

        department_name = random_option.get_attribute("label").strip()

        # 🔥 IMPORTANT FIX: always reset first
        try:
            select.select_by_index(0)  # reset selection
        except:
            pass

        # 🔥 select final department
        select.select_by_value(random_option.get_attribute("value"))

        # 🔥 extra safety (prevents UI multi-selection glitches)
        self.driver.find_element(By.TAG_NAME, "body").click()

        return department_name

    def get_selected_unit(self, max_attempts=20):

        tried_departments = []

        for _ in range(max_attempts):

            dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "deptUnitCode")
                )
            )

            select = Select(dropdown)

            # Wait for units to load
            WebDriverWait(self.driver, 5).until(
                lambda d: len(select.options) > 0
            )

            options = [
                option for option in select.options
                if option.get_attribute("label")
                   and option.get_attribute("label").strip()
                   and option.get_attribute("label").strip().upper() != "SELECT"
            ]

            # If there is already a selected unit
            for option in options:
                if option.is_selected():
                    return option.get_attribute("label").strip()

            # If units exist but none is selected
            if options:
                random_unit = random.choice(options)

                select.select_by_value(
                    random_unit.get_attribute("value")
                )

                return random_unit.get_attribute("label").strip()

            # No units available -> choose another department
            current_department = self.select_random_visiting_dpt(
                exclude_departments=tried_departments
            )

            tried_departments.append(current_department)

            time.sleep(2)

        raise Exception("No department found having at least one unit.")

    def select_opd_dr_desk_unit(self, unit_name):

        unit_name = str(unit_name).strip()

        self.logger.info(
            f"Selecting OPD Doctor Desk Unit: {unit_name!r}"
        )

        # Convert both the requested value and HTML option
        # to uppercase for case-insensitive comparison.
        xpath = (
            "//select[@name='select-option']"
            "/option["
            "translate(normalize-space(text()),"
            "'abcdefghijklmnopqrstuvwxyz',"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ')="
            f"'{unit_name.upper()}'"
            "]"
        )

        self.logger.info(
            f"OPD Unit XPath: {xpath}"
        )

        option = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )

        self.logger.info(
            f"Found OPD Unit option: {option.text!r}"
        )

        # Get the actual value from the matched option
        option_value = option.get_attribute("value")

        self.logger.info(
            f"OPD Unit option value: {option_value!r}"
        )

        # Select using Selenium Select
        dropdown = WebDriverWait(
            self.driver,
            15
        ).until(
            EC.presence_of_element_located(
                (By.NAME, "select-option")
            )
        )

        select = Select(dropdown)

        select.select_by_value(
            option_value
        )

        self.logger.info(
            f"Successfully selected OPD Unit: "
            f"{option.text!r}"
        )

    def get_blob_pdf_text(self):
        """
        Read blob PDF directly from memory
        and return extracted text.
        """

        # Get blob URL
        iframe = self.driver.find_element(
            By.XPATH,
            "//iframe[contains(@src,'blob:')]"
        )

        blob_url = iframe.get_attribute("src")

        print(f"Blob URL: {blob_url}")

        # Convert blob to base64
        pdf_base64 = self.driver.execute_async_script("""
            var blobUrl = arguments[0];
            var callback = arguments[arguments.length - 1];

            fetch(blobUrl)
                .then(response => response.blob())
                .then(blob => {
                    var reader = new FileReader();

                    reader.onloadend = function() {
                        callback(reader.result);
                    };

                    reader.readAsDataURL(blob);
                })
                .catch(error => {
                    callback("ERROR:" + error);
                });
        """, blob_url)

        if str(pdf_base64).startswith("ERROR:"):
            raise Exception(
                f"Failed to fetch PDF blob: {pdf_base64}"
            )

        # Convert base64 to bytes
        base64_data = pdf_base64.split(",")[1]
        pdf_bytes = base64.b64decode(base64_data)

        # Read PDF directly from memory
        pdf_stream = BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)

        pdf_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text

        return pdf_text

    def get_barcode_blob(self):
        """
        Read barcode PDF directly from memory
        and return extracted text.
        """

        # Get blob URL
        iframe = self.driver.find_element(
            By.XPATH,
            "//iframe[contains(@src,'blob:')]"
        )

        blob_url = iframe.get_attribute("src")

        print(f"Blob URL: {blob_url}")

        # Convert blob to base64
        pdf_base64 = self.driver.execute_async_script("""
            var blobUrl = arguments[0];
            var callback = arguments[arguments.length - 1];

            fetch(blobUrl)
                .then(response => response.blob())
                .then(blob => {
                    var reader = new FileReader();

                    reader.onloadend = function() {
                        callback(reader.result);
                    };

                    reader.readAsDataURL(blob);
                })
                .catch(error => {
                    callback("ERROR:" + error);
                });
        """, blob_url)

        if str(pdf_base64).startswith("ERROR:"):
            raise Exception(
                f"Failed to fetch PDF blob: {pdf_base64}"
            )

        # Convert base64 to bytes
        base64_data = pdf_base64.split(",")[1]
        barcode_bytes = base64.b64decode(base64_data)

        # Read PDF directly from memory
        barcode_stream = BytesIO(barcode_bytes)
        reader = PdfReader(barcode_stream)

        barcode_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                barcode_text += text

        return barcode_text

    def click_rx_btn(self):
        rx_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.opd_rx_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            rx_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            rx_btn
        )

    def enter_chief_comp(self,complaint):
        patient_chief_comp_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.chief_complaint_textbox)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_chief_comp_field
        )
        patient_chief_comp_field.send_keys(complaint)
        patient_chief_comp_field.send_keys(Keys.ARROW_DOWN)
        patient_chief_comp_field.send_keys(Keys.ENTER)

    def click_chief_comp_add(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='visitFormOPD']//button[text()='Add']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            add_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            add_btn
        )

    def enter_diagnosis(self, code):
        diagnosis_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.diagnosis_selection_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            diagnosis_field
        )
        diagnosis_field.send_keys(code)
        time.sleep(3)
        diagnosis_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        diagnosis_field.send_keys(Keys.ENTER)
        time.sleep(2)

    def get_diagnosis_name(self):
        diagnosis_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='diagnosisName']")
            )
        ).get_attribute("value")

        return diagnosis_name


    def click_diagnosis_add(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='diagnosisForm']//button[text()='Add']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            add_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            add_btn
        )


    def click_investigation_tab(self):
        investigation_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.investigation_medication_tab_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            investigation_tab
        )
        self.driver.execute_script(
            "arguments[0].click();",
            investigation_tab
        )

    def enter_test_name(self, test):
        test_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.test_name_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            test_name_field
        )
        test_name_field.send_keys(test)
        time.sleep(3)
        test_name_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        test_name_field.send_keys(Keys.ENTER)

    def select_random_test_name(self):

        field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.test_name_xpath)
            )
        )

        # Scroll to the input field
        self.driver.execute_script("""
            const y = arguments[0].getBoundingClientRect().top + window.pageYOffset;
            window.scrollTo({
                top: y - (window.innerHeight / 2),
                behavior: 'instant'
            });
        """, field)

        field.click()

        # Search text
        field.send_keys("CBC")
        time.sleep(2)

        options = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'list-group-item')]"
                )
            )
        )

        print(f"Found {len(options)} options")

        random_option = random.choice(options)

        selected_test = random_option.text.strip()

        print(f"Selected Test: {selected_test}")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            random_option
        )

        time.sleep(1)

        try:
            random_option.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].click();",
                random_option
            )

        return selected_test

    def select_blood_sugar_test_name(self):

        field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.test_name_xpath)
            )
        )

        # Scroll to the input field
        self.driver.execute_script("""
            const y = arguments[0].getBoundingClientRect().top + window.pageYOffset;
            window.scrollTo({
                top: y - (window.innerHeight / 2),
                behavior: 'instant'
            });
        """, field)

        field.click()
        field.clear()

        # Search text
        field.send_keys("blood Sugar")
        time.sleep(2)

        options = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'list-group-item')]"
                )
            )
        )

        print(f"Found {len(options)} options")

        random_option = random.choice(options)

        selected_test = random_option.text.strip()

        print(f"Selected Test: {selected_test}")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            random_option
        )

        time.sleep(1)

        try:
            random_option.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].click();",
                random_option
            )

        return selected_test

    def enter_clinical_indication(self, clinical_indication):
        clinical_indication_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='clinicalIndication']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            clinical_indication_field
        )
        clinical_indication_field.send_keys(clinical_indication)

    def enter_clinical_history(self, clinical_history):
        clinical_history_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-placeholder='Clinical History & Examination']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            clinical_history_field
        )
        clinical_history_field.send_keys(clinical_history)

    def click_test_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='opdInvestigationFormOPD']//button[text()='Add']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            add_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            add_btn
        )

    def enter_drug_name(self, test):
        drug_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.drug_name_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            drug_name_field
        )
        drug_name_field.send_keys(test)
        time.sleep(3)
        drug_name_field.send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        drug_name_field.send_keys(Keys.ENTER)

    def select_random_drug_name(self):

        field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.drug_name_xpath)
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior:'smooth', block:'start'});",
            field
        )

        time.sleep(2)
        field.click()

        field.send_keys("PARACETAMOL TAB 500MG ")

        options = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'list-group-item')]"
                )
            )
        )

        print(f"Found {len(options)} drug options")

        random_option = random.choice(options)

        selected_drug = random_option.text.strip()

        print(f"Selected Drug: {selected_drug}")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            random_option
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            random_option
        )

        return selected_drug

    def select_random_dose(self):
        dose_dropdown = Select(
            self.driver.find_element(By.XPATH, "//select[@name='doseCode']")
        )

        options = [
            option for option in dose_dropdown.options
            if option.get_attribute("value")
        ]

        random_option = random.choice(options)

        dose_name = random_option.get_attribute("textContent").strip().upper()

        random_option.click()

        return dose_name

    def select_random_frequency(self):
        frequency_dropdown = Select(
            self.driver.find_element(By.XPATH, "//select[@name='frequencyCode']")
        )

        options = [
            option for option in frequency_dropdown.options
            if option.get_attribute("value")
        ]

        random_option = random.choice(options)

        frequency_name = random_option.get_attribute("textContent").strip().upper()

        random_option.click()

        return frequency_name

    def enter_instruction(self,instruction):
        instruction_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.drug_instruction_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            instruction_field
        )
        instruction_field.send_keys(instruction)


    def click_drug_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='drugFormOPD']//button[text()='Add']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            add_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            add_btn
        )

    def click_followup_tab(self):
        follow_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.followup_tab_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            follow_tab
        )
        self.driver.execute_script(
            "arguments[0].click();",
            follow_tab
        )

    def enter_followup_days(self,followup_days):
        followup_days_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.rx_revisit_days)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            followup_days_field
        )
        followup_days_field.send_keys(followup_days)


    def get_followup_date(self):
        date_value = self.driver.find_element(
            By.XPATH,
            "//div[contains(@class,'date-picker-stacked')]//input[@placeholder='Select Date']"
        ).get_attribute("value")
        return date_value

    def click_preview_save_btn(self):
        preview_save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='PREVIEW & SAVE']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            preview_save_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            preview_save_btn
        )

    def get_patient_from_pet_reg_details(self):
        data = {}

        # Patient Details
        container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='row row']")
            )
        )

        all_text = container.text

        for line in all_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()


        

        # Diagnosis Details
        diagnosis_elements = self.driver.find_elements(
            By.XPATH,
            "//div[h6[normalize-space()='Diagnosis']]//ol/li"
        )

        data["Diagnosis"] = [
            diagnosis.text.strip()
            for diagnosis in diagnosis_elements
        ]

        # Rx / Drug Details
        rows = self.driver.find_elements(
            By.XPATH,
            "//table[contains(@class,'remove-table-padding')]//tr[position()>1]"
        )

        data["Drugs"] = []

        for row in rows:

            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) >= 6:
                drug_info = {
                    "Drug Name": cols[1].text.strip(),
                    "Frequency": cols[2].text.strip(),
                    "Route": cols[3].text.strip(),
                    "Days": cols[4].text.strip(),
                    "Instruction": cols[5].text.strip()
                }

                data["Drugs"].append(drug_info)

        # Follow-Up Details
        followup_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'heading-with-content') and .//h6[contains(.,'Follow Up')]]"
                )
            )
        )

        followup_text = followup_container.text

        match = re.search(r"\d{2}-[A-Za-z]{3}-\d{4}", followup_text)

        data["Follow Up Date"] = match.group() if match else None

        # Consultant / Resident Name
        try:
            consultant_name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(@class,'signature-content')]//p[1]"
                    )
                )
            ).text.strip()

            data["Consultant Name"] = consultant_name

        except Exception:
            data["Consultant Name"] = None

        return data

    def enter_search_name_in_opd(self, name):

        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )

        self.driver.execute_script("""
            arguments[0].value = '';
            arguments[0].focus();
        """, search_box)
        search_box.clear()
        search_box.send_keys(name)
        time.sleep(3)

    def click_rx_save_btn(self):
        wait = WebDriverWait(self.driver, 10)

        # Wait for Save button
        save_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Save']")
            )
        )

        # Scroll Save button into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            save_btn
        )

        # Click Save
        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

        # Wait for successful save message
        success_msg = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='swal2-html-container' "
                    "and normalize-space()='OPD saved successfully']"
                )
            )
        )

        assert success_msg.is_displayed(), (
            "OPD saved success message was not displayed."
        )

        return True


    def click_3_dots_in_listing_page(self):
        three_dots_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, self.three_dot_in_listing_page)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            three_dots_btn
        )

        ActionChains(self.driver).move_to_element(
            three_dots_btn
        ).perform()

    def hover_click_change_patient_category(self):

        change_patient_cat = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.change_patient_category
                )
            )
        )

        ActionChains(self.driver).move_to_element(change_patient_cat).perform()

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            change_patient_cat
        )

    def select_random_patient_category(self):

        # Wait for the patient category dropdown
        dropdown_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.NAME,
                    "newPatientCategoryCode"
                )
            )
        )

        # Create Selenium Select object
        select = Select(dropdown_element)

        # Select BPL category
        category_name = "BPL"
        category_value = "31"

        self.logger.info(
            f"Selecting patient category: {category_name}"
        )

        self.logger.info(
            f"Category value: {category_value}"
        )

        # Select BPL by value
        select.select_by_value(category_value)

        time.sleep(2)

        self.logger.info(
            f"Patient category selected successfully: "
            f"{category_name}"
        )

        return category_name

    def select_random_approved_by(self):

        dropdown_element = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.approved_by_xpath)
            )
        )
        dropdown_element.click()
        time.sleep(3)
        dropdown = Select(dropdown_element)

        options = dropdown.options[1:]  # skip Select

        random_option = random.choice(options)

        selected_approved_by = random_option.text.strip()

        print(f"Selected approved by: {selected_approved_by}")

        # select using actual option element
        dropdown.select_by_value(
            random_option.get_attribute("value")
        )

        return selected_approved_by


    def click_change_cat_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.change_category_save_btn)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            save_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

    def enter_category_verification(self,verification_id):
        verification_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.category_verification)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            verification_field
        )
        verification_field.send_keys(verification_id)

    def select_random_recommended_by(self):

        dropdown_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.recommended_by_xpath)
            )
        )

        dropdown = Select(dropdown_element)

        options = dropdown.options[1:]

        random_option = random.choice(options)

        selected_name = random_option.text.strip()
        selected_value = random_option.get_attribute("value")

        dropdown.select_by_value(selected_value)

        print(f"Selected Approved By: {selected_name}")

        return selected_name

    def hover_click_duplicate_opd(self):

        duplicate_opd_opt = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.print_duplicate_opd_xpath
                )
            )
        )

        ActionChains(self.driver).move_to_element(duplicate_opd_opt).perform()

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            duplicate_opd_opt
        )

    def click_duplicate_print_btn(self):
        print_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.duplicate_opd_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            print_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            print_btn
        )

    def hover_click_barcode_print(self):

        barcode_opt = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.print_barcode_xpath
                )
            )
        )

        ActionChains(self.driver).move_to_element(barcode_opt).perform()

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            barcode_opt
        )

    def click_barcode_btn(self):
        barcode_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.barcode_btn)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            barcode_button
        )
        self.driver.execute_script(
            "arguments[0].click();",
            barcode_button
        )

    def hover_click_mobile_modification(self):

        mob_mod_opt = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.mobile_number_modification
                )
            )
        )

        ActionChains(self.driver).move_to_element(mob_mod_opt).perform()

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            mob_mod_opt
        )

    def enter_update_mobile_number(self,updated_mobile_number):
        mobile_number_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.mobile_number_field_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            mobile_number_field
        )
        mobile_number_field.clear()
        mobile_number_field.send_keys(updated_mobile_number)

    def click_modify_btn(self):
        modify_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.modify_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            modify_button
        )
        self.driver.execute_script(
            "arguments[0].click();",
            modify_button
        )

    def click_yes_pop_up(self):
        yes_popup_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class,'swal2-confirm') and normalize-space()='Yes']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            yes_popup_button
        )
        self.driver.execute_script(
            "arguments[0].click();",
            yes_popup_button
        )

    def click_brought_dead_radio_btn(self):
        unknown_radio_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@id='isBroughtDead']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            unknown_radio_btn
        )

    def select_random_brought_dead_declared_by(self):

        dropdown_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.brought_dead_declared_by_xpath)
            )
        )

        dropdown = Select(dropdown_element)

        # Skip first Select option
        options = dropdown.options[1:]

        random_option = random.choice(options)

        selected_person = random_option.get_attribute("label")
        selected_value = random_option.get_attribute("value")

        print(f"Selected Person: {selected_person}")
        print(f"Selected Value: {selected_value}")

        # Select using value
        dropdown.select_by_value(selected_value)

        return selected_person


    def click_is_trauma_radio_btn(self):
        is_trauma_radio_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@id='isTrauma']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            is_trauma_radio_btn
        )

    def click_verify_Abha_with_other_modes(self):
        abha_diff_mode_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='CreateOrVerifyByOtherModes']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            abha_diff_mode_btn
        )

    def enter_mob_for_abha_verification(self,mobile_number):
        mobile_number_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Enter Mobile Number']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            mobile_number_field
        )
        mobile_number_field.clear()
        mobile_number_field.send_keys(mobile_number)

    def click_send_otp_btn(self):
        send_otp_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Send OTP']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            send_otp_btn
        )

    def enter_otp(self):

        print("Please enter OTP manually...")

        while True:

            otp_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@class='code-inputs']//input[@class='code-input']")
                )
            )

            try:

                otp_value = ""

                for element in otp_elements:
                    otp_value += element.get_attribute("value")

                if len(otp_value) == 6:
                    print("OTP entered:", otp_value)
                    break

            except Exception:
                pass

            time.sleep(1)

    def click_verify_otp(self):
        verify_otp_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Verify OTP']")
            )
        )

        verify_otp_btn.click()

    def get_patient_all_details(self):

        details_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'row') and .//label[@name='pname']]"
                )
            )
        )

        details_text = details_element.text.strip()

        print("Patient Details:")
        print(details_text)

        return details_text

    def click_add_abha_patient(self):
        add_patient_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Add Patient']")
            )
        )

        add_patient_btn.click()

    def hover_click_patient_detail_modification(self):

        patient_mod_opt = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    self.patient_detail_mod
                )
            )
        )

        ActionChains(self.driver).move_to_element(patient_mod_opt).perform()

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            patient_mod_opt
        )

    def click_patient_audit_trail_option(self):
        patient_audit_trail = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.patient_audit_trail_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_audit_trail
        )

    def enter_crn_number_for_audit(self,value):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='crNo']")
            )
        )
        search_box.send_keys(value)
        time.sleep(3)
        search_box.send_keys(Keys.ENTER)

    def click_verify_Abha(self, abha_address):
        abha_address_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='healthId']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            abha_address_field
        )
        abha_address_field.send_keys(abha_address)

    def click_verify_btn(self):
        abha_verify_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='resetORVerifyBtn']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            abha_verify_btn
        )

    def scroll_table_left(self):

        row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//tbody[@class='ant-table-tbody']//tr[1]"
                )
            )
        )

        self.driver.execute_script("""
            let element = arguments[0];

            let parent = element.parentElement;

            while(parent){
                if(parent.scrollWidth > parent.clientWidth){
                    parent.scrollLeft = 0;
                    break;
                }
                parent = parent.parentElement;
            }
        """, row)

        print("Table moved to left")



    def scroll_table_right(self):

        row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'ant-table-content')]"
                )
            )
        )

        self.driver.execute_script("""
            let element = arguments[0];

            let parent = element.parentElement;

            while(parent){
                if(parent.scrollWidth > parent.clientWidth){
                    parent.scrollLeft = parent.scrollWidth;
                    break;
                }
                parent = parent.parentElement;
            }
        """, row)

        print("Table moved to right")

    def select_random_revisit_dpt(self, exclude_departments=None):

        if exclude_departments is None:
            exclude_departments = [
                "PAEDIATRICS",
                "OBSTETRICS AND GYNAECOLOGY",
                "RADIATION ONCOLOGY",
                "SURGICAL ONCOLOGY"
            ]

        revisit_department = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.visiting_dpt_xpath)
            )
        )

        select = Select(revisit_department)

        # 🔥 get clean valid options
        valid_options = [
            option for option in select.options
            if option.get_attribute("label")
               and option.get_attribute("label").strip()
               and option.get_attribute("label").strip().upper() != "SELECT"
               and option.get_attribute("label").strip() not in exclude_departments
        ]

        if not valid_options:
            raise Exception("No more unique revisit departments available in dropdown")

        # 🔥 pick random department
        random_option = random.choice(valid_options)

        revisit_department_name = random_option.get_attribute("label").strip()

        # 🔥 IMPORTANT FIX: always reset first
        try:
            select.select_by_index(0)
        except:
            pass

        # 🔥 select final department
        select.select_by_value(
            random_option.get_attribute("value")
        )

        # 🔥 extra safety (prevents UI multi-selection glitches)
        self.driver.find_element(By.TAG_NAME, "body").click()

        return revisit_department_name


    def click_adt_module(self):
        adt = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.adt_module_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            adt
        )

        self.driver.execute_script(
            "arguments[0].click();",
            adt
        )

    def click_single_window_option(self):
        patient_single_window = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.single_window_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_single_window
        )

    def click_new_admission_btn(self):
        new_admission = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.new_admission_btn_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            new_admission
        )

        self.driver.execute_script(
            "arguments[0].click();",
            new_admission
        )


    def enter_crn_number_for_adt(self,value):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='crNo']")
            )
        )
        search_box.send_keys(value)
        time.sleep(3)
        search_box.send_keys(Keys.ENTER)

    def select_random_consultant_unit_option(self):

        # click dropdown control
        dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[contains(normalize-space(),'Consultant & Unit')]"
                    "/ancestor::div[contains(@class,'col-lg-3')]"
                    "//div[contains(@class,'searchable-dropdown__control')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(1)

        # click react select box
        dropdown.click()

        time.sleep(1)

        # get real input
        input_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[contains(normalize-space(),'Consultant & Unit')]"
                    "/ancestor::div[contains(@class,'col-lg-3')]"
                    "//input[contains(@class,'searchable-dropdown__input')]"
                )
            )
        )

        # focus input
        self.driver.execute_script(
            "arguments[0].focus();",
            input_box
        )

        time.sleep(1)

        # keyboard selection
        input_box.send_keys(Keys.ARROW_DOWN)
        input_box.send_keys(Keys.ARROW_DOWN)
        input_box.send_keys(Keys.ENTER)




    def select_ward_option(self,ward_name):
        from selenium.webdriver.support.ui import Select

        ward_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='wardCode']")
            )
        )

        select = Select(ward_dropdown)

        select.select_by_visible_text(ward_name)

    def click_adt_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='SAVE']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            save_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )


    def select_the_non_admitted_type(self):
        type_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='type']")
            )
        )

        select = Select(type_dropdown)

        select.select_by_visible_text("Non Acceptance")

    def enter_search_crn_in_ipd(self, crn):

        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mobile/CRN/Name/']"))
        )

        self.driver.execute_script("""
            arguments[0].value = '';
            arguments[0].focus();
        """, search_box)

        search_box.send_keys(crn)
        time.sleep(3)

    def click_patient_action_acceptance(self):
        # 1. Click Patient Action button
        patient_action = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@title='Patient Action']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            patient_action
        )

        patient_action.click()

        # 2. Click Acceptance from dropdown
        acceptance = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//li[@role='menuitem' and .//span[normalize-space()='Acceptance']]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            acceptance
        )

        acceptance.click()

    def select_bed_ipd(self):

        bed_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='bed']")
            )
        )

        select = Select(bed_dropdown)

        # remove Select option
        valid_beds = [
            option for option in select.options
            if option.text.strip()
               and option.text.strip().upper() != "SELECT"
        ]

        if not valid_beds:
            raise Exception("No beds available in dropdown")

        random_bed = random.choice(valid_beds)

        bed_name = random_bed.text.strip()

        select.select_by_value(
            random_bed.get_attribute("value")
        )

        print(
            f"Selected Random Bed: {bed_name}"
        )

        return bed_name

    def click_patient_acceptance_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='SAVE']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            save_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

    def select_ward_with_available_bed(self, exclude_wards=None):

        if exclude_wards is None:
            exclude_wards = []

        ward_dropdown_xpath = "//select[@name='wardCode']"

        checked_wards = []

        while True:

            # ==========================
            # Get Ward Dropdown
            # ==========================

            ward_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, ward_dropdown_xpath)
                )
            )

            select = Select(ward_element)

            # ==========================
            # Get Remaining Wards
            # ==========================

            valid_wards = [
                option for option in select.options
                if option.text.strip()
                   and option.text.strip().upper() != "SELECT"
                   and option.text.strip() not in exclude_wards
                   and option.text.strip() not in checked_wards
            ]

            # ==========================
            # All wards checked
            # ==========================

            if not valid_wards:
                raise Exception(
                    "All wards checked. No available bed found."
                )

            # Random ward

            random_ward = random.choice(valid_wards)

            ward_name = random_ward.text.strip()

            checked_wards.append(ward_name)

            select.select_by_value(
                random_ward.get_attribute("value")
            )

            print(
                f"Checking ward: {ward_name}"
            )

            time.sleep(2)

            # ===================================
            # Ward Full Popup
            # ===================================

            try:

                popup = WebDriverWait(
                    self.driver, 3
                ).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//div[@id='swal2-html-container' and contains(text(),'Ward is Full')]"
                        )
                    )
                )

                print(
                    popup.text
                )

                WebDriverWait(
                    self.driver, 5
                ).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(@class,'swal2-confirm') and normalize-space()='OK']"
                        )
                    )
                ).click()

                time.sleep(2)

                continue



            except TimeoutException:
                pass

            # ===================================
            # Open Bed Status
            # ===================================

            self.driver.find_element(
                By.XPATH,
                "//button[contains(text(),'Bed Status')]"
            ).click()

            time.sleep(3)

            # ===================================
            # Check Available Beds
            # ===================================

            available_beds = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'bed-available')]"
            )

            if available_beds:

                print(
                    f"Available bed found in {ward_name}"
                )

                self.driver.find_element(
                    By.XPATH,
                    "//button[@class='btn-close' and @aria-label='Close']"
                ).click()

                return ward_name



            else:

                print(
                    f"No bed in {ward_name}"
                )

                self.driver.find_element(
                    By.XPATH,
                    "//button[@class='btn-close' and @aria-label='Close']"
                ).click()

                time.sleep(2)

                continue

    def click_ipd_module(self):
        ipd = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.ipd_module_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            ipd
        )

        self.driver.execute_script(
            "arguments[0].click();",
            ipd
        )

    def click_ipd_nursing_option(self):
        ipd_nursing = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.ipd_nursing_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            ipd_nursing
        )

    def click_baby_admission_option(self):
        baby_admission = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.baby_admission_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            baby_admission
        )

    def enter_baby_admission_crn(self,value):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='crNo']"))
        )

        self.driver.execute_script("""
                    arguments[0].value = '';
                    arguments[0].focus();
                """, search_box)

        search_box.send_keys(value)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)


    def enter_baby_gender(self,gender):
        gender_dropdown = Select(
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//select[@name='gender']")
                )
            )
        )

        gender_dropdown.select_by_value(gender)

    def select_dep_ward_random_unit(self):

        unit_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='unitCode']")
            )
        )

        select = Select(unit_dropdown)

        valid_units = [
            option for option in select.options
            if option.text.strip()
               and option.text.strip().upper() != "SELECT"
        ]

        if not valid_units:
            raise Exception("No unit available")

        random_unit = random.choice(valid_units)

        unit_name = random_unit.text.strip()

        select.select_by_value(
            random_unit.get_attribute("value")
        )

        print(
            f"Selected Unit: {unit_name}"
        )

        return unit_name

    def select_random_admit_by(self):

        admit_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='admitByCode']")
            )
        )

        select = Select(admit_dropdown)

        valid_doctors = [
            option for option in select.options
            if option.text.strip()
               and option.text.strip().upper() != "SELECT"
        ]

        if not valid_doctors:
            raise Exception("No doctor available")

        random_doctor = random.choice(valid_doctors)

        doctor_name = random_doctor.text.strip()

        select.select_by_value(
            random_doctor.get_attribute("value")
        )

        print(
            f"Selected Admit By Doctor: {doctor_name}"
        )

        return doctor_name


    def enter_baby_weight(self, weight):
        baby_weight_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='babyWeight']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            baby_weight_field
        )
        baby_weight_field.send_keys(weight)

    def select_baby_ward_room_bed(self, max_attempts=50):

        ward_xpath = "//select[@name='babyWard']"
        room_xpath = "//select[@name='babyRoom']"
        bed_xpath = "//select[@name='babyBed']"

        attempted_wards = []

        for attempt in range(max_attempts):

            print(f"\nAttempt {attempt + 1}")

            # ==========================
            # SELECT RANDOM WARD
            # ==========================

            ward_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, ward_xpath)
                )
            )

            ward_select = Select(ward_element)

            wards = [
                option for option in ward_select.options
                if option.text.strip()
                   and option.text.strip().upper() != "SELECT"
                   and option.text.strip() not in attempted_wards
            ]

            if not wards:
                raise Exception(
                    "No ward available with room and bed"
                )

            random_ward = random.choice(wards)

            ward_name = random_ward.text.strip()

            ward_select.select_by_value(
                random_ward.get_attribute("value")
            )

            print(
                f"Selected Ward : {ward_name}"
            )

            time.sleep(2)

            # ==========================
            # CHECK ROOMS
            # ==========================

            room_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, room_xpath)
                )
            )

            room_select = Select(room_element)

            rooms = [
                option for option in room_select.options
                if option.text.strip()
                   and option.text.strip().upper() != "SELECT"
            ]

            # No room in this ward
            if not rooms:
                print(
                    f"No room available in {ward_name}"
                )

                attempted_wards.append(ward_name)

                continue

            attempted_rooms = []

            # ==========================
            # TRY ROOMS
            # ==========================

            while rooms:

                random_room = random.choice(rooms)

                room_name = random_room.text.strip()

                room_select.select_by_value(
                    random_room.get_attribute("value")
                )

                print(
                    f"Selected Room : {room_name}"
                )

                time.sleep(2)

                # ==========================
                # CHECK BEDS
                # ==========================

                bed_element = WebDriverWait(
                    self.driver, 10
                ).until(
                    EC.presence_of_element_located(
                        (By.XPATH, bed_xpath)
                    )
                )

                bed_select = Select(bed_element)

                beds = [
                    option for option in bed_select.options
                    if option.text.strip()
                       and option.text.strip().upper() != "SELECT"
                ]

                if beds:

                    random_bed = random.choice(beds)

                    bed_name = random_bed.text.strip()

                    bed_select.select_by_value(
                        random_bed.get_attribute("value")
                    )

                    print(
                        "SUCCESS"
                    )

                    print(
                        f"Ward : {ward_name}"
                    )

                    print(
                        f"Room : {room_name}"
                    )

                    print(
                        f"Bed : {bed_name}"
                    )

                    return {
                        "ward": ward_name,
                        "room": room_name,
                        "bed": bed_name
                    }



                else:

                    print(
                        f"No bed in room {room_name}"
                    )

                    attempted_rooms.append(room_name)

                    # remove checked room

                    rooms = [
                        r for r in rooms
                        if r.text.strip() not in attempted_rooms
                    ]

                    # if no rooms left change ward

                    if not rooms:
                        print(
                            f"No beds in any room of {ward_name}"
                        )

                        attempted_wards.append(
                            ward_name
                        )

                        break

        raise Exception(
            "Could not find ward-room-bed combination"
        )

    def select_random_delivery_type(self):

        delivery_type = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='deliveryType']")
            )
        )

        select = Select(delivery_type)

        valid_options = [
            option for option in select.options
            if option.text.strip()
               and option.text.strip().upper() != "SELECT"
        ]

        if not valid_options:
            raise Exception("No delivery type available")

        random_option = random.choice(valid_options)

        delivery_name = random_option.text.strip()

        select.select_by_value(
            random_option.get_attribute("value")
        )

        print(f"Selected Delivery Type: {delivery_name}")

        return delivery_name


    def birth_type(self):
        birth_type = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='birthType']")
            )
        )

        select = Select(birth_type)

        select.select_by_visible_text("One Live Birth")

    def enter_child_disc_number(self, disc_number):
        disc_number_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='discNo']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            disc_number_field
        )
        disc_number_field.send_keys(disc_number)

    def get_baby_name(self):

        baby_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='babyName']")
            )
        )

        baby_name_value = baby_name.get_attribute("value")

        return baby_name_value

    def increase_date_time_by_5_minutes(self):

        date_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@placeholder='Select date']"
                )
            )
        )

        # Scroll element into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            date_field
        )

        time.sleep(1)

        # get current value
        current_value = date_field.get_attribute("value")

        print("Current Date Time:", current_value)

        # convert and add 5 minutes
        current_datetime = datetime.strptime(
            current_value,
            "%d-%b-%Y %H:%M:%S"
        )

        updated_datetime = current_datetime + timedelta(minutes=5)

        updated_value = updated_datetime.strftime(
            "%d-%b-%Y %H:%M:%S"
        )

        print("Updated Date Time:", updated_value)

        # replace value
        date_field.click()

        date_field.send_keys(
            Keys.CONTROL,
            "a"
        )

        date_field.send_keys(updated_value)

        ok_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[span[normalize-space()='OK']]"
                )
            )
        )

        ok_btn.click()

        return updated_value

    def enter_search_baby_name(self, value):

        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.search_xpath
                )
            )
        )

        # click using JS
        self.driver.execute_script(
            "arguments[0].click();",
            search_box
        )

        time.sleep(1)

        # clear existing value
        search_box.clear()

        # enter value
        search_box.send_keys(value)

        time.sleep(3)

        # press enter
        search_box.send_keys(Keys.ENTER)

    def select_random_department_with_unit(self):

        skip_departments = [
            "PAEDIATRICS",
            "PAEDIATRIC SURGERY"
        ]

        department_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//select[@name='department']")
            )
        )

        department_select = Select(department_dropdown)

        departments = department_select.options[1:]

        random.shuffle(departments)

        for department in departments:

            department_name = department.get_attribute("label").strip()
            department_value = department.get_attribute("value")

            if department_name in skip_departments:
                continue

            department_select.select_by_value(
                department_value
            )

            print(f"Trying Department: {department_name}")

            time.sleep(3)

            unit_dropdown = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//select[@name='visitUnitCode']")
                )
            )

            unit_select = Select(unit_dropdown)

            available_units = [
                unit for unit in unit_select.options
                if unit.text.strip().upper() != "SELECT UNIT"
            ]

            if not available_units:
                print(f"No unit found for {department_name}")
                continue

            selected_unit = unit_select.first_selected_option.text.strip()

            # Already selected unit
            if selected_unit.upper() != "SELECT UNIT":
                print(
                    f"Preselected Unit: {selected_unit}"
                )

                department_unit = (
                    f"{department_name}"
                    f"({selected_unit})"
                )

                print(
                    f"Department With Unit: {department_unit}"
                )

                return department_unit

            # Select random unit
            random_unit = random.choice(
                available_units
            )

            unit_select.select_by_value(
                random_unit.get_attribute("value")
            )

            selected_unit = random_unit.text.strip()

            print(
                f"Selected Unit: {selected_unit}"
            )

            department_unit = (
                f"{department_name}"
                f"({selected_unit})"
            )

            print(
                f"Department With Unit: {department_unit}"
            )

            return department_unit

        raise Exception(
            "No department found with valid unit"
        )


    def enter_update_patient_name(self, patient_name):
        patient_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, self.patient_name_id)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_name_field
        )
        patient_name_field.send_keys(patient_name)


    def click_new_baby_admission_btn(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class,'btn-primary') and normalize-space()='New Born Baby Admission']"
                )
            )
        ).click()

    def select_department_until_save_success(self):

        tried_departments = set()

        while True:

            department_unit = self.select_random_department_with_unit(
            )

            tried_departments.add(
                department_unit.split("(")[0]
            )

            self.click_revisit_save_btn()

            try:
                WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//div[@id='swal2-html-container' and contains(.,'Please configure charge for this Category.')]"
                        )
                    )
                )

                self.driver.find_element(
                    By.XPATH,
                    "//button[contains(@class,'swal2-confirm')]"
                ).click()

                continue

            except TimeoutException:
                return department_unit



    def click_patient_revisit_option(self):
        patient_revisit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "Patient Revisit")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_revisit
        )

    def select_payment_mode_if_required(self):

        payment_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//select[@name='paymentModeCode']"
                )
            )
        )

        # Scroll dropdown into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            payment_dropdown
        )

        select = Select(payment_dropdown)

        selected_option = select.first_selected_option.text.strip()

        if selected_option.upper() != "SELECT":
            print(f"Payment Mode already selected: {selected_option}")
            return selected_option

        available_modes = [
            option
            for option in select.options
            if option.text.strip().upper() != "SELECT"
        ]

        if not available_modes:
            raise Exception("No payment modes available.")

        random_mode = random.choice(available_modes)

        # Select using value instead of visible text
        select.select_by_value(
            random_mode.get_attribute("value")
        )

        print(f"Selected Payment Mode: {random_mode.text.strip()}")

        return random_mode.text.strip()

    def get_patient_details_from_search_result(self, crn):
        """
        Extract patient name and mobile number from the first search-result
        row matching the supplied CRN.
        """

        row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//tr[@data-row-key='{crn}']"
                )
            )
        )

        # Patient name = second TD
        patient_name = row.find_element(
            By.XPATH,
            "./td[2]/span"
        ).text.strip()

        # Mobile number = tenth TD
        mobile_number = row.find_element(
            By.XPATH,
            "./td[10]/span"
        ).text.strip()

        return patient_name, mobile_number

    def select_admission_type_in_adt(self):

        dropdown = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//select[@name='statusAtAdmission']"
                )
            )
        )

        select = Select(dropdown)

        options = select.options

        # Ignore "Select" option
        valid_options = [
            option for option in options
            if option.get_attribute("value")
        ]

        selected_option = random.choice(valid_options)

        select.select_by_value(
            selected_option.get_attribute("value")
        )

        selected_text = selected_option.text.strip()

        self.logger.info(
            f"Admission Type selected: {selected_text}"
        )

        return selected_text

    def select_unit_and_ward_with_available_bed(self):
        """
        Initial department is kept as-is because it is already pre-selected.

        Flow:
            Existing Department
                ↓
            Random Consultant & Unit
                ↓
            Check all wards
                ↓
            Bed found → return
                ↓
            No bed in department
                ↓
            Change Department
                ↓
            Random Consultant & Unit
                ↓
            Check wards
                ↓
            Repeat
        """

        dept_dropdown_xpath = "//select[@name='deptCode']"

        checked_departments = []

        while True:

            # ==========================================================
            # CURRENT DEPARTMENT
            # ==========================================================

            dept_element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH, dept_dropdown_xpath)
                )
            )

            dept_select = Select(dept_element)

            current_department = (
                dept_select.first_selected_option.text.strip()
            )

            self.logger.info(
                f"Current department: {current_department}"
            )

            # Avoid checking same department again
            if current_department not in checked_departments:
                checked_departments.append(
                    current_department
                )

            # ==========================================================
            # SELECT CONSULTANT & UNIT
            # ==========================================================

            self.logger.info(
                f"Selecting Consultant & Unit for department: "
                f"{current_department}"
            )

            self.select_random_consultant_unit_option()

            time.sleep(2)

            # ==========================================================
            # CHECK WARDS
            # ==========================================================

            try:

                ward_name = (
                    self.select_ward_with_available_bed()
                )

                self.logger.info(
                    f"Available bed found | "
                    f"Department: {current_department} | "
                    f"Ward: {ward_name}"
                )

                return {
                    "department": current_department,
                    "ward": ward_name
                }

            except Exception as e:

                self.logger.warning(
                    f"No available bed found in department: "
                    f"{current_department}"
                )

            # ==========================================================
            # FIND ANOTHER DEPARTMENT
            # ==========================================================

            dept_element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH, dept_dropdown_xpath)
                )
            )

            dept_select = Select(dept_element)

            available_departments = [
                option
                for option in dept_select.options
                if option.get_attribute("value")
                   and option.text.strip()
                   and option.text.strip().upper() != "SELECT"
                   and option.text.strip()
                   not in checked_departments
            ]

            # ==========================================================
            # NO DEPARTMENTS LEFT
            # ==========================================================

            if not available_departments:
                raise Exception(
                    "No department has an available bed. "
                    f"Departments checked: {checked_departments}"
                )

            # ==========================================================
            # SELECT NEW DEPARTMENT
            # ==========================================================

            random_department = random.choice(
                available_departments
            )

            new_department = (
                random_department.text.strip()
            )

            self.logger.warning(
                f"No bed available in '{current_department}'. "
                f"Changing department to '{new_department}'"
            )

            dept_select.select_by_value(
                random_department.get_attribute("value")
            )

            time.sleep(3)

            self.logger.info(
                f"New department selected: {new_department}"
            )

    def enter_patient_2_city(self, patient_city_name):
        patient_city_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='city']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_city_field
        )
        patient_city_field.send_keys(patient_city_name)

    def click_all_print_buttons(self):
        wait = WebDriverWait(self.driver, 20)

        print_xpath = (
            "//tr[contains(@class,'ant-table-row')]"
        "/td[contains(@class,'ant-table-cell-fix-right')]"
        "//span[contains(@class,'cursor-pointer')]"
        )

        # Wait until at least one print button exists
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, print_xpath)
            )
        )

        # Get number of actual table rows
        rows = self.driver.find_elements(
            By.XPATH,
            "//tbody[contains(@class,'ant-table-tbody')]/tr[contains(@class,'ant-table-row') and not(contains(@class,'ant-table-measure-row'))]"
        )

        print(f"Total rows found: {len(rows)}")

        for index in range(len(rows)):

            try:
                print(f"Clicking Print button {index + 1}")

                # Re-find print buttons every time
                print_buttons = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, print_xpath)
                    )
                )

                print(f"Print buttons currently found: {len(print_buttons)}")

                # Re-check index because DOM may have changed
                if index >= len(print_buttons):
                    print(f"Print button {index + 1} not found.")
                    continue

                print_button = print_buttons[index]

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    print_button
                )

                wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"({print_xpath})[{index + 1}]")
                    )
                )

                print_button.click()

                print(f"Print button {index + 1} clicked.")

                # Wait for PDF / print popup
                close_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Close']")
                    )
                )

                print("PDF opened.")

                time.sleep(3)

                close_button.click()

                print("PDF closed.")

                time.sleep(1)

            except Exception as e:
                print(f"Failed on print button {index + 1}: {e}")



    def click_quick_patient_modification_option(self):
        patient_registration = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Quick Patient Detail Modification']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patient_registration
        )

    def select_cash_payment_mode_cancel(self):

        payment_dropdown = Select(
            self.driver.find_element(
                By.XPATH,
                "//select[@name='paymentMode']"
            )
        )

        payment_dropdown.select_by_value("1")





















    


































































