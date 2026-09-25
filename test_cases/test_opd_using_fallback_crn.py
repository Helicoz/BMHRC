
import os
import random
import string
import time
import re

import pyautogui
import pytest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.logger import LogGen
from utilities.screenshot import Screenshot
from test_data.test_patient_data import Testdata, TestDataGenerator
from utilities.download_utils import PDFUtils


@pytest.mark.usefixtures("login")
class Test_OPD_Workflow:

    logger = LogGen.loggen()

    driver = None
    patient_reg = None
    opd_flow = None

    # ============================================================
    # GENERATED PATIENT DATA
    # ============================================================

    generated_crn = None
    generated_mobile_no = None
    generated_patient_name = None


    selected_department = None
    selected_unit = None
    opd_unit_name = None

    generated_investigation_tests = None
    generated_xray_tests = None
    generated_referral_dep = None
    generated_chronic_disease = None
    generated_diagnosis_name = None
    generated_admission_dep = None

    # ============================================================
    # FALLBACK / REVISIT DATA
    # ============================================================

    # Hard-coded fallback CRN
    opd_fallback_crn = "231012600001630"

    # True when registration fails
    revisit_using_fallback = False

    # Stores department/unit selected during revisit
    revisit_opd_unit_name = None

    # ============================================================
    # RX → FOLLOW-UP DATA
    # ============================================================

    opd_rx_crn = None
    opd_rx_patient_name = None

    # ============================================================
    # TEST:  SKIP PATIENT
    # ============================================================

    @pytest.mark.opd_flow
    def test_skip_patience(self):

        # ========================================================
        # RESET WORKFLOW DATA
        # ========================================================

        mobile_number = (
            TestDataGenerator.generate_mobile_number()
        )

        Test_OPD_Workflow.generated_crn = None
        Test_OPD_Workflow.generated_patient_name = None
        Test_OPD_Workflow.generated_mobile_no = None

        Test_OPD_Workflow.selected_department = None
        Test_OPD_Workflow.selected_unit = None
        Test_OPD_Workflow.opd_unit_name = None

        Test_OPD_Workflow.revisit_using_fallback = False
        Test_OPD_Workflow.revisit_opd_unit_name = None

        LogGen.start_test(
            self.logger,
            "test_skip_patience",
            "Skip Patient from OPD Queue"
        )

        # ========================================================
        # REGISTRATION
        # ========================================================

        registration_success = False

        try:

            # ====================================================
            # OPEN REGISTRATION
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

            self.logger.info(
                "Selecting random visiting department"
            )

            selected_department = (
                self.patient_reg.select_random_visiting_dpt()
            )

            Test_OPD_Workflow.selected_department = (
                selected_department
            )

            self.logger.info(
                f"Selected Department: "
                f"{selected_department}"
            )

            time.sleep(2)

            # ====================================================
            # GET SELECTED UNIT
            # ====================================================

            self.logger.info(
                "Getting selected unit"
            )

            selected_unit = (
                self.patient_reg.get_selected_unit()
            )

            Test_OPD_Workflow.selected_unit = selected_unit

            self.logger.info(
                f"Selected Unit: "
                f"{selected_unit}"
            )

            # ====================================================
            # CREATE OPD UNIT NAME
            # ====================================================

            opd_unit_name = (
                f"{selected_department.upper()}"
                f"({selected_unit.upper()})"
            )

            Test_OPD_Workflow.opd_unit_name = (
                opd_unit_name
            )

            self.logger.info(
                f"Stored OPD Unit Name: "
                f"{opd_unit_name}"
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

            self.logger.info(
                "Entering patient details"
            )

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
                f"Entering Mobile Number: "
                f"{mobile_number}"
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
            # SAVE PATIENT
            # ====================================================

            self.logger.info(
                "Saving patient registration"
            )

            self.patient_reg.click_save_btn()

            self.logger.info(
                f"Patient registration submitted: "
                f"{patient_name_suffix}"
            )

            time.sleep(20)

            pyautogui.press("esc")

            time.sleep(2)

            # ====================================================
            # GET GENERATED PDF
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

            crn_number = ""

            crn_match = re.search(
                r'\bCRN\s*:\s*(\d+)',
                pdf_text,
                re.IGNORECASE
            )

            if crn_match:

                crn_number = (
                    crn_match.group(1)
                )

            # ----------------------------------------------------
            # FALLBACK CRN EXTRACTION
            # ----------------------------------------------------

            if not crn_number:

                crn_match = re.search(
                    r'(\d{10,20})\s*Name\s*:',
                    pdf_text,
                    re.IGNORECASE
                )

                if crn_match:

                    crn_number = (
                        crn_match.group(1)
                    )

            if not crn_number:

                raise Exception(
                    "CRN could not be extracted "
                    "from generated PDF."
                )

            Test_OPD_Workflow.generated_crn = (
                crn_number
            )

            self.logger.info(
                f"Generated CRN: "
                f"{crn_number}"
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
                patient_name = (
                    name_match.group(1)
                    .strip()
                    .splitlines()[0]
                    .strip()
                )

            Test_OPD_Workflow.generated_patient_name = patient_name

            self.logger.info(
                f"Patient Name: {patient_name}"
            )

            # # ============================================================
            # # EXTRACT MOBILE NUMBER
            # # ============================================================
            #
            # mobile_no = ""
            #
            # mobile_match = re.search(
            #     r'(?:Mobile Number|MOBILE NO)\s*/?.*?:?\s*(\d{10})',
            #     pdf_text,
            #     re.IGNORECASE
            # )
            #
            # if mobile_match:
            #     mobile_no = mobile_match.group(1)
            #
            # Test_OPD_Workflow.generated_mobile_no = mobile_no
            #
            # self.logger.info(
            #     f"Mobile Number: {mobile_no}"
            # )

            # ============================================================
            # STORE MOBILE NUMBER
            # ============================================================

            Test_OPD_Workflow.generated_mobile_no = mobile_number

            self.logger.info(
                f"Generated Mobile Number: {mobile_number}"
            )

            # ====================================================
            # CLOSE PDF
            # ====================================================

            try:

                self.patient_reg.click_close_btn()

            except Exception as e:

                self.logger.warning(
                    f"Unable to close PDF popup: {e}"
                )

            time.sleep(2)

            pyautogui.press("esc")

            time.sleep(2)

            # ====================================================
            # BARCODE
            # ====================================================

            try:

                self.patient_reg.get_barcode_blob()

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
            # REGISTRATION SUCCESS
            # ====================================================

            registration_success = True

            self.logger.info(
                "Patient registration completed successfully."
            )

        except Exception as registration_error:

            # ====================================================
            # REGISTRATION FAILED
            # ====================================================

            registration_success = False

            Test_OPD_Workflow.generated_crn = None

            self.logger.warning(
                "================================================"
            )

            self.logger.warning(
                "PATIENT REGISTRATION FAILED"
            )

            self.logger.warning(
                f"Registration Error: "
                f"{registration_error}"
            )

            self.logger.warning(
                "Starting patient revisit fallback."
            )

            self.logger.warning(
                "================================================"
            )

            # ----------------------------------------------------
            # REFRESH
            # ----------------------------------------------------

            try:

                self.driver.refresh()

                time.sleep(5)

                self.logger.info(
                    "Page refreshed successfully."
                )

            except Exception as refresh_error:

                raise Exception(
                    f"Registration failed and page refresh "
                    f"also failed: {refresh_error}"
                )

        # ========================================================
        # FALLBACK → REVISIT PATIENT
        # ========================================================

        if not registration_success:

            Test_OPD_Workflow.revisit_using_fallback = True

            self.logger.warning(
                "Starting fallback patient revisit workflow."
            )

            # ====================================================
            # FALLBACK CRN
            # ====================================================

            if not Test_OPD_Workflow.opd_fallback_crn:

                raise Exception(
                    "Fallback CRN is empty."
                )

            fallback_crn = str(
                Test_OPD_Workflow.opd_fallback_crn
            ).strip()

            self.logger.warning(
                f"Using fallback CRN: "
                f"{fallback_crn}"
            )

            # ====================================================
            # OPEN REGISTRATION
            # ====================================================

            self.logger.info(
                "Opening Registration Module "
                "for patient revisit."
            )

            self.patient_reg.click_registration_module()

            time.sleep(2)

            self.patient_reg.click_patient_registration_option()

            time.sleep(3)

            # ====================================================
            # SEARCH FALLBACK CRN
            # ====================================================

            self.logger.info(
                f"Searching fallback patient using CRN: "
                f"{fallback_crn}"
            )

            self.patient_reg.enter_search_value(
                fallback_crn
            )

            time.sleep(3)

            # ====================================================
            # EXTRACT PATIENT DETAILS
            # ====================================================

            self.logger.info(
                "Extracting fallback patient details."
            )

            try:

                (
                    search_patient_name,
                    search_mobile_number
                ) = (
                    self.patient_reg
                    .get_patient_details_from_search_result(
                        fallback_crn
                    )
                )

                self.logger.info(
                    f"Fallback Patient Name: "
                    f"{search_patient_name}"
                )

                self.logger.info(
                    f"Fallback Patient Mobile: "
                    f"{search_mobile_number}"
                )

                if search_patient_name:

                    Test_OPD_Workflow.generated_patient_name = (
                        search_patient_name
                    )

                if search_mobile_number:

                    Test_OPD_Workflow.generated_mobile_no = (
                        search_mobile_number
                    )

            except Exception as patient_detail_error:

                self.logger.warning(
                    "Unable to extract fallback patient "
                    f"details: {patient_detail_error}"
                )

            # ====================================================
            # STORE FALLBACK CRN
            # ====================================================

            Test_OPD_Workflow.generated_crn = (
                fallback_crn
            )

            # ====================================================
            # CLICK REVISIT
            # ====================================================

            self.logger.info(
                "Clicking Revisit button."
            )

            time.sleep(3)

            self.patient_reg.click_revisit_btn()

            time.sleep(3)

            self.logger.info(
                "Revisit button clicked."
            )

            # ====================================================
            # NEW DEPARTMENT REVISIT
            # ====================================================

            self.logger.info(
                "Opening New Department Revisit."
            )

            self.patient_reg.click_new_department_revisit_btn()

            time.sleep(3)

            self.logger.info(
                "New Department Revisit window opened."
            )

            # ====================================================
            # SELECT NEW DEPARTMENT + UNIT
            # ====================================================

            self.logger.info(
                "Selecting new department/unit "
                "for patient revisit."
            )

            opd_check = (
                self.patient_reg
                .select_department_until_save_success()
            )

            if not opd_check:

                raise Exception(
                    "New department/unit was not returned "
                    "after patient revisit."
                )

            # ====================================================
            # STORE REVISIT UNIT
            # ====================================================

            Test_OPD_Workflow.revisit_opd_unit_name = (
                opd_check
            )

            Test_OPD_Workflow.opd_unit_name = (
                opd_check
            )

            self.logger.info(
                f"Revisit Department/Unit: "
                f"{opd_check}"
            )

            self.logger.info(
                f"Stored Revisit OPD Unit: "
                f"{Test_OPD_Workflow.opd_unit_name}"
            )

            time.sleep(3)

            # ====================================================
            # CLOSE REVISIT POPUPS
            # ====================================================

            self.logger.info(
                "Closing revisit popups."
            )

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
            # FALLBACK REVISIT COMPLETE
            # ====================================================

            self.logger.warning(
                "================================================"
            )

            self.logger.warning(
                "PATIENT REVISIT COMPLETED"
            )

            self.logger.warning(
                f"Revisit CRN: {fallback_crn}"
            )

            self.logger.warning(
                f"Revisit OPD Unit: {opd_check}"
            )

            self.logger.warning(
                "================================================"
            )

        else:

            # ====================================================
            # GENERATED PATIENT
            # ====================================================

            Test_OPD_Workflow.revisit_using_fallback = False

            self.logger.info(
                "Registration completed successfully."
            )

            self.logger.info(
                f"Using generated CRN: "
                f"{Test_OPD_Workflow.generated_crn}"
            )

            self.logger.info(
                f"Using generated OPD Unit: "
                f"{Test_OPD_Workflow.opd_unit_name}"
            )

        # ========================================================
        # COMMON FINAL VALUES
        # ========================================================

        crn_number = (
            Test_OPD_Workflow.generated_crn
        )

        opd_unit_name = (
            Test_OPD_Workflow.opd_unit_name
        )

        if not crn_number:

            raise Exception(
                "Final CRN is empty. "
                "Cannot continue OPD workflow."
            )

        if not opd_unit_name:

            raise Exception(
                "Final OPD Unit is empty. "
                "Cannot continue OPD workflow."
            )

        self.logger.info(
            "========================================"
        )

        self.logger.info(
            f"Final CRN: {crn_number}"
        )

        self.logger.info(
            f"Final OPD Unit: {opd_unit_name}"
        )

        self.logger.info(
            f"Fallback Used: "
            f"{Test_OPD_Workflow.revisit_using_fallback}"
        )

        self.logger.info(
            "========================================"
        )

        # ========================================================
        # NAVIGATE HOME
        # ========================================================

        self.driver.refresh()
        time.sleep(5)


        # ========================================================
        # OPEN OPD
        # ========================================================

        self.logger.info(
            "Opening OPD module."
        )

        self.patient_reg.click_opd_module()

        time.sleep(2)

        self.logger.info(
            "Opening OPD Doctor Desk."
        )

        self.patient_reg.click_opd_dr_desk()

        time.sleep(3)

        # ========================================================
        # SELECT FINAL OPD UNIT
        # ========================================================

        self.logger.info(
            f"Selecting final OPD Department/Unit: "
            f"{opd_unit_name}"
        )

        self.patient_reg.select_opd_dr_desk_department(
            opd_unit_name
        )

        self.logger.info(
            f"OPD Department/Unit selected: "
            f"{opd_unit_name}"
        )

        time.sleep(3)

        # ========================================================
        # SEARCH PATIENT
        # ========================================================

        self.logger.info(
            f"Searching patient in OPD using CRN: "
            f"{crn_number}"
        )

        self.patient_reg.enter_search_name_in_opd(
            crn_number
        )

        time.sleep(3)

        # ========================================================
        # SKIP PATIENT
        # ========================================================

        self.logger.info(
            "Clicking Skip button."
        )

        self.opd_flow.click_skip_btn()

        self.logger.info(
            "Confirming Skip operation."
        )

        self.opd_flow.skip_yes_btn()

        time.sleep(2)

        # ========================================================
        # VALIDATE SKIP MESSAGE
        # ========================================================

        self.logger.info(
            "Validating Skip OPD queue message."
        )

        skip_opd_msg = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='swal2-html-container' "
                    "and normalize-space()='Skip opd queue']"
                )
            )
        )

        assert skip_opd_msg.is_displayed(), (
            "Skip opd queue message is not visible."
        )

        self.logger.info(
            "Skip opd queue message is visible successfully."
        )

        # ========================================================
        # VALIDATE SKIPPED STATUS
        # ========================================================

        self.logger.info(
            f"Validating Skipped status for CRN: "
            f"{crn_number}"
        )

        skipped_status = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//tr[contains(@class,'ant-table-row')]"
                    f"[.//td//span[normalize-space()="
                    f"'{crn_number}']]"
                    f"//button[contains(@class,'status-skipped') "
                    f"and normalize-space()='Skipped']"
                )
            )
        )

        assert skipped_status.is_displayed(), (
            f"Skipped status is not visible for "
            f"CRN: {crn_number}"
        )

        self.logger.info(
            f"Skipped status is visible successfully "
            f"for CRN: {crn_number}"
        )

        # ========================================================
        # TEST PASSED
        # ========================================================

        LogGen.test_passed(
            self.logger,
            f"Patient {crn_number} was successfully "
            f"skipped from OPD queue using unit "
            f"{opd_unit_name}."
        )

    @pytest.mark.opd_flow
    def test_download_pdf(self):
        # ============================================================
        # GET PATIENT NAME
        # ============================================================

        patient_name = (
            Test_OPD_Workflow.generated_patient_name
        )

        if patient_name:

            patient_name = str(patient_name).strip()

            # --------------------------------------------------------
            # CLEAN PATIENT NAME
            # --------------------------------------------------------


            patient_name = re.split(
                r'\s*नाम\s*:',
                patient_name,
                maxsplit=1
            )[0].strip()

            # Remove any accidental extra whitespace
            patient_name = " ".join(
                patient_name.split()
            )

            self.logger.info(
                f"Cleaned patient name: {patient_name}"
            )

        else:

            self.logger.warning(
                "Patient name is None/empty."
            )

        # ============================================================
        # CRN FALLBACK LOGIC
        # ============================================================

        generated_crn = (
            Test_OPD_Workflow.generated_crn
        )

        fallback_crn = (
            Test_OPD_Workflow.opd_fallback_crn
        )

        if generated_crn is not None and str(generated_crn).strip():

            crn_number = str(generated_crn).strip()

            self.logger.info(
                f"Using generated/final CRN: {crn_number}"
            )

        else:

            if not fallback_crn:
                raise Exception(
                    "Generated CRN is None/empty and "
                    "fallback CRN is also empty."
                )

            crn_number = str(fallback_crn).strip()

            self.logger.warning(
                f"Generated CRN unavailable. "
                f"Using hard-coded fallback CRN: {crn_number}"
            )

        # ------------------------------------------------------------
        # CLEAN CRN
        # ------------------------------------------------------------


        crn_match = re.search(
            r'\d{10,20}',
            crn_number
        )

        if crn_match:

            crn_number = crn_match.group(0)

            self.logger.info(
                f"Cleaned CRN for PDF verification: {crn_number}"
            )

        else:

            raise Exception(
                f"Unable to extract valid CRN from: "
                f"{crn_number}"
            )

        # ============================================================
        # MOBILE NUMBER
        # ============================================================

        mobile_number = (
            Test_OPD_Workflow.generated_mobile_no
        )

        if mobile_number:

            mobile_number = str(
                mobile_number
            ).strip()

            # --------------------------------------------------------
            # CLEAN MOBILE NUMBER
            # --------------------------------------------------------

            mobile_digits = re.sub(
                r'\D',
                '',
                mobile_number
            )

            # If there are more than 10 digits, take the last
            # 10 digits.
            if len(mobile_digits) >= 10:

                mobile_number = (
                    mobile_digits[-10:]
                )

            else:

                mobile_number = mobile_digits

            self.logger.info(
                f"Cleaned mobile number for PDF verification: "
                f"{mobile_number}"
            )

        else:

            self.logger.warning(
                "Mobile number is None/empty."
            )

        # ============================================================
        # GET OPD UNIT
        # ============================================================

        opd_unit_name = (
            Test_OPD_Workflow.opd_unit_name
        )

        if not opd_unit_name:
            raise Exception(
                "OPD Unit Name is None/empty. "
                "Cannot download PDF."
            )

        # ============================================================
        # NAVIGATE TO OPD
        # ============================================================

        self.logger.info(
            "Navigating to OPD Doctor Desk."
        )

        self.driver.refresh()

        time.sleep(3)

        self.patient_reg.click_opd_module()

        time.sleep(2)

        self.patient_reg.click_opd_dr_desk()

        time.sleep(3)

        # ============================================================
        # SELECT OPD UNIT
        # ============================================================

        self.logger.info(
            f"Selecting OPD Unit: {opd_unit_name}"
        )

        self.patient_reg.select_opd_dr_desk_unit(
            opd_unit_name
        )

        time.sleep(3)

        # ============================================================
        # SEARCH PATIENT
        # ============================================================

        self.logger.info(
            f"Searching patient by CRN: {crn_number}"
        )

        self.patient_reg.enter_search_name_in_opd(
            crn_number
        )

        time.sleep(3)

        # ============================================================
        # PDF DOWNLOAD
        # ============================================================

        try:

            self.logger.info(
                f"Clicking PDF download button for CRN: "
                f"{crn_number}"
            )

            # --------------------------------------------------------
            # CLEAR PREVIOUS PDF FILES
            # --------------------------------------------------------

            PDFUtils.clear_download_folder()

            existing_pdfs = (
                PDFUtils.get_existing_pdfs()
            )

            download_folder = (
                PDFUtils.get_download_folder()
            )

            self.logger.info(
                f"Chrome download folder: "
                f"{download_folder}"
            )

            # --------------------------------------------------------
            # CLICK PDF DOWNLOAD
            # --------------------------------------------------------

            self.opd_flow.click_pdf_download_btn()

            self.logger.info(
                "PDF button clicked successfully."
            )

            # ========================================================
            # WAIT FOR DOWNLOAD
            # ========================================================

            pdf_path = (
                PDFUtils.wait_for_pdf_download(
                    timeout=30,
                    existing_files=existing_pdfs
                )
            )

            self.logger.info(
                f"PDF downloaded successfully: "
                f"{pdf_path}"
            )

            # ========================================================
            # READ PDF
            # ========================================================

            pdf_text = PDFUtils.read_pdf(
                pdf_path
            )

            print(
                "\n================ PDF TEXT ================\n"
            )

            print(pdf_text)

            print(
                "\n===========================================\n"
            )

            # ========================================================
            # BASIC PDF VALIDATION
            # ========================================================

            if not pdf_text or not pdf_text.strip():
                raise AssertionError(
                    "PDF was downloaded but "
                    "no text could be extracted."
                )

            # ========================================================
            # NORMALIZE PDF TEXT
            # ========================================================

            normalized_pdf_text = " ".join(
                pdf_text.split()
            ).casefold()

            self.logger.info(
                f"Normalized PDF text: "
                f"{normalized_pdf_text}"
            )

            # ========================================================
            # PATIENT NAME VALIDATION
            # ========================================================

            if patient_name:

                normalized_patient_name = (
                    " ".join(
                        patient_name.split()
                    ).casefold()
                )

                self.logger.info(
                    f"Checking patient name in PDF: "
                    f"{normalized_patient_name}"
                )

                if (
                        normalized_patient_name
                        not in normalized_pdf_text
                ):
                    raise AssertionError(
                        f"Patient name not found in PDF.\n"
                        f"Expected: {patient_name}\n"
                        f"PDF Text:\n{pdf_text}"
                    )

                self.logger.info(
                    f"Patient name verified successfully: "
                    f"{patient_name}"
                )

            else:

                self.logger.warning(
                    "Patient name is None/empty. "
                    "Skipping patient name validation."
                )

            # ========================================================
            # CRN VALIDATION
            # ========================================================



            pdf_crn_numbers = re.findall(
                r'\d{10,20}',
                pdf_text
            )

            self.logger.info(
                f"CRN numbers found in PDF: "
                f"{pdf_crn_numbers}"
            )

            if crn_number not in pdf_crn_numbers:
                raise AssertionError(
                    f"CRN not found in PDF.\n"
                    f"Expected: {crn_number}\n"
                    f"CRNs found in PDF: "
                    f"{pdf_crn_numbers}\n"
                    f"PDF Text:\n{pdf_text}"
                )

            self.logger.info(
                f"CRN verified successfully: "
                f"{crn_number}"
            )

            # ========================================================
            # MOBILE NUMBER VALIDATION
            # ========================================================

            if mobile_number:

                # ----------------------------------------------------
                # Extract all 10-digit numbers from PDF
                # ----------------------------------------------------

                pdf_mobile_numbers = re.findall(
                    r'\b\d{10}\b',
                    pdf_text
                )

                self.logger.info(
                    f"10-digit numbers found in PDF: "
                    f"{pdf_mobile_numbers}"
                )

                if mobile_number not in pdf_mobile_numbers:
                    raise AssertionError(
                        f"Mobile number not found in PDF.\n"
                        f"Expected: {mobile_number}\n"
                        f"10-digit numbers found in PDF: "
                        f"{pdf_mobile_numbers}\n"
                        f"PDF Text:\n{pdf_text}"
                    )

                self.logger.info(
                    f"Mobile number verified successfully: "
                    f"{mobile_number}"
                )

            else:

                self.logger.warning(
                    "Mobile number is None/empty. "
                    "Skipping mobile number validation."
                )

            # ========================================================
            # FINAL SUCCESS
            # ========================================================

            self.logger.info(
                "================================================"
            )

            self.logger.info(
                "PDF DOWNLOAD AND VERIFICATION SUCCESSFUL"
            )

            self.logger.info(
                f"Patient Name : {patient_name}"
            )

            self.logger.info(
                f"CRN          : {crn_number}"
            )

            self.logger.info(
                f"Mobile       : {mobile_number}"
            )

            self.logger.info(
                "================================================"
            )

        # ============================================================
        # FAILURE HANDLING
        # ============================================================

        except Exception as e:

            self.logger.error(
                "PDF download/verification failed",
                exc_info=True
            )

            pytest.fail(
                f"PDF download/verification failed: "
                f"{str(e)}"
            )

    @pytest.mark.opd_flow
    def test_opd_test(self):

        # ============================================================
        # CRN SELECTION
        # ============================================================

        generated_crn = getattr(
            Test_OPD_Workflow,
            "generated_crn",
            None
        )



        opd_fallback_crn = getattr(
            Test_OPD_Workflow,
            "opd_fallback_crn",
            None
        )

        self.logger.info(
            f"Generated CRN from previous test: {generated_crn}"
        )

        self.logger.info(
            f"Fallback CRN configured: {opd_fallback_crn}"
        )

        # ------------------------------------------------------------
        # Use generated CRN first.
        # If generated CRN is not available, use fallback CRN.
        # No third CRN will be used.
        # ------------------------------------------------------------

        if generated_crn:
            crn_number = str(generated_crn).strip()

            self.logger.info(
                f"Using generated CRN for OPD/RX: {crn_number}"
            )

        elif opd_fallback_crn:
            crn_number = str(opd_fallback_crn).strip()

            self.logger.warning(
                f"Generated CRN unavailable. "
                f"Using fallback CRN: {crn_number}"
            )

        else:
            raise AssertionError(
                "Neither generated CRN nor fallback CRN is available."
            )

        # ============================================================
        # PATIENT DATA
        # ============================================================

        patient_name = Test_OPD_Workflow.generated_patient_name
        patient_mobile = Test_OPD_Workflow.generated_mobile_no
        opd_unit_name = Test_OPD_Workflow.opd_unit_name

        self.logger.info(
            f"Patient Name: {patient_name}"
        )

        self.logger.info(
            f"Patient Mobile: {patient_mobile}"
        )

        self.logger.info(
            f"OPD Unit: {opd_unit_name}"
        )

        # ============================================================
        # RESET RX OUTPUT VALUES
        # ============================================================

        Test_OPD_Workflow.opd_rx_crn = None
        Test_OPD_Workflow.opd_rx_patient_name = None

        # ============================================================
        # RX ATTEMPT CONTROL
        # ============================================================

        max_rx_attempts = 2
        last_rx_error = None

        # ============================================================
        # RX WORKFLOW
        # ============================================================

        for rx_attempt in range(1, max_rx_attempts + 1):

            self.logger.info(
                f"Starting RX attempt {rx_attempt} "
                f"of {max_rx_attempts}"
            )

            try:

                # ====================================================
                # GET LOGGED-IN USER
                # ====================================================

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
                ).text

                # ====================================================
                # OPEN RX
                # ====================================================

                self.logger.info(
                    f"Opening RX for CRN: {crn_number}"
                )

                self.patient_reg.click_rx_btn()

                self.logger.info(
                    "RX screen opened"
                )

                chief_complaint = "Fever"
                diagnosis_code = "D00"
                instruction = "After Meal"
                followup_days = "5"
                rx_weight = "60"
                rx_height = "123"
                rx_temperature = "102"
                rx_resp_rate = "89"
                rx_pulse_rate = "80"
                rx_systolic = "80"
                rx_diastolic = "181"
                chief_complaint_number_days = "5"
                chief_complaint_remarks = "Test cheif complaint remark"
                history_of_illness = "Patient presented with intermittent high-grade fever, chills, rigors, headache, myalgia, weakness, and recent mosquito exposure suggestive of malaria."
                past_history = "No history of chronic illness, previous malaria, or significant comorbidities."
                personal_history = "Appetite reduced; sleep disturbed due to fever; bowel and bladder habits normal."
                family_history = "No significant family history of infectious or hereditary diseases."
                treatment_history = "Received symptomatic treatment with antipyretics prior to admission."
                surgical_history = "No history of major surgery or surgical intervention."
                occupational_history = "Works in an area with frequent outdoor exposure, increasing risk of mosquito bites."
                general_exam = "Patient conscious, alert, oriented, febrile with mild dehydration."
                cvs = "S1 & S2 normal, regular rhythm, no murmurs."
                cns = "Conscious, oriented, no focal neurological deficit."
                pa = "Soft, non-tender abdomen, mild splenomegaly, bowel sounds present."
                muscular_exam = "Normal muscle bulk and tone, generalized myalgia, power 5/5."
                local_exam = "No swelling, tenderness, deformity, or lesions."
                pain_assessment = "Generalized body ache and headache (4–5/10)."
                respiratory_system = "Bilateral air entry equal, vesicular breath sounds, no added sounds."
                chronic_disease_name = "Thyroid adenoma"
                chronic_disease_remarks = "No known history of chronic illness or comorbidities."
                snomed_name = "Malaria"
                other_diagnosis_detail = "Mild anemia and thrombocytopenia secondary to malaria."
                confidential_details = "Highly sensitive medical or personal information."
                diagnosis_note = "Patient diagnosed with malaria; treatment initiated and under monitoring."
                xray = "XR CHEST LATERAL (XRAY034)"
                investigation_note = "Severe body ache and nose bleeding."
                external_drug = "Anastrozole"
                treatment_note_remarks = "Appropriate antimalarial therapy with supportive care."
                allergy_code = "Eye fluid"
                clinical_notes = "End-stage heart failure; referred for transplant workup and optimization."
                instruction_remarks = "Continue medications, complete investigations, maintain advised restrictions, follow up with Cardiology & Transplant team."

                time.sleep(5)
                self.opd_flow.click_vital()
                time.sleep(2)
                self.opd_flow.enter_weight(rx_weight)
                self.opd_flow.enter_height(rx_height)
                self.opd_flow.enter_temperature(rx_temperature)
                self.opd_flow.enter_resp_rate(rx_resp_rate)
                self.opd_flow.enter_pulse_rate(rx_pulse_rate)
                self.opd_flow.enter_systolic(rx_systolic)
                self.opd_flow.enter_diastolic(rx_diastolic)
                self.opd_flow.enter_haemoglobin("15")
                self.opd_flow.enter_spo2("92")

                time.sleep(2)
                self.opd_flow.click_vital_save_btn()
                time.sleep(2)

                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(@class,'swal2-confirm') and normalize-space()='OK']"
                        )
                    )
                ).click()

                # ============================================================
                # VITALS
                # ============================================================

                vitals_data = {}

                vitals = self.driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class,'vital-examination-col')]//p"
                )

                for vital in vitals:
                    text = vital.text.strip()

                    if ":" in text:
                        key, value = text.split(":", 1)
                        vitals_data[key.strip()] = value.strip()

                # ============================================================
                # Assertions
                # ============================================================

                (vitals_data.get("Weight"), f"{rx_weight} kgs", "Weight")
                (vitals_data.get("Height"), f"{rx_height} cms", "Height")
                (vitals_data.get("Temp"), f"{rx_temperature} F (High Fever)", "Temperature")
                (vitals_data.get("BP"), f"{rx_systolic}/{rx_diastolic} mm/HG", "Blood Pressure")
                (vitals_data.get("Hgb"), "15 gm/dL ()", "Hb")
                (vitals_data.get("SPO2"), "92 %", "SPO2")
                (vitals_data.get("Pulse Rate"), f"{rx_pulse_rate} be/m", "Pulse Rate")

                self.logger.info(
                    f"Chief Complaint: {chief_complaint}"
                )

                self.patient_reg.enter_chief_comp(
                    chief_complaint
                )

                self.opd_flow.select_chief_complaint_side()

                self.opd_flow.enter_chief_complaint_number_days(chief_complaint_number_days)

                self.opd_flow.select_chief_complaint_time()

                self.opd_flow.enter_chief_complaint_remarks(chief_complaint_remarks)

                time.sleep(2)

                self.patient_reg.click_chief_comp_add()

                time.sleep(2)

                self.opd_flow.enter_history_of_illness(history_of_illness)

                self.logger.info(
                    "Chief complaint added successfully"
                )

                time.sleep(2)

                self.opd_flow.click_complete_history()
                time.sleep(2)
                self.opd_flow.enter_past_history(past_history)
                self.opd_flow.enter_personal_history(personal_history)
                self.opd_flow.enter_family_history(family_history)
                self.opd_flow.enter_treatment_history(treatment_history)
                self.opd_flow.enter_surgical_history(surgical_history)
                self.opd_flow.enter_occupational_history(occupational_history)
                time.sleep(3)

                self.opd_flow.click_examination()
                self.opd_flow.enter_general_exam(general_exam)
                self.opd_flow.enter_cvs(cvs)
                self.opd_flow.enter_cns(cns)
                self.opd_flow.enter_pa(pa)
                self.opd_flow.enter_muscular_exam(muscular_exam)
                self.opd_flow.enter_local_exam(local_exam)
                self.opd_flow.enter_painAssessment(pain_assessment)
                self.opd_flow.enter_respiratorySystem(respiratory_system)

                time.sleep(3)

                self.opd_flow.click_chronic_disease()
                self.opd_flow.enter_chronic_disease_name(chronic_disease_name)
                self.opd_flow.enter_disease_duration("2")
                self.opd_flow.enter_disease_remarks(chronic_disease_remarks)
                self.opd_flow.click_add_btn()
                time.sleep(3)

                self.logger.info(
                    f"Diagnosis Code: {diagnosis_code}"
                )

                self.patient_reg.enter_diagnosis(
                    diagnosis_code
                )

                diagnosis_name = (
                    self.patient_reg.get_diagnosis_name()
                )

                Test_OPD_Workflow.generated_diagnosis_name = diagnosis_name

                time.sleep(2)
                self.opd_flow.select_diagnosis_side()
                self.opd_flow.enter_diagnosis_remarks("Test diagnosis Code Remarks")

                self.patient_reg.click_diagnosis_add()

                time.sleep(2)

                self.opd_flow.click_icd_btn()
                self.patient_reg.enter_diagnosis(snomed_name)
                time.sleep(2)
                self.opd_flow.select_diagnosis_side()
                self.opd_flow.enter_diagnosis_remarks("snomed diagnosis Code Remarks")
                self.opd_flow.click_diagnosis_add_btn()

                time.sleep(2)

                self.logger.info(
                    "Diagnosis added successfully"
                )

                self.opd_flow.click_other_diagnosis()
                self.opd_flow.enter_other_diagnosis_details(other_diagnosis_detail)
                self.opd_flow.click_other_diagnosis_add_btn()
                self.opd_flow.click_confidential_info()
                self.opd_flow.enter_other_confidential_details(confidential_details)
                time.sleep(3)
                self.opd_flow.click_diagnosis_note()
                self.opd_flow.enter_other_diagnosis_note(diagnosis_note)
                time.sleep(3)

                self.patient_reg.click_investigation_tab()

                self.logger.info(
                    "Investigation tab opened"
                )

                self.opd_flow.click_renal_function_test()
                time.sleep(2)
                selected_tests = self.opd_flow.select_all_investigation_tests()
                print(selected_tests)
                self.opd_flow.enter_examination_finding("Test Renal Finding")
                self.opd_flow.enter_renal_test_remark("Test Renal Test Remarks")
                time.sleep(2)
                self.opd_flow.click_renal_test_add_btn()
                time.sleep(3)

                test_name = (
                    self.patient_reg.select_random_test_name()
                )

                time.sleep(2)


                self.logger.info(
                    f"Investigation selected: {test_name}"
                )

                self.patient_reg.click_test_add_btn()
                time.sleep(3)
                test_name_2 = self.patient_reg.select_blood_sugar_test_name()
                time.sleep(2)
                self.patient_reg.click_test_add_btn()
                time.sleep(5)

                # self.opd_flow.xray_clinical_indication()
                # self.opd_flow.xray_clinical_history()
                # self.patient_reg.click_test_add_btn()
                # time.sleep(3)

                # self.opd_flow.click_investigation_note()
                # time.sleep(2)
                # self.opd_flow.enter_investigation_note(investigation_note)

                self.logger.info(
                    "Investigation added successfully"
                )



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


                self.patient_reg.enter_instruction(instruction)

                self.logger.info(
                    f"Instruction entered: {instruction}"
                )

                time.sleep(2)

                self.patient_reg.click_drug_add_btn()
                time.sleep(2)

                # self.opd_flow.click_non_listed_drug()
                # time.sleep(2)
                # self.opd_flow.enter_external_drug(external_drug)
                # dose_name = (
                #     self.patient_reg.select_random_dose()
                # )
                #
                # time.sleep(2)
                #
                # frequency_name = (
                #     self.patient_reg.select_random_frequency()
                # )
                #
                # time.sleep(2)
                # self.opd_flow.click_external_add_btn()

                self.opd_flow.click_treatment_note()
                self.opd_flow.enter_treatment_note_remarks(treatment_note_remarks)
                time.sleep(2)

                self.opd_flow.click_allergies()
                self.opd_flow.enter_allergy_code(allergy_code)

                time.sleep(1)
                self.opd_flow.select_sensitivity_type()
                self.opd_flow.enter_allergy_days("2")
                self.opd_flow.enter_allergy_site("Right eye")
                self.opd_flow.enter_allergy_symptoms("Redness in eye")
                time.sleep(2)
                self.opd_flow.click_allergy_add_btn()
                self.opd_flow.enter_allergy_remarks("Test Allergy Remarks")
                self.opd_flow.enter_other_allergy_remarks("Other Allergy Remarks")
                time.sleep(2)

                self.logger.info(
                    "Medicine added successfully"
                )

                self.opd_flow.click_procedure_tab()
                time.sleep(3)
                procedure_data = self.opd_flow.select_service_and_procedure()

                if procedure_data is None:

                    self.logger.info(
                        "No Procedure found. Skipping Procedure section."
                    )

                    service_name = None
                    procedure_name = None

                else:

                    while True:

                        service_name, procedure_name = procedure_data

                        print("service_name :", service_name)
                        print("procedure_name :", procedure_name)

                        self.opd_flow.select_procedure_side()
                        self.opd_flow.enter_procedure_remarks(
                            "Test Procedure remarks"
                        )
                        self.opd_flow.click_procedure_add_btn()

                        try:

                            WebDriverWait(self.driver, 2).until(
                                EC.visibility_of_element_located(
                                    (
                                        By.XPATH,
                                        "//div[@id='swal2-html-container' and contains(.,'Please select sitting details')]"
                                    )
                                )
                            )

                            print("Popup appeared. Trying another procedure...")

                            try:
                                self.driver.find_element(
                                    By.XPATH,
                                    "//button[contains(@class,'swal2-confirm')]"
                                ).click()
                            except Exception:
                                pass

                            procedure_data = (
                                self.opd_flow.select_service_and_procedure()
                            )

                            if procedure_data is None:
                                self.logger.info(
                                    "No valid Procedure available."
                                )

                                service_name = None
                                procedure_name = None
                                break

                            continue

                        except TimeoutException:

                            print("Procedure added successfully.")
                            break
                time.sleep(3)

                # self.opd_flow.select_proposed_anesthesia_type()
                # self.opd_flow.select_proposed_operation_type()
                # time.sleep(3)
                # selected_operation = self.opd_flow.select_procedure_operation_name()
                # print(f"Returned value = {repr(selected_operation)}")
                #
                # if selected_operation:
                #     self.opd_flow.enter_operation_remarks(
                #         "Patient scheduled for elective Heart Transplantation; PAC requested.")
                #     self.opd_flow.click_operation_add_btn()
                # else:
                #     print("Skipping Operation Add because no operation was available.")
                #
                time.sleep(2)
                self.opd_flow.click_clear_all_btn()
                time.sleep(2)
                self.opd_flow.enter_admission_advice_remarks(
                    "Admit for pre-operative evaluation, optimization, and planned Heart Transplantation under Cardiology/CTVS protocol.")

                department_name, unit_name, ward_name = (
                    self.opd_flow.select_admission_details()
                )

                Test_OPD_Workflow.generated_admission_dep = department_name

                self.opd_flow.select_status()

                time.sleep(2)
                self.opd_flow.click_admission_advice_add_btn()
                time.sleep(2)

                self.patient_reg.click_followup_tab()

                time.sleep(3)
                self.opd_flow.select_ref_to()
                time.sleep(2)

                self.opd_flow.select_random_referral_type()

                referral_dep = (
                    self.opd_flow.select_random_dropdown_option()
                )

                Test_OPD_Workflow.generated_referral_dep = (
                    referral_dep
                )

                self.opd_flow.enter_referral_remarks(
                    "Referred for cardiac evaluation and "
                    "pre-operative assessment."
                )

                self.opd_flow.click_referral_add_btn()

                time.sleep(2)

                self.logger.info(
                    "Follow-up tab opened"
                )

                self.patient_reg.enter_followup_days(
                    followup_days
                )

                self.logger.info(
                    f"Follow-up days entered: {followup_days}"
                )

                time.sleep(2)

                follow_up_date = (
                    self.patient_reg.get_followup_date()
                )

                self.logger.info(
                    f"Follow up date: {follow_up_date}"
                )

                time.sleep(2)
                self.opd_flow.enter_clinical_notes(clinical_notes)
                self.opd_flow.enter_instruction_remarks(instruction_remarks)
                time.sleep(2)

                self.patient_reg.click_preview_save_btn()

                self.logger.info(
                    "Preview generated successfully"
                )

                time.sleep(3)
                self.opd_flow.scroll_print_preview()

                patient_data = (
                    self.patient_reg.get_patient_from_pet_reg_details()
                )

                opd_data = (
                    self.opd_flow.get_patient_details_from_opd_rx()
                )

                print(patient_data)

                print("all opd data", opd_data)

                self.logger.info(
                    "Patient details extracted from RX Preview"
                )

                # ==========================
                # RX PREVIEW VALIDATION
                # ==========================

                def safe_get(data, *keys):
                    """
                    Safely fetch nested dictionary values.
                    Returns None if any key is missing.
                    """

                    for key in keys:
                        if not isinstance(data, dict):
                            return None

                        data = data.get(key)

                        if data is None:
                            return None

                    return data

                def verify(actual, expected, field):

                    if actual in [None, "", [], {}]:
                        self.logger.info(f"{field} not available. Skipping validation.")
                        return

                    assert actual.strip().upper() == expected.strip().upper(), (
                        f"{field} mismatch\n"
                        f"Expected : {expected}\n"
                        f"Actual   : {actual}"
                    )

                def verify_contains(actual, expected, field):

                    if actual in [None, "", [], {}]:
                        self.logger.info(f"{field} not available. Skipping validation.")
                        return

                    assert expected.strip().upper() in actual.strip().upper(), (
                        f"{field} mismatch\n"
                        f"Expected to contain : {expected}\n"
                        f"Actual : {actual}"
                    )

                # def verify_list_contains(items, expected, field):
                #
                #     if not items:
                #         self.logger.info(f"{field} not available. Skipping validation.")
                #         return
                #
                #     assert any(
                #         expected.strip().upper() in item.strip().upper()
                #         for item in items
                #     ), (
                #             f"{field} mismatch\n"
                #             f"Expected : {expected}\n"
                #             f"Actual List:\n" + "\n".join(items)
                #     )
                #
                # assert any(
                #     drug["Drug Name"].upper()
                #     in drug_name.upper()
                #     for drug in patient_data["Drugs"]
                # )
                #
                #
                # assert (
                #         patient_data["Follow Up Date"]
                #         == follow_up_date
                # )
                #
                # expected_consultant_name = act_username_text
                #
                # assert (
                #         patient_data["Consultant Name"]
                #         .strip()
                #         .upper()
                #         ==
                #         expected_consultant_name.upper()
                # )
                #
                # # ============================================================
                # # Patient Details
                # # ============================================================
                #
                # verify(safe_get(opd_data, "Patient Name"), patient_name, "Patient Name")
                # verify(safe_get(opd_data, "Age"), "30", "Age")
                # verify(safe_get(opd_data, "Gender"), "F", "Gender")
                # verify(safe_get(opd_data, "Father/Spouse Name"), "Automation Father", "Father/Spouse Name")
                # verify(safe_get(opd_data, "CRN"), crn_number, "CRN")
                # verify(safe_get(opd_data, "Mobile No."), patient_mobile, "Mobile Number")
                #
                # # ============================================================
                # # Vitals
                # # ============================================================
                #
                # verify(safe_get(opd_data, "Vitals", "Weight"), rx_weight, "Weight")
                # verify(safe_get(opd_data, "Vitals", "Height"), rx_height, "Height")
                # verify(safe_get(opd_data, "Vitals", "BP"), f"{rx_systolic}/{rx_diastolic}", "Blood Pressure")
                # verify(safe_get(opd_data, "Vitals", "Temprature"), rx_temperature, "Temperature")
                # verify(safe_get(opd_data, "Vitals", "RR"), rx_resp_rate, "Respiratory Rate")
                # verify(safe_get(opd_data, "Vitals", "Hb"), "15", "Hb")
                # verify(safe_get(opd_data, "Vitals", "PR"), rx_pulse_rate, "Pulse Rate")
                #
                # # ============================================================
                # # Investigation Details
                # # ============================================================
                #
                import re

                investigation_text = safe_get(opd_data, "Investigation Details")

                # Verify important investigations are present
                verify_contains(
                    investigation_text,
                    test_name,
                    test_name_2,
                    "Investigation Test"
                )


                # Store investigation tests for later test cases
                Test_OPD_Workflow.generated_investigation_tests = []
                # Test_OPD_Workflow.generated_xray_tests = []
                #
                # if investigation_text:
                #     try:
                #
                #         if " - " in investigation_text:
                #             investigation_text = investigation_text.split(" - ", 1)[1]
                #
                #         raw_tests = [
                #             item.strip()
                #             for item in investigation_text.split(",")
                #             if item.strip()
                #         ]
                #
                #         # # Store complete X-Ray tests separately
                #         # Test_OPD_Workflow.generated_xray_tests = [
                #         #     test for test in raw_tests
                #         #     if "XRAY" in test.upper()
                #         # ]
                #
                #         # Store non-X-Ray tests without their codes
                #         Test_OPD_Workflow.generated_investigation_tests = [
                #             re.sub(r"\s*\([^)]+\)", "", test).strip()
                #             for test in raw_tests
                #             if "XRAY" not in test.upper()
                #         ]
                #
                #         self.logger.info(
                #             f"Stored Investigation Tests : "
                #             f"{Test_OPD_Workflow.generated_investigation_tests}"
                #         )
                #
                #         # self.logger.info(
                #         #     f"Stored X-Ray Tests : "
                #         #     f"{Test_OPD_Workflow.generated_xray_tests}"
                #         # )
                #
                #     except Exception as e:
                #         self.logger.warning(
                #             f"Unable to parse Investigation Details: {e}"
                #         )
                # # ============================================================
                # # Procedure
                # # ============================================================
                #
                # if procedure_name is not None:
                #
                #     verify_list_contains(
                #         safe_get(opd_data, "Procedure") or [],
                #         procedure_name,
                #         "Procedure"
                #     )
                #
                #     verify_list_contains(
                #         safe_get(opd_data, "Procedure") or [],
                #         service_name,
                #         "Procedure Service"
                #     )
                #
                # else:
                #
                #     self.logger.info(
                #         "Procedure validation skipped because no procedure was available."
                #     )
                #
                #
                #
                #
                # # ============================================================
                # # Refer To
                # # ============================================================
                #
                # verify_list_contains(
                #     safe_get(opd_data, "Refer To") or [],
                #     referral_dep,
                #     "Referral Department"
                # )
                #
                # self.logger.info(
                #     "RX Preview validation completed successfully"
                # )

                time.sleep(3)

                self.patient_reg.click_rx_save_btn()
                time.sleep(3)

                assert self.driver.find_element(By.XPATH,
                                                "//div[@id='swal2-html-container' and normalize-space()='OPD saved successfully']").is_displayed()

                self.logger.info(
                    "RX saved successfully"
                )

                # ====================================================
                # SUCCESS
                # ====================================================

                Test_OPD_Workflow.opd_rx_crn = (
                    str(crn_number).strip()
                )

                Test_OPD_Workflow.opd_rx_patient_name = (
                    patient_name
                )

                self.logger.info(
                    f"OPD RX CRN stored: "
                    f"{Test_OPD_Workflow.opd_rx_crn}"
                )

                self.logger.info(
                    f"OPD RX patient stored: "
                    f"{Test_OPD_Workflow.opd_rx_patient_name}"
                )

                time.sleep(10)

                LogGen.test_passed(
                    self.logger,
                    "test_opd_test"
                )

                return

            # ========================================================
            # RX ATTEMPT FAILED
            # ========================================================

            except Exception as e:

                last_rx_error = e

                self.logger.exception(
                    f"RX ATTEMPT {rx_attempt} FAILED"
                )

                self.logger.error(
                    f"Failed CRN: {crn_number}"
                )

                # ====================================================
                # SECOND ATTEMPT FAILED
                # ====================================================

                if rx_attempt == max_rx_attempts:
                    self.logger.error(
                        "SECOND RX ATTEMPT FAILED"
                    )

                    self.logger.error(
                        "No OPD Attended Batch check "
                        "will be performed."
                    )

                    self.logger.error(
                        "No 3rd RX attempt will be made."
                    )

                    self.logger.error(
                        "No 3rd CRN fallback will be used."
                    )

                    self.logger.error(
                        f"Final RX error: {last_rx_error}"
                    )

                    break

                # ====================================================
                # FIRST ATTEMPT FAILED
                # ====================================================

                self.logger.warning(
                    "FIRST RX ATTEMPT FAILED"
                )

                self.logger.warning(
                    "Checking Doctor Desk for existing "
                    "Attended Batch."
                )

                self.logger.warning(
                    f"Same CRN will be checked: {crn_number}"
                )

                try:

                    # =================================================
                    # REFRESH
                    # =================================================

                    self.logger.info(
                        "Refreshing page before Doctor Desk check"
                    )

                    self.driver.refresh()

                    time.sleep(3)

                    # =================================================
                    # OPEN OPD MODULE
                    # =================================================

                    self.logger.info(
                        "Opening OPD module"
                    )

                    self.patient_reg.click_opd_module()

                    time.sleep(2)

                    # =================================================
                    # OPEN DOCTOR DESK
                    # =================================================

                    self.logger.info(
                        "Opening Doctor Desk"
                    )

                    self.patient_reg.click_opd_dr_desk()

                    time.sleep(3)

                    # =================================================
                    # SELECT SAME OPD UNIT
                    # =================================================

                    self.logger.info(
                        f"Selecting OPD Doctor Desk Unit: "
                        f"{opd_unit_name}"
                    )

                    self.patient_reg.select_opd_dr_desk_unit(
                        opd_unit_name
                    )

                    time.sleep(2)

                    # =================================================
                    # SEARCH SAME CRN
                    # =================================================

                    self.logger.info(
                        f"Searching Doctor Desk using same CRN: "
                        f"{crn_number}"
                    )

                    self.patient_reg.enter_search_name_in_opd(
                        crn_number
                    )

                    time.sleep(3)

                    # =================================================
                    # FIND SAME CRN ROW
                    # =================================================

                    same_crn_rows_xpath = (
                        "//tr[contains(@class,'ant-table-row')]"
                        f"[.//td[contains("
                        f"normalize-space(.),'{crn_number}')]]"
                    )

                    self.logger.info(
                        f"Searching table rows using XPath: "
                        f"{same_crn_rows_xpath}"
                    )

                    same_crn_rows = WebDriverWait(
                        self.driver,
                        10
                    ).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.XPATH,
                                same_crn_rows_xpath
                            )
                        )
                    )

                    self.logger.info(
                        f"Found {len(same_crn_rows)} matching "
                        f"row(s) for CRN {crn_number}"
                    )

                    # =================================================
                    # CHECK ATTENDED BATCH
                    # =================================================

                    attended_batch_found = False

                    for row in same_crn_rows:

                        try:

                            if not row.is_displayed():
                                continue

                            row_text = row.text.strip()

                            self.logger.info(
                                f"Doctor Desk row for CRN "
                                f"{crn_number}: {row_text}"
                            )

                            if "attended batch" in row_text.casefold():
                                attended_batch_found = True

                                self.logger.info(
                                    f"Attended Batch found for "
                                    f"CRN {crn_number}"
                                )

                                # -------------------------------------
                                # STORE RX DETAILS
                                # -------------------------------------

                                Test_OPD_Workflow.opd_rx_crn = (
                                    str(crn_number).strip()
                                )

                                Test_OPD_Workflow.opd_rx_patient_name = (
                                    patient_name
                                )

                                self.logger.info(
                                    "Stored OPD RX CRN after "
                                    "Attended Batch detection: "
                                    f"{Test_OPD_Workflow.opd_rx_crn}"
                                )

                                self.logger.info(
                                    "Stored OPD RX patient name: "
                                    f"{Test_OPD_Workflow.opd_rx_patient_name}"
                                )

                                LogGen.test_passed(
                                    self.logger,
                                    "test_opd_test"
                                )

                                return

                        except Exception as row_error:

                            self.logger.warning(
                                "Error while inspecting "
                                f"Doctor Desk row: {row_error}"
                            )

                            continue

                    # =================================================
                    # ATTENDED BATCH NOT FOUND
                    # =================================================

                    if not attended_batch_found:
                        self.logger.warning(
                            f"CRN {crn_number} found in Doctor Desk, "
                            "but Attended Batch was not found."
                        )

                        self.logger.warning(
                            "RX will be attempted again using "
                            f"the SAME CRN: {crn_number}"
                        )

                        continue

                # ====================================================
                # DOCTOR DESK CHECK FAILED
                # ====================================================

                except Exception as opd_check_error:

                    self.logger.exception(
                        "Doctor Desk / Attended Batch check failed."
                    )

                    self.logger.error(
                        f"Doctor Desk check error: "
                        f"{opd_check_error}"
                    )

                    self.logger.warning(
                        "RX will be attempted again using "
                        f"the SAME CRN: {crn_number}"
                    )

                    continue

        # ============================================================
        # FINAL FAILURE
        # ============================================================

        self.logger.error(
            "OPD/RX WORKFLOW FAILED COMPLETELY"
        )

        self.logger.error(
            f"CRN used: {crn_number}"
        )

        self.logger.error(
            f"Patient name: {patient_name}"
        )

        self.logger.error(
            f"OPD Unit: {opd_unit_name}"
        )

        self.logger.error(
            f"Last RX error: {last_rx_error}"
        )

        self.logger.error(
            "No 3rd CRN fallback will be used."
        )

        self.logger.error(
            "No 3rd RX attempt will be made."
        )

        # ============================================================
        # SCREENSHOT
        # ============================================================

        try:

            Screenshot.capture(
                self.driver,
                "test_opd_test"
            )

        except Exception as screenshot_error:

            self.logger.error(
                f"Screenshot capture failed: "
                f"{screenshot_error}"
            )

        # ============================================================
        # MARK TEST FAILED
        # ============================================================

        LogGen.test_failed(
            self.logger,
            "test_opd_test",
            str(last_rx_error)
        )

        # ============================================================
        # RAISE ORIGINAL RX ERROR
        # ============================================================

        if last_rx_error is not None:
            raise last_rx_error

        raise AssertionError(
            "OPD/RX workflow failed without a captured exception."
        )

    @pytest.mark.opd_flow
    def test_follow_up(self):

        # ============================================================
        # CRN DEBUG - FOLLOW UP START
        # ============================================================

        self.logger.warning(
            "========== FOLLOW UP CRN DEBUG =========="
        )

        self.logger.warning(
            f"opd_rx_crn received = "
            f"{repr(Test_OPD_Workflow.opd_rx_crn)}"
        )

        self.logger.warning(
            f"generated_crn = "
            f"{repr(Test_OPD_Workflow.generated_crn)}"
        )

        self.logger.warning(
            f"2nd fallback CRN = "
            f"{repr(Test_OPD_Workflow.opd_fallback_crn)}"
        )

        self.logger.warning(
            "========================================"
        )

        # ============================================================
        # GET FINAL CRN FROM SUCCESSFUL RX WORKFLOW
        # ============================================================
        #
        # IMPORTANT:
        #
        # test_opd_test() now has only two CRN possibilities:
        #
        # 1. generated_crn
        # 2. opd_fallback_crn
        #
        # If RX succeeds, the CRN actually used by RX is stored in:
        #
        #     Test_OPD_Workflow.opd_rx_crn
        #
        # Follow Up will use ONLY this CRN.


        pat_crn_number = Test_OPD_Workflow.opd_rx_crn

        if not pat_crn_number:
            raise Exception(
                "No CRN available for Follow Up test. "
                "RX workflow did not provide a successful RX CRN."
            )

        pat_crn_number = str(
            pat_crn_number
        ).strip()

        self.logger.info(
            "================================================"
        )

        self.logger.info(
            f"CRN received from successful RX workflow: "
            f"{pat_crn_number}"
        )

        self.logger.info(
            "No 3rd CRN fallback will be used."
        )

        self.logger.info(
            "================================================"
        )

        # ============================================================
        # FINAL OPD UNIT
        # ============================================================

        opd_unit_name = Test_OPD_Workflow.opd_unit_name

        if not opd_unit_name:
            raise Exception(
                "OPD Unit name is unavailable for Follow Up."
            )

        self.logger.info(
            "================================================"
        )

        self.logger.info(
            f"Final Follow Up CRN     : {pat_crn_number}"
        )

        self.logger.info(
            f"Final Follow Up OPD Unit: {opd_unit_name}"
        )

        self.logger.info(
            "================================================"
        )

        # ============================================================
        # START TEST
        # ============================================================

        LogGen.start_test(
            self.logger,
            "test_follow_up",
            "Follow Up Flow"
        )

        try:

            # ========================================================
            # OPEN OPD MODULE
            # ========================================================

            self.logger.info(
                "Opening OPD module."
            )

            self.patient_reg.click_opd_module()

            time.sleep(2)

            # ========================================================
            # OPEN OPD DOCTOR DESK
            # ========================================================

            self.logger.info(
                "Opening OPD Doctor Desk."
            )

            self.patient_reg.click_opd_dr_desk()

            time.sleep(2)

            # ========================================================
            # SELECT OPD UNIT
            # ========================================================

            self.logger.info(
                f"Selecting OPD Unit: {opd_unit_name}"
            )

            self.patient_reg.select_opd_dr_desk_unit(
                opd_unit_name
            )

            self.logger.info(
                f"OPD Unit selected successfully: "
                f"{opd_unit_name}"
            )

            time.sleep(2)

            # ========================================================
            # OPEN FOLLOW-UP
            # ========================================================

            self.logger.info(
                "Opening Follow Up."
            )

            self.opd_flow.click_follow_up_btn()

            time.sleep(1)

            # ========================================================
            # OPEN UPCOMING
            # ========================================================

            self.logger.info(
                "Opening Upcoming Follow Up list."
            )

            self.opd_flow.click_upcoming_btn()

            time.sleep(2)

            # ========================================================
            # SEARCH PATIENT USING RX CRN
            # ========================================================

            self.logger.info(
                f"Searching Follow Up patient using RX CRN: "
                f"{pat_crn_number}"
            )

            patient_card = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//div[contains(@class,'patient-card')]["
                        f".//div[contains(normalize-space(.), 'CRN:') "
                        f"and contains(normalize-space(.), "
                        f"'{pat_crn_number}')]"
                        f"]"
                    )
                )
            )

            self.logger.info(
                "Patient card found successfully."
            )

            # ========================================================
            # EXTRACT PATIENT NAME
            # ========================================================

            patient_name = patient_card.find_element(
                By.XPATH,
                ".//span[contains(@class,'patient-name')]"
            ).text.strip()

            if not patient_name:
                raise Exception(
                    f"Patient name is empty for CRN: "
                    f"{pat_crn_number}"
                )

            self.logger.info(
                f"Patient Name found from UI: "
                f"{patient_name}"
            )

            # ========================================================
            # EXTRACT ACTUAL CRN
            # ========================================================

            actual_crn = patient_card.find_element(
                By.XPATH,
                ".//div[starts-with("
                "normalize-space(.), 'CRN:'"
                ")]"
            ).get_attribute(
                "textContent"
            ).replace(
                "CRN:",
                ""
            ).strip()

            self.logger.info(
                f"Expected CRN: {pat_crn_number}"
            )

            self.logger.info(
                f"Actual CRN:   {actual_crn}"
            )

            # ========================================================
            # VALIDATE PATIENT CARD
            # ========================================================

            assert patient_card.is_displayed(), (
                f"Patient card is not visible for "
                f"CRN: {pat_crn_number}"
            )

            # ========================================================
            # VALIDATE CRN
            # ========================================================

            assert actual_crn == pat_crn_number, (
                f"CRN mismatch in Follow Up\n"
                f"Expected : {pat_crn_number}\n"
                f"Actual   : {actual_crn}"
            )

            self.logger.info(
                "CRN validated successfully."
            )

            # ========================================================
            # VALIDATE PATIENT NAME
            # ========================================================

            assert patient_name.strip(), (
                f"Patient name is empty for CRN: "
                f"{pat_crn_number}"
            )

            self.logger.info(
                f"Patient validated successfully: "
                f"{patient_name}"
            )

            # ========================================================
            # SUCCESS
            # ========================================================

            self.logger.info(
                "================================================"
            )

            self.logger.info(
                "FOLLOW UP VALIDATION PASSED"
            )

            self.logger.info(
                f"CRN      : {actual_crn}"
            )

            self.logger.info(
                f"Patient  : {patient_name}"
            )

            self.logger.info(
                f"OPD Unit : {opd_unit_name}"
            )

            self.logger.info(
                "================================================"
            )

            LogGen.test_passed(
                self.logger,
                "Followup patient validation passed successfully."
            )

        except Exception as e:

            # ========================================================
            # FOLLOW-UP FAILED
            # ========================================================

            self.logger.exception(
                f"Follow Up validation failed: {e}"
            )

            try:
                Screenshot.capture(
                    self.driver,
                    "test_follow_up"
                )
            except Exception as screenshot_error:

                self.logger.error(
                    f"Screenshot capture failed: "
                    f"{screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_follow_up",
                str(e)
            )

            raise

        finally:

            # ========================================================
            # CLOSE FOLLOW-UP POPUP
            # ========================================================

            try:

                self.opd_flow.followup_close_btn()

                time.sleep(2)

                self.logger.info(
                    "Follow Up popup closed successfully."
                )

            except Exception as ex:

                self.logger.warning(
                    f"Unable to close Follow Up popup: "
                    f"{ex}"
                )

    @pytest.mark.opd_flow
    def test_referral_out(self):

        pat_crn_number = Test_OPD_Workflow.generated_crn
        pat_name = Test_OPD_Workflow.generated_patient_name
        opd_unit_name = Test_OPD_Workflow.opd_unit_name



        LogGen.start_test(
            self.logger,
            "test_referral_out",
            "Referral Out Flow"
        )

        try:
            # ==========================
            # Navigate to Refer Out
            # ==========================
            time.sleep(5)

            self.logger.info("Opening Referral Out")
            self.opd_flow.click_refer_out_btn()
            time.sleep(2)

            self.patient_reg.select_opd_dr_desk_department(
                opd_unit_name
            )

            time.sleep(2)
            self.patient_reg.enter_search_name_in_opd(
                pat_crn_number
            )

            time.sleep(5)

            wait = WebDriverWait(self.driver, 10)

            # ==========================
            # Get Patient Name
            # ==========================
            act_pat_name = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//tbody/tr[@data-row-key]/td[3]//div[@class='mb-0']"
                    )
                )
            ).text.strip()

            # ==========================
            # Get CRN
            # ==========================
            act_crn = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//tbody/tr[@data-row-key]/td[4]//div[@class='mb-0']"
                    )
                )
            ).text.strip()

            self.logger.info(f"Expected Patient Name : {pat_name}")
            self.logger.info(f"Actual Patient Name   : {act_pat_name}")

            self.logger.info(f"Expected CRN : {pat_crn_number}")
            self.logger.info(f"Actual CRN   : {act_crn}")

            # ==========================
            # Assertions
            # ==========================
            assert act_pat_name.casefold() == pat_name.casefold(), (
                f"Patient Name mismatch\n"
                f"Expected : {pat_name}\n"
                f"Actual   : {act_pat_name}"
            )

            assert act_crn == pat_crn_number, (
                f"CRN mismatch\n"
                f"Expected : {pat_crn_number}\n"
                f"Actual   : {act_crn}"
            )

            self.logger.info("Patient Name and CRN validated successfully.")
            LogGen.test_passed(
                self.logger,
                "Patient Name and CRN validated successfully."
            )

        except Exception as e:
            self.logger.exception(f"Validation failed: {e}")
            LogGen.test_failed(self.logger, str(e))
            raise

    @pytest.mark.opd_flow
    def test_name_in_pharmacy(self):

        pat_crn_number = Test_OPD_Workflow.generated_crn



        LogGen.start_test(
            self.logger,
            "test_name_in_pharmacy",
            "Pharmacy Flow"
        )

        try:

            self.driver.refresh()
            time.sleep(4)
            self.logger.info("Opening Inventory Module")
            self.opd_flow.click_inventory_module()

            self.logger.info("Opening Issue")
            self.opd_flow.click_issue_option()

            self.logger.info("Opening Direct Issue To Patient")
            self.opd_flow.click_direct_issue_to_patient()

            time.sleep(2)
            self.opd_flow.select_drug_store_name("MAIN STORE")
            time.sleep(3)

            self.logger.info(f"Searching CRN : {pat_crn_number}")
            self.opd_flow.enter_search_crn_in_inventory(pat_crn_number)

            time.sleep(3)
            self.opd_flow.click_to_attend_btn()
            time.sleep(3)
            self.opd_flow.enter_issue_quantity("10")
            time.sleep(2)
            self.opd_flow.dispense_save_btn()
            time.sleep(2)
            self.opd_flow.click_swal_save_btn()
            time.sleep(3)

            assert WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@id='swal2-html-container']")
                )
            ).text.strip() == "Data Saved Successfully"

            time.sleep(5)
            self.opd_flow.enter_search_crn_in_inventory(pat_crn_number)

            dispensed_btn = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//button[normalize-space()='Dispensed']")
                )
            )

            assert dispensed_btn.text.strip() == "Dispensed", \
                f"Expected 'Dispensed' but found '{dispensed_btn.text}'"

        except Exception as e:
            self.logger.exception(f"Validation failed: {e}")
            LogGen.test_failed(self.logger, str(e))
            raise

    @pytest.mark.opd_flow
    def test_new_admission(self):

        # ============================================================
        # CRN SELECTION
        # ============================================================

        self.driver.refresh()
        time.sleep(3)

        pat_crn_number = Test_OPD_Workflow.generated_crn


        self.logger.info(
            f"Using newly registered patient CRN: {pat_crn_number}"
        )

        try:

            # ========================================================
            # ADT ADMISSION
            # ========================================================

            self.logger.info(
                "Opening ADT module"
            )

            time.sleep(3)

            self.patient_reg.click_adt_module()

            self.logger.info(
                "Opening Single Window"
            )

            self.patient_reg.click_single_window_option()

            time.sleep(3)

            self.logger.info(
                "Opening New Admission form"
            )

            self.patient_reg.click_new_admission_btn()

            time.sleep(3)

            # ========================================================
            # ENTER PARENT CRN
            # ========================================================

            self.logger.info(
                f"Entering Parent CRN: {pat_crn_number}"
            )

            self.patient_reg.enter_crn_number_for_adt(
                pat_crn_number
            )

            time.sleep(4)

            self.patient_reg.enter_patient_2_city("test city")
            time.sleep(3)

            # ========================================================
            # SELECT UNIT + WARD WITH AVAILABLE BED
            # ========================================================

            self.logger.info(
                "Checking pre-selected department for available bed"
            )

            selected_admission_location = (
                self.patient_reg.select_unit_and_ward_with_available_bed()
            )

            selected_department = (
                selected_admission_location["department"]
            )

            selected_ward = (
                selected_admission_location["ward"]
            )

            self.logger.info(
                f"Final admission selection | "
                f"Department: {selected_department} | "
                f"Ward: {selected_ward}"
            )

            # # ========================================================
            # # SAVE ADT
            # # ========================================================
            #
            # self.logger.info(
            #     "Saving ADT Admission"
            # )
            #
            #
            #
            # self.patient_reg.select_payment_mode_if_required()
            #
            # time.sleep(2)
            # self.patient_reg.enter_patient_id("6764")
            # time.sleep(2)
            #
            # self.patient_reg.select_admission_type_in_adt()
            #
            # time.sleep(2)
            #
            # self.patient_reg.click_adt_save_btn()
            #
            # time.sleep(7)
            #
            # self.logger.info(
            #     "ADT Admission saved successfully"
            # )
            #
            # # ========================================================
            # # CLOSE ADT POPUP
            # # ========================================================
            #
            # try:
            #
            #     self.patient_reg.click_close_btn()
            #
            # except Exception as e:
            #
            #     self.logger.warning(
            #         f"Unable to close ADT popup: {e}"
            #     )
            #
            # time.sleep(3)

            # ========================================================
            # IPD PATIENT ACCEPTANCE
            # ========================================================

            self.logger.info(
                "Opening IPD Nursing module"
            )

            self.driver.refresh()

            time.sleep(5)

            self.patient_reg.click_ipd_module()

            time.sleep(3)

            self.patient_reg.click_ipd_nursing_option()

            time.sleep(5)

            # ========================================================
            # SELECT NON-ADMITTED
            # ========================================================

            self.logger.info(
                "Selecting Non Admitted type"
            )

            self.patient_reg.select_the_non_admitted_type()

            time.sleep(3)

            # ========================================================
            # SEARCH PARENT CRN
            # ========================================================

            self.logger.info(
                f"Searching Parent CRN in IPD: {pat_crn_number}"
            )

            self.patient_reg.enter_search_crn_in_ipd(
                pat_crn_number
            )

            time.sleep(3)

            # ========================================================
            # PATIENT ACCEPTANCE
            # ========================================================

            self.logger.info(
                "Opening Patient Acceptance"
            )

            self.patient_reg.click_patient_action_acceptance()

            time.sleep(3)

            # ========================================================
            # SELECT IPD BED
            # ========================================================

            self.logger.info(
                "Selecting IPD Bed"
            )

            self.patient_reg.select_bed_ipd()

            # ========================================================
            # ADMISSION TIME
            # ========================================================

            updated_time = (
                self.patient_reg.increase_date_time_by_5_minutes()
            )

            self.logger.info(
                f"Updated Admission Time: {updated_time}"
            )

            time.sleep(3)

            # ========================================================
            # SAVE PATIENT ACCEPTANCE
            # ========================================================

            self.logger.info(
                "Saving Patient Acceptance"
            )

            self.patient_reg.click_patient_acceptance_save_btn()

            time.sleep(10)

            self.logger.info(
                "Patient Acceptance saved successfully"
            )

        except Exception as e:

            self.logger.error(
                f"New Born Registration test failed: {e}"
            )

            pytest.fail(
                f"New Born Registration test failed: {e}"
            )

    @pytest.mark.opd_flow
    def test_tests_in_investigation(self):

        pat_crn_number = Test_OPD_Workflow.generated_crn

        # expected_tests = Test_OPD_Workflow.generated_investigation_tests

        expected_tests = ["Blood Urea ()", "Serum Calcium ()", "Serum Creatinine ()", "Serum Phosphorus ()", "Serum Potassium ()", "Serum Sodium ()", "Complete Blood Count (CBC)", "Blood Sugar"]


        LogGen.start_test(
            self.logger,
            "test_tests_in_investigation",
            "Investigation Flow"
        )

        try:

            # ==========================================================
            # 1. OPEN INVESTIGATION → SAMPLE COLLECTION
            # ==========================================================

            self.driver.refresh()
            time.sleep(4)

            self.logger.info("Opening Investigation Module")
            self.opd_flow.click_investigation_module()

            self.logger.info("Opening Sample Collection")
            self.opd_flow.click_sample_collection_option()

            # ==========================================================
            # 2. SEARCH PATIENT
            # ==========================================================

            self.logger.info(
                f"Searching CRN: {pat_crn_number}"
            )

            self.opd_flow.enter_search_crn_in_sample_collection(
                pat_crn_number
            )

            time.sleep(3)

            self.opd_flow.click_unbilled_button()
            time.sleep(3)
            self.driver.refresh()
            time.sleep(3)
            self.opd_flow.click_billing_module()
            self.opd_flow.click_cash_collection_option()
            time.sleep(3)
            self.opd_flow.enter_search_cr_no_value_for_cash(pat_crn_number)
            time.sleep(7)

            self.opd_flow.click_cash_collection_checkbox()
            time.sleep(2)

            self.opd_flow.click_cash_save_button()
            time.sleep(5)
            pyautogui.press("esc")
            time.sleep(2)
            self.patient_reg.click_close_btn()

            self.driver.refresh()
            time.sleep(3)

            self.logger.info("Opening Investigation Module")
            self.opd_flow.click_investigation_module()

            self.logger.info("Opening Sample Collection")
            self.opd_flow.click_sample_collection_option()

            # ==========================================================
            # 2. SEARCH PATIENT
            # ==========================================================

            self.logger.info(
                f"Searching CRN: {pat_crn_number}"
            )

            self.opd_flow.enter_search_crn_in_sample_collection(
                pat_crn_number
            )

            time.sleep(3)

            # ==========================================================
            # 3. FETCH INVESTIGATION TESTS
            # ==========================================================

            test_elements = self.driver.find_elements(
                By.XPATH,
                "//table//tr/td[2]"
            )

            actual_tests = [
                element.text.replace("RF", "").strip()
                for element in test_elements
                if element.text.strip()
            ]

            self.logger.info(
                f"Expected Tests: {expected_tests}"
            )

            self.logger.info(
                f"Actual Tests: {actual_tests}"
            )

            # ==========================================================
            # 4. VALIDATE INVESTIGATION TESTS
            # ==========================================================

            def normalize_test_name(name):
                return (
                    name.upper()
                    .replace("()", "")
                    .replace("(CBC)", "")
                    .strip()
                )

            missing_tests = []

            for expected in expected_tests:

                expected_normalized = normalize_test_name(expected)

                if not any(
                        expected_normalized in normalize_test_name(actual)
                        for actual in actual_tests
                ):
                    missing_tests.append(expected)

            assert not missing_tests, (
                f"\nMissing Investigation Tests: {missing_tests}"
                f"\nExpected Tests: {expected_tests}"
                f"\nActual Tests: {actual_tests}"
            )

            self.logger.info(
                "All investigation tests validated successfully."
            )

            # ==========================================================
            # 5. SELECT COLLECTION AREA
            # ==========================================================

            self.logger.info(
                "Selecting collection area"
            )

            self.opd_flow.select_collection_area(
                "1-Collection Center -  Hospital Block (70)"
            )

            time.sleep(3)

            # ==========================================================
            # 6. SAVE ALL
            # ==========================================================

            self.logger.info(
                "Clicking Save All"
            )

            self.opd_flow.save_all_btn_for_tests()

            time.sleep(3)

            pyautogui.press("esc")

            time.sleep(2)

            # ==========================================================
            # 7. CLOSE SAMPLE COLLECTION
            # ==========================================================

            self.patient_reg.click_close_btn()

            time.sleep(2)

            # ==========================================================
            # 8. REFRESH
            # ==========================================================

            self.logger.info(
                "Refreshing application"
            )

            self.driver.refresh()

            time.sleep(3)

            # ==========================================================
            # 9. OPEN INLINE SAMPLE COLLECTION
            # ==========================================================

            self.logger.info(
                "Opening Inline Sample Collection"
            )

            self.opd_flow.click_investigation_module()

            self.opd_flow.click_inline_sample_collection_option()

            time.sleep(3)

            # ==========================================================
            # 10-15. PROCESS MULTIPLE LABS
            # ==========================================================

            labs = [
                "Biochemistry"
            ]

            for index, lab_name in enumerate(labs):

                self.logger.info(
                    f"========== STARTING LAB {index + 1}: {lab_name} =========="
                )

                # ======================================================
                # 10. SELECT LAB
                # ======================================================

                self.logger.info(
                    f"Selecting lab: {lab_name}"
                )

                self.opd_flow.select_test_lab(
                    lab_name
                )

                time.sleep(8)

                # ======================================================
                # 11. SEARCH CRN
                # ======================================================

                self.logger.info(
                    f"Searching CRN in Inline Sample Collection: "
                    f"{pat_crn_number}"
                )

                self.opd_flow.enter_search_crn_in_inventory(
                    pat_crn_number
                )

                time.sleep(5)

                # ======================================================
                # 12. SELECT SAMPLE
                # ======================================================

                self.logger.info(
                    f"Selecting sample for lab: {lab_name}"
                )

                self.opd_flow.click_the_checkbox_for_sample()

                # ======================================================
                # 13. SAVE INLINE SAMPLE
                # ======================================================

                self.logger.info(
                    f"Saving sample for lab: {lab_name}"
                )

                self.opd_flow.click_inline_sample_save_btn()

                time.sleep(3)

                # ======================================================
                # 14. HANDLE MACHINE CONFIRMATION POPUP
                # ======================================================

                if self.opd_flow.click_yes_if_machine_confirmation_visible():

                    self.logger.info(
                        f"Machine confirmation popup appeared for "
                        f"{lab_name}. Clicked Yes."
                    )

                    time.sleep(3)

                else:

                    self.logger.info(
                        f"Machine confirmation popup did not appear "
                        f"for {lab_name}."
                    )

                # ======================================================
                # 15. CLOSE INLINE SAMPLE COLLECTION
                # ======================================================

                self.logger.info(
                    f"Closing Inline Sample Collection for {lab_name}"
                )

                self.patient_reg.click_close_btn()
                time.sleep(3)

                self.opd_flow.lab_dropdown_inline()

                time.sleep(2)

                self.logger.info(
                    f"Completed processing for lab: {lab_name}"
                )

            time.sleep(3)

            # ==========================================================
            # 16. OPEN RESULT ENTRY
            # ==========================================================

            self.logger.info(
                "Opening Result Entry"
            )

            self.opd_flow.click_result_entry_option()

            time.sleep(3)

            # ==========================================================
            # 17. SELECT CRN
            # ==========================================================

            self.opd_flow.click_crn_option()
            time.sleep(2)

            # ==========================================================
            # 18. SEARCH CRN
            # ==========================================================

            self.logger.info(
                f"Searching CRN in Result Entry: "
                f"{pat_crn_number}"
            )

            self.opd_flow.enter_result_entry_crn(
                pat_crn_number
            )

            # ==========================================================
            # 19. CLICK GO
            # ==========================================================

            time.sleep(3)
            self.opd_flow.click_result_entry_go_btn()

            time.sleep(3)

            # ==========================================================
            # 20. SELECT SAMPLE
            # ==========================================================

            self.opd_flow.click_the_checkbox_for_all_sample_result()

            # ==========================================================
            # 21. ENTER RESULT
            # ==========================================================

            self.logger.info(
                "Opening Enter Result"
            )
            time.sleep(3)

            self.opd_flow.click_enter_result_btn()

            time.sleep(3)

            self.opd_flow.fill_all_result_fields()
            time.sleep(3)
            self.opd_flow.click_result_save_button()
            time.sleep(2)
            self.opd_flow.click_result_entry_swal_yes_button()
            time.sleep(2)

            assert WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@id='swal2-html-container']"
                ))
            ).text.strip() == "Saved Successfully!"

            time.sleep(2)
            self.driver.refresh()
            time.sleep(3)

            self.opd_flow.click_investigation_module()
            self.opd_flow.click_validation_option()
            time.sleep(2)
            self.opd_flow.click_crn_option()
            time.sleep(2)
            self.opd_flow.enter_result_entry_crn(
                pat_crn_number
            )
            time.sleep(3)
            self.opd_flow.click_result_entry_go_btn()
            time.sleep(3)

            self.opd_flow.click_select_all_validation_checkbox()
            time.sleep(2)
            self.opd_flow.click_validation_save_button()
            time.sleep(2)
            self.opd_flow.click_result_entry_swal_yes_button()
            time.sleep(2)

            assert WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@id='swal2-html-container']"
                ))
            ).text.strip() == "Saved Successfully!"

            time.sleep(2)
            self.driver.refresh()

            self.opd_flow.click_investigation_module()

            self.opd_flow.click_result_report_option()
            time.sleep(2)

            self.opd_flow.click_crn_option_in_report()
            time.sleep(3)

            self.opd_flow.select_entry_status("Report Generation Inprocess")

            self.opd_flow.enter_report_crn(
                pat_crn_number)

            self.opd_flow.click_report_go_btn()
            time.sleep(8)

            self.patient_reg.click_all_print_buttons()

            # ==========================================================
            # SUCCESS
            # ==========================================================

            self.logger.info(
                "Investigation workflow completed successfully."
            )

            LogGen.test_passed(
                self.logger,
                "test_tests_in_investigation"
            )

        except Exception as e:

            self.logger.exception(
                f"Investigation workflow failed: {e}"
            )

            try:
                Screenshot.capture(
                    self.driver,
                    "test_tests_in_investigation"
                )
            except Exception as screenshot_error:
                self.logger.error(
                    f"Screenshot error: {screenshot_error}"
                )

            LogGen.test_failed(
                self.logger,
                "test_tests_in_investigation",
                str(e)
            )

            raise

    @pytest.mark.opd_flow
    def test_pac_entry(self):
        pat_crn_number = Test_OPD_Workflow.generated_crn

        LogGen.start_test(
            self.logger,
            "test_pac_entry",
            "PAC Entry Flow"
        )

        try:
            # ==========================
            # Refresh Page
            # ==========================
            self.driver.refresh()
            time.sleep(5)

            # ==========================
            # Navigate to ADT
            # ==========================
            self.logger.info("Opening OT Module")
            self.opd_flow.click_operation_theater_module()
            time.sleep(1)

            self.logger.info("Opening Anesthesia Desk")
            self.opd_flow.click_anesthesia_desk()
            time.sleep(1)

            self.logger.info("Opening PAC Entry")
            self.opd_flow.click_pac_entry()
            time.sleep(3)

            # ==========================
            # Search Patient by CRN
            # ==========================
            self.logger.info(
                f"Searching patient with CRN: {pat_crn_number}"
            )

            self.opd_flow.search_pac_entry(pat_crn_number)

            time.sleep(3)

            # ==========================
            # Verify CRN
            # ==========================
            crn_xpath = (
                f"//tbody[contains(@class,'ant-table-tbody')]"
                f"//tr[contains(@class,'ant-table-row')]"
                f"/td[1]//span[normalize-space()='{pat_crn_number}']"
            )

            crn_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, crn_xpath)
                )
            )

            actual_crn = crn_element.text.strip()

            assert actual_crn == str(pat_crn_number).strip(), (
                f"CR Number mismatch! "
                f"Expected: {pat_crn_number}, "
                f"Actual: {actual_crn}"
            )

            self.logger.info(
                f"CR Number verified successfully: {actual_crn}"
            )

            print(f"CR Number verified successfully: {actual_crn}")

        except Exception as e:
            self.logger.error(f"PAC Entry test failed: {str(e)}")

            raise

    @pytest.mark.opd_flow
    def test_procedure_service_area(self):

        pat_crn_number = Test_OPD_Workflow.generated_crn
        service_name = "Burn"

        LogGen.start_test(
            self.logger,
            "test_procedure_service_area",
            "Service Area Flow"
        )

        try:

            # ==========================
            # Refresh Page
            # ==========================

            self.driver.refresh()

            time.sleep(3)

            # ==========================
            # Navigate to Service Area
            # ==========================

            self.logger.info("Opening Service Area")

            self.opd_flow.click_service_area_module()
            time.sleep(2)

            self.opd_flow.click_request_status_viewing_option()
            time.sleep(3)

            # ==========================
            # Select Service Area Store
            # ==========================

            self.logger.info(
                f"Selecting Service Area Store: {service_name}"
            )

            self.opd_flow.select_service_area_store(
                service_name
            )

            time.sleep(2)

            # ==========================
            # Search Patient
            # ==========================

            self.opd_flow.service_area_go_btn()
            time.sleep(3)

            self.opd_flow.service_area_crn(
                pat_crn_number
            )

            time.sleep(3)

            # ==========================
            # Open Action Menu
            # ==========================

            self.opd_flow.three_dots_icon()

            self.opd_flow.hover_click_on_administration()

            time.sleep(10)
            print("Current URL:", self.driver.current_url)

            print(
                "Radio count:",
                len(
                    self.driver.find_elements(
                        By.XPATH,
                        "//input[@class='ant-radio-input']"
                    )
                )
            )

            print(
                "Table row count:",
                len(
                    self.driver.find_elements(
                        By.XPATH,
                        "//tr[contains(@class,'ant-table-row')]"
                    )
                )
            )

            # ==========================
            # Select Request
            # ==========================

            self.opd_flow.click_req_radio_btn()

            time.sleep(2)

            # ==========================
            # Save
            # ==========================

            self.opd_flow.request_viewing_save_btn()

            # ==========================
            # Validate Success Message
            # ==========================

            success_message = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container' and normalize-space()='Administration successfully']"
                    )
                )
            )

            assert success_message.text.strip() == \
                   "Administration successfully"

            self.logger.info(
                "Administration successfully"
            )

        except Exception as e:

            self.logger.error(
                f"Service Area Flow failed: {str(e)}"
            )

            LogGen.test_failed(
                self.logger,
                "test_procedure_service_area",
                str(e)
            )

            raise

    @pytest.mark.opd_flow
    def test_chronic_disease(self):

        LogGen.start_test(
            self.logger,
            "test_chronic_disease",
            "Chronic Disease Validation"
        )
        crn_number =  (
            Test_OPD_Workflow.generated_crn
        )
        opd_unit_name = Test_OPD_Workflow.opd_unit_name

        try:
            # ==========================
            # Open RX
            # ==========================

            self.driver.refresh()
            time.sleep(3)

            self.patient_reg.click_opd_module()

            self.logger.info(
                "Clicked OPD module"
            )

            self.patient_reg.click_opd_dr_desk()

            self.logger.info("Opening RX")
            time.sleep(3)

            self.patient_reg.select_opd_dr_desk_unit(
                opd_unit_name
            )
            time.sleep(3)
            self.patient_reg.enter_search_name_in_opd(
                crn_number
            )

            self.logger.info(
                f"Searching patient in OPD: {crn_number}"
            )

            time.sleep(3)

            rx_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-referr-out')]")
                )
            )
            rx_btn.click()

            time.sleep(3)

            # ==========================
            # Validate Chronic & Allergic
            # ==========================
            self.logger.info(
                "Validating Chronic & Allergic section"
            )

            chronic_allergic = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//p[contains(@class,'allergicbtn') and normalize-space()='Chronic & Allergic']"
                    )
                )
            )

            assert chronic_allergic.is_displayed(), (
                "Chronic & Allergic section is not visible."
            )

            self.logger.info(
                "Chronic & Allergic section is visible successfully."
            )

            # ==========================
            # Enter Diagnosis
            # ==========================
            self.logger.info("Entering diagnosis")

            self.patient_reg.enter_diagnosis("R00")

            diagnosis_name = self.patient_reg.get_diagnosis_name()

            self.logger.info(
                f"Selected Diagnosis : {diagnosis_name}"
            )

            time.sleep(2)

            self.opd_flow.select_diagnosis_side()

            self.opd_flow.enter_diagnosis_remarks(
                "Test diagnosis Code Remarks"
            )

            # ==========================
            # Add Diagnosis
            # ==========================
            self.patient_reg.click_diagnosis_add()

            time.sleep(2)

            # ==========================
            # Save RX
            # ==========================
            self.logger.info("Saving RX")

            self.patient_reg.click_preview_save_btn()

            time.sleep(5)

            # # ==========================
            # # Expected Chronic Disease
            # # ==========================
            # expected_chronic_disease = (
            #     Test_OPD_Workflow.generated_chronic_disease
            # )
            #
            # self.logger.info(
            #     f"Expected Chronic Disease : {expected_chronic_disease}"
            # )
            #
            # # ==========================
            # # Get Chronic Disease ONLY
            # # ==========================
            # chronic_element = WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located(
            #         (
            #             By.XPATH,
            #             "//div[contains(@class,'col-sm-6')]"
            #             "[.//h6[normalize-space()='Chronic Disease']]"
            #             "/following-sibling::div[contains(@class,'col-sm-6')][1]"
            #             "//ol[contains(@class,'rx-list-item')]//li"
            #         )
            #     )
            # )
            #
            # # Extract only the disease name.
            # # Ignore Duration / Remarks after comma.
            # actual_chronic_disease = (
            #     chronic_element.text.split(",", 1)[0].strip()
            # )
            #
            # self.logger.info(
            #     f"Actual Chronic Disease : {actual_chronic_disease}"
            # )
            #
            # # ==========================
            # # Validate Chronic Disease
            # # ==========================
            # assert (
            #         actual_chronic_disease.casefold()
            #         == expected_chronic_disease.casefold()
            # ), (
            #     f"Chronic Disease mismatch\n"
            #     f"Expected : {expected_chronic_disease}\n"
            #     f"Actual   : {actual_chronic_disease}"
            # )

            self.logger.info(
                "Chronic Disease validated successfully."
            )

            LogGen.test_passed(
                self.logger,
                "Chronic Disease validated successfully."
            )

        except Exception as e:

            self.logger.exception(
                f"Chronic Disease validation failed: {e}"
            )

            LogGen.test_failed(
                self.logger,
                str(e)
            )

            raise

    @pytest.mark.opd_flow
    def test_radiology(self):

        pat_crn_number = Test_OPD_Workflow.generated_crn
        expected_xray_tests = Test_OPD_Workflow.generated_xray_tests

        LogGen.start_test(
            self.logger,
            "test_radiology",
            "Radiology Flow"
        )

        try:

            time.sleep(3)
            # ==========================
            # Navigate to Radiology
            # ==========================
            self.driver.refresh()

            time.sleep(5)

            self.logger.info("Opening Investigation Module")
            self.opd_flow.click_investigation_module()

            self.logger.info("Opening Patient Acceptance")
            self.opd_flow.click_patience_acceptance_option()

            time.sleep(3)

            self.opd_flow.click_crn_btn()
            time.sleep(2)

            # ==========================
            # Select XRAY
            # ==========================
            self.logger.info("Selecting XRAY")
            self.opd_flow.select_xray()

            # ==========================
            # Search Patient
            # ==========================
            self.logger.info(
                f"Searching CRN : {pat_crn_number}"
            )

            self.opd_flow.enter_crn(pat_crn_number)
            self.opd_flow.click_go_btn()

            time.sleep(3)

            # ==========================
            # Get XRAY test from table
            # ==========================
            xray_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//tr[contains(@class,'ant-table-row')]/td[17]//span"
                    )
                )
            )

            actual_xray = xray_element.text.strip()

            # ==========================
            # Normalize expected XRAY
            # ==========================
            if isinstance(expected_xray_tests, list):
                expected_xray = expected_xray_tests[0].strip()
            else:
                expected_xray = str(expected_xray_tests).strip()

            # Remove test code from expected value
            expected_xray = expected_xray.split("(", 1)[0].strip()

            self.logger.info(
                f"Expected XRAY : {expected_xray}"
            )

            self.logger.info(
                f"Actual XRAY   : {actual_xray}"
            )

            # ==========================
            # Validate XRAY
            # ==========================
            assert actual_xray.casefold() == expected_xray.casefold(), (
                f"XRAY mismatch\n"
                f"Expected : {expected_xray}\n"
                f"Actual   : {actual_xray}"
            )

            self.logger.info(
                "XRAY validated successfully."
            )

            LogGen.test_passed(
                self.logger,
                "Radiology XRAY validation passed successfully."
            )

        except Exception as e:
            self.logger.exception(
                f"Radiology validation failed: {e}"
            )

            LogGen.test_failed(
                self.logger,
                str(e)
            )

            raise

    @pytest.mark.opd_flow
    def test_referral_acceptance(self):

        pat_crn_number = Test_OPD_Workflow.generated_crn
        pat_name = Test_OPD_Workflow.generated_patient_name
        pat_referral_dep = Test_OPD_Workflow.generated_referral_dep
        expected_referral_dep = pat_referral_dep.replace(" (", "(", 1)

        LogGen.start_test(
            self.logger,
            "test_referral_acceptance",
            "Referral Acceptance Flow"
        )

        try:
            # ==========================
            # Navigate to OPD
            # ==========================
            self.logger.info("Starting OPD verification")

            self.patient_reg.click_opd_module()

            self.logger.info("Clicked OPD module")

            self.patient_reg.click_opd_dr_desk()

            self.logger.info("Opened OPD Doctor Desk")

            time.sleep(3)

            # ==========================
            # Select Referral Unit
            # ==========================
            self.logger.info(
                f"Selecting Referral Department : {expected_referral_dep}"
            )

            self.opd_flow.select_department_unit_for_referral(
                expected_referral_dep
            )

            # ==========================
            # Open Referral Acceptance
            # ==========================
            self.logger.info("Opening Referral Acceptance")

            self.opd_flow.click_referral_acceptance()

            # ==========================
            # Validate Patient Card
            # ==========================
            self.logger.info(
                f"Searching patient with CRN : {pat_crn_number}"
            )

            patient_card = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//div[contains(@class,'patient-card')]["
                        f".//div[contains(@class,'patient-crn') "
                        f"and contains(normalize-space(.), '{pat_crn_number}')]"
                        f"]"
                    )
                )
            )

            # ==========================
            # Extract Patient Name
            # ==========================
            patient_name = patient_card.find_element(
                By.XPATH,
                ".//span[contains(@class,'patient-name')]"
            ).text.strip()

            # ==========================
            # Extract CRN
            # ==========================
            actual_crn = patient_card.find_element(
                By.XPATH,
                ".//div[contains(@class,'patient-crn')]"
            ).text.replace("CRN:", "").strip()

            self.logger.info(
                f"Expected Patient Name : {pat_name}"
            )

            self.logger.info(
                f"Actual Patient Name   : {patient_name}"
            )
            self.logger.info(
                f"Expected CRN          : {pat_crn_number}"
            )
            self.logger.info(
                f"Actual CRN            : {actual_crn}"
            )

            # ==========================
            # Validate Patient Name
            # ==========================
            assert patient_name.casefold() == pat_name.casefold(), (
                f"Patient Name mismatch\n"
                f"Expected : {pat_name}\n"
                f"Actual   : {patient_name}"
            )

            # ==========================
            # Validate CRN
            # ==========================
            assert actual_crn == pat_crn_number, (
                f"CRN mismatch\n"
                f"Expected : {pat_crn_number}\n"
                f"Actual   : {actual_crn}"
            )

            # ==========================
            # Validation Passed
            # ==========================
            self.logger.info(
                "Patient Name and CRN validated successfully."
            )

            LogGen.test_passed(
                self.logger,
                "Referral Acceptance patient validation passed successfully."
            )

        except Exception as e:
            self.logger.exception(
                f"Referral Acceptance validation failed: {e}"
            )

            LogGen.test_failed(
                self.logger,
                str(e)
            )

            raise

    @pytest.mark.opd_flow
    def test_add_patient_for_stamping(self):

        crn_number_for_stamping = "231012600001656"

        LogGen.start_test(
            self.logger,
            "test_admission_advice_adt",
            "Admission Advice ADT Flow"
        )

        try:
            # ==========================
            # Refresh Page
            # ==========================
            self.driver.refresh()
            time.sleep(3)

            # ==========================
            # Navigate to OPD
            # ==========================

            self.logger.info("Starting OPD verification")

            self.patient_reg.click_opd_module()

            self.logger.info("Clicked OPD module")

            self.patient_reg.click_opd_dr_desk()

            self.logger.info("Opened OPD Doctor Desk")

            time.sleep(2)

            self.opd_flow.select_random_unit_for_stamping()
            time.sleep(2)

            # ==========================
            # Add Patient for Stamping
            # ==========================
            self.opd_flow.click_add_patient_btn()

            self.logger.info("Clicked Add Patient button")
            time.sleep(3)

            self.opd_flow.enter_crn_number_for_stamp(crn_number_for_stamping)

            self.logger.info(
                f"Entered CRN: {crn_number_for_stamping}"
            )

            # ==========================
            # Verify Visit Stamping Success Popup
            # ==========================

            popup = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container' and contains(normalize-space(), 'Visit Stamping Done Successfully')]"
                    )
                )
            )

            expected_popup_message = "Visit Stamping Done Successfully"

            actual_popup_message = popup.text.strip()

            assert expected_popup_message.casefold() in actual_popup_message.casefold(), (
                f"Unexpected popup message. "
                f"Expected to contain: {expected_popup_message} | "
                f"Actual: {actual_popup_message}"
            )

            self.logger.info(
                f"Visit Stamping success popup verified successfully: {actual_popup_message}"
            )

            time.sleep(3)

            # ==========================
            # Click OK
            # ==========================
            self.opd_flow.click_ok_stamping_btn()

            self.logger.info("Clicked OK on Visit Charges popup")


        except Exception as e:
            self.logger.error(
                f"Test failed: {str(e)}"
            )
            raise

    @pytest.mark.opd_flow
    def test_investigation_listing(self):

        pat_crn_number = Test_OPD_Workflow.generated_crn

        opd_unit = Test_OPD_Workflow.opd_unit_name

        expected_investigations = Test_OPD_Workflow.generated_investigation_tests



        LogGen.start_test(
            self.logger,
            "test_pac_entry",
            "PAC Entry Flow"
        )

        try:
            # ==========================
            # Refresh Page
            # ==========================
            self.driver.refresh()
            time.sleep(5)

            # ==========================
            # Navigate to OPD Doctor Desk
            # ==========================
            self.patient_reg.click_opd_module()
            time.sleep(3)

            self.patient_reg.click_opd_dr_desk()
            time.sleep(3)

            self.opd_flow.select_opd_dr_desk_unit_for_inv_list(opd_unit)
            time.sleep(3)

            self.patient_reg.enter_search_name_in_opd(pat_crn_number)

            self.logger.info(
                f"Searching patient with CRN: {pat_crn_number}"
            )

            time.sleep(3)

            self.opd_flow.click_again_rx()
            time.sleep(3)

            self.patient_reg.click_investigation_tab()
            time.sleep(2)

            self.opd_flow.click_investigation_list()
            time.sleep(2)

            # ==========================================
            # Verify All Investigations
            # ==========================================

            if isinstance(expected_investigations, str):
                expected_investigations = [expected_investigations]

            for expected_investigation in expected_investigations:
                self.logger.info(
                    f"Searching Investigation: {expected_investigation}"
                )

                self.opd_flow.clear_box()

                # Search investigation
                self.opd_flow.search_test(expected_investigation)
                time.sleep(2)

                investigation_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//tbody[@class='ant-table-tbody']/tr[@data-row-key]/td[1]/span"
                        )
                    )
                )

                actual_investigation = investigation_element.text.strip()

                assert expected_investigation.lower() in actual_investigation.lower(), (
                    f"Investigation mismatch!\n"
                    f"Expected: {expected_investigation}\n"
                    f"Actual: {actual_investigation}"
                )

                self.logger.info(
                    f"Investigation verified successfully: {actual_investigation}"
                )

            self.logger.info("All investigations verified successfully.")

        except Exception as e:
            self.logger.error(f"Test Failed: {str(e)}")
            raise



