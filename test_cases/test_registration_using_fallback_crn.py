import re
import pyautogui
import pytest
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import LogGen
from utilities.screenshot import Screenshot
from test_data.test_patient_data import Testdata, TestDataGenerator
import random
import string

@pytest.mark.usefixtures("login")
class Test_New_Patient_Workflow:

    logger = LogGen.loggen()
    driver = None
    patient_reg = None

    # ============================================================
    # WORKFLOW DATA
    # ============================================================

    generated_crn = None
    generated_mobile_no = None
    generated_patient_name = None

    selected_department = None
    selected_unit = None
    opd_unit_name = None

    generated_updated_name = None
    new_selected_department = None
    new_selected_unit = None
    new_opd_unit_name = None
    new_generated_crn = None

    # ============================================================
    # FALLBACK CRN
    # ============================================================

    revisit_hardcoded_crn = "231012600001605"
    revisit_opd_unit_name = None

    # True if fallback CRN was used
    revisit_using_fallback = False

    # ============================================================
    # SEARCH & CREATE PATIENT DATA
    # ============================================================

    search_create_crn = None
    search_create_patient_name = None
    search_create_mobile_no = None

    search_create_department = None
    search_create_unit = None
    search_create_opd_unit_name = None


    @pytest.mark.patient_registration_flow_part1
    def test_new_registration(self):

        # Reset registration data
        Test_New_Patient_Workflow.generated_crn = None
        Test_New_Patient_Workflow.generated_patient_name = None
        Test_New_Patient_Workflow.generated_mobile_no = None

        mobile_number = (
            TestDataGenerator.generate_mobile_number()
        )

        LogGen.start_test(
            self.logger,
            "test_new_registration",
            "Patient Registration"
        )

        try:

            # ====================================================
            # CREATE PATIENT
            # ====================================================

            self.logger.info(
                "Opening Registration Module"
            )

            self.patient_reg.click_registration_module()

            self.logger.info(
                "Opening Patient Registration"
            )

            self.patient_reg.click_patient_registration_option()

            self.logger.info(
                "Clicking New Registration button"
            )

            self.patient_reg.click_new_registration_btn()

            time.sleep(3)

            # ====================================================
            # SELECT DEPARTMENT
            # ====================================================

            selected_department = (
                self.patient_reg.select_random_visiting_dpt()
            )

            Test_New_Patient_Workflow.selected_department = (
                selected_department
            )

            self.logger.info(
                f"Selected Department: {selected_department}"
            )

            time.sleep(2)

            # ====================================================
            # GET UNIT
            # ====================================================

            selected_unit = (
                self.patient_reg.get_selected_unit()
            )

            Test_New_Patient_Workflow.selected_unit = (
                selected_unit
            )

            self.logger.info(
                f"Selected Unit: {selected_unit}"
            )

            opd_unit_name = (
                f"{selected_department}"
                f"({selected_unit})"
            )

            Test_New_Patient_Workflow.opd_unit_name = (
                opd_unit_name
            )

            self.logger.info(
                f"OPD Unit Name: {opd_unit_name}"
            )

            # ====================================================
            # GENERATE PATIENT NAME
            # ====================================================

            suffix = ''.join(
                random.choices(
                    string.ascii_letters,
                    k=3
                )
            )

            patient_name_suffix = (
                f"{Testdata.PATIENT_NAME}{suffix}"
            )

            self.logger.info(
                f"Generated Patient Name: "
                f"{patient_name_suffix}"
            )

            self.patient_reg.select_visiting_dpt(
                selected_department
            )

            # ====================================================
            # ENTER PATIENT DETAILS
            # ====================================================

            self.patient_reg.enter_patient_name(
                patient_name_suffix
            )

            self.patient_reg.select_random_payment_mode()

            self.patient_reg.enter_patient_age(
                "30"
            )

            self.patient_reg.select_gender(
                "Female"
            )

            self.logger.info(
                f"Entering Mobile Number: {mobile_number}"
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


            self.patient_reg.enter_patient_spouse(
                "Test Spouse"
            )


            self.patient_reg.enter_patient_guardian(
                "Automation guardian"
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
                "77738"
            )


            # ====================================================
            # SAVE
            # ====================================================

            self.logger.info(
                "Saving patient registration"
            )
            time.sleep(2)

            self.patient_reg.click_save_btn()

            time.sleep(11)

            pyautogui.press("esc")

            time.sleep(2)

            # ====================================================
            # GET PDF
            # ====================================================

            self.logger.info(
                "Opening generated OPD PDF"
            )

            pdf_text = (
                self.patient_reg.get_blob_pdf_text()
            )

            self.logger.info(
                "PDF text extracted successfully"
            )

            print(pdf_text)

            # ====================================================
            # EXTRACT CRN
            # ====================================================

            import re

            # ============================================================
            # EXTRACT CRN
            # ============================================================

            crn_number = ""

            # Primary method: CRN : <number>
            crn_match = re.search(
                r'\bCRN\s*:\s*(\d+)',
                pdf_text,
                re.IGNORECASE
            )

            if crn_match:
                crn_number = crn_match.group(1)

            # Fallback: PDF extractor sometimes removes "CRN :"
            # and puts CRN directly before "Name :"
            if not crn_number:
                crn_match = re.search(
                    r'(\d{10,20})\s*Name\s*:',
                    pdf_text,
                    re.IGNORECASE
                )

                if crn_match:
                    crn_number = crn_match.group(1)

            Test_New_Patient_Workflow.generated_crn = crn_number

            self.logger.info(
                f"CRN: {crn_number}"
            )

            # ============================================================
            # EXTRACT PATIENT NAME
            # ============================================================

            patient_name = ""

            name_match = re.search(
                r'\bName\s*:\s*(.*?)\s*(?=ெபயZ|Age\s*/\s*Sex\s*:)',
                pdf_text,
                re.IGNORECASE | re.DOTALL
            )

            if name_match:
                patient_name = name_match.group(1).strip()

            Test_New_Patient_Workflow.generated_patient_name = patient_name

            self.logger.info(
                f"Patient Name: {patient_name}"
            )

            # ============================================================
            # EXTRACT MOBILE NUMBER
            # ============================================================

            mobile_no = ""

            mobile_match = re.search(
                r'(?:Mobile Number|MOBILE NO)\s*/?.*?:?\s*(\d{10})',
                pdf_text,
                re.IGNORECASE
            )

            if mobile_match:
                mobile_no = mobile_match.group(1)

            Test_New_Patient_Workflow.generated_mobile_no = mobile_no

            self.logger.info(
                f"Mobile Number: {mobile_no}"
            )

            # ====================================================
            # CLOSE PDF
            # ====================================================

            try:
                self.patient_reg.click_close_btn()
            except Exception:
                pass

            time.sleep(2)

            pyautogui.press("esc")

            time.sleep(2)

            # ====================================================
            # BARCODE
            # ====================================================

            try:

                barcode_text = (
                    self.patient_reg.get_barcode_blob()
                )

                self.logger.info(
                    "Barcode extracted successfully"
                )

            except Exception as e:

                self.logger.warning(
                    f"Barcode extraction failed: {e}"
                )

            try:
                self.patient_reg.click_close_btn()
            except Exception:
                pass

            # ====================================================
            # FINAL REGISTRATION DATA
            # ====================================================

            self.logger.info(
                "========================================"
            )

            self.logger.info(
                "REGISTRATION WORKFLOW DATA"
            )

            self.logger.info(
                f"Generated CRN: "
                f"{Test_New_Patient_Workflow.generated_crn}"
            )

            self.logger.info(
                f"Generated Patient Name: "
                f"{Test_New_Patient_Workflow.generated_patient_name}"
            )

            self.logger.info(
                f"Generated Mobile: "
                f"{Test_New_Patient_Workflow.generated_mobile_no}"
            )

            self.logger.info(
                "========================================"
            )

            LogGen.test_passed(
                self.logger,
                "test_new_registration"
            )

        except Exception as e:

            # IMPORTANT:
            # If registration fails, keep CRN as None.
            Test_New_Patient_Workflow.generated_crn = None

            self.logger.exception(
                f"Patient registration failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_new_registration"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_new_registration",
                str(e)
            )

            raise


    @pytest.mark.patient_registration_flow_part1
    def test_revisit_patient(self):

        # ========================================================
        # DETERMINE CRN / FLOW
        # ========================================================

        generated_crn = (
            Test_New_Patient_Workflow.generated_crn
        )

        if generated_crn:

            # ----------------------------------------------------
            # NORMAL REGISTRATION SCENARIO
            # ----------------------------------------------------

            pat_crn_number = generated_crn

            Test_New_Patient_Workflow.revisit_using_fallback = (
                False
            )

            self.logger.info(
                "Registration CRN found."
            )

            self.logger.info(
                f"Using newly generated CRN: "
                f"{pat_crn_number}"
            )

        else:

            # ----------------------------------------------------
            # FALLBACK SCENARIO
            # ----------------------------------------------------

            pat_crn_number = (
                Test_New_Patient_Workflow.revisit_hardcoded_crn
            )

            Test_New_Patient_Workflow.revisit_using_fallback = (
                True
            )

            # Store fallback CRN separately
            Test_New_Patient_Workflow.revisit_crn = (
                pat_crn_number
            )

            self.logger.warning(
                "No CRN generated during registration."
            )

            self.logger.warning(
                f"Using fallback CRN: "
                f"{pat_crn_number}"
            )

        LogGen.start_test(
            self.logger,
            "test_revisit_patient",
            "Patient Revisit"
        )

        try:

            # ====================================================
            # REFRESH
            # ====================================================

            self.driver.refresh()

            time.sleep(5)

            # ====================================================
            # OPEN REGISTRATION
            # ====================================================

            self.logger.info(
                "Opening Registration Module"
            )

            self.patient_reg.click_registration_module()

            time.sleep(2)

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            # ====================================================
            # SEARCH BY CRN
            # ====================================================

            self.logger.info(
                f"Searching patient using CRN: "
                f"{pat_crn_number}"
            )

            self.patient_reg.enter_search_value(
                pat_crn_number
            )

            time.sleep(3)

            # ====================================================
            # EXTRACT PATIENT NAME + MOBILE
            # ====================================================

            self.logger.info(
                "Extracting patient details from CRN search result"
            )

            (
                search_patient_name,
                search_mobile_number
            ) = (
                self.patient_reg
                .get_patient_details_from_search_result(
                    pat_crn_number
                )
            )

            self.logger.info(
                f"Search Result Patient Name: "
                f"{search_patient_name}"
            )

            self.logger.info(
                f"Search Result Mobile: "
                f"{search_mobile_number}"
            )

            # ====================================================
            # UPDATE SHARED WORKFLOW DATA
            # ====================================================

            if search_patient_name:
                Test_New_Patient_Workflow.generated_patient_name = (
                    search_patient_name
                )

            if search_mobile_number:
                Test_New_Patient_Workflow.generated_mobile_no = (
                    search_mobile_number
                )

            # ====================================================
            # DO NOT OVERWRITE generated_crn IN FALLBACK
            # ====================================================
            #
            # generated_crn = CRN generated by registration
            # revisit_crn   = fallback CRN
            # ====================================================

            if not Test_New_Patient_Workflow.revisit_using_fallback:
                Test_New_Patient_Workflow.generated_crn = (
                    pat_crn_number
                )

            # ====================================================
            # CREATE LOCAL VALUES
            # ====================================================

            pat_name = (
                Test_New_Patient_Workflow.generated_patient_name
            )

            pat_mobile_no = (
                Test_New_Patient_Workflow.generated_mobile_no
            )

            self.logger.info(
                "========================================"
            )

            self.logger.info(
                f"Final CRN: {pat_crn_number}"
            )

            self.logger.info(
                f"Final Patient Name: {pat_name}"
            )

            self.logger.info(
                f"Final Mobile: {pat_mobile_no}"
            )

            self.logger.info(
                f"Fallback Used: "
                f"{Test_New_Patient_Workflow.revisit_using_fallback}"
            )

            self.logger.info(
                "========================================"
            )

            # ====================================================
            # CLICK REVISIT
            # ====================================================

            self.logger.info(
                "Clicking Revisit button"
            )

            time.sleep(3)

            self.patient_reg.click_revisit_btn()

            time.sleep(3)

            self.logger.info(
                "Revisit button clicked"
            )

            # ====================================================
            # NEW DEPARTMENT REVISIT
            # ====================================================

            self.patient_reg.click_new_department_revisit_btn()

            time.sleep(3)

            self.logger.info(
                "New Department Revisit window opened"
            )

            # ====================================================
            # SELECT DEPARTMENT / UNIT
            # ====================================================

            self.logger.info(
                "Selecting department/unit for revisit"
            )

            opd_check = (
                self.patient_reg
                .select_department_until_save_success()
            )

            # ====================================================
            # VALIDATE RETURNED UNIT
            # ====================================================

            if not opd_check:
                raise AssertionError(
                    "select_department_until_save_success() "
                    "did not return an OPD unit."
                )

            opd_check = str(
                opd_check
            ).strip()

            self.logger.info(
                f"OPD Unit returned from selection method: "
                f"{opd_check!r}"
            )

            # ====================================================
            # STORE REVISIT OPD UNIT
            # ====================================================

            Test_New_Patient_Workflow.revisit_opd_unit_name = (
                opd_check
            )

            self.logger.info(
                f"Stored revisit OPD Unit: "
                f"{Test_New_Patient_Workflow.revisit_opd_unit_name!r}"
            )

            time.sleep(7)

            # ====================================================
            # CLOSE POPUPS
            # ====================================================

            pyautogui.press("esc")

            time.sleep(2)

            try:

                self.patient_reg.click_close_btn()

            except Exception as e:

                self.logger.warning(
                    f"Unable to close first popup: {e}"
                )

            time.sleep(2)

            pyautogui.press("esc")

            time.sleep(2)

            try:

                self.patient_reg.click_close_btn()

            except Exception as e:

                self.logger.warning(
                    f"Unable to close second popup: {e}"
                )

            time.sleep(5)

            # ====================================================
            # OPD VERIFICATION
            # ====================================================

            self.logger.info(
                "Starting OPD verification"
            )

            self.patient_reg.click_opd_module()

            time.sleep(2)

            self.patient_reg.click_opd_dr_desk()

            time.sleep(3)

            # ====================================================
            # SELECT OPD DEPARTMENT / UNIT
            # ====================================================

            self.logger.info(
                f"Selecting OPD Department/Unit: "
                f"{opd_check}"
            )

            self.patient_reg.select_opd_dr_desk_department(
                opd_check
            )

            time.sleep(3)

            # ====================================================
            # VERIFY PATIENT NAME
            # ====================================================

            if pat_name:

                self.logger.info(
                    f"Verifying patient in OPD: "
                    f"{pat_name}"
                )

                element = WebDriverWait(
                    self.driver,
                    10
                ).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f"//div[@class='mb-0'][contains("
                            f"translate(normalize-space(),"
                            f"'abcdefghijklmnopqrstuvwxyz',"
                            f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),"
                            f"'{pat_name.upper()}')]"
                        )
                    )
                )

                actual_name = (
                    element.text.strip()
                )

                self.logger.info(
                    f"Patient found in OPD: "
                    f"{actual_name}"
                )

                if actual_name.lower() != pat_name.lower():
                    raise AssertionError(
                        f"Patient name mismatch. "
                        f"Expected: {pat_name}, "
                        f"Found: {actual_name}"
                    )

                self.logger.info(
                    "Patient name verified successfully"
                )

            else:

                self.logger.warning(
                    "Patient name unavailable."
                )

                self.logger.warning(
                    "Skipping OPD patient-name verification."
                )

            # ====================================================
            # SUCCESS
            # ====================================================

            self.logger.info(
                f"Revisit completed successfully. "
                f"CRN: {pat_crn_number}"
            )

            self.logger.info(
                f"Revisit OPD Unit: {opd_check}"
            )

            LogGen.test_passed(
                self.logger,
                "test_revisit_patient"
            )

        except Exception as e:

            self.logger.exception(
                f"Patient revisit failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_revisit_patient"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_revisit_patient",
                str(e)
            )

            raise


    @pytest.mark.patient_registration_flow_part1
    def test_search_by_mobile_number(self):

        # IMPORTANT:
        # These values may have come from:
        #
        # 1. Successful registration
        # OR
        # 2. Fallback CRN search in revisit test

        pat_mobile_no = (
            Test_New_Patient_Workflow.generated_mobile_no
        )

        pat_name = (
            Test_New_Patient_Workflow.generated_patient_name
        )

        LogGen.start_test(
            self.logger,
            "test_search_by_mobile_number",
            "Patient Registration"
        )

        try:

            # ====================================================
            # VALIDATE TEST DATA
            # ====================================================

            if not pat_mobile_no:

                raise RuntimeError(
                    "No mobile number available for "
                    "mobile-number search."
                )

            if not pat_name:

                raise RuntimeError(
                    "No patient name available for "
                    "mobile-number search."
                )

            self.logger.info(
                "========================================"
            )

            self.logger.info(
                f"Mobile Number Used: {pat_mobile_no}"
            )

            self.logger.info(
                f"Patient Name Used: {pat_name}"
            )

            self.logger.info(
                "========================================"
            )

            # ====================================================
            # REFRESH
            # ====================================================

            self.driver.refresh()

            time.sleep(5)

            # ====================================================
            # OPEN REGISTRATION
            # ====================================================

            self.logger.info(
                "Opening Registration Module"
            )

            self.patient_reg.click_registration_module()

            time.sleep(2)

            self.logger.info(
                "Opening Patient Registration"
            )

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            # ====================================================
            # SEARCH BY MOBILE
            # ====================================================

            self.logger.info(
                f"Searching patient using mobile number: "
                f"{pat_mobile_no}"
            )

            self.patient_reg.enter_search_value(
                pat_mobile_no
            )

            time.sleep(3)

            # ====================================================
            # FIND PATIENT
            # ====================================================

            self.logger.info(
                "Waiting for patient record to appear"
            )

            element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//td[contains("
                        f"@class,"
                        f"'ant-table-cell-fix-left-last')]"
                        f"//span[translate("
                        f"normalize-space(text()),"
                        f"'abcdefghijklmnopqrstuvwxyz',"
                        f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ')="
                        f"'{pat_name.upper()}']"
                    )
                )
            )

            actual_name = (
                element.text.strip()
            )

            self.logger.info(
                f"Patient name displayed: "
                f"{actual_name}"
            )

            # ====================================================
            # ASSERT PATIENT NAME
            # ====================================================

            assert actual_name.lower() == (
                pat_name.lower()
            ), (
                f"Patient mismatch. "
                f"Expected: {pat_name}, "
                f"Actual: {actual_name}"
            )

            self.logger.info(
                "Patient name validation passed"
            )

            self.logger.info(
                f"Patient found successfully using "
                f"mobile number: {pat_mobile_no}"
            )

            LogGen.test_passed(
                self.logger,
                "test_search_by_mobile_number"
            )

        except Exception as e:

            try:

                Screenshot.capture(
                    self.driver,
                    "test_search_by_mobile_number"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_search_by_mobile_number",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_search_patient_by_name(self):

        # ============================================================
        # GET PATIENT NAME
        # ============================================================

        pat_name = Test_New_Patient_Workflow.generated_patient_name

        LogGen.start_test(
            self.logger,
            "test_search_patient_by_name",
            "Patient Registration"
        )

        try:

            # ========================================================
            # VALIDATE PATIENT NAME IS AVAILABLE
            # ========================================================

            if not pat_name:
                raise AssertionError(
                    "Patient name is not available. "
                    "Neither the newly registered patient nor the "
                    "fallback patient name was extracted."
                )

            self.logger.info(
                f"Patient name to search: {pat_name}"
            )

            # ========================================================
            # REFRESH PAGE
            # ========================================================

            self.logger.info(
                "Refreshing page before patient name search"
            )

            self.driver.refresh()

            time.sleep(5)

            # ========================================================
            # OPEN REGISTRATION MODULE
            # ========================================================

            self.logger.info(
                "Opening Registration Module"
            )

            self.patient_reg.click_registration_module()

            time.sleep(2)

            # ========================================================
            # OPEN PATIENT REGISTRATION
            # ========================================================

            self.logger.info(
                "Opening Patient Registration"
            )

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            # ========================================================
            # SEARCH PATIENT BY NAME
            # ========================================================

            self.logger.info(
                "Starting patient search by name"
            )

            self.logger.info(
                f"Entering patient name in search box: {pat_name}"
            )

            self.patient_reg.enter_search_value(
                pat_name
            )

            self.logger.info(
                f"Searching patient: {pat_name}"
            )

            time.sleep(3)

            # ========================================================
            # WAIT FOR PATIENT RECORD
            # ========================================================

            self.logger.info(
                "Waiting for patient record to appear in search results"
            )

            patient_xpath = (
                "//td[contains(@class,'ant-table-cell-fix-left-last')]"
                "//span["
                "translate("
                "normalize-space(text()),"
                "'abcdefghijklmnopqrstuvwxyz',"
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"
                ")="
                f"'{pat_name.upper()}'"
                "]"
            )

            element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        patient_xpath
                    )
                )
            )

            self.logger.info(
                "Patient record found in search results"
            )

            # ========================================================
            # EXTRACT ACTUAL NAME
            # ========================================================

            actual_name = element.text.strip()

            self.logger.info(
                f"Patient name displayed in listing: {actual_name}"
            )

            # ========================================================
            # ASSERT PATIENT NAME
            # ========================================================

            self.logger.info(
                "Validating searched patient name"
            )

            assert actual_name.lower() == pat_name.lower(), (
                f"Patient mismatch. "
                f"Expected: {pat_name}, "
                f"Actual: {actual_name}"
            )

            self.logger.info(
                "Patient name validation passed"
            )

            # ========================================================
            # SUCCESS
            # ========================================================

            self.logger.info(
                f"Patient found successfully in search: "
                f"{actual_name}"
            )

            LogGen.test_passed(
                self.logger,
                "test_search_patient_by_name"
            )

        except Exception as e:

            self.logger.exception(
                f"Patient search by name failed: {e}"
            )

            # ========================================================
            # SCREENSHOT
            # ========================================================

            if self.driver:

                try:

                    Screenshot.capture(
                        self.driver,
                        "test_search_patient_by_name"
                    )

                    self.logger.info(
                        "Failure screenshot captured successfully"
                    )

                except Exception as screenshot_error:

                    self.logger.error(
                        f"Screenshot error: {screenshot_error}"
                    )

            # ========================================================
            # TEST FAILED
            # ========================================================

            LogGen.test_failed(
                self.logger,
                "test_search_patient_by_name",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_print_duplicate_opd(self):

        # ============================================================
        # GET FINAL CRN
        # ============================================================
        # Normal flow:
        #     generated_crn -> newly generated CRN
        #
        # Fallback flow:
        #     revisit_crn -> hardcoded/fallback CRN
        #
        # Do NOT overwrite generated_crn during fallback.
        # ============================================================

        if Test_New_Patient_Workflow.revisit_using_fallback:

            pat_crn_number = (
                Test_New_Patient_Workflow.revisit_hardcoded_crn
            )

            self.logger.info(
                f"Fallback flow detected. "
                f"Using revisit CRN: {pat_crn_number}"
            )

        else:

            pat_crn_number = (
                Test_New_Patient_Workflow.generated_crn
            )

            self.logger.info(
                f"Normal registration flow detected. "
                f"Using generated CRN: {pat_crn_number}"
            )

        LogGen.start_test(
            self.logger,
            "test_print_duplicate_opd",
            "Patient Registration"
        )

        try:

            # ========================================================
            # VALIDATE CRN
            # ========================================================

            if not pat_crn_number:
                raise AssertionError(
                    "No CRN available for Duplicate OPD printing."
                )

            pat_crn_number = str(
                pat_crn_number
            ).strip()

            self.logger.info(
                f"Final CRN used for Duplicate OPD: "
                f"{pat_crn_number}"
            )

            self.logger.info(
                f"Fallback used during workflow: "
                f"{Test_New_Patient_Workflow.revisit_using_fallback}"
            )

            # ========================================================
            # SEARCH PATIENT USING FINAL CRN
            # ========================================================

            self.logger.info(
                "Opening Patient Registration page"
            )

            self.driver.refresh()

            time.sleep(3)

            # ========================================================
            # OPEN REGISTRATION MODULE
            # ========================================================

            self.logger.info(
                "Opening Registration Module"
            )

            self.patient_reg.click_registration_module()

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            # ========================================================
            # SEARCH PATIENT
            # ========================================================

            self.logger.info(
                f"Searching patient using CRN: "
                f"{pat_crn_number}"
            )

            self.patient_reg.enter_search_value(
                pat_crn_number
            )

            time.sleep(3)

            # ========================================================
            # VERIFY PATIENT EXISTS
            # ========================================================

            self.logger.info(
                "Verifying patient record exists before "
                "printing duplicate OPD"
            )

            WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//tr[@data-row-key='{pat_crn_number}']"
                    )
                )
            )

            self.logger.info(
                f"Patient found successfully using CRN: "
                f"{pat_crn_number}"
            )

            # ========================================================
            # OPEN PATIENT ACTION MENU
            # ========================================================

            self.logger.info(
                "Opening patient action menu"
            )

            self.patient_reg.click_3_dots_in_listing_page()

            self.logger.info(
                "Selecting Duplicate OPD option"
            )

            self.patient_reg.hover_click_duplicate_opd()

            time.sleep(5)

            # ========================================================
            # PRINT DUPLICATE OPD
            # ========================================================

            self.logger.info(
                "Clicking duplicate OPD print button"
            )

            self.patient_reg.click_duplicate_print_btn()

            self.logger.info(
                "Duplicate OPD print initiated"
            )

            time.sleep(7)

            pyautogui.press("esc")

            self.logger.info(
                "Closed print dialog"
            )

            # ========================================================
            # DUPLICATE OPD PDF
            # ========================================================

            self.logger.info(
                "Verifying duplicate OPD PDF"
            )

            time.sleep(3)

            duplicate_pdf_text = (
                self.patient_reg.get_blob_pdf_text()
            )

            self.logger.info(
                "Duplicate OPD PDF loaded successfully"
            )

            print(
                "========== DUPLICATE OPD PDF =========="
            )

            print(
                duplicate_pdf_text
            )

            print(
                "========================================"
            )

            # ========================================================
            # ASSERT CRN EXISTS
            # ========================================================

            assert "CRN :" in duplicate_pdf_text, (
                "CRN not found in duplicate OPD PDF"
            )

            # ========================================================
            # EXTRACT CRN FROM PDF
            # ========================================================

            duplicate_crn = (
                duplicate_pdf_text
                .split("CRN :", 1)[1]
                .split("NAME :", 1)[0]
                .strip()
            )

            # Normalize whitespace
            duplicate_crn = " ".join(
                duplicate_crn.split()
            )

            self.logger.info(
                f"Duplicate OPD PDF CRN: "
                f"{duplicate_crn}"
            )

            self.logger.info(
                f"Expected workflow CRN: "
                f"{pat_crn_number}"
            )

            # ========================================================
            # ASSERT CRN MATCHES FINAL WORKFLOW CRN
            # ========================================================

            assert duplicate_crn == pat_crn_number, (

                f"CRN mismatch in Duplicate OPD PDF | "
                f"Expected: {pat_crn_number} | "
                f"Actual: {duplicate_crn}"
            )

            self.logger.info(
                "Duplicate OPD CRN matched successfully"
            )

            # ========================================================
            # ASSERT DUPLICATE TEXT
            # ========================================================

            assert "OPD Card Duplicate" in duplicate_pdf_text, (

                "OPD Card Duplicate text not found in PDF"
            )

            self.logger.info(
                "'OPD Card Duplicate' text verified successfully"
            )

            # ========================================================
            # CLOSE PDF
            # ========================================================

            self.logger.info(
                "Closing duplicate OPD PDF"
            )

            self.patient_reg.click_close_btn()

            time.sleep(5)

            self.logger.info(
                "Duplicate OPD verification completed successfully"
            )

            # ========================================================
            # TEST PASSED
            # ========================================================

            LogGen.test_passed(
                self.logger,
                "test_print_duplicate_opd"
            )

        except Exception as e:

            # ========================================================
            # TEST FAILED
            # ========================================================

            self.logger.exception(
                f"Duplicate OPD test failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_print_duplicate_opd_failed"
                )

                self.logger.info(
                    "Failure screenshot captured successfully"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_print_duplicate_opd",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_print_duplicate_barcode(self):

        # ============================================================
        # GET FINAL CRN
        # ============================================================
        # Normal registration flow:
        #     generated_crn -> newly generated CRN
        #
        # Fallback flow:
        #     revisit_crn -> fallback CRN
        #
        # Do NOT overwrite generated_crn during fallback.
        # ============================================================

        if Test_New_Patient_Workflow.revisit_using_fallback:

            pat_crn_number = (
                Test_New_Patient_Workflow.revisit_hardcoded_crn
            )

            self.logger.info(
                f"Fallback flow detected. "
                f"Using revisit CRN: {pat_crn_number}"
            )

        else:

            pat_crn_number = (
                Test_New_Patient_Workflow.generated_crn
            )

            self.logger.info(
                f"Normal registration flow detected. "
                f"Using generated CRN: {pat_crn_number}"
            )

        LogGen.start_test(
            self.logger,
            "test_print_duplicate_barcode",
            "Patient Registration"
        )

        try:

            # ========================================================
            # VALIDATE CRN
            # ========================================================

            if not pat_crn_number:
                raise AssertionError(
                    "No CRN available for Duplicate Barcode printing."
                )

            pat_crn_number = str(
                pat_crn_number
            ).strip()

            self.logger.info(
                f"Final CRN used for Duplicate Barcode: "
                f"{pat_crn_number}"
            )

            self.logger.info(
                f"Fallback used during workflow: "
                f"{Test_New_Patient_Workflow.revisit_using_fallback}"
            )

            # ========================================================
            # NAVIGATE TO PATIENT REGISTRATION
            # ========================================================

            self.logger.info(
                "Refreshing page"
            )

            self.driver.refresh()

            time.sleep(5)

            # ========================================================
            # OPEN REGISTRATION MODULE
            # ========================================================

            self.logger.info(
                "Opening Registration Module"
            )

            self.patient_reg.click_registration_module()

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            # ========================================================
            # SEARCH PATIENT USING FINAL CRN
            # ========================================================

            self.logger.info(
                f"Searching patient using CRN: "
                f"{pat_crn_number}"
            )

            self.patient_reg.enter_search_value(
                pat_crn_number
            )

            time.sleep(3)

            # ========================================================
            # VERIFY PATIENT EXISTS
            # ========================================================

            self.logger.info(
                "Verifying patient record exists before "
                "printing duplicate barcode"
            )

            WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//tr[@data-row-key='{pat_crn_number}']"
                    )
                )
            )

            self.logger.info(
                f"Patient found successfully using CRN: "
                f"{pat_crn_number}"
            )

            # ========================================================
            # OPEN PATIENT ACTION MENU
            # ========================================================

            self.logger.info(
                "Opening patient action menu"
            )

            self.patient_reg.click_3_dots_in_listing_page()

            self.logger.info(
                "Opening barcode print option"
            )

            self.patient_reg.hover_click_barcode_print()

            time.sleep(5)

            # ========================================================
            # PRINT BARCODE
            # ========================================================

            self.logger.info(
                "Clicking barcode print button"
            )

            self.patient_reg.click_barcode_btn()

            self.logger.info(
                "Duplicate barcode generated"
            )

            time.sleep(7)

            pyautogui.press("esc")

            self.logger.info(
                "Closed print dialog"
            )

            # ========================================================
            # BARCODE VERIFICATION
            # ========================================================

            self.logger.info(
                "Verifying duplicate barcode"
            )

            time.sleep(5)

            duplicate_barcode_text = (
                self.patient_reg.get_barcode_blob()
            )

            self.logger.info(
                "Duplicate barcode content retrieved successfully"
            )

            print(
                "========== DUPLICATE BARCODE =========="
            )

            print(
                duplicate_barcode_text
            )

            print(
                "======================================="
            )

            # ========================================================
            # ASSERT CRN EXISTS IN BARCODE
            # ========================================================

            assert pat_crn_number in duplicate_barcode_text, (

                f"Barcode CRN mismatch | "
                f"Expected CRN: {pat_crn_number}"
            )

            self.logger.info(
                f"CRN verified successfully in duplicate barcode: "
                f"{pat_crn_number}"
            )

            # ========================================================
            # CLOSE BARCODE
            # ========================================================

            self.logger.info(
                "Closing duplicate barcode window"
            )

            self.patient_reg.click_close_btn()

            time.sleep(5)

            self.logger.info(
                "Duplicate barcode verification completed successfully"
            )

            # ========================================================
            # TEST PASSED
            # ========================================================

            LogGen.test_passed(
                self.logger,
                "test_print_duplicate_barcode"
            )

        except Exception as e:

            self.logger.exception(
                f"Duplicate barcode test failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_print_duplicate_barcode_failed"
                )

                self.logger.info(
                    "Failure screenshot captured successfully"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_print_duplicate_barcode",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_change_patient_category(self):

        # ============================================================
        # CRN SELECTION
        # ============================================================

        generated_crn = (
            Test_New_Patient_Workflow.generated_crn
        )

        if generated_crn:

            pat_crn_number = generated_crn

            self.logger.info(
                f"Registration CRN found. "
                f"Using newly generated CRN: {pat_crn_number}"
            )

            using_fallback = False

        else:

            pat_crn_number = (
                Test_New_Patient_Workflow.revisit_hardcoded_crn
            )

            self.logger.warning(
                "No CRN generated during registration."
            )

            self.logger.warning(
                f"Using fallback CRN: {pat_crn_number}"
            )

            using_fallback = True

        # ============================================================
        # GENERATE CATEGORY VERIFICATION ID
        # ============================================================

        random_category_id = (
            TestDataGenerator.generate_four_digit_number()
        )

        LogGen.start_test(
            self.logger,
            "test_change_patient_category",
            "Patient Registration"
        )

        self.logger.info(
            "===================================="
        )

        self.logger.info(
            f"CRN Used: {pat_crn_number}"
        )

        self.logger.info(
            f"Using Fallback CRN: {using_fallback}"
        )

        self.logger.info(
            f"Category Verification ID: {random_category_id}"
        )

        self.logger.info(
            "===================================="
        )

        try:

            # ========================================================
            # NAVIGATE TO PATIENT REGISTRATION
            # ========================================================

            self.logger.info(
                "Navigating to Patient Registration page"
            )

            self.driver.refresh()

            time.sleep(4)

            # ========================================================
            # OPEN REGISTRATION MODULE
            # ========================================================

            self.logger.info(
                "Opening Registration Module"
            )

            self.patient_reg.click_registration_module()

            time.sleep(2)

            self.patient_reg.click_patient_registration_option()

            self.logger.info(
                "Patient Registration page opened"
            )

            time.sleep(3)

            # ========================================================
            # SEARCH PATIENT BY CRN
            # ========================================================

            self.logger.info(
                f"Searching patient using CRN: {pat_crn_number}"
            )

            self.patient_reg.enter_search_value(
                pat_crn_number
            )

            time.sleep(3)

            self.logger.info(
                f"CRN search completed: {pat_crn_number}"
            )

            # ========================================================
            # OPTIONAL: VERIFY SEARCH RESULT EXISTS
            # ========================================================

            self.logger.info(
                "Waiting for patient search result"
            )

            patient_row = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//tr[@data-row-key='{pat_crn_number}']"
                    )
                )
            )

            self.logger.info(
                f"Patient record found for CRN: {pat_crn_number}"
            )

            # ========================================================
            # OPEN PATIENT ACTION MENU
            # ========================================================

            self.logger.info(
                "Opening patient action menu"
            )

            self.patient_reg.click_3_dots_in_listing_page()

            self.logger.info(
                "Patient action menu opened successfully"
            )

            # ========================================================
            # CHANGE PATIENT CATEGORY
            # ========================================================

            self.logger.info(
                "Opening Change Patient Category option"
            )

            self.patient_reg.hover_click_change_patient_category()

            time.sleep(5)

            self.logger.info(
                "Change Patient Category popup opened"
            )

            # ========================================================
            # SELECT NEW CATEGORY
            # ========================================================

            self.logger.info(
                "Selecting new patient category"
            )

            expected_category = (
                self.patient_reg.select_random_patient_category()
            )

            self.logger.info(
                f"Selected category: {expected_category}"
            )

            print(
                f"Selected category: {expected_category}"
            )

            time.sleep(3)

            # ========================================================
            # CATEGORY VERIFICATION ID
            # ========================================================

            self.logger.info(
                f"Entering category verification ID: "
                f"{random_category_id}"
            )

            self.patient_reg.enter_category_verification(
                random_category_id
            )

            # ========================================================
            # RECOMMENDED BY
            # ========================================================

            self.logger.info(
                "Selecting Recommended By user"
            )

            self.patient_reg.select_random_recommended_by()

            self.logger.info(
                "Recommended By selected successfully"
            )

            # ========================================================
            # APPROVED BY
            # ========================================================

            self.logger.info(
                "Selecting Approved By user"
            )

            self.patient_reg.select_random_approved_by()

            self.logger.info(
                "Approved By selected successfully"
            )

            # ========================================================
            # SAVE CATEGORY CHANGE
            # ========================================================

            self.logger.info(
                "Submitting patient category change request"
            )

            self.patient_reg.click_change_cat_save_btn()

            self.logger.info(
                "Patient category change submitted"
            )

            # ========================================================
            # SUCCESS MESSAGE VERIFY
            # ========================================================

            self.logger.info(
                "Waiting for success confirmation message"
            )

            success_msg = WebDriverWait(
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

            actual_msg = (
                success_msg.text.strip()
            )

            self.logger.info(
                f"Success message received: {actual_msg}"
            )

            # ========================================================
            # ASSERTION
            # ========================================================

            assert actual_msg == (
                "Patient Category Changed Successfully !!"
            ), (
                f"Unexpected success message | "
                f"Expected: Patient Category Changed Successfully !! | "
                f"Actual: {actual_msg}"
            )

            self.logger.info(
                "Patient category changed successfully"
            )

            # ========================================================
            # FINAL LOG
            # ========================================================

            self.logger.info(
                "===================================="
            )

            self.logger.info(
                "CHANGE PATIENT CATEGORY COMPLETED"
            )

            self.logger.info(
                f"CRN Used: {pat_crn_number}"
            )

            self.logger.info(
                f"Fallback Used: {using_fallback}"
            )

            self.logger.info(
                f"New Category: {expected_category}"
            )

            self.logger.info(
                "===================================="
            )

            LogGen.test_passed(
                self.logger,
                "test_change_patient_category"
            )

        except Exception as e:

            self.logger.exception(
                f"Change Patient Category failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_change_patient_category_failed"
                )

                self.logger.info(
                    "Failure screenshot captured successfully"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_change_patient_category",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_modify_mobile_number(self):

        # ============================================================
        # CRN SELECTION
        # ============================================================

        generated_crn = (
            Test_New_Patient_Workflow.generated_crn
        )

        if generated_crn:

            pat_crn_number = generated_crn

            self.logger.info(
                f"Registration CRN found. "
                f"Using newly generated CRN: {pat_crn_number}"
            )

            using_fallback = False

        else:

            pat_crn_number = (
                Test_New_Patient_Workflow.revisit_hardcoded_crn
            )

            self.logger.warning(
                "No CRN generated during registration."
            )

            self.logger.warning(
                f"Using fallback CRN: {pat_crn_number}"
            )

            using_fallback = True

        # ============================================================
        # OLD MOBILE NUMBER
        # ============================================================

        pat_mobile_no = (
            Test_New_Patient_Workflow.generated_mobile_no
        )

        if not pat_mobile_no:
            self.logger.warning(
                "No mobile number stored from previous test."
            )

        # ============================================================
        # GENERATE NEW MOBILE NUMBER
        # ============================================================

        updated_number = (
            TestDataGenerator.generate_mobile_number()
        )

        # ============================================================
        # TEST START
        # ============================================================

        LogGen.start_test(
            self.logger,
            "test_modify_mobile_number",
            "Patient Registration"
        )

        self.logger.info(
            "===================================="
        )

        self.logger.info(
            f"CRN Used: {pat_crn_number}"
        )

        self.logger.info(
            f"Using Fallback CRN: {using_fallback}"
        )

        self.logger.info(
            f"Old Mobile: {pat_mobile_no}"
        )

        self.logger.info(
            f"Updated Mobile: {updated_number}"
        )

        self.logger.info(
            "===================================="
        )

        try:
            # ========================================================
            # OPEN PATIENT REGISTRATION
            # ========================================================

            self.logger.info(
                "Opening patient modification"
            )

            self.driver.refresh()
            time.sleep(3)

            self.patient_reg.click_registration_module()

            time.sleep(2)

            self.patient_reg.click_patient_mobile_modification_option()

            self.logger.info(
                "Opened Patient Registration page"
            )

            time.sleep(3)

            # ========================================================
            # SEARCH PATIENT BY CRN
            # ========================================================

            self.logger.info(
                f"Searching patient using CRN: {pat_crn_number}"
            )

            self.patient_reg.enter_search_cr_no_value(
                pat_crn_number
            )

            time.sleep(3)

            self.logger.info(
                f"CRN search completed: {pat_crn_number}"
            )

            # ========================================================
            # ENTER NEW MOBILE NUMBER
            # ========================================================

            self.logger.info(
                f"Updating mobile number to: {updated_number}"
            )

            self.patient_reg.enter_update_mobile_number(
                updated_number
            )

            # ========================================================
            # MODIFY
            # ========================================================

            self.logger.info(
                "Clicking Modify button"
            )

            self.patient_reg.click_modify_btn()

            time.sleep(2)

            # ========================================================
            # CONFIRM UPDATE
            # ========================================================

            self.logger.info(
                "Confirming mobile number update"
            )

            self.patient_reg.click_yes_pop_up()

            # ========================================================
            # SUCCESS MESSAGE
            # ========================================================

            self.logger.info(
                "Waiting for mobile update success message"
            )

            success_msg = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container' "
                        "and normalize-space()="
                        "'Patient Mobile Number successfully updated!!']"
                    )
                )
            )

            actual_message = (
                success_msg.text.strip()
            )

            self.logger.info(
                f"Success message received: {actual_message}"
            )

            # ========================================================
            # ASSERT SUCCESS MESSAGE
            # ========================================================

            assert actual_message == (
                "Patient Mobile Number successfully updated!!"
            ), (
                f"Unexpected message | "
                f"Expected: "
                f"Patient Mobile Number successfully updated!! | "
                f"Actual: {actual_message}"
            )

            self.logger.info(
                "Mobile number update success message verified"
            )

            time.sleep(5)

            # ========================================================
            # VERIFY UPDATED MOBILE
            # ========================================================

            self.logger.info(
                "Starting updated mobile number verification"
            )

            self.driver.refresh()
            time.sleep(4)

            self.patient_reg.click_registration_module()

            time.sleep(2)

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            # ========================================================
            # SEARCH USING UPDATED MOBILE
            # ========================================================

            self.logger.info(
                f"Searching patient using updated mobile: "
                f"{updated_number}"
            )

            self.patient_reg.enter_search_value(
                updated_number
            )

            time.sleep(5)

            # ========================================================
            # VERIFY SEARCH RESULT
            # ========================================================

            self.logger.info(
                "Waiting for patient record after mobile search"
            )

            WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//table//tbody//tr"
                    )
                )
            )

            self.logger.info(
                "Patient record found using updated mobile number"
            )

            # ========================================================
            # SCROLL TABLE RIGHT
            # ========================================================

            self.logger.info(
                "Scrolling table to mobile number column"
            )

            self.patient_reg.scroll_table_right()

            time.sleep(2)

            # ========================================================
            # GET UPDATED MOBILE
            # ========================================================

            self.logger.info(
                "Fetching updated mobile number from listing"
            )

            actual_mobile_number = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//tr[@rowindex='0']//td[10]//span"
                    )
                )
            ).text.strip()

            self.logger.info(
                f"Mobile number displayed in listing: "
                f"{actual_mobile_number}"
            )

            # ========================================================
            # ASSERT UPDATED MOBILE
            # ========================================================

            self.logger.info(
                "Validating updated mobile number"
            )

            assert actual_mobile_number == updated_number, (
                f"Mobile mismatch | "
                f"Expected: {updated_number} | "
                f"Actual: {actual_mobile_number}"
            )

            self.logger.info(
                "Updated mobile number verified successfully"
            )

            # ========================================================
            # UPDATE STORED MOBILE FOR FUTURE TEST CASES
            # ========================================================

            Test_New_Patient_Workflow.generated_mobile_no = (
                updated_number
            )

            self.logger.info(
                f"Stored updated mobile number for future tests: "
                f"{updated_number}"
            )

            # ========================================================
            # FINAL SUCCESS
            # ========================================================

            self.logger.info(
                "===================================="
            )

            self.logger.info(
                "MODIFY MOBILE NUMBER COMPLETED"
            )

            self.logger.info(
                f"CRN Used: {pat_crn_number}"
            )

            self.logger.info(
                f"Updated Mobile: {updated_number}"
            )

            self.logger.info(
                f"Fallback Used: {using_fallback}"
            )

            self.logger.info(
                "===================================="
            )

            LogGen.test_passed(
                self.logger,
                "test_modify_mobile_number"
            )

        except Exception as e:

            self.logger.exception(
                f"Modify mobile number failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_modify_mobile_number_failed"
                )

                self.logger.info(
                    "Failure screenshot captured successfully"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_modify_mobile_number",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_patient_update(self):

        # ============================================================
        # CRN SELECTION
        # ============================================================

        if Test_New_Patient_Workflow.revisit_using_fallback:

            # --------------------------------------------------------
            # FALLBACK FLOW
            # --------------------------------------------------------
            pat_crn_number = (
                Test_New_Patient_Workflow.revisit_hardcoded_crn
            )

            self.logger.info(
                "Fallback flow detected."
            )

            self.logger.info(
                f"Using fallback/revisit CRN: "
                f"{pat_crn_number}"
            )

        else:

            # --------------------------------------------------------
            # NORMAL REGISTRATION FLOW
            # --------------------------------------------------------
            pat_crn_number = (
                Test_New_Patient_Workflow.generated_crn
            )

            self.logger.info(
                "Normal registration flow detected."
            )

            self.logger.info(
                f"Using generated CRN: "
                f"{pat_crn_number}"
            )

        # ============================================================
        # START TEST
        # ============================================================

        LogGen.start_test(
            self.logger,
            "test_patient_update",
            "Patient Registration"
        )

        self.logger.info(
            "===================================="
        )

        self.logger.info(
            f"CRN Number Used: {pat_crn_number}"
        )

        self.logger.info(
            "===================================="
        )

        try:

            # ========================================================
            # VERIFY CRN IS AVAILABLE
            # ========================================================

            if not pat_crn_number:
                raise AssertionError(
                    "No CRN available for patient update. "
                    "Neither generated CRN nor fallback/revisit CRN was stored."
                )

            # Convert CRN to string so XPath/search works consistently
            pat_crn_number = str(
                pat_crn_number
            ).strip()

            self.logger.info(
                f"Final CRN selected for patient update: "
                f"{pat_crn_number}"
            )

            # ========================================================
            # UPDATE PATIENT
            # ========================================================

            time.sleep(2)

            self.logger.info(
                f"Updating patient with CRN: "
                f"{pat_crn_number}"
            )

            # ========================================================
            # OPEN ACTION MENU
            # ========================================================
            #
            # self.logger.info(
            #     "Opening patient action menu"
            # )
            #
            # self.patient_reg.click_3_dots_in_listing_page()
            #
            # self.logger.info(
            #     "Three dots menu opened successfully"
            # )
            #
            # # ========================================================
            # # OPEN PATIENT DETAIL MODIFICATION
            # # ========================================================
            #
            # self.logger.info(
            #     "Opening Patient Detail Modification"
            # )
            #
            # self.patient_reg.hover_click_patient_detail_modification()
            #
            # self.logger.info(
            #     "Patient Detail Modification screen opened"
            # )

            # ========================================================
            # OPEN QUICK PATIENT MODIFICATION
            # ========================================================

            self.driver.refresh()

            time.sleep(5)

            self.patient_reg.click_registration_module()

            self.logger.info(
                "Opening Patient Registration"
            )

            self.patient_reg.click_quick_patient_modification_option()

            time.sleep(5)

            # ========================================================
            # ENTER CRN
            # ========================================================

            self.logger.info(
                f"Entering CRN for patient modification: "
                f"{pat_crn_number}"
            )

            self.patient_reg.enter_crn_number_for_audit(
                pat_crn_number
            )

            # ========================================================
            # UPDATE PATIENT NAME
            # ========================================================

            self.logger.info(
                "Updating patient first name"
            )

            self.patient_reg.enter_update_patient_name(
                "One"
            )

            self.logger.info(
                "Entered suffix 'One' in patient first name field"
            )

            # ========================================================
            # GET UPDATED NAME FROM TEXTBOX
            # ========================================================

            updated_name = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//input[@id='firstName']"
                    )
                )
            ).get_attribute("value").strip()

            Test_New_Patient_Workflow.generated_updated_name = (
                updated_name
            )

            self.logger.info(
                f"Updated patient name captured: "
                f"{updated_name}"
            )

            # ========================================================
            # CLICK MODIFY
            # ========================================================

            self.logger.info(
                "Clicking Modify button"
            )

            self.patient_reg.click_modify_btn()

            self.logger.info(
                "Modify button clicked successfully"
            )

            # ========================================================
            # UPDATE SUCCESS MESSAGE
            # ========================================================

            self.logger.info(
                "Waiting for patient update success message"
            )

            success_msg = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container' "
                        "and normalize-space()="
                        "'Patient details successfully updated']"
                    )
                )
            )

            actual_success_message = (
                success_msg.text.strip()
            )

            self.logger.info(
                f"Success popup message: "
                f"{actual_success_message}"
            )

            # ========================================================
            # ASSERT SUCCESS MESSAGE
            # ========================================================

            assert actual_success_message == (
                "Patient details successfully updated"
            ), (
                f"Unexpected update message | "
                f"Expected: Patient details successfully updated | "
                f"Actual: {actual_success_message}"
            )

            self.logger.info(
                "Patient update success message verified"
            )

            time.sleep(7)

            # ========================================================
            # VERIFY UPDATED NAME
            # ========================================================

            self.logger.info(
                "Starting updated patient name verification"
            )

            # If the popup is still open, close it
            try:

                pyautogui.press("esc")

                time.sleep(2)

            except Exception:

                pass

            # ========================================================
            # SEARCH PATIENT USING CRN
            # ========================================================

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            self.logger.info(
                f"Searching patient using CRN: "
                f"{pat_crn_number}"
            )

            self.patient_reg.enter_search_value(
                pat_crn_number
            )

            time.sleep(4)

            # ========================================================
            # FIND PATIENT ROW USING CRN
            # ========================================================

            self.logger.info(
                f"Waiting for patient row with CRN: "
                f"{pat_crn_number}"
            )

            patient_row = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//tr[@data-row-key='{pat_crn_number}']"
                    )
                )
            )

            self.logger.info(
                "Patient row found successfully"
            )

            # ========================================================
            # GET PATIENT NAME FROM SAME ROW
            # ========================================================

            actual_name = WebDriverWait(
                patient_row,
                10
            ).until(
                lambda row: row.find_element(
                    By.XPATH,
                    ".//td[contains("
                    "@class,"
                    "'ant-table-cell-fix-left-last'"
                    ")]//span"
                )
            ).text.strip()

            self.logger.info(
                f"Expected Updated Name: "
                f"{updated_name}"
            )

            self.logger.info(
                f"Actual Name From Listing: "
                f"{actual_name}"
            )

            # ========================================================
            # ASSERT UPDATED NAME
            # ========================================================

            assert actual_name.lower() == (
                updated_name.lower()
            ), (
                f"Patient name mismatch | "
                f"CRN: {pat_crn_number} | "
                f"Expected: {updated_name} | "
                f"Actual: {actual_name}"
            )

            self.logger.info(
                "Updated patient name verified successfully"
            )

            # ========================================================
            # AUDIT TRAIL
            # ========================================================

            self.logger.info(
                "Opening Patient Audit Trail"
            )

            self.patient_reg.click_patient_audit_trail_option()

            self.logger.info(
                "Patient Audit Trail option clicked"
            )

            time.sleep(2)

            # ========================================================
            # ENTER CRN FOR AUDIT
            # ========================================================

            self.logger.info(
                f"Entering CRN for audit trail: "
                f"{pat_crn_number}"
            )

            self.patient_reg.enter_crn_number_for_audit(
                pat_crn_number
            )

            time.sleep(5)

            self.logger.info(
                "Audit trail opened successfully"
            )

            time.sleep(7)

            # ========================================================
            # FINAL SUCCESS
            # ========================================================

            self.logger.info(
                "===================================="
            )

            self.logger.info(
                "PATIENT UPDATE WORKFLOW COMPLETED"
            )

            self.logger.info(
                f"CRN: {pat_crn_number}"
            )

            self.logger.info(
                f"Updated Name: {actual_name}"
            )

            self.logger.info(
                "===================================="
            )

            LogGen.test_passed(
                self.logger,
                "test_patient_update"
            )

        except Exception as e:

            # ========================================================
            # FAILURE LOGGING
            # ========================================================

            self.logger.exception(
                f"Patient update failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_patient_update_failed"
                )

                self.logger.info(
                    "Failure screenshot captured successfully"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: "
                    f"{screenshot_error}"
                )

            self.logger.error(
                "========== TEST FAILED =========="
            )

            self.logger.error(
                f"CRN Number: "
                f"{pat_crn_number}"
            )

            self.logger.error(
                f"Updated Name: "
                f"{locals().get('updated_name', 'Not Generated')}"
            )

            self.logger.error(
                f"Actual Name: "
                f"{locals().get('actual_name', 'Not Available')}"
            )

            LogGen.test_failed(
                self.logger,
                "test_patient_update",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_reg_to_rx_flow(self):

        # ============================================================
        # GET PATIENT DATA
        # ============================================================

        pat_name = (
            Test_New_Patient_Workflow.generated_patient_name
        )

        pat_updated_name = (
            Test_New_Patient_Workflow.generated_updated_name
        )

        # ============================================================
        # GET OPD UNIT
        # ============================================================
        #
        # IMPORTANT:
        # If registration succeeded, opd_unit_name will exist.
        #
        # If registration failed and fallback CRN was used,
        # test_revisit_patient stored the unit in
        # revisit_opd_unit_name.
        #
        # Therefore we prefer revisit_opd_unit_name.
        # ============================================================

        revisit_opd_unit = (
            Test_New_Patient_Workflow.revisit_opd_unit_name
        )

        original_opd_unit = (
            Test_New_Patient_Workflow.opd_unit_name
        )

        if revisit_opd_unit:

            pat_opd_unit = revisit_opd_unit

            self.logger.info(
                f"Using OPD Unit obtained from revisit: "
                f"{pat_opd_unit}"
            )

        elif original_opd_unit:

            pat_opd_unit = original_opd_unit

            self.logger.info(
                f"Revisit OPD Unit not available. "
                f"Using registration OPD Unit: {pat_opd_unit}"
            )

        else:

            raise AssertionError(
                "OPD Unit is not available from either "
                "registration or revisit."
            )

        # ============================================================
        # START TEST
        # ============================================================

        LogGen.start_test(
            self.logger,
            "test_reg_to_rx_flow",
            "Patient Registration"
        )

        self.logger.info(
            "============================================"
        )

        self.logger.info(
            "REGISTRATION TO RX FLOW"
        )

        self.logger.info(
            f"OPD Unit: {pat_opd_unit}"
        )

        self.logger.info(
            f"Patient Name: {pat_name}"
        )

        self.logger.info(
            f"Updated Patient Name: {pat_updated_name}"
        )

        self.logger.info(
            "============================================"
        )

        try:

            # ========================================================
            # REFRESH
            # ========================================================

            self.logger.info(
                "Refreshing page"
            )

            self.driver.refresh()

            time.sleep(4)

            self.logger.info(
                "Page refreshed successfully"
            )

            # ========================================================
            # GET LOGGED-IN CONSULTANT
            # ========================================================

            act_username_text = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//a[contains(@class,'dropdown-toggle')]"
                    )
                )
            ).text.strip()

            self.logger.info(
                f"Logged in consultant: {act_username_text}"
            )

            # ========================================================
            # OPD FLOW
            # ========================================================

            self.logger.info(
                "============================================"
            )

            self.logger.info(
                "STARTING OPD FLOW"
            )

            self.logger.info(
                f"Selecting OPD Unit: {pat_opd_unit}"
            )

            self.patient_reg.click_opd_module()

            self.logger.info(
                "Clicked OPD module"
            )

            self.patient_reg.click_opd_dr_desk()

            self.logger.info(
                "Opened OPD Doctor Desk"
            )

            time.sleep(3)

            # ========================================================
            # SELECT OPD UNIT
            # ========================================================

            self.patient_reg.select_opd_dr_desk_unit(
                pat_opd_unit
            )

            time.sleep(3)

            self.logger.info(
                f"OPD Unit selected successfully: "
                f"{pat_opd_unit}"
            )

            # ========================================================
            # SEARCH PATIENT IN OPD
            # ========================================================

            # Prefer updated name because patient_update may
            # have changed the patient's name.
            #
            # If updated name is not available, use the
            # currently stored patient name.

            search_name = (
                pat_updated_name
                if pat_updated_name
                else pat_name
            )

            if not search_name:
                raise AssertionError(
                    "Patient name is not available for OPD search."
                )

            self.logger.info(
                f"Searching patient in OPD using name: "
                f"{search_name}"
            )

            self.patient_reg.enter_search_name_in_opd(
                search_name
            )

            time.sleep(3)

            # ========================================================
            # VERIFY PATIENT IN OPD
            # ========================================================

            self.logger.info(
                "Waiting for patient to appear in OPD listing"
            )

            element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains("
                        f"translate(normalize-space(text()),"
                        f"'abcdefghijklmnopqrstuvwxyz',"
                        f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),"
                        f"'{search_name.upper()}')]"
                    )
                )
            )

            assert element.is_displayed(), (
                f"Patient '{search_name}' "
                f"is not displayed in OPD."
            )

            actual_opd_name = (
                element.text.strip()
            )

            self.logger.info(
                f"Patient found in OPD: "
                f"{actual_opd_name}"
            )

            self.logger.info(
                "Patient OPD verification passed"
            )

            # ========================================================
            # RX FLOW
            # ========================================================

            self.logger.info(
                "============================================"
            )

            self.logger.info(
                "STARTING RX FLOW"
            )

            self.patient_reg.click_rx_btn()

            self.logger.info(
                "RX screen opened successfully"
            )

            time.sleep(3)

            # ========================================================
            # RX TEST DATA
            # ========================================================

            chief_complaint = "Fever"
            diagnosis_code = "R50.9"
            instruction = "After Meal"
            followup_days = "5"

            self.logger.info(
                f"Chief Complaint: {chief_complaint}"
            )

            self.logger.info(
                f"Diagnosis Code: {diagnosis_code}"
            )

            self.logger.info(
                f"Instruction: {instruction}"
            )

            self.logger.info(
                f"Follow-up Days: {followup_days}"
            )

            # ========================================================
            # CHIEF COMPLAINT
            # ========================================================

            self.patient_reg.enter_chief_comp(
                chief_complaint
            )

            time.sleep(2)

            self.patient_reg.click_chief_comp_add()

            time.sleep(2)

            self.logger.info(
                "Chief complaint added successfully"
            )

            # ========================================================
            # DIAGNOSIS
            # ========================================================

            self.patient_reg.enter_diagnosis(
                diagnosis_code
            )

            time.sleep(2)

            self.patient_reg.click_diagnosis_add()

            time.sleep(2)

            self.logger.info(
                "Diagnosis added successfully"
            )

            time.sleep(2)

            self.patient_reg.click_investigation_tab()

            self.logger.info(
                "Investigation tab opened"
            )

            time.sleep(2)

            test_name = (
                self.patient_reg.select_random_test_name()
            )

            self.logger.info(
                f"Investigation selected: {test_name}"
            )

            time.sleep(2)

            self.patient_reg.enter_clinical_indication(
                "test"
            )

            self.logger.info(
                "Clinical indication entered"
            )

            time.sleep(2)

            self.patient_reg.enter_clinical_history(
                "Test"
            )

            self.logger.info(
                "Clinical history entered"
            )

            time.sleep(2)

            self.patient_reg.click_test_add_btn()

            self.logger.info(
                "Investigation added successfully"
            )

            time.sleep(2)

            drug_name = (
                self.patient_reg.select_random_drug_name()
            )

            self.logger.info(
                f"Drug selected: {drug_name}"
            )

            time.sleep(2)

            dose_name = (
                self.patient_reg.select_random_dose()
            )

            time.sleep(2)

            frequency_name = (
                self.patient_reg.select_random_frequency()
            )

            time.sleep(2)

            self.patient_reg.click_drug_add_btn()

            self.logger.info(
                "Medicine added successfully"
            )

            # ========================================================
            # RX PREVIEW
            # ========================================================

            self.patient_reg.click_preview_save_btn()

            self.logger.info(
                "RX Preview generated successfully"
            )

            time.sleep(5)

            patient_data = (
                self.patient_reg.get_patient_from_pet_reg_details()
            )

            print(patient_data)

            self.logger.info(
                "Patient details extracted from RX Preview"
            )

            # ========================================================
            # RX PREVIEW VALIDATION
            # ========================================================

            self.logger.info(
                "============================================"
            )

            self.logger.info(
                "STARTING RX PREVIEW VALIDATION"
            )

            # --------------------------------------------------------
            # DRUG VALIDATION
            # --------------------------------------------------------

            assert any(
                drug["Drug Name"].upper()
                in drug_name.upper()
                for drug in patient_data["Drugs"]
            ), (
                f"Drug mismatch | "
                f"Expected: {drug_name} | "
                f"Actual: {patient_data['Drugs']}"
            )

            self.logger.info(
                "Drug name verified successfully"
            )

            # --------------------------------------------------------
            # CONSULTANT VALIDATION
            # --------------------------------------------------------

            expected_consultant_name = (
                act_username_text
            )

            actual_consultant_name = (
                patient_data["Consultant Name"]
                .strip()
            )

            assert (
                    actual_consultant_name.upper()
                    ==
                    expected_consultant_name.upper()
            ), (
                f"Consultant mismatch | "
                f"Expected: {expected_consultant_name} | "
                f"Actual: {actual_consultant_name}"
            )

            self.logger.info(
                f"Consultant verified successfully: "
                f"{actual_consultant_name}"
            )

            self.logger.info(
                "RX Preview validation completed successfully"
            )

            # ========================================================
            # SAVE RX
            # ========================================================

            self.patient_reg.click_rx_save_btn()

            self.logger.info(
                "RX saved successfully"
            )

            # ========================================================
            # FINAL SUCCESS
            # ========================================================

            self.logger.info(
                "============================================"
            )

            self.logger.info(
                "REGISTRATION TO RX FLOW COMPLETED"
            )

            self.logger.info(
                f"Final OPD Unit: {pat_opd_unit}"
            )

            self.logger.info(
                f"Final Patient Name: {search_name}"
            )

            self.logger.info(
                "============================================"
            )

            LogGen.test_passed(
                self.logger,
                "test_reg_to_rx_flow"
            )

        except Exception as e:

            self.logger.exception(
                f"Registration to RX flow failed: {e}"
            )

            try:

                Screenshot.capture(
                    self.driver,
                    "test_reg_to_rx_flow_TC_011"
                )

                self.logger.info(
                    "Failure screenshot captured successfully"
                )

            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_reg_to_rx_flow",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_search_and_create_patient(self):

        not_reg_user = TestDataGenerator.generate_not_reg_patient_name()
        mobile_number = TestDataGenerator.generate_mobile_number()

        LogGen.start_test(
            self.logger,
            "test_search_and_create_patient",
            "Patient Registration"
        )

        self.logger.info(
            f"Test Data | Patient Name: {not_reg_user} | "
            f"Mobile Number: {mobile_number}"
        )

        try:

            self.patient_reg.click_registration_module()

            self.logger.info(
                "Registration module opened"
            )

            self.patient_reg.click_patient_registration_option()

            self.logger.info(
                "Patient Registration page opened"
            )

            time.sleep(3)

            # ==========================
            # SEARCH NON REGISTERED PATIENT
            # ==========================

            self.logger.info(
                f"Searching non-registered patient: {not_reg_user}"
            )

            self.patient_reg.enter_search_value(not_reg_user)

            time.sleep(5)

            self.patient_reg.click_yes_btn()

            self.logger.info(
                "Confirmed patient creation from search popup"
            )

            time.sleep(3)

            # ==========================
            # PATIENT DETAILS
            # ==========================

            self.logger.info(
                "Selecting random department"
            )

            new_selected_department = (
                self.patient_reg.select_random_visiting_dpt()
            )
            Test_New_Patient_Workflow.new_selected_department = new_selected_department

            self.logger.info(
                f"Selected Department: {new_selected_department}"
            )

            time.sleep(2)

            new_selected_unit = (
                self.patient_reg.get_selected_unit()
            )
            Test_New_Patient_Workflow.new_selected_unit = new_selected_unit

            self.logger.info(
                f"Selected Unit: {new_selected_unit}"
            )

            new_opd_unit_name = (
                f"{new_selected_department.upper()}({new_selected_unit.upper()})"
            )
            Test_New_Patient_Workflow.new_opd_unit_name = new_opd_unit_name

            self.logger.info(
                f"Generated OPD Unit Name: {new_opd_unit_name}"
            )

            time.sleep(2)

            self.logger.info(
                "Entering patient registration details"
            )

            self.patient_reg.enter_patient_name(not_reg_user)
            self.patient_reg.select_random_payment_mode()
            self.patient_reg.enter_patient_age("18")
            self.patient_reg.select_gender("Male")
            self.patient_reg.enter_patient_mobile_no(mobile_number)

            self.patient_reg.enter_patient_father(
                "Automation father"
            )

            self.patient_reg.enter_patient_mother(
                "Automation mother"
            )

            self.patient_reg.enter_patient_guardian(
                "Automation guardian"
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
                "77738"
            )

            self.logger.info(
                "All patient details entered successfully"
            )

            self.patient_reg.click_save_btn()

            self.logger.info(
                "Patient saved successfully"
            )

            time.sleep(12)

            pyautogui.press('esc')

            self.logger.info(
                "Closed popup using ESC"
            )

            # ==========================
            # PDF / BARCODE
            # ==========================

            self.logger.info(
                "Starting PDF verification"
            )

            pdf_text = (
                self.patient_reg.get_blob_pdf_text()
            )

            self.logger.info(
                "PDF opened successfully"
            )

            assert "CRN :" in pdf_text, (
                "CRN not found in PDF"
            )

            # ==========================
            # CRN EXTRACTION
            # ==========================

            new_crn_number = ""

            # Primary method: CRN : <number>
            crn_match = re.search(
                r'\bCRN\s*:\s*(\d+)',
                pdf_text,
                re.IGNORECASE
            )

            if crn_match:
                new_crn_number = crn_match.group(1)

            # Fallback: PDF extractor sometimes removes "CRN :"
            # and puts CRN directly before "Name :"
            if not new_crn_number:

                crn_match = re.search(
                    r'(\d{10,20})\s*Name\s*:',
                    pdf_text,
                    re.IGNORECASE
                )

                if crn_match:
                    new_crn_number = crn_match.group(1)

            # ==========================
            # STORE GENERATED CRN
            # ==========================

            Test_New_Patient_Workflow.generated_crn = new_crn_number

            Test_New_Patient_Workflow.new_generated_crn = new_crn_number

            self.logger.info(
                f"CRN generated successfully: {new_crn_number}"
            )

            self.patient_reg.click_close_btn()

            self.logger.info(
                "PDF closed successfully"
            )

            time.sleep(3)

            pyautogui.press('esc')

            self.logger.info(
                "Pressed ESC"
            )

            time.sleep(3)

            self.patient_reg.click_close_btn()

            self.logger.info(
                "Closed remaining popup"
            )

            time.sleep(3)

            # ==========================
            # REGISTRATION SEARCH VERIFY
            # ==========================

            self.logger.info(
                "Navigating back to Registration Search"
            )

            self.patient_reg.click_home_tab()

            self.patient_reg.click_patient_registration_option()

            self.logger.info(
                f"Searching newly registered patient: {not_reg_user}"
            )

            self.patient_reg.enter_search_value(
                not_reg_user
            )

            element = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//tbody[@class='ant-table-tbody']"
                        f"//*[contains(normalize-space(),"
                        f"'{not_reg_user}')]"
                    )
                )
            )

            actual_name = element.text.strip()

            self.logger.info(
                f"Patient found in registration list: {actual_name}"
            )

            assert not_reg_user.upper() in actual_name.upper(), \
                (
                    f"Patient '{not_reg_user}' not found. "
                    f"Actual: {actual_name}"
                )

            self.logger.info(
                "Patient found in Registration Search"
            )

            LogGen.test_passed(
                self.logger,
                "test_search_and_create_patient"
            )

        except Exception as e:

            if self.driver:

                try:

                    Screenshot.capture(
                        self.driver,
                        "test_search_and_create_patient"
                    )

                except Exception as screenshot_error:

                    self.logger.error(
                        f"Screenshot error: {screenshot_error}"
                    )

            LogGen.test_failed(
                self.logger,
                "test_search_and_create_patient",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_cancel_patient(self):

        # ============================================================
        # CRN FALLBACK LOGIC
        # ============================================================

        self.driver.refresh()
        time.sleep(3)

        generated_crn = Test_New_Patient_Workflow.generated_crn


        if generated_crn:
            new_crn_number = generated_crn

            self.logger.info(
                f"Generated CRN found. "
                f"Using newly registered patient CRN: {new_crn_number}"
            )

            using_fallback = False

        else:
            new_crn_number = (
                Test_New_Patient_Workflow.revisit_hardcoded_crn
            )

            self.logger.warning(
                "No CRN generated during new patient registration."
            )

            self.logger.warning(
                f"Using fallback CRN: {new_crn_number}"
            )

            using_fallback = True

        # ============================================================
        # EXISTING TEST DATA
        # ============================================================

        new_selected_department = (
            Test_New_Patient_Workflow.new_selected_department
        )

        table_value = (
            Test_New_Patient_Workflow.new_opd_unit_name
        )

        LogGen.start_test(
            self.logger,
            "test_cancel_patient",
            "Patient Registration"
        )

        self.logger.info(
            "=========================================="
        )

        self.logger.info(
            f"Test Data | CRN: {new_crn_number}"
        )

        self.logger.info(
            f"Department: {new_selected_department}"
        )

        self.logger.info(
            f"OPD Unit: {table_value}"
        )

        self.logger.info(
            f"Using Fallback CRN: {using_fallback}"
        )

        self.logger.info(
            "=========================================="
        )

        try:

            # ========================================================
            # OPEN REGISTRATION MODULE
            # ========================================================

            self.logger.info(
                "Opening Registration module"
            )

            self.patient_reg.click_registration_module()

            # ========================================================
            # CANCEL PATIENT
            # ========================================================

            self.logger.info(
                "Opening Patient Cancellation screen"
            )

            self.patient_reg.click_patient_cancellation_option()

            time.sleep(5)

            self.logger.info(
                f"Searching patient using CRN: {new_crn_number}"
            )

            self.patient_reg.enter_search_value(
                new_crn_number
            )

            time.sleep(3)

            self.logger.info(
                "Proceeding with patient cancellation"
            )

            self.patient_reg.click_cancel_proceed_btn()

            self.patient_reg.click_cancel_radio_btn()

            self.patient_reg.click_cancellation_radio_btn()

            self.logger.info(
                "Entering cancellation reason"
            )

            self.patient_reg.enter_cancellation_reason(
                "test cancel"
            )

            time.sleep(3)

            self.patient_reg.select_cash_payment_mode_cancel()
            time.sleep(2)

            self.logger.info(
                "Saving patient cancellation"
            )

            self.patient_reg.click_save_cancel_btn()

            self.logger.info(
                "Patient cancelled successfully"
            )

            time.sleep(3)

            pyautogui.press('esc')

            try:

                self.logger.info(
                    "Closing cancellation popup"
                )

                self.patient_reg.click_close_btn()

            except Exception:

                self.logger.info(
                    "No popup found to close"
                )

            time.sleep(5)

            # ========================================================
            # VALIDATION 1
            # DEPARTMENT SHOULD NOT COME
            # ========================================================

            self.logger.info(
                "Starting Validation 1 - "
                "Verifying cancelled department is removed"
            )

            self.driver.refresh()

            time.sleep(5)

            self.patient_reg.click_registration_module()

            self.patient_reg.click_patient_registration_option()

            self.logger.info(
                f"Searching cancelled patient: {new_crn_number}"
            )

            self.patient_reg.enter_search_after_cancel(
                new_crn_number
            )

            time.sleep(3)

            self.logger.info(
                "Opening revisit screen"
            )

            self.patient_reg.click_revisit_btn()

            time.sleep(3)

            self.logger.info(
                "Fetching available department list"
            )

            options = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        "//select[contains(@name,'department')]/option"
                    )
                )
            )

            departments = [
                option.text.strip().upper()
                for option in options
            ]

            self.logger.info(
                f"Departments available after cancellation: "
                f"{departments}"
            )

            self.logger.info(
                f"Checking removed department: "
                f"{new_selected_department}"
            )

            assert new_selected_department.upper() not in departments, (
                f"{new_selected_department} still available "
                f"after cancellation"
            )

            self.logger.info(
                "Cancelled department removed successfully"
            )

            # ========================================================
            # TEST PASSED
            # ========================================================

            LogGen.test_passed(
                self.logger,
                "test_cancel_patient"
            )

        except Exception as e:

            LogGen.test_failed(
                self.logger,
                "test_cancel_patient",
                str(e)
            )

            self.logger.error(
                f"Failure Details | "
                f"CRN: {new_crn_number} | "
                f"Department: {new_selected_department} | "
                f"OPD Unit: {table_value} | "
                f"Fallback: {using_fallback}",
                exc_info=True
            )

            Screenshot.capture(
                self.driver,
                "test_cancel_patient_exception"
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_loop_registration(self):

        self.driver.refresh()
        time.sleep(5)

        mobile_number = TestDataGenerator.generate_mobile_number()

        LogGen.start_test(
            self.logger,
            "test_loop_registration",
            "Patient Registration"
        )

        self.logger.info(
            f"Generated Mobile Number: {mobile_number}"
        )

        try:

            created_patients = []
            number_of_registrations = 2

            self.logger.info(
                f"Starting creation of {number_of_registrations} patients"
            )

            # ==========================================
            # CREATE PATIENTS
            # ==========================================

            for i in range(number_of_registrations):
                self.logger.info(
                    f"========== Registration {i + 1} Started =========="
                )
                self.patient_reg.click_registration_module()
                time.sleep(1)
                self.patient_reg.click_patient_registration_option()

                self.logger.info(
                    "Patient Registration page opened"
                )

                self.patient_reg.click_new_registration_btn()

                self.logger.info(
                    "New Registration form opened"
                )

                time.sleep(2)

                selected_department = (
                    self.patient_reg.select_random_visiting_dpt(
                        exclude_departments=[
                            p["department"]
                            for p in created_patients
                        ]
                    )
                )

                self.logger.info(
                    f"Selected Department: {selected_department}"
                )

                selected_unit = (
                    self.patient_reg.get_selected_unit()
                )

                self.logger.info(
                    f"Selected Unit: {selected_unit}"
                )

                opd_unit_name = (
                    f"{selected_department.upper()}"
                    f"({selected_unit.upper()})"
                )

                suffix = ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=3
                    )
                )

                patient_name_suffix = (
                    f"{Testdata.PATIENT_NAME}{suffix}"
                )

                self.logger.info(
                    f"Generated Patient Name: {patient_name_suffix}"
                )

                self.patient_reg.enter_patient_name(
                    patient_name_suffix
                )

                self.patient_reg.select_random_payment_mode()
                self.patient_reg.enter_patient_age("18")
                self.patient_reg.select_gender("Male")
                self.patient_reg.enter_patient_mobile_no(
                    mobile_number
                )

                self.patient_reg.enter_patient_father(
                    "Automation father"
                )

                self.patient_reg.enter_patient_mother(
                    "Automation mother"
                )

                self.patient_reg.enter_patient_guardian(
                    "Automation guardian"
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
                    "77738"
                )

                self.logger.info(
                    "Saving patient registration"
                )

                self.patient_reg.click_save_btn()

                created_patients.append(
                    {
                        "patient_name": patient_name_suffix,
                        "department": selected_department,
                        "unit": selected_unit
                    }
                )

                self.logger.info(
                    f"""
           Patient Created Successfully
           Name : {patient_name_suffix}
           Department : {selected_department}
           Unit : {selected_unit}
           OPD Unit : {opd_unit_name}
           """
                )

                time.sleep(15)

                pyautogui.press('esc')

                # ==========================
                # PDF CHECK
                # ==========================

                self.logger.info(
                    f"Starting PDF verification for {patient_name_suffix}"
                )

                time.sleep(2)

                pdf_text = (
                    self.patient_reg.get_blob_pdf_text()
                )

                assert patient_name_suffix.upper() in pdf_text.upper(), (
                    f"{patient_name_suffix} not found in PDF"
                )

                self.logger.info(
                    "PDF verification passed"
                )

                self.patient_reg.click_close_btn()

                time.sleep(3)

                pyautogui.press('esc')

                # ==========================
                # BARCODE CHECK
                # ==========================

                self.logger.info(
                    f"Starting Barcode verification for {patient_name_suffix}"
                )

                time.sleep(3)

                barcode_text = (
                    self.patient_reg.get_barcode_blob()
                )

                assert patient_name_suffix.upper() in barcode_text.upper(), (
                    f"{patient_name_suffix} not found in barcode"
                )

                self.logger.info(
                    "Barcode verification passed"
                )

                self.patient_reg.click_close_btn()

                self.logger.info(
                    f"========== Registration {i + 1} Completed Successfully =========="
                )

            # ==========================================
            # SEARCH VALIDATION
            # ==========================================

            self.logger.info(
                "========== Starting Search Validation =========="
            )

            self.patient_reg.click_registration_module()

            self.logger.info(
                "Registration module opened"
            )

            self.patient_reg.click_patient_registration_option()

            self.logger.info(
                "Patient Registration page opened"
            )

            time.sleep(5)

            for patient in created_patients:
                search_name = patient["patient_name"]

                self.logger.info(
                    f"Searching patient: {search_name}"
                )

                self.patient_reg.enter_search_value(
                    search_name
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
                            f"'{search_name.upper()}']"
                        )
                    )
                )

                actual_name = element.text.strip()

                self.logger.info(
                    f"Search Result: {actual_name}"
                )

                assert actual_name.lower() == search_name.lower(), (
                    f"Patient mismatch {actual_name}"
                )

                self.logger.info(
                    f"Patient verified successfully: {search_name}"
                )

                time.sleep(3)

            self.logger.info(
                "All created patients verified successfully"
            )

            LogGen.test_passed(
                self.logger,
                "test_loop_registration"
            )

        except Exception as e:

            Screenshot.capture(
                self.driver,
                "test_loop_registration_TC_009"
            )

            LogGen.test_failed(
                self.logger,
                "test_loop_registration",
                str(e)
            )

            raise

    @pytest.mark.patient_registration_flow_part1
    def test_abha_search_otp_and_register(self):

        LogGen.start_test(
            self.logger,
            "test_abha_search_otp_and_register",
            "Patient Registration"
        )

        try:

            # ==========================
            # CREATE ABHA PATIENT
            # ==========================

            self.logger.info("Refreshing application")
            self.driver.refresh()
            time.sleep(5)

            self.logger.info("Opening Registration Module")
            self.patient_reg.click_registration_module()

            self.logger.info("Opening Patient Registration")
            self.patient_reg.click_patient_registration_option()

            self.logger.info("Opening New Registration form")
            self.patient_reg.click_new_registration_btn()

            time.sleep(3)

            self.logger.info("Selecting ABHA verification with other modes")
            self.patient_reg.click_verify_Abha_with_other_modes()

            time.sleep(3)

            self.logger.info("Entering mobile number for ABHA verification")
            if not self.abha_mobile:
                raise Exception(
                    "ABHA verification mobile number was not provided."
                )

            self.logger.info(
                f"Using ABHA verification mobile: {self.abha_mobile}"
            )

            self.patient_reg.enter_mob_for_abha_verification(
                self.abha_mobile
            )

            time.sleep(1)

            self.logger.info("Sending OTP")
            self.patient_reg.click_send_otp_btn()

            self.logger.info("Entering OTP")
            self.patient_reg.enter_otp()

            self.logger.info("Verifying OTP")
            self.patient_reg.click_verify_otp()

            time.sleep(5)

            self.logger.info("Fetching patient details from ABHA")
            patient_details = self.patient_reg.get_patient_all_details()

            import re

            match = re.search(
                r"Patient Name:\s*(.*)",
                patient_details
            )

            if match:
                abha_patient_name = match.group(1).strip()
            else:
                raise Exception("Patient name not found in details")

            print("ABHA Patient Name:", abha_patient_name)

            self.logger.info(
                f"ABHA Patient Name: {abha_patient_name}"
            )

            self.logger.info("Adding ABHA patient")
            self.patient_reg.click_add_abha_patient()

            time.sleep(5)

            self.logger.info("Selecting random visiting department")
            self.patient_reg.select_random_visiting_dpt()

            self.logger.info("Getting selected unit")
            self.patient_reg.get_selected_unit()

            self.patient_reg.select_random_payment_mode()

            self.logger.info("Entering patient family details")
            self.patient_reg.enter_patient_father("Automation father")
            self.patient_reg.enter_patient_mother("Automation mother")

            self.patient_reg.enter_patient_post_office("Automation post office")

            self.patient_reg.enter_patient_street("Automation street")

            self.logger.info("Saving patient registration")
            self.patient_reg.click_save_btn()

            time.sleep(3)

            try:

                self.logger.info(
                    "Checking whether existing patient popup is displayed"
                )

                radio = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//tbody[contains(@class,'ant-table-tbody')]//tr[contains(@class,'ant-table-row')][1]//span[contains(@class,'ant-radio-inner')]"
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    radio
                )

                self.logger.info(
                    "Existing patient radio button selected"
                )

                time.sleep(4)

                self.patient_reg.click_new_department_revisit_btn()

                self.logger.info(
                    "New revisit department selected"
                )

                time.sleep(3)

                revisited_dep = (
                    self.patient_reg.select_random_department_with_unit()
                )

                self.logger.info(
                    f"Revisit department selected: {revisited_dep}"
                )

                time.sleep(3)

                self.patient_reg.click_revisit_save_btn()

                self.logger.info(
                    "Revisit saved successfully"
                )

            except TimeoutException:

                self.logger.info(
                    "Existing patient popup not displayed. Continuing normal registration flow."
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

            pdf_text = self.patient_reg.get_blob_pdf_text()

            print(pdf_text)

            assert "CRN :" in pdf_text, \
                "CRN not found in PDF"

            crn_number = (
                pdf_text.split("CRN :")[1]
                .split("NAME :")[0]
                .strip()
            )

            print(f"CRN Number: {crn_number}")

            self.logger.info(
                f"CRN generated successfully: {crn_number}"
            )

            self.patient_reg.click_close_btn()

            time.sleep(3)

            pyautogui.press('esc')

            # ==========================
            # BARCODE VERIFICATION
            # ==========================

            self.logger.info(
                "Starting barcode verification"
            )

            time.sleep(3)

            barcode_text = self.patient_reg.get_barcode_blob()

            print(barcode_text)

            self.logger.info(
                "Barcode generated successfully"
            )

            self.patient_reg.click_close_btn()

            # ==========================
            # SEARCH PATIENT
            # ==========================

            self.logger.info(
                "Opening Patient Registration for search"
            )

            self.patient_reg.click_home_tab()

            self.patient_reg.click_patient_registration_option()

            self.logger.info(
                f"Searching patient using CRN: {crn_number}"
            )

            self.patient_reg.enter_search_value(crn_number)

            time.sleep(5)

            self.logger.info(
                "Waiting for patient details to appear in search results"
            )

            table_patient_name = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//tbody[contains(@class,'ant-table-tbody')]//tr[contains(@class,'ant-table-row')][1]//td[2]//span"
                    )
                )
            ).text.strip()

            print("Table Patient Name:", table_patient_name)

            self.logger.info(
                f"Patient Name found in table: {table_patient_name}"
            )

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//tbody[contains(@class,'ant-table-tbody')]//tr[contains(@class,'ant-table-row')]"
                    )
                )
            )

            crn_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//tbody[contains(@class,'ant-table-tbody')]//tr[contains(@class,'ant-table-row')]//td[1]//span[normalize-space()='{crn_number}']"
                    )
                )
            )

            assert crn_element.is_displayed(), (
                f"CRN {crn_number} not visible in table"
            )

            self.logger.info(
                f"CRN verified successfully: {crn_number}"
            )

            assert table_patient_name.upper() == abha_patient_name.upper(), (
                f"Patient name mismatch. "
                f"ABHA: {abha_patient_name}, Search Result: {table_patient_name}"
            )

            self.logger.info(
                "Patient name matched successfully"
            )

            LogGen.test_passed(
                self.logger,
                "test_abha_search_otp_and_register"
            )

        except Exception as e:

            Screenshot.capture(
                self.driver,
                "test_abha"
            )

            LogGen.test_failed(
                self.logger,
                "test_abha_search_otp_and_register",
                str(e)
            )

            raise




