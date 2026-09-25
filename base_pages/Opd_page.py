import re
import base64
from io import BytesIO
from datetime import datetime, timedelta
from selenium.common import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
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



class Opd_Page:


    def __init__(self, driver):
        self.driver = driver

    def get_visible_select(self, name):
        wait = WebDriverWait(self.driver, 20)

        def visible_element(driver):
            elements = driver.find_elements(By.NAME, name)

            for element in elements:
                if element.is_displayed():
                    return element

            return False

        return wait.until(visible_element)


    


    def select_chief_complaint_side(self):
        dropdown = Select(
            self.driver.find_element(
                By.XPATH,
                "//select[@name='sideCode']"
            )
        )

        options = [
            option for option in dropdown.options
            if option.text.strip().upper() != "SIDE"
        ]

        random_option = random.choice(options)
        dropdown.select_by_visible_text(random_option.text.strip())


    def enter_chief_complaint_number_days(self, days):
        comp_days = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='noOfDays']"))
        )
        comp_days.clear()
        comp_days.send_keys(days)


    def select_chief_complaint_time(self):
        dropdown = Select(
            self.driver.find_element(
                By.XPATH,
                "//select[@name='durationCode']"
            )
        )

        dropdown.select_by_visible_text("Day/s")

    def enter_chief_complaint_remarks(self, remarks):
        remark_text = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='remarks']"))
        )
        remark_text.clear()
        remark_text.send_keys(remarks)

    def enter_history_of_illness(self, illness):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@contenteditable='true' and contains(@class,'editable-content-comp')]"
                )
            )
        )

        # Scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        # JS click
        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        # Clear existing text (if any)
        self.driver.execute_script("arguments[0].innerHTML = '';", element)

        # Enter new text
        element.send_keys(illness)

    def click_vital(self):
        element_vital = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Modify vital/ GE']"
                )
            )
        )
        element_vital.click()

    def enter_weight(self, value):
        weight = self.driver.find_element(
            By.XPATH,
            "//input[@name='weight']"
        )
        weight.clear()
        weight.send_keys(value)

    def enter_height(self, value):
        height= self.driver.find_element(
            By.XPATH,
            "//input[@name='height']"
        )
        height.clear()
        height.send_keys(value)


    def enter_temperature(self, value):
        temperature= self.driver.find_element(
            By.XPATH,
            "//input[@name='temperature']"
        )
        temperature.clear()
        temperature.send_keys(value)

    def enter_resp_rate(self, value):
        resp_rate = self.driver.find_element(
            By.XPATH,
            "//input[@name='respRate']"
        )
        resp_rate.clear()
        resp_rate.send_keys(value)

    def enter_pulse_rate(self, value):
        pulse_rate = self.driver.find_element(
            By.XPATH,
            "//input[@name='pulseRate']"
        )
        pulse_rate.clear()
        pulse_rate.send_keys(value)

    def enter_systolic(self, value):
        systolic = self.driver.find_element(
            By.XPATH,
            "//input[@name='systolic']"
        )
        systolic.clear()
        systolic.send_keys(value)

    def enter_diastolic(self, value):
        diastolic = self.driver.find_element(
            By.XPATH,
            "//input[@name='diastolic']"
        )
        diastolic.clear()
        diastolic.send_keys(value)

    def enter_fasting(self, value):
        self.driver.find_element(
            By.XPATH,
            "//input[@name='fasting']"
        ).send_keys(value)

    def enter_pp(self, value):
        self.driver.find_element(
            By.XPATH,
            "//input[@name='pp']"
        ).send_keys(value)

    def enter_hba1c(self, value):
        self.driver.find_element(
            By.XPATH,
            "//input[@name='hba1c']"
        ).send_keys(value)

    def enter_rbs(self, value):
        self.driver.find_element(
            By.XPATH,
            "//input[@name='rbs']"
        ).send_keys(value)

    def enter_haemoglobin(self, value):
        haemoglobin = self.driver.find_element(
            By.XPATH,
            "//input[@name='haemoglobin']"
        )
        haemoglobin.clear()
        haemoglobin.send_keys(value)

    def enter_spo2(self, value):

        spo2 = self.driver.find_element(
            By.XPATH,
            "//input[@name='spo2']"
        )
        spo2.clear()
        spo2.send_keys(value)

    def click_vital_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Save']")
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

    def click_complete_history(self):
        complete_history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Complete History']")
            )
        )
        complete_history.click()


    def enter_past_history(self,value):
        past_history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='pastHistory']")
            )
        )
        past_history.clear()
        past_history.send_keys(value)

    def enter_personal_history(self,value):
        personal_history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='personalHistory']")
            )
        )
        personal_history.clear()
        personal_history.send_keys(value)

    def enter_family_history(self,value):
        family_history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='familyHistory']")
            )
        )
        family_history.clear()
        family_history.send_keys(value)

    def enter_treatment_history(self,value):
        treatment_history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='treatmentHistory']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            treatment_history
        )
        treatment_history.clear()
        treatment_history.send_keys(value)

    def enter_surgical_history(self,value):
        surgical_history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='surgicalHistory']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            surgical_history
        )
        surgical_history.clear()
        surgical_history.send_keys(value)

    def enter_occupational_history(self,value):
        occupational_history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='occupationalHistory']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            occupational_history
        )
        occupational_history.clear()
        occupational_history.send_keys(value)

    def click_examination(self):
        examination = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Examination']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            examination
        )
        self.driver.execute_script(
            "arguments[0].click();",
            examination
        )

    def enter_general_exam(self,value):
        general_exam = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='otherExam']")
            )
        )
        general_exam.clear()
        general_exam.send_keys(value)

    def enter_cvs(self,value):
        cvs = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='cvs']")
            )
        )
        cvs.clear()
        cvs.send_keys(value)

    def enter_cns(self,value):
        cns = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='cns']")
            )
        )
        cns.clear()
        cns.send_keys(value)

    def enter_pa(self, value):
        pa = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='pa']")
            )
        )
        pa.clear()
        pa.send_keys(value)

    def enter_muscular_exam(self, value):
        muscularExam = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='muscularExam']")
            )
        )
        muscularExam.clear()
        muscularExam.send_keys(value)

    def enter_local_exam(self, value):
        localExam = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='localExam']")
            )
        )
        localExam.clear()
        localExam.send_keys(value)

    def enter_painAssessment(self, value):
        painAssessment = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='painAssessment']")
            )
        )
        painAssessment.clear()
        painAssessment.send_keys(value)

    def enter_respiratorySystem(self, value):
        respiratorySystem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='respiratorySystem']")
            )
        )
        respiratorySystem.clear()
        respiratorySystem.send_keys(value)


    def click_chronic_disease(self):
        chronic_disease = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Chronic Disease']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            chronic_disease
        )
        self.driver.execute_script(
            "arguments[0].click();",
            chronic_disease
        )


    def enter_chronic_disease_name(self,value):
        disease = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='diseaseId']")
            )
        )
        disease.clear()
        disease.send_keys(value)
        disease.send_keys(Keys.ARROW_DOWN)
        disease.send_keys(Keys.ENTER)
        time.sleep(2)

    def enter_disease_duration(self,value):
        duration = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='diseaseDuration']")
            )
        )
        duration.clear()
        duration.send_keys(value)

    def enter_disease_remarks(self,value):
        remarks = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@name='diseaseRemarks']")
            )
        )
        remarks.clear()
        remarks.send_keys(value)

    def click_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='cronicForm-opd']//button[normalize-space()='Add']")
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

    def select_diagnosis_side(self):
        dropdown = Select(
            self.driver.find_element(
                By.XPATH,
                "//select[@name='diagnosisSideCode']"
            )
        )

        options = [
            option for option in dropdown.options
            if option.text.strip().upper() != "SIDE"
        ]

        random_option = random.choice(options)
        dropdown.select_by_visible_text(random_option.text.strip())


    def enter_diagnosis_remarks(self,value):
        remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='diagnosisRemarks']")
            )
        )
        remarks.clear()
        remarks.send_keys(value)


    def click_icd_btn(self):
        icd_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@role='switch' and @aria-checked='true']")
            )
        )
        icd_btn.click()

    def click_diagnosis_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='snomedDiagnosisForm']//button[normalize-space()='Add']")
            )
        )
        add_btn.click()


    def click_other_diagnosis(self):
        other_diagnosis = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Other Diagnosis']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            other_diagnosis
        )
        self.driver.execute_script(
            "arguments[0].click();",
            other_diagnosis
        )


    def enter_other_diagnosis_details(self,value):
        details = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='otherDiagnosisDetails']")
            )
        )
        details.clear()
        details.send_keys(value)

    def click_other_diagnosis_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class,'btn-add')]")
            )
        )
        add_btn.click()

    def click_confidential_info(self):
        confidential_info = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Confidential Info']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            confidential_info
        )
        self.driver.execute_script(
            "arguments[0].click();",
            confidential_info
        )

    def enter_other_confidential_details(self,value):
        details = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='otherConfidentialDetails']")
            )
        )
        details.clear()
        details.send_keys(value)

    def click_diagnosis_note(self):
        diagnosis_note = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Diagnosis Note']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            diagnosis_note
        )
        self.driver.execute_script(
            "arguments[0].click();",
            diagnosis_note
        )

    def enter_other_diagnosis_note(self,value):
        note = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='otherDiagnosisNote']")
            )
        )
        note.clear()
        note.send_keys(value)


    def click_renal_function_test(self):
        renal_test = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='RENAL PROFILE / RFT']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            renal_test
        )
        self.driver.execute_script(
            "arguments[0].click();",
            renal_test
        )

    def select_all_investigation_tests(self):
        test_names = []

        checkboxes = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[@id='scrollableDiv']//input[@type='checkbox']"
                )
            )
        )

        for checkbox in checkboxes:

            # Get the investigation/test name associated with this checkbox
            test_name = checkbox.find_element(
                By.XPATH,
                "./following-sibling::label//label[contains(@class,'form-label')]"
            ).text.strip()

            test_names.append(test_name)

            # Click only if it is not already selected
            if not checkbox.is_selected():
                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox
                )

        print("Selected Investigation Tests:", test_names)

        return test_names


    def enter_examination_finding(self,value):
        examination_finding = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@contenteditable='true' and @data-placeholder='Relevent Clinical History & Examination Findings']")
            )
        )
        examination_finding.clear()
        examination_finding.send_keys(value)


    def enter_renal_test_remark(self,value):
        renal_test_remark = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                    (By.XPATH, "//textarea[@name='sideRemarkPopup']")
            )
        )
        renal_test_remark.clear()
        renal_test_remark.send_keys(value)

    def click_renal_test_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='ADD']")
            )
        )
        add_btn.click()


    def click_investigation_note(self):
        investigation_note = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Investigation Note']")
            )
        )
        investigation_note.click()

    def enter_investigation_note(self,value):
        diagnosis_note = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='otherDiagnosisNote']")
            )
        )
        # Scroll to the element
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            diagnosis_note
        )

        self.driver.execute_script(
            "arguments[0].click();",
            diagnosis_note
        )
        diagnosis_note.clear()
        diagnosis_note.send_keys(value)

    def enter_drug_strength(self,value):
        strength = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name = 'doseName']")
            )
        )
        strength.clear()
        strength.click()
        strength.send_keys(value)

    def click_titration_btn(self):
        titration = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class,'btn-view')]")
            )
        )
        titration.click()

    def enter_titration_strength(self,value):
        strength = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='strength']")
            )
        )
        strength.clear()
        strength.click()
        strength.send_keys(value)


    def enter_titration_dose(self,value):
        m_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//form[@name='splInvFieldsFormOPD']//span[label[normalize-space()='M']]/input"
                )
            )
        )
        m_input.clear()
        m_input.send_keys(value)

        e_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//form[@name='splInvFieldsFormOPD']//span[label[normalize-space()='E']]/input"
                )
            )
        )
        e_input.clear()
        e_input.send_keys(value)

    def enter_titration_days(self,value):
        days = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='afterDays']")
            )
        )
        days.clear()
        days.click()
        days.send_keys(value)

    def enter_titration_remark(self,value):
        titration_remark = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='remark']")
            )
        )
        titration_remark.clear()
        titration_remark.send_keys(value)

    def click_titration_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='splInvFieldsFormOPD']//button[normalize-space()='Add']")
            )
        )
        add_btn.click()


    def click_titration_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='SAVE']")
            )
        )
        save_btn.click()

    def click_non_listed_drug_view(self):
        non_listed_drug = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Non-Listed Drugs/Consumables']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            non_listed_drug
        )


    def click_non_listed_drug(self):
        non_listed_drug = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Non-Listed Drugs/Consumables']")
            )
        )
        non_listed_drug.click()

    def enter_external_drug(self,value):
        name = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@name='externalDrugFormOPD']//input[@name='drugName']")
            )
        )
        name.clear()
        name.click()
        name.send_keys(value)

    def enter_external_strength(self,value):
        strength = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@name='externalDrugFormOPD']//input[@name='doseName']")
            )
        )
        strength.clear()
        strength.click()
        strength.send_keys(value)



    def enter_external_dose(self, value):
        m_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//form[@name='externalDrugFormOPD']//span[label[normalize-space()='M']]/input"
                )
            )
        )
        m_input.clear()
        m_input.send_keys(value)

        e_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//form[@name='externalDrugFormOPD']//span[label[normalize-space()='E']]/input"
                )
            )
        )
        e_input.clear()
        e_input.send_keys(value)

    def enter_external_instruction(self,value):
        titration_remark = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@name='externalDrugFormOPD']//input[@name='drugInstruction']")
            )
        )
        titration_remark.clear()
        titration_remark.send_keys(value)

    def click_external_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='externalDrugFormOPD']//button[normalize-space()='Add']")
            )
        )
        add_btn.click()

    def click_treatment_note(self):
        treatment_note = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Treatment Note']")
            )
        )
        treatment_note.click()

    def enter_treatment_note_remarks(self, value):
        treatment_note_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@data-placeholder,'Drugs should not be prescribed')]")
            )
        )
        treatment_note_remarks.clear()
        treatment_note_remarks.send_keys(value)

    def click_allergies(self):
        Allergies = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class,'addMoreBtn') and normalize-space()='Allergies']")
            )
        )
        Allergies.click()

    def enter_allergy_code(self, value):
        treatment_note_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@name='allergyFormOPD']//input[@name='allergyNameCode']")
            )
        )
        treatment_note_remarks.clear()
        treatment_note_remarks.send_keys(value)
        time.sleep(2)
        treatment_note_remarks.send_keys(Keys.ARROW_DOWN)
        treatment_note_remarks.send_keys(Keys.ENTER)

    def select_sensitivity_type(self):
        dropdown = Select(
            self.driver.find_element(
                By.XPATH,
                "//select[@name='sensitivityCode']"
            )
        )

        options = [
            option for option in dropdown.options
            if option.get_attribute("value") != ""
        ]

        random_option = random.choice(options)
        dropdown.select_by_visible_text(random_option.text.strip())

    def enter_allergy_days(self, value):
        allergy_days = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='durationTime']")
            )
        )
        allergy_days.clear()
        allergy_days.send_keys(value)

    def enter_allergy_site(self, value):
        allergy_site = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='allergySiteCode']")
            )
        )
        allergy_site.clear()
        allergy_site.send_keys(value)

    def enter_allergy_symptoms(self, value):
        allergy_symptoms = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='allergySymptomsCode']")
            )
        )
        allergy_symptoms.clear()
        allergy_symptoms.send_keys(value)

    def click_allergy_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='allergyFormOPD']//button[@type='button' and normalize-space()='Add']")
            )
        )
        add_btn.click()

    def enter_allergy_remarks(self, value):
        allergy_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='allergyRemarks']")
            )
        )
        allergy_remarks.clear()
        allergy_remarks.send_keys(value)

    def enter_other_allergy_remarks(self, value):
        other_allergy_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='otherAllergy']")
            )
        )
        other_allergy_remarks.clear()
        other_allergy_remarks.send_keys(value)

    def click_procedure_tab(self):
        procedure_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h6[normalize-space()='Procedure, OT & Admission Advice']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            procedure_tab
        )
        self.driver.execute_script(
            "arguments[0].click();",
            procedure_tab
        )

    def select_service_and_procedure(self):

        # ============================================================
        # SELECT SERVICE AREA
        # ============================================================

        service_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='serviceAreaCode']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            service_element
        )

        service_dropdown = Select(service_element)

        service_name = "BURN"

        service_dropdown.select_by_visible_text(service_name)

        print(f"Selected Service : {service_name}")

        # ============================================================
        # WAIT FOR PROCEDURE DROPDOWN
        # ============================================================

        procedure_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//select[@name='procedureCode']"
                )
            )
        )

        procedure_dropdown = Select(procedure_element)

        # ============================================================
        # CHECK WHETHER PROCEDURE EXISTS
        # ============================================================

        procedure_options = procedure_dropdown.options

        # Remove placeholder / empty options
        valid_procedure_options = [
            option for option in procedure_options
            if option.get_attribute("value").strip() != ""
               and option.text.strip() != ""
        ]

        # ============================================================
        # NO PROCEDURE AVAILABLE
        # ============================================================

        if not valid_procedure_options:
            print(
                f"No procedure available for service area: {service_name}"
            )



            return None

        # ============================================================
        # WAIT UNTIL PROCEDURE GETS A VALUE
        # ============================================================

        try:

            WebDriverWait(self.driver, 10).until(
                lambda driver: (
                        Select(
                            driver.find_element(
                                By.XPATH,
                                "//select[@name='procedureCode']"
                            )
                        ).first_selected_option
                        .get_attribute("value")
                        .strip()
                        != ""
                )
            )

        except TimeoutException:



            return None

        # ============================================================
        # GET SELECTED PROCEDURE
        # ============================================================

        selected_procedure = procedure_dropdown.first_selected_option

        procedure_name = selected_procedure.text.strip()

        # Extra safety check
        if not procedure_name:


            return None

        print(
            f"Procedure Auto Selected : {procedure_name}"
        )

        # ============================================================
        # RETURN SERVICE + PROCEDURE
        # ============================================================

        return (
            service_name,
            procedure_name
        )

    def select_procedure_side(self):
        dropdown = Select(
            self.driver.find_element(
                By.XPATH,
                "//select[@name='procedureSideCode']"
            )
        )

        options = [
            option for option in dropdown.options
            if option.text.strip().upper() != "SIDE"
        ]

        random_option = random.choice(options)
        dropdown.select_by_visible_text(random_option.text.strip())

    def enter_procedure_remarks(self,value):
        other_allergy_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='procedureSideRemarks']")
            )
        )
        other_allergy_remarks.clear()
        other_allergy_remarks.send_keys(value)

    def click_procedure_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='procedureForm']//button[contains(@class,'btn-add')]")
            )
        )
        add_btn.click()

    def select_proposed_anesthesia_type(self):
        anesthesia = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//select[@name='anesthesiaCode']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            anesthesia
        )

        WebDriverWait(self.driver, 5).until(
            lambda d: anesthesia.is_displayed() and anesthesia.is_enabled()
        )

        Select(anesthesia).select_by_index(1)  # or select_by_visible_text(...)

    def select_proposed_operation_type(self):
        operation_type = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//select[@name='operationTypeCode']"
            ))
        )

        # Scroll to center
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            operation_type
        )

        # JS click
        self.driver.execute_script(
            "arguments[0].click();",
            operation_type
        )

        Select(operation_type).select_by_visible_text("MAJOR")

    def select_procedure_operation_name(self):
        wait = WebDriverWait(self.driver, 20)

        # --------------------------------------------------
        # 1. Open Operation Name dropdown
        # --------------------------------------------------
        operation_control = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//label[normalize-space()='Operation Name']"
                    "/following-sibling::div"
                    "//div[contains(@class,'searchable-dropdown__control')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior:'instant', block:'center'});",
            operation_control
        )

        time.sleep(0.5)

        self.driver.execute_script(
            "arguments[0].click();",
            operation_control
        )

        # --------------------------------------------------
        # 2. Locate input
        # --------------------------------------------------
        operation_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//label[normalize-space()='Operation Name']"
                    "/following-sibling::div"
                    "//input[@role='combobox']"
                )
            )
        )

        # --------------------------------------------------
        # 3. Wait for options
        # --------------------------------------------------
        option_xpath = (
            "//div[contains(@class,'searchable-dropdown__option')]"
        )

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, option_xpath)
            )
        )

        # --------------------------------------------------
        # 4. Get TEXT only
        # --------------------------------------------------
        option_elements = self.driver.find_elements(
            By.XPATH,
            option_xpath
        )

        option_texts = []

        for option in option_elements:
            try:
                text = option.get_attribute("textContent").strip()

                if (
                        text
                        and text.upper() != "SELECT"
                        and text not in option_texts
                ):
                    option_texts.append(text)

            except StaleElementReferenceException:
                # React refreshed the dropdown.
                # Skip this stale element.
                continue

        print(f"Total Operation options: {len(option_texts)}")
        print(f"Available Operations: {option_texts}")

        # --------------------------------------------------
        # 5. No options
        # --------------------------------------------------
        if not option_texts:
            print("No Operation Name available.")
            operation_input.send_keys(Keys.ESCAPE)
            return None

        # --------------------------------------------------
        # 6. Select random operation NAME
        # --------------------------------------------------
        selected_operation = random.choice(option_texts)

        print(f"Selected Operation: {selected_operation}")

        # --------------------------------------------------
        # 7. Search selected operation
        # --------------------------------------------------
        operation_input.click()
        operation_input.clear()
        operation_input.send_keys(selected_operation)

        # --------------------------------------------------
        # 8. Find the option AGAIN
        # --------------------------------------------------
        searched_option_xpath = (
            "//div[contains(@class,'searchable-dropdown__option')"
            " and normalize-space(.)="
            f"'{selected_operation}']"
        )

        searched_option = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, searched_option_xpath)
            )
        )

        print(
            f"Option found: {searched_option.text.strip()}"
        )

        # --------------------------------------------------
        # 9. Scroll selected option
        # --------------------------------------------------
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior:'instant', block:'center'});",
            searched_option
        )

        time.sleep(0.5)

        # --------------------------------------------------
        # 10. Click the NEW element
        # --------------------------------------------------
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, searched_option_xpath)
            )
        )

        searched_option = self.driver.find_element(
            By.XPATH,
            searched_option_xpath
        )

        self.driver.execute_script(
            "arguments[0].click();",
            searched_option
        )

        # --------------------------------------------------
        # 11. Verify
        # --------------------------------------------------
        wait.until(
            lambda d: (
                              d.find_element(
                                  By.XPATH,
                                  "//label[normalize-space()='Operation Name']"
                                  "/following-sibling::div"
                                  "//input[@role='combobox']"
                              ).get_attribute("value") or ""
                      ).strip() == selected_operation
        )

        print(
            f"Operation selected successfully: "
            f"{selected_operation}"
        )

        return selected_operation


    def enter_operation_remarks(self, value):
        other_allergy_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//textarea[@name='otherOTDesc']")
            )
        )
        other_allergy_remarks.clear()
        other_allergy_remarks.send_keys(value)

    def click_operation_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='pacRequisitionForm']//button[normalize-space()='Add']")
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



    def select_admission_details(self):

        wait = WebDriverWait(self.driver, 20)

        # Get visible Department dropdown
        dept = self.get_visible_select("deptCode")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dept
        )

        department_select = Select(dept)

        # Skip first SELECT option
        for dept_index in range(1, len(department_select.options)):

            # Re-fetch Department every iteration
            department_select = Select(self.get_visible_select("deptCode"))
            department_select.select_by_index(dept_index)

            print(f"\nDepartment : {department_select.first_selected_option.text}")

            # Wait until Unit dropdown refreshes
            wait.until(lambda d: len(Select(self.get_visible_select("unit")).options) > 0)

            unit_select = Select(self.get_visible_select("unit"))
            unit_options = unit_select.options

            if len(unit_options) <= 1:
                print("No Unit Found")
                continue

            # ================= UNIT =======================
            for unit_index in range(1, len(unit_options)):

                unit_select = Select(self.get_visible_select("unit"))
                unit_select.select_by_index(unit_index)

                print(f"   Unit : {unit_select.first_selected_option.text}")

                # Wait until Ward refreshes
                wait.until(lambda d: len(Select(self.get_visible_select("ward")).options) > 0)

                ward_select = Select(self.get_visible_select("ward"))
                ward_options = ward_select.options

                if len(ward_options) <= 1:
                    print("   No Ward Found")
                    continue

                # ================= WARD =======================
                for ward_index in range(1, len(ward_options)):

                    ward_select = Select(self.get_visible_select("ward"))
                    ward_select.select_by_index(ward_index)

                    print(f"      Ward : {ward_select.first_selected_option.text}")

                    # Wait until Bed refreshes
                    wait.until(lambda d: len(Select(self.get_visible_select("bedCode")).options) > 0)

                    bed_select = Select(self.get_visible_select("bedCode"))
                    bed_options = bed_select.options

                    if len(bed_options) <= 1:
                        print("      No Bed Found")
                        continue

                    # ================= BED =======================
                    bed_select.select_by_index(1)

                    department_name = department_select.first_selected_option.text.strip()
                    unit_name = unit_select.first_selected_option.text.strip()
                    ward_name = ward_select.first_selected_option.text.strip()

                    print(f"         Bed : {bed_select.first_selected_option.text}")
                    print("\nAdmission Details Selected Successfully")
                    return (
                        department_name,
                        unit_name,
                        ward_name,
                    )

        raise Exception("No valid Department → Unit → Ward → Bed combination found.")


    def select_status(self):
        status = Select(self.driver.find_element(By.XPATH,
                                            "//form[@name='OPDaddmissionAdviceForm']//select[@name='patStatusVal']"
                                            ))

        # Skip first "Select" option
        random_index = random.randint(1, len(status.options) - 1)
        status.select_by_index(random_index)

        print("Selected Status:", status.first_selected_option.text)

    def enter_admission_advice_remarks(self, value):
        admission_advice_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//h6[normalize-space()='Admission Advice']/ancestor::div[contains(@class,'card-body')]//textarea[@name='remarks']")
            )
        )
        admission_advice_remarks.clear()
        admission_advice_remarks.send_keys(value)

    def select_ref_to(self):
        referral_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='referralType']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            referral_dropdown
        )

        Select(referral_dropdown).select_by_visible_text("Internal Department")



    def select_random_referral_type(self):
        referral_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//select[@name='referToDtls']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            referral_element
        )

        referral_dropdown = Select(referral_element)

        # Referral types
        options = {
            "1": "ROUTINE",
            "2": "EMERGENCY"
        }

        selected_value = random.choice(list(options.keys()))
        selected_text = options[selected_value]

        # Select using option value
        referral_dropdown.select_by_value(selected_value)

        print(f"Selected Referral Type: {selected_text}")

        return selected_text

    def select_random_dropdown_option(self):

        wait = WebDriverWait(self.driver, 20)

        # Open dropdown
        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[normalize-space()='Referral Department']/following-sibling::div//div[contains(@class,'searchable-dropdown__control')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        dropdown.click()


        # Wait until menu is opened
        wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//label[normalize-space()='Referral Department']/following-sibling::div//input[@role='combobox']"
            ))
        )

        # Get all options
        options = wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//div[contains(@class,'searchable-dropdown__option')]"
            ))
        )

        # Remove blank/disabled options
        options = [
            option for option in options
            if option.text.strip()
               and "disabled" not in option.get_attribute("class").lower()
        ]

        if not options:
            raise Exception("No dropdown options found.")

        option = random.choice(options)
        selected_text = option.text.strip()

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'nearest'});",
            option
        )

        self.driver.execute_script("arguments[0].click();", option)

        print(f"Selected Department : {selected_text}")

        return selected_text

    def enter_referral_remarks(self, value):
        referral_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@name='referralForm']//textarea[@name='referralReason']")
            )
        )
        referral_remarks.clear()
        referral_remarks.send_keys(value)


    def click_referral_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//form[@name='referralForm']//button[@type='button' and normalize-space()='Add']")
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


    def enter_clinical_notes(self, value):
        clinical_notes = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@contenteditable='true' and @data-placeholder='Enter clinical notes...']")
            )
        )
        clinical_notes.clear()
        clinical_notes.send_keys(value)

    def enter_instruction_remarks(self, value):
        instruction_remarks = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@contenteditable='true' and @data-placeholder='Enter Instruction']")
            )
        )
        instruction_remarks.clear()
        instruction_remarks.send_keys(value)

    def select_test_name(self, test_name):
        test_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@name='testCode' and @placeholder='Search Test Name']"
                )
            )
        )

        # Scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            test_input
        )

        # JS click
        self.driver.execute_script(
            "arguments[0].click();",
            test_input
        )

        # Type test name
        test_input.clear()
        test_input.send_keys(test_name)

        # Wait for dropdown suggestions
        time.sleep(2)

        # Select first suggestion
        test_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.3)
        test_input.send_keys(Keys.ENTER)

        print(f"Selected Test : {test_name}")

    def fill_hiv_form(
            self,
            patient_id="419940246272",
            art_reg_no="ART123456",
            clinical_remarks="Clinical features suggestive of malaria.",
            duration_of_illness="4 Days"
    ):

        wait = WebDriverWait(self.driver, 10)

        def enter_text(label, value):
            textbox = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//span[contains(normalize-space(),'{label}')]"
                        "/ancestor::td/following-sibling::td//input"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                textbox
            )
            self.driver.execute_script(
                "arguments[0].click();",
                textbox
            )

            textbox.clear()
            textbox.send_keys(value)

        # Patient ID (AADHAR)
        enter_text("Patient ID (AADHAR)", patient_id)

        # Pre ART / ART Reg No.
        enter_text("Pre ART/ ART Reg No.", art_reg_no)

        # Clinical Remarks
        enter_text("Clinical Remarks", clinical_remarks)

        # Duration of Illness
        enter_text("Duration of Illness", duration_of_illness)

        # First Visit / Follow up
        visit_dropdown = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(normalize-space(),'First Visit/ Follow up')]"
                    "/ancestor::td/following-sibling::td//select"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            visit_dropdown
        )
        self.driver.execute_script(
            "arguments[0].click();",
            visit_dropdown
        )

        Select(visit_dropdown).select_by_visible_text("First Visit")

        print("HIV form filled successfully.")



    def click_clear_all_btn(self):
        clr_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h6[normalize-space()='Admission Advice']/ancestor::div[contains(@class,'justify-content-sm-start')]//img[@alt='Clear All']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            clr_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            clr_btn
        )

    def scroll_print_preview(self):
        wait = WebDriverWait(self.driver, 10)

        scrollable = wait.until(
            EC.visibility_of_element_located((By.ID, "scrollableDiv"))
        )

        # Scroll down
        for _ in range(10):
            self.driver.execute_script(
                "arguments[0].scrollBy(0, 300);",
                scrollable
            )
            time.sleep(1)

        # Scroll back to top
        for _ in range(10):
            self.driver.execute_script(
                "arguments[0].scrollBy(0, -300);",
                scrollable
            )
            time.sleep(1)

        # Ensure at top
        self.driver.execute_script(
            "arguments[0].scrollTop = 0;",
            scrollable
        )


    def get_patient_details_from_opd_rx(self):

        data = {}

        # ============================================================
        #                    PATIENT DETAILS
        # ============================================================

        container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'row row')]"
                )
            )
        )

        first_row = container.find_element(
            By.XPATH,
            ".//div[1]/span"
        ).text.strip()

        print("first_row =", repr(first_row))

        parts = first_row.split("|")

        if len(parts) >= 2:

            data["Patient Name"] = parts[0].strip()

            age_gender = parts[1].strip()

            if "/" in age_gender:

                first, second = [
                    x.strip()
                    for x in age_gender.split("/", 1)
                ]

                if "YR" in first.upper():
                    data["Age"] = first.replace("Yr", "").strip()
                    data["Gender"] = second

                elif "YR" in second.upper():
                    data["Age"] = second.replace("Yr", "").strip()
                    data["Gender"] = first

                else:
                    data["Age"] = first
                    data["Gender"] = second

        labels = container.find_elements(
            By.XPATH,
            ".//label[span]"
        )

        for label in labels:

            try:

                key = label.find_element(
                    By.TAG_NAME,
                    "span"
                ).text.replace(
                    ":",
                    ""
                ).strip()

                value = label.text.replace(
                    label.find_element(
                        By.TAG_NAME,
                        "span"
                    ).text,
                    ""
                ).strip()

                data[key] = value

            except Exception:
                pass

        # ============================================================
        #                        VITALS
        # ============================================================

        data["Vitals"] = {}

        vitals = self.driver.find_elements(
            By.XPATH,
            "//span[contains(@class,'vitalRxBtn')]"
        )

        for vital in vitals:

            if ":" in vital.text:
                key, value = vital.text.split(":", 1)

                data["Vitals"][key.strip()] = value.strip()

        # ============================================================
        #                   CLINICAL HISTORY
        # ============================================================

        data["Clinical History"] = {}

        chief_complaints = self.driver.find_elements(
            By.XPATH,
            "//h6[normalize-space()='Chief Complaint']"
            "/ancestor::div[contains(@class,'row')]"
            "//ol[contains(@class,'rx-list-item')]/li"
        )

        data["Clinical History"]["Chief Complaint"] = [

            complaint.text.strip()

            for complaint in chief_complaints

            if complaint.text.strip()

        ]

        try:

            data["Clinical History"]["History Of Present Illness"] = (
                self.driver.find_element(
                    By.XPATH,
                    "//div[contains(@class,'editable-content-comp') and @contenteditable='false']"
                ).text.strip()
            )

        except Exception:

            data["Clinical History"]["History Of Present Illness"] = None

        # ============================================================
        #                    MEDICAL HISTORY
        # ============================================================

        data["Medical History"] = {}

        chronic_diseases = self.driver.find_elements(
            By.XPATH,
            "//h6[normalize-space()='Chronic Disease']/ancestor::div[@class='col-sm-6']/following-sibling::div[@class='col-sm-6'][2]//ol/li"
        )

        data["Medical History"]["Chronic Disease"] = [

            disease.text.strip()

            for disease in chronic_diseases

            if disease.text.strip()

        ]

        allergies = self.driver.find_elements(
            By.XPATH,
            "//h6[normalize-space()='Allergy']/ancestor::div[@class='col-sm-6']/following-sibling::div[@class='col-sm-6'][2]//ol/li"
        )

        data["Medical History"]["Allergy"] = [

            allergy.text.strip()

            for allergy in allergies

            if allergy.text.strip()

        ]

        # ============================================================
        #                     DIAGNOSIS
        # ============================================================

        data["Diagnosis"] = {}

        diagnosis_list = self.driver.find_elements(
            By.XPATH,
            "//h6[normalize-space()='Diagnosis']"
            "/ancestor::div[contains(@class,'col-sm-12')]"
            "//ol[contains(@class,'rx-list-item')]/li"
        )

        data["Diagnosis"]["Diagnosis List"] = [
            item.text.strip()
            for item in diagnosis_list
            if item.text.strip()
        ]

        try:
            data["Diagnosis"]["Diagnosis Note"] = self.driver.find_element(
                By.XPATH,
                "//h6[contains(normalize-space(),'Diagnosis Note')]"
                "/ancestor::div[contains(@class,'col-sm-12')]"
            ).text.replace(
                "Diagnosis Note",
                ""
            ).strip()

        except Exception:
            data["Diagnosis"]["Diagnosis Note"] = None

        # ============================================================
        #                     EXAMINATION
        # ============================================================

        data["Examination"] = {}

        exam_fields = self.driver.find_elements(
            By.XPATH,
            "//div[@class='col-sm-6'][.//span[contains(text(),'CVS')]]/div[span]"
        )

        for field in exam_fields:

            try:

                label = field.find_element(
                    By.TAG_NAME,
                    "span"
                ).text.replace(
                    ":",
                    ""
                ).strip()

                value = field.text.replace(
                    field.find_element(
                        By.TAG_NAME,
                        "span"
                    ).text,
                    ""
                ).strip()

                data["Examination"][label] = value

            except Exception:
                pass

        # ============================================================
        #                  COMPLETE HISTORY
        # ============================================================

        data["Complete History"] = {}

        history_fields = self.driver.find_elements(
            By.XPATH,
            "//div[@class='col-sm-6'][.//span[normalize-space()='Past History :']]/div[span]"
        )

        for field in history_fields:

            try:

                label = field.find_element(
                    By.TAG_NAME,
                    "span"
                ).text.replace(
                    ":",
                    ""
                ).strip()

                value = field.text.replace(
                    field.find_element(
                        By.TAG_NAME,
                        "span"
                    ).text,
                    ""
                ).strip()

                data["Complete History"][label] = value

            except Exception:
                pass

        # ============================================================
        #                 CONFIDENTIAL INFO
        # ============================================================

        try:

            data["Confidential Info"] = self.driver.find_element(
                By.XPATH,
                "//h6[normalize-space()='Confidential Info']"
                "/ancestor::div[contains(@class,'col-sm-12')]"
            ).text.replace(
                "Confidential Info",
                ""
            ).strip()

        except Exception:

            data["Confidential Info"] = None

        # ============================================================
        #                           RX
        # ============================================================

        data["Rx"] = []

        try:

            rx_table = self.driver.find_element(
                By.XPATH,
                "//h6[normalize-space()='Rx']"
                "/ancestor::div[contains(@class,'col-sm-12')]"
                "//table"
            )

            headers = [
                header.text.strip()
                for header in rx_table.find_elements(
                    By.XPATH,
                    ".//tr[1]/th"
                )
            ]

            rows = rx_table.find_elements(
                By.XPATH,
                ".//tr[position()>1]"
            )

            for row in rows:

                cols = row.find_elements(
                    By.TAG_NAME,
                    "td"
                )

                if len(cols) != len(headers):
                    continue

                drug = {}

                for header, col in zip(headers, cols):
                    key = (
                        header.replace(".", "")
                        .replace("/", "_")
                        .replace(" ", "_")
                    )

                    drug[key] = col.text.strip()

                data["Rx"].append(drug)

        except Exception:

            data["Rx"] = []

        # ============================================================
        #                  TREATMENT ADVICE
        # ============================================================

        try:

            data["Treatment Advice"] = self.driver.find_element(
                By.XPATH,
                "//h6[normalize-space()='Treatment Advice']"
                "/ancestor::div[contains(@class,'col-sm-12')]"
                "//p"
            ).text.strip()

        except Exception:

            data["Treatment Advice"] = None

        # ============================================================
        #               INVESTIGATION DETAILS
        # ============================================================

        try:

            data["Investigation Details"] = self.driver.find_element(
                By.XPATH,
                "//h6[normalize-space()='Investigation Details']"
                "/ancestor::div[contains(@class,'col-sm-12')]"
                "//div[contains(@class,'ps-2')]"
            ).text.strip()

        except Exception:

            data["Investigation Details"] = None

        # ============================================================
        #                     PROCEDURE
        # ============================================================

        procedure_list = self.driver.find_elements(
            By.XPATH,
            "//h6[normalize-space()='Procedure']"
            "/ancestor::div[contains(@class,'col-sm-12')]"
            "//ol[contains(@class,'rx-list-item')]/li"
        )

        data["Procedure"] = [
            procedure.text.strip()
            for procedure in procedure_list
            if procedure.text.strip()
        ]

        # ============================================================
        #                   CLINICAL NOTE
        # ============================================================

        try:

            data["Clinical Note"] = self.driver.find_element(
                By.XPATH,
                "//h6[normalize-space()='Clinical Note']"
                "/ancestor::div[contains(@class,'col-sm-12')]"
                "//div[@contenteditable='false']"
            ).text.strip()

        except Exception:

            data["Clinical Note"] = None

        # ============================================================
        #                     INSTRUCTION
        # ============================================================

        try:

            data["Instruction"] = self.driver.find_element(
                By.XPATH,
                "//h6[normalize-space()='Instruction']"
                "/ancestor::div[contains(@class,'col-sm-12')]"
                "//div[contains(@class,'mb-1')]"
            ).text.strip()

        except Exception:

            data["Instruction"] = None

        # ============================================================
        #                      REFER TO
        # ============================================================

        referral_elements = self.driver.find_elements(
            By.XPATH,
            "//h6[contains(normalize-space(),'Refer To')]"
            "/ancestor::div[contains(@class,'col-sm-12')]"
            "//ol/li"
        )

        data["Refer To"] = [
            referral.text.strip()
            for referral in referral_elements
            if referral.text.strip()
        ]

        # ============================================================
        #                     RETURN DATA
        # ============================================================

        return data




    def click_inventory_module(self):
        inventory = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[@title='Inventory']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            inventory
        )

        self.driver.execute_script(
            "arguments[0].click();",
            inventory
        )


    def click_issue_option(self):
        issue = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='Issue']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            issue
        )

        self.driver.execute_script(
            "arguments[0].click();",
            issue
        )

    def click_direct_issue_to_patient(self):
        direct_issue = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li/a[normalize-space()='Direct Issue To Patient']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            direct_issue
        )

        self.driver.execute_script(
            "arguments[0].click();",
            direct_issue
        )

    def enter_search_crn_in_inventory(self, crn):

        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search' and @type='search']"))
        )

        search_box.click()
        self.driver.execute_script("""
            arguments[0].value = '';
            arguments[0].focus();
        """, search_box)
        search_box.clear()
        search_box.send_keys(crn)
        time.sleep(3)


    def click_investigation_module(self):

        investigation = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[@title='Investigation']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            investigation
        )

        self.driver.execute_script(
            "arguments[0].click();",
            investigation
        )


    def click_sample_collection_option(self):
        sample_collection = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='Sample Collection']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            sample_collection
        )

        self.driver.execute_script(
            "arguments[0].click();",
            sample_collection
        )


    def enter_search_crn_in_sample_collection(self, crn):

        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='globalTextSearch' and @name='crNo']"))
        )

        self.driver.execute_script("""
            arguments[0].value = '';
            arguments[0].focus();
        """, search_box)
        search_box.clear()
        search_box.send_keys(crn)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)


    def select_test_grp(self):
        dropdown = Select(
            self.driver.find_element(By.XPATH, "//select[@name='isTestGroup']")
        )

        dropdown.select_by_visible_text("Radiological investigations")


    def xray_clinical_indication(self):
        clinical_indication = self.driver.find_element(
            By.XPATH,
            "//textarea[@name='clinicalIndication']"
        )

        clinical_indication.click()
        clinical_indication.clear()  # Won't work on contenteditable divs
        clinical_indication.send_keys("Patient has severe abdominal pain with fever.")


    def xray_clinical_history(self):
        clinical_history = self.driver.find_element(
            By.XPATH,
            "//div[@data-placeholder='Clinical History & Examination']"
        )

        clinical_history.click()
        clinical_history.clear()
        clinical_history.send_keys("Patient has history of intermittent fever with chills and body ache.")



    def click_referral_acceptance(self):

        referral_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Referral Acceptance']")
            )
        )

        referral_btn.click()

    def select_department_unit_for_referral(self, unit_name):
        unit_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//select[@name='select-option' and @title='Select Department/Unit']"
                )
            )
        )

        Select(unit_dropdown).select_by_visible_text(unit_name)


    def click_follow_up_btn(self):
        followup_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Follow-up Acceptance']")
            )
        )

        followup_btn.click()

    def click_upcoming_btn(self):
        upcoming_tab = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[@for='tab-upcoming' and contains(normalize-space(), 'Upcoming')]")
            )
        )

        upcoming_tab.click()

    def followup_close_btn(self):
        close_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//header[.//div[contains(@class,'drawer-title') and normalize-space()='Follow-up Acceptance']]//button[contains(@class,'drawer-close')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            close_btn
        )


    def click_patience_acceptance_option(self):
        patience_acceptance = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='Patient Acceptance']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            patience_acceptance
        )

        self.driver.execute_script(
            "arguments[0].click();",
            patience_acceptance
        )

    def select_xray(self):
        wait = WebDriverWait(self.driver, 10)

        # Open Lab Name dropdown
        lab_input = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[normalize-space()='Lab Name']"
                    "/following-sibling::div"
                    "//input[contains(@class,'searchable-dropdown__input')]"
                )
            )
        )

        lab_input.click()
        lab_input.send_keys("XRAY")

        # Select XRAY from dropdown
        xray_option = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'searchable-dropdown__option') "
                    "and contains(translate(normalize-space(.), "
                    "'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'XRAY')]"
                )
            )
        )

        xray_option.click()

    def click_crn_btn(self):
        crn_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'button-container')]//button[normalize-space()='CRN']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            crn_btn
        )

    def enter_crn(self, crn_number):
        crn_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='crno' and @placeholder='CRN']")
            )
        )

        crn_input.clear()
        crn_input.send_keys(crn_number)

    def click_go_btn(self):
        go_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class,'btn-primary') and normalize-space()='Go']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            go_btn
        )


    def click_admission_advice_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'card-body')][.//h6[normalize-space()='Admission Advice']]//button[contains(@class,'add-blue-button') and normalize-space()='Add']"
                )
            )
        )

        add_btn.click()


    def click_skip_btn(self):
        forward_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//td[contains(@class,'table-btn-group')]/button[3]")
            )
        )

        forward_btn.click()

    def skip_yes_btn(self):
        yes_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'swal2-confirm') and normalize-space()='Yes']")
            )
        )

        yes_btn.click()

    def enter_crn_number_for_skip(self,crn_number):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Mobile/CRN/Name/']")
            )
        )

        search_input.clear()
        search_input.send_keys(crn_number)

    def click_add_patient_btn(self):
        add_patient_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@title='Add Patient']")
            )
        )
        add_patient_btn.click()

    def enter_crn_number_for_stamp(self, crn_number):
        crn_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'modal-content')]//label[normalize-space()='CRN']/following-sibling::input[@name='crNo']")
            )
        )

        # JavaScript click
        self.driver.execute_script(
            "arguments[0].click();",
            crn_input
        )

        crn_input.clear()
        crn_input.send_keys(crn_number)
        time.sleep(2)
        crn_input.send_keys(Keys.ENTER)

    def click_ok_stamping_btn(self):
        ok_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='OK']")
            )
        )
        ok_btn.click()

    def again_search_crn(self, crn_no):
        crn_search = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//input[@placeholder='Mobile/CRN/Name/']")
            )
        )

        # JavaScript click
        self.driver.execute_script(
            "arguments[0].click();",
            crn_search
        )

        crn_search.clear()
        crn_search.send_keys(crn_no)
        time.sleep(2)
        crn_search.send_keys(Keys.ENTER)


    def click_pdf_download_btn(self):
        pdf_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and @class = 'white-button btn-sm align-content-center btn btn-primary  mx-1 btn btn-primary']")
            )
        )

        pdf_btn.click()

    def click_operation_theater_module(self):

        ot = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[@title='Operation theater']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            ot
        )

        self.driver.execute_script(
            "arguments[0].click();",
            ot
        )


    def click_anesthesia_desk(self):
        anesthesia_desk = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='Anesthesia Desk']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            anesthesia_desk
        )

        self.driver.execute_script(
            "arguments[0].click();",
            anesthesia_desk
        )


    def click_pac_entry(self):
        pac_entry = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='PAC Entry']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            pac_entry
        )

        self.driver.execute_script(
            "arguments[0].click();",
            pac_entry
        )

    def search_pac_entry(self,crn_no):
        pac_entry = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type= 'search' and @class = 'ant-input css-mncuj7 ant-input-outlined']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            pac_entry
        )

        self.driver.execute_script(
            "arguments[0].click();",
            pac_entry
        )

        pac_entry.clear()

        pac_entry.send_keys(crn_no)


    def click_investigation_list(self):
        list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Investigation List']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            list
        )

        self.driver.execute_script(
            "arguments[0].click();",
            list
        )

    def search_test(self,test_name):
        test_entry = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='search' and @class= 'ant-input css-mncuj7 ant-input-outlined']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            test_entry
        )

        self.driver.execute_script(
            "arguments[0].click();",
            test_entry
        )

        test_entry.clear()

        test_entry.send_keys(test_name)


    def clear_box(self):
        test_entry = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='search' and @class= 'ant-input css-mncuj7 ant-input-outlined']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            test_entry
        )

        self.driver.execute_script(
            "arguments[0].click();",
            test_entry
        )

        test_entry.send_keys(Keys.CONTROL, "a")
        test_entry.send_keys(Keys.BACKSPACE)


    def click_refer_out_btn(self):
        out_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[normalize-space()='Refer Out']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            out_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            out_btn
        )


    def click_again_rx(self):
        again_rx_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'btn-referr-out')]")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            again_rx_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            again_rx_btn
        )


    def click_lab_report(self):
        lab_report_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Lab Reports']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            lab_report_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            lab_report_btn
        )


    def click_on_previous_btn(self):
        previous_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Previous']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            previous_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            previous_btn
        )


    def previous_close_btn(self):
        close_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'btn-close') and @aria-label='Close']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            close_btn
        )
        self.driver.execute_script(
            "arguments[0].click();",
            close_btn
        )


    def adt_3_dot_icon(self):

        three_dots = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type = 'button' and @tootip = '[object Object]']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            three_dots
        )
        self.driver.execute_script(
            "arguments[0].click();",
            three_dots
        )


    def search_from_patient_listing(self,test_name):
        test_entry = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='search' and @placeholder ='Search']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            test_entry
        )

        self.driver.execute_script(
            "arguments[0].click();",
            test_entry
        )

        test_entry.clear()

        test_entry.send_keys(test_name)

    def select_opd_dr_desk_unit_for_inv_list(self, unit_name):

        dropdown_xpath = "//select[@name='select-option']"

        dropdown = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (By.XPATH, dropdown_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        # Convert:
        # CASUALTY(CASUALTY UNIT 1)
        # to:
        # CASUALTY(Casualty Unit 1)

        parts = unit_name.split("(", 1)

        if len(parts) == 2:
            department = parts[0].strip().title()
            unit = parts[1].rstrip(")").strip()

            unit_name = (
                f"{department}("
                f"{unit.title()})"
            )

        Select(dropdown).select_by_visible_text(unit_name)

        return unit_name

    def select_random_unit_for_stamping(self):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//select[@name='select-option']")
            )
        )

        select = Select(dropdown)

        # Get all valid options (ignore placeholder if any)
        options = [
            option for option in select.options
            if option.get_attribute("value").strip() != ""
        ]

        random_option = random.choice(options)
        random_option.click()

        selected_unit = random_option.text.strip()
        print(f"Selected Unit: {selected_unit}")

        return selected_unit

    def select_drug_store_name(self, store_name):

        # ============================================================
        # DRUG STORE DROPDOWN
        # ============================================================

        dropdown = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[normalize-space()='Store']"
                    "/following-sibling::div"
                    "//div[contains(@class,'searchable-dropdown__control')]"
                )
            )
        )

        dropdown.click()

        # ============================================================
        # SEARCH STORE
        # ============================================================

        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//label[normalize-space()='Store']"
                    "/following-sibling::div"
                    "//input[contains(@class,'searchable-dropdown__input')]"
                )
            )
        )

        search_input.send_keys(store_name)

        # ============================================================
        # SELECT STORE OPTION
        # ============================================================

        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//*[contains(@class,'searchable-dropdown__option') "
                    f"and normalize-space()='{store_name}']"
                )
            )
        )

        option.click()


    def click_to_attend_btn(self):
        attend_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Click To Attend']")
            )
        )
        attend_btn.click()

    def dispense_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//i[.//*[name()='svg' and @data-icon='floppy-disk']]"
            ))
        )
        save_btn.click()

    def click_swal_save_btn(self):
        swal_save = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and normalize-space()='Save']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            swal_save
        )

        self.driver.execute_script(
            "arguments[0].click();",
            swal_save
        )

    def adt_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'blue-button') and normalize-space()='SAVE']")
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

    def enter_issue_qty(self,qty):
        issue_qty = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='issueqty']")
            )
        )

        issue_qty.clear()
        issue_qty.send_keys(qty)

    def enter_issue_quantity(self, quantity):
        """
        Enter quantity in the Issue Qtl field.
        """

        issue_qty_xpath = "//input[@name='issueqty']"

        issue_qty_input = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (By.XPATH, issue_qty_xpath)
            )
        )


        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            issue_qty_input
        )

        self.driver.execute_script(
            "arguments[0].click();",
            issue_qty_input
        )

        issue_qty_input.clear()
        issue_qty_input.send_keys(quantity)

    def select_collection_area(self, area):

        dropdown_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[normalize-space()='Collection Area']"
                    "/following-sibling::div"
                    "//input[contains(@class,'searchable-dropdown__input') "
                    "and @role='combobox']"
                )
            )
        )

        dropdown_input.click()
        dropdown_input.send_keys(area)
        time.sleep(2)
        dropdown_input.send_keys(Keys.ENTER)

        # option = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable(
        #         (
        #             By.XPATH,
        #             f"//div[contains(@class,'searchable-dropdown__option') "
        #             f"and normalize-space(.)='{area}']"
        #         )
        #     )
        # )
        #
        # option.click()

    def select_all_requisition_checkboxes(self):
        checkboxes = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//table[contains(@class,'modify-table')]"
                "//tr[contains(@class,'reques')]"
                "//input[@type='checkbox']"
            ))
        )

        for checkbox in checkboxes:
            if not checkbox.is_selected():
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    checkbox
                )
                checkbox.click()

    def save_all_btn_for_tests(self):
        save_all_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@type='button' and normalize-space()='Save All']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            save_all_btn
        )

        time.sleep(1)

        save_all_btn.click()


    def click_inline_sample_collection_option(self):
        inline_sample = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Inline Sample Acceptance']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            inline_sample
        )

    def select_test_lab(self, option_name):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[normalize-space()='Lab']"
                    "/following-sibling::div"
                    "//input[@role='combobox' and contains(@class,'searchable-dropdown__input')]"
                )
            )
        )

        dropdown.click()
        dropdown.send_keys(option_name)

        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[contains(@class,'searchable-dropdown__option') "
                    f"and normalize-space(.)='{option_name}']"
                )
            )
        )

        option.click()


    def click_inline_sample_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='button' and @title='Save' and normalize-space()='Save']")
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

    def click_the_checkbox_for_sample(self):

        checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//th[contains(@class,'ant-table-selection-column')]"
                    "//input[@type='checkbox' and @aria-label='Select all']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            checkbox
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

    def click_yes_if_machine_confirmation_visible(self):
        try:
            yes_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[contains(@class,'swal2-popup')"
                        " and .//div[@id='swal2-html-container'"
                        " and normalize-space()='Would you like to submit data without selecting machine?']]"
                        "//button[contains(@class,'swal2-confirm')"
                        " and normalize-space()='Yes']"
                    )
                )
            )

            yes_button.click()

            return True

        except TimeoutException:
            return False


    def click_result_entry_option(self):
        inline_sample = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Result Entry Multi-Mode']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            inline_sample
        )

    def click_crn_option(self):
        crn_click = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'d-flex') and contains(@class,'align-items-center')]//div[@class='pill-group'][1]//button[normalize-space()='CRN']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            crn_click
        )


    def enter_result_entry_crn(self, crn_number):
        crn_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='crNo' and @placeholder='Enter CRN']")
            )
        )

        crn_input.clear()
        crn_input.send_keys(crn_number)

    def click_result_entry_go_btn(self):
        go_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'inv-btn')]//button[normalize-space()='Search' and not(@disabled)]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            go_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            go_btn
        )

    def click_enter_result_btn(self):
        xpath = "//button[normalize-space()='Enter Result']"

        button = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, xpath)
            )
        )

        # Scroll the button to the center of the viewport
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            button
        )

        # Small wait for any UI movement/React rendering
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )

        try:
            button.click()


        except ElementClickInterceptedException:

            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

    def click_the_checkbox_for_all_sample_result(self):
        checkbox_xpath = "//tr[th[contains(@class,'ant-table-row-expand-icon-cell')]]/th[2]/input[@type='checkbox']"

        checkbox = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, checkbox_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            checkbox
        )

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )


    def lab_dropdown_inline(self):
        lab_dropdown = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'col-lg-2')]"
                    "[.//label[normalize-space()='Lab']]"
                    "//div[contains(@class,'searchable-dropdown__control')]"
                )
            )
        )

        lab_dropdown.click()

        time.sleep(1)

    def fill_all_result_fields(self):
        wait = WebDriverWait(self.driver, 20)

        modal = wait.until(
            EC.presence_of_element_located(
                (By.ID, "scrollableDiv")
            )
        )

        def scroll_field_to_bottom(field):
            self.driver.execute_script(
                """
                const field = arguments[0];

                let parent = field.parentElement;

                while (parent) {
                    const style = window.getComputedStyle(parent);

                    if (
                        (style.overflowY === 'auto' ||
                         style.overflowY === 'scroll') &&
                        parent.scrollHeight > parent.clientHeight
                    ) {
                        const fieldRect = field.getBoundingClientRect();
                        const parentRect = parent.getBoundingClientRect();

                        parent.scrollTop +=
                            fieldRect.bottom -
                            parentRect.bottom +
                            50;

                        return true;
                    }

                    parent = parent.parentElement;
                }

                return false;
                """,
                field
            )

        # ==========================================
        # INPUT FIELDS
        # ==========================================
        inputs = modal.find_elements(
            By.XPATH,
            ".//input[@type='text']"
        )

        for index, field in enumerate(inputs, start=1):
            try:
                scroll_field_to_bottom(field)

                time.sleep(0.5)

                if field.is_displayed() and field.is_enabled():
                    field.clear()
                    field.send_keys(str(index))

                    print(f"Input {index} filled successfully.")

            except Exception as e:
                print(f"Skipping input {index}: {e}")

        # ==========================================
        # TEXTAREAS
        # ==========================================
        text_areas = modal.find_elements(
            By.XPATH,
            ".//textarea[not(@name='finalRemark')]"
        )

        for index, field in enumerate(text_areas, start=1):
            try:
                scroll_field_to_bottom(field)

                time.sleep(0.5)

                if field.is_displayed() and field.is_enabled():
                    field.clear()
                    field.send_keys(str(index))

                    print(f"Textarea {index} filled successfully.")

            except Exception as e:
                print(f"Skipping textarea {index}: {e}")

    def click_result_save_button(self):
        wait = WebDriverWait(self.driver, 15)

        save_xpath = "//div[@id='scrollableDiv']/div[contains(@class,'text-center')]//button[@type='button' and @title='Save' and normalize-space(.)='Save']"

        # Find Save button
        save_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, save_xpath)
            )
        )

        # Find the modal scroll container
        modal = wait.until(
            EC.presence_of_element_located(
                (By.ID, "scrollableDiv")
            )
        )

        # Scroll the modal completely to the bottom
        self.driver.execute_script(
            """
            arguments[0].scrollTop = arguments[0].scrollHeight;
            """,
            modal
        )

        time.sleep(1)

        # Re-locate Save button after scrolling
        save_button = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, save_xpath)
            )
        )

        time.sleep(1)

        # JavaScript fallback
        self.driver.execute_script(
            "arguments[0].click();",
            save_button
        )

    def click_result_entry_swal_yes_button(self):
        yes_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'swal2-container')]//button[contains(@class,'swal2-confirm') and normalize-space()='Yes']"
            ))
        )

        yes_button.click()


    def click_validation_option(self):
        inline_sample = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Result Validation Multi-Mode']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            inline_sample
        )

    def click_select_all_validation_checkbox(self):
        xpath = "//tr[th[contains(@class,'ant-table-row-expand-icon-cell')]]/th[2]//input[@aria-label='Select all']"

        checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            checkbox
        )

        time.sleep(2)

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )


    def click_validation_save_button(self):
        save_xpath = (
            "//button[@type='button' and @title='Save and Validate' and normalize-space()='Save and Validate']"
        )

        save_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, save_xpath))
        )

        # Scroll Save button to the center of the viewport
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: 'instant',
                block: 'center',
                inline: 'nearest'
            });
            """,
            save_button
        )

        time.sleep(1)

        # Re-locate after scrolling
        save_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, save_xpath))
        )

        try:
            save_button.click()

        except ElementClickInterceptedException:


            self.driver.execute_script(
                "arguments[0].click();",
                save_button
            )

    def click_result_report_option(self):
        report = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Result Report Printing']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            report
        )


    def click_crn_option_in_report(self):
        crn_click = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='rrp-tab-btn rrp-tab-btn-active' and normalize-space()='CRN']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            crn_click
        )

    def enter_report_crn(self, crn_number):
        crn_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='crNo' and @placeholder='CRN']")
            )
        )

        crn_input.clear()
        crn_input.send_keys(crn_number)

    def click_report_go_btn(self):
        go_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'inv-btn')]//button[normalize-space()='Go' and not(@disabled)]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            go_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            go_btn
        )

    def select_entry_status(self, status):
        wait = WebDriverWait(self.driver, 20)

        dropdown = wait.until(
            lambda driver: next(
                (
                    element
                    for element in driver.find_elements(
                    By.XPATH,
                    "//select[@name='entryStatus']"
                )
                    if element.is_displayed() and element.is_enabled()
                ),
                False
            )
        )

        options = dropdown.find_elements(By.TAG_NAME, "option")

        print("Available options:")

        for option in options:
            print(
                f"Text: '{option.text}' | "
                f"Value: '{option.get_attribute('value')}'"
            )

        Select(dropdown).select_by_visible_text(status)

        print(f"Selected: {status}")

    def click_service_area_module(self):

        service_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[@title='Service area']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            service_area
        )

        self.driver.execute_script(
            "arguments[0].click();",
            service_area
        )


    def click_request_status_viewing_option(self):

        request = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='Request Status Viewing']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            request
        )

        self.driver.execute_script(
            "arguments[0].click();",
            request
        )

    def select_service_area_store(self, store_name):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//select[@name='storeId']")
            )
        )

        option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//select[@name='storeId']"
                    f"/option[@label='{store_name}']"
                )
            )
        )

        # Select the option
        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(
                new Event('change', { bubbles: true })
            );
            """,
            dropdown,
            option.get_attribute("value")
        )


    def service_area_go_btn(self):
        go_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and normalize-space()='Go']")
            )
        )
        go_button.click()

    def service_area_crn(self,crn_no):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Search' and @type='search']")
            )
        )

        search_box.clear()
        search_box.send_keys(crn_no)


    def hover_click_on_administration(self):
        admin_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(@class,'ant-dropdown-menu-title-content') and normalize-space()='Administration']"
                )
            )
        )

        admin_option.click()

    def click_req_radio_btn(self):

        radio_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//tr[contains(@class,'ant-table-row') and @rowindex='0']"
                    "//label[contains(@class,'ant-radio-wrapper')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            radio_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            radio_button
        )


    def request_viewing_save_btn(self):
        save_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and normalize-space()='Save']")
            )
        )
        save_button.click()


    def three_dots_icon(self):

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(@class,'table-dropdown')]//*[contains(@class,'fa-ellipsis-vertical')]"
                )
            )
        ).click()

    def click_unbilled_button(self):

        unbilled_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(normalize-space(), 'UnBilled')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            unbilled_button
        )

        unbilled_button.click()

    def click_billing_module(self):

        billing = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[@title='Billing']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            billing
        )

        self.driver.execute_script(
            "arguments[0].click();",
            billing
        )

    def click_cash_collection_option(self):
        cash_collection = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='Cash Collection']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            cash_collection
        )

        self.driver.execute_script(
            "arguments[0].click();",
            cash_collection
        )


    def click_cash_collection_checkbox(self):

        checkbox_xpath = (
            "//tr[@data-row-key='0']"
            "//td[contains(@class,'ant-table-selection-column')]"
            "//label[contains(@class,'ant-checkbox-wrapper')]"
        )

        checkbox = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, checkbox_xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            checkbox
        )

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, checkbox_xpath)
            )
        )

        checkbox.click()


    def click_cash_save_button(self):

        save_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class,'blue-button') and normalize-space()='Save']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            save_button
        )

        save_button.click()

    def enter_search_cr_no_value_for_cash(self, value):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='crNo']")
            )
        )
        search_box.clear()
        search_box.send_keys(value)
        time.sleep(3)
        search_box.send_keys(Keys.ENTER)













































































































