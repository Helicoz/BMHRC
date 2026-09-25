import re

import pyautogui
import pytest
import time

from pygments.console import esc
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import LogGen
from utilities.screenshot import Screenshot
from test_data.test_patient_data import Testdata, TestDataGenerator
from selenium.webdriver.support.ui import Select
from utilities.download_utils import PDFUtils
import random
import string

@pytest.mark.usefixtures("login")
class Test_Inventory_Workflow:
    logger = LogGen.loggen()
    driver = None
    inventory_flow = None
    opd_flow = None
    admin_lp = None
    generated_crn = None
    generated_mobile_no = None
    username2 = "USER_ROHIT"
    password2 = "Cdac@2026"
    username = "SUDEEP"
    password = "Cdac@2120"



    @pytest.mark.inventory_flow
    def test_indent_desk_local_po(self):

        LogGen.start_test(
            self.logger,
            "test_skip_patience",
            "Skip Patient from OPD Queue"
        )

        # =====================================================
        # INDENT DESK
        # =====================================================
        try:

            self.logger.info("Opening Registration Module")
            self.inventory_flow.click_inventory_module()

            self.logger.info("Opening Patient Registration")
            self.inventory_flow.click_demand_option()

            self.logger.info("Clicking New Registration button")
            self.inventory_flow.click_indent_desk_btn()

            time.sleep(3)

            self.inventory_flow.select_store("SSB 1 Pharmacy")
            time.sleep(1)

            self.inventory_flow.select_category("Drugs")
            time.sleep(1)

            self.inventory_flow.select_request_type("Indent for Local PO")

            self.inventory_flow.click_go_btn()

            time.sleep(3)

            self.inventory_flow.click_add_items_btn()

            random_drugs_1 = self.inventory_flow.select_random_item()

            self.inventory_flow.click_move_right_btn()

            # random_drugs_2 = self.inventory_flow.select_random_item()
            # self.inventory_flow.click_move_right_btn()

            self.inventory_flow.click_OK_btn()

            time.sleep(3)

            self.inventory_flow.enter_required_quantity_for_all_rows("6")

            self.inventory_flow.enter_remarks("Test remarks 1")

            self.inventory_flow.click_save_btn()

            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()

            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container']"
                    )
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Indent Raised Successfully.", (
                f"Message mismatch!\n"
                f"Expected: Indent Raised Successfully.\n"
                f"Actual: {actual_msg}"
            )

            print("Indent raised successfully.")

            time.sleep(5)

            act_indent_number = self.inventory_flow.get_first_indent_number()

            print("Indent number:", act_indent_number)

        except AssertionError:
            self.logger.exception("Indent Desk verification failed.")
            raise

        except Exception:
            self.logger.exception("Indent Desk flow failed.")
            raise

        # =====================================================
        # PO DESK
        # =====================================================
        try:

            self.driver.refresh()
            time.sleep(5)

            self.inventory_flow.click_inventory_module()
            time.sleep(2)

            self.inventory_flow.click_order_management_option()

            self.inventory_flow.click_po_desk_option()

            time.sleep(10)

            self.inventory_flow.select_searchable_dropdown("OPD PHARMACY")

            time.sleep(2)

            self.inventory_flow.select_category("Drugs")

            time.sleep(2)

            self.inventory_flow.select_po_type("Local PO")

            time.sleep(2)

            self.inventory_flow.select_po_status("Pending(or Draft)")

            time.sleep(5)

            self.inventory_flow.click_po_add_btn()

            time.sleep(5)

            self.inventory_flow.search_indent_number(act_indent_number)

            time.sleep(3)

            checkbox = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//tr[.//span[normalize-space()='{act_indent_number}']]//span[contains(@class,'ant-checkbox')]"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                checkbox
            )

            checkbox.click()

            time.sleep(3)

            self.inventory_flow.click_compile_btn()

            time.sleep(3)

            self.inventory_flow.click_compile_btn()

            time.sleep(3)

            self.inventory_flow.enter_remarks("Test Remarks 2")

            self.inventory_flow.click_save_draft_btn()

            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()

            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@id='swal2-html-container']")
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Draft PO Generated successfully", (
                f"Message mismatch!\n"
                f"Expected: Draft PO Generated successfully\n"
                f"Actual: {actual_msg}"
            )

            print("Draft PO generated successfully.")

            time.sleep(5)

            self.inventory_flow.click_first_po_action_btn()

            time.sleep(1)

            self.inventory_flow.click_finalize_po()

            time.sleep(3)

            self.inventory_flow.save_after_po()

            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()

            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@id='swal2-html-container']")
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Data Save Successfully!!", (
                f"Message mismatch!\n"
                f"Expected: Data Save Successfully!!\n"
                f"Actual: {actual_msg}"
            )

            time.sleep(5)

            self.inventory_flow.select_po_status("In Process")

            time.sleep(3)

            po_number = self.inventory_flow.get_first_po_number()

            print("Po number:", po_number)

        except AssertionError:
            self.logger.exception("PO Desk verification failed.")
            raise

        except Exception:
            self.logger.exception("PO Desk flow failed.")
            raise

        # =====================================================
        # CHALLAN RECEIVE
        # =====================================================
        try:

            self.driver.refresh()

            time.sleep(5)

            self.inventory_flow.click_inventory_module()

            self.inventory_flow.click_receive_option()

            self.inventory_flow.click_challan_receive_option()

            time.sleep(5)

            self.inventory_flow.search_po_number_challan(po_number)

            time.sleep(3)

            self.inventory_flow.click_direct_receive_btn()

            time.sleep(3)

            self.inventory_flow.select_received_date_today()

            time.sleep(3)

            self.inventory_flow.select_random_received_by_in_challan()

            self.inventory_flow.enter_challan_number("233333")

            self.inventory_flow.select_supplier_date()

            self.inventory_flow.enter_no_of_batches("1")

            time.sleep(3)

            self.inventory_flow.click_add_btn()

            time.sleep(3)

            order_qty = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//span[normalize-space()='Order Qty:']/following-sibling::span"
                ))
            ).text

            qty = re.search(r"\d+", order_qty).group()

            print(qty)

            self.inventory_flow.enter_batch_no("234RTR")

            self.inventory_flow.select_mfg_date_today()

            time.sleep(3)

            self.inventory_flow.select_exp_date_after_4_5_days()

            time.sleep(3)

            self.inventory_flow.enter_quantity(qty)

            self.inventory_flow.enter_rate("100")

            self.inventory_flow.enter_discount("10")

            self.inventory_flow.enter_gst("5")

            self.inventory_flow.schedule_item_ok_btn()

            time.sleep(3)

            self.inventory_flow.challan_save_btn()

            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()

            time.sleep(2)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@id='swal2-html-container']"
                ))
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Challan processed successfully!", (
                f"Message mismatch!\n"
                f"Expected: Challan processed successfully!\n"
                f"Actual: {actual_msg}"
            )

            print("Challan processed successfully.")

        except AssertionError:
            self.logger.exception("Challan Receive verification failed.")
            raise

        except Exception:
            self.logger.exception("Challan Receive flow failed.")
            raise

        # =====================================================
        # CHALLAN APPROVAL
        # =====================================================
        try:

            self.driver.refresh()

            time.sleep(5)

            self.inventory_flow.click_inventory_module()

            self.inventory_flow.click_approval_option()

            self.inventory_flow.click_challan_approval_option()

            time.sleep(8)

            self.inventory_flow.select_challan_store_searchable_dropdown("OPD Pharmacy")

            time.sleep(3)

            self.inventory_flow.select_po_by_value("10222500059")

            time.sleep(3)

            self.inventory_flow.click_first_po_action_btn()

            time.sleep(3)

            self.inventory_flow.click_challan_approve_btn()

            time.sleep(3)

            self.inventory_flow.enter_description("description 1")

            self.inventory_flow.click_challan_approval_save_btn()

            self.inventory_flow.click_swal_save_btn()

            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@id='swal2-html-container']"
                ))
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Challan saved successfully!", (
                f"Message mismatch!\n"
                f"Expected: Challan saved successfully!\n"
                f"Actual: {actual_msg}"
            )

            print("Challan saved successfully.")

        except AssertionError:
            self.logger.exception("Challan Approval verification failed.")
            raise

        except Exception:
            self.logger.exception("Challan Approval flow failed.")
            raise

        self.driver.refresh()
        time.sleep(5)

    @pytest.mark.inventory_flow
    def test_indent_desk_bulk_po(self):

        LogGen.start_test(
            self.logger,
            "test_skip_patience",
            "Skip Patient from OPD Queue"
        )

        # =====================================================
        # INDENT DESK
        # =====================================================
        try:

            self.driver.refresh()
            time.sleep(3)

            self.logger.info("Opening Registration Module")
            self.inventory_flow.click_inventory_module()

            self.logger.info("Opening Patient Registration")
            self.inventory_flow.click_demand_option()

            self.logger.info("Clicking New Registration button")
            self.inventory_flow.click_indent_desk_btn()

            time.sleep(3)

            self.inventory_flow.select_store("SSB 1 Pharmacy")
            time.sleep(1)

            self.inventory_flow.select_category("Drugs")
            time.sleep(1)

            self.inventory_flow.select_request_type("Indent for Bulk PO")

            self.inventory_flow.click_go_btn()

            time.sleep(3)

            self.inventory_flow.click_add_items_btn()

            random_drugs_1 = self.inventory_flow.select_random_item()

            self.inventory_flow.click_move_right_btn()

            self.inventory_flow.click_OK_btn()

            time.sleep(3)

            self.inventory_flow.enter_required_quantity_for_all_rows("6")

            supplier_value = self.inventory_flow.select_random_supplier()

            print(supplier_value)

            self.inventory_flow.enter_remarks("Test remarks")

            self.inventory_flow.click_save_btn()

            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()

            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container']"
                    )
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Indent Raised Successfully.", (
                f"Message mismatch!\n"
                f"Expected: Indent Raised Successfully.\n"
                f"Actual: {actual_msg}"
            )

            print("Indent raised successfully.")

            time.sleep(5)

            act_indent_number = self.inventory_flow.get_first_indent_number()

            print("Indent number:", act_indent_number)

        except AssertionError:
            self.logger.exception("Indent Desk verification failed.")
            raise

        except Exception:
            self.logger.exception("Indent Desk flow failed.")
            raise

        # =====================================================
        # PO DESK
        # =====================================================
        try:

            self.driver.refresh()
            time.sleep(5)

            self.inventory_flow.click_inventory_module()
            time.sleep(2)

            self.inventory_flow.click_order_management_option()

            self.inventory_flow.click_po_desk_option()

            time.sleep(8)

            self.inventory_flow.select_searchable_dropdown("INJECTION STORE")
            time.sleep(2)

            self.inventory_flow.select_category("Drugs")
            time.sleep(2)

            self.inventory_flow.select_po_type("Bulk PO")
            time.sleep(2)

            self.inventory_flow.select_po_status("Pending(or Draft)")
            time.sleep(5)

            self.inventory_flow.click_po_add_btn()
            time.sleep(5)

            # Select Supplier
            self.inventory_flow.select_supplier_name_po_desk(supplier_value)
            time.sleep(2)

            self.inventory_flow.search_indent_number(act_indent_number)
            time.sleep(3)

            checkbox = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//tr[.//span[normalize-space()='{act_indent_number}']]//span[contains(@class,'ant-checkbox')]"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                checkbox
            )

            checkbox.click()

            time.sleep(3)

            self.inventory_flow.click_compile_btn()
            time.sleep(3)

            self.inventory_flow.click_compile_btn()
            time.sleep(3)

            self.inventory_flow.enter_remarks("Test Remarks")

            self.inventory_flow.click_save_draft_btn()
            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()
            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container']"
                    )
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Draft PO Generated successfully", (
                f"Message mismatch!\n"
                f"Expected: Draft PO Generated successfully\n"
                f"Actual: {actual_msg}"
            )

            print("Draft PO generated successfully.")

            time.sleep(5)

            self.inventory_flow.click_first_po_action_btn()
            time.sleep(1)

            self.inventory_flow.click_finalize_po()
            time.sleep(3)

            self.inventory_flow.save_after_po()
            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()
            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container']"
                    )
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Data Save Successfully!!", (
                f"Message mismatch!\n"
                f"Expected: Data Save Successfully!!\n"
                f"Actual: {actual_msg}"
            )

            time.sleep(5)

            self.inventory_flow.select_po_status("In Process")
            time.sleep(3)

            po_number = self.inventory_flow.get_first_po_number()

            print("Po number:", po_number)

        except AssertionError:
            self.logger.exception("PO Desk verification failed.")
            raise

        except Exception:
            self.logger.exception("PO Desk flow failed.")
            raise

        # =====================================================
        # CHALLAN RECEIVE
        # =====================================================
        try:

            self.driver.refresh()

            time.sleep(5)

            self.inventory_flow.click_inventory_module()

            self.inventory_flow.click_receive_option()

            self.inventory_flow.click_challan_receive_option()

            time.sleep(5)

            self.inventory_flow.search_po_number_challan(po_number)

            time.sleep(3)

            self.inventory_flow.click_direct_receive_btn()

            time.sleep(3)

            self.inventory_flow.select_received_date_today()

            time.sleep(3)

            self.inventory_flow.select_random_received_by_in_challan()

            self.inventory_flow.enter_challan_number("234221")

            self.inventory_flow.select_supplier_date()

            self.inventory_flow.enter_no_of_batches("1")

            time.sleep(3)

            self.inventory_flow.click_add_btn()

            time.sleep(3)

            order_qty = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//span[normalize-space()='Order Qty:']/following-sibling::span"
                ))
            ).text

            qty = re.search(r"\d+", order_qty).group()

            print("Order Qty:", qty)

            self.inventory_flow.enter_batch_no("234RT")

            self.inventory_flow.select_mfg_date_today()

            time.sleep(3)

            self.inventory_flow.select_exp_date_after_4_5_days()

            time.sleep(3)

            self.inventory_flow.enter_quantity(qty)

            self.inventory_flow.enter_rate("100")

            self.inventory_flow.enter_discount("10")

            self.inventory_flow.enter_gst("5")

            self.inventory_flow.schedule_item_ok_btn()

            time.sleep(3)

            self.inventory_flow.challan_save_btn()

            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()

            time.sleep(2)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@id='swal2-html-container']"
                ))
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Challan processed successfully!", (
                f"Message mismatch!\n"
                f"Expected: Challan processed successfully!\n"
                f"Actual: {actual_msg}"
            )

            print("Challan processed successfully.")

        except AssertionError:
            self.logger.exception("Challan Receive verification failed.")
            raise

        except Exception:
            self.logger.exception("Challan Receive flow failed.")
            raise

        # =====================================================
        # CHALLAN APPROVAL
        # =====================================================
        try:

            self.driver.refresh()

            time.sleep(5)

            self.inventory_flow.click_inventory_module()

            self.inventory_flow.click_approval_option()

            self.inventory_flow.click_challan_approval_option()

            time.sleep(8)

            self.inventory_flow.select_challan_store_searchable_dropdown("Injection Store")

            time.sleep(3)

            self.inventory_flow.select_po_by_value(po_number)

            time.sleep(3)

            self.inventory_flow.click_first_po_action_btn()

            time.sleep(3)

            self.inventory_flow.click_challan_approve_btn()

            time.sleep(3)

            self.inventory_flow.enter_description("description")

            self.inventory_flow.click_challan_approval_save_btn()

            self.inventory_flow.click_swal_save_btn()

            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@id='swal2-html-container']"
                ))
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Challan saved successfully!", (
                f"Message mismatch!\n"
                f"Expected: Challan saved successfully!\n"
                f"Actual: {actual_msg}"
            )

            print("Challan saved successfully.")

        except AssertionError:
            self.logger.exception("Challan Approval verification failed.")
            raise

        except Exception:
            self.logger.exception("Challan Approval flow failed.")
            raise

        self.driver.refresh()
        time.sleep(5)

    @pytest.mark.inventory_flow
    def test_indent_desk_issue(self):
        LogGen.start_test(
            self.logger,
            "test_skip_patience",
            "Skip Patient from OPD Queue"
        )

        # =====================================================
        # INDENT DESK
        # =====================================================
        try:

            self.driver.refresh()
            time.sleep(3)

            self.logger.info("Opening Registration Module")
            self.inventory_flow.click_inventory_module()

            self.logger.info("Opening Patient Registration")
            self.inventory_flow.click_demand_option()

            self.logger.info("Clicking New Registration button")
            self.inventory_flow.click_indent_desk_btn()

            time.sleep(3)

            self.inventory_flow.select_store("SSHC PHARMACY")
            time.sleep(1)

            self.inventory_flow.select_category("Drugs")
            time.sleep(1)

            self.inventory_flow.select_request_type("Indent for Issue")

            self.inventory_flow.click_go_btn()

            time.sleep(3)

            self.inventory_flow.select_issuing_store("Tablet Store")
            time.sleep(3)

            self.inventory_flow.click_add_items_btn()

            random_drugs_1 = self.inventory_flow.select_random_item()

            self.inventory_flow.click_move_right_btn()

            self.inventory_flow.click_OK_btn()

            time.sleep(3)

            self.inventory_flow.enter_required_quantity_for_all_rows("6")

            self.inventory_flow.select_random_received_by()


            self.inventory_flow.enter_remarks("Test remarks")

            self.inventory_flow.click_save_btn()

            time.sleep(3)

            self.inventory_flow.click_swal_save_btn()

            time.sleep(3)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container']"
                    )
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Indent Raised Successfully.", (
                f"Message mismatch!\n"
                f"Expected: Indent Raised Successfully.\n"
                f"Actual: {actual_msg}"
            )

            print("Indent raised successfully.")

            time.sleep(5)

            act_indent_number = self.inventory_flow.get_first_indent_number()

            print("Indent number:", act_indent_number)

        except AssertionError:
            self.logger.exception("Indent Desk verification failed.")
            raise

        except Exception:
            self.logger.exception("Indent Desk flow failed.")
            raise



        self.driver.refresh()
        time.sleep(5)

        self.logger.info("Opening Registration Module")
        self.inventory_flow.click_inventory_module()

        self.inventory_flow.click_approval_option()
        time.sleep(3)
        self.inventory_flow.click_approval_desk_option()
        time.sleep(3)
        self.inventory_flow.select_approval_request_type("Indent For Issue")
        time.sleep(3)
        self.inventory_flow.search_indent_number(act_indent_number)
        time.sleep(3)
        self.inventory_flow.click_first_po_action_btn()
        time.sleep(3)
        self.inventory_flow.click_approval()
        time.sleep(3)
        self.inventory_flow.enter_description("Test description")

        self.inventory_flow.click_challan_approval_save_btn()
        time.sleep(3)
        self.inventory_flow.click_swal_save_btn()
        time.sleep(7)
        pyautogui.press('esc')
        time.sleep(3)
        self.inventory_flow.close_btn()
        time.sleep(3)
        self.admin_lp.hover_user_icon()
        time.sleep(5)
        self.admin_lp.enter_username(self.username2)

        self.admin_lp.enter_password(
            self.password2
        )

        self.admin_lp.enter_captcha()

        self.admin_lp.click_login_btn()

        time.sleep(5)

        self.logger.info("Opening Registration Module")
        self.inventory_flow.click_inventory_module()

        self.logger.info("Opening Registration Module")
        self.inventory_flow.click_inventory_module()

        self.inventory_flow.click_approval_option()
        time.sleep(3)
        self.inventory_flow.click_approval_desk_option()
        time.sleep(3)
        self.inventory_flow.select_approval_request_type("Indent For Issue")
        time.sleep(3)
        self.inventory_flow.search_indent_number(act_indent_number)
        time.sleep(3)
        self.inventory_flow.click_first_po_action_btn()
        time.sleep(3)
        self.inventory_flow.click_approval()
        time.sleep(3)
        self.inventory_flow.enter_description("Test description")
        self.inventory_flow.click_challan_approval_save_btn()
        time.sleep(3)
        self.inventory_flow.click_swal_save_btn()
        time.sleep(7)
        pyautogui.press('esc')
        time.sleep(3)
        self.inventory_flow.close_btn()
        time.sleep(3)
        self.admin_lp.hover_user_icon()
        time.sleep(5)
        self.admin_lp.enter_username(self.username)

        self.admin_lp.enter_password(
            self.password
        )

        self.admin_lp.enter_captcha()

        self.admin_lp.click_login_btn()


        try:
            self.driver.refresh()
            time.sleep(5)

            self.inventory_flow.click_inventory_module()
            self.inventory_flow.click_issue_desk_option()
            time.sleep(3)
            self.inventory_flow.select_issuing_store_for_issue_desk("TABLET STORE")
            time.sleep(2)
            self.inventory_flow.select_indent_type("Issue To store")
            time.sleep(3)

            self.inventory_flow.search_indent_number(act_indent_number)
            time.sleep(3)

            self.inventory_flow.click_first_po_action_btn()

            self.inventory_flow.click_issue_indent_desk()

            time.sleep(3)

            self.inventory_flow.save_after_po()
            time.sleep(2)
            self.inventory_flow.click_swal_ok_btn()
            time.sleep(2)

            success_msg = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='swal2-html-container' and normalize-space()='Data Saved Successfully']"
                    )
                )
            )

            actual_msg = success_msg.text.strip()

            assert actual_msg == "Data Saved Successfully", (
                f"Message mismatch!\n"
                f"Expected: Data Saved Successfully\n"
                f"Actual: {actual_msg}"
            )

            time.sleep(8)
            pyautogui.press('esc')

        except AssertionError:
            self.logger.exception("Indent Desk verification failed.")
            raise

        except Exception:
            self.logger.exception("Issue desk failed")
            raise

        try:


            self.driver.refresh()
            time.sleep(5)
            self.inventory_flow.click_inventory_module()
            time.sleep(3)
            self.inventory_flow.click_receive_option()
            self.inventory_flow.click_ack_desk_option()
            time.sleep(3)
            self.inventory_flow.select_ack_store("SSHC PHARMACY")
            time.sleep(2)
            self.inventory_flow.search_indent_number(act_indent_number)
            time.sleep(3)
            self.inventory_flow.click_first_po_action_btn()
            self.inventory_flow.click_acknowledge()

            self.inventory_flow.enter_comments("Testtttt")

            self.inventory_flow.challan_save_btn()
            time.sleep(3)
            self.inventory_flow.click_swal_save_btn()
            time.sleep(3)

            assert WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[contains(@class,'modal-title') and normalize-space()='Report For Acknowledge']"
                ))
            ).is_displayed()

        except AssertionError:
            self.logger.exception("Acknowledge fail")
            raise

        except Exception:
            self.logger.exception("Acknowledge fail")
            raise






