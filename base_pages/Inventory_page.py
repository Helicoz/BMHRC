import re
import base64
from io import BytesIO
from datetime import datetime, timedelta
from selenium.common import TimeoutException
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



class Inventory_Page:


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

    def click_demand_option(self):
        demand = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Demand']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            demand
        )

    def click_indent_desk_btn(self):
        indent_desk = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Indent Desk']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            indent_desk
        )

        self.driver.execute_script(
            "arguments[0].click();",
            indent_desk
        )

    def select_store(self, store_name):
        wait = WebDriverWait(self.driver, 15)

        # Click anywhere on the dropdown
        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@name='storeName']/preceding-sibling::div"
            ))
        )
        dropdown.click()

        # Wait for the input box
        search_box = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[contains(@id,'react-select') and contains(@id,'-input')]"
            ))
        )

        search_box.clear()
        search_box.send_keys(store_name)
        search_box.send_keys(Keys.ENTER)


    def select_category(self, category_name):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='category']")
            )
        )

        Select(dropdown).select_by_visible_text(category_name)

        print(f"Selected Category: {category_name}")

        return category_name

    def select_request_type(self, request_type):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='requestType']")
            )
        )

        Select(dropdown).select_by_visible_text(request_type)

        print(f"Selected Request Type: {request_type}")

        return request_type


    def click_go_btn(self):

        go_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'add-blue-button') and normalize-space()='Go']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            go_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            go_btn
        )


    def click_add_items_btn(self):

        add_item_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'white-button') and normalize-space()='Add Items']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            add_item_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            add_item_btn
        )

    def select_random_item(self):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'rdl-control-container')]//select[@multiple]"
                )
            )
        )

        select = Select(dropdown)

        # Only enabled options
        options = [
            option for option in select.options
            if option.text.strip()
               and option.get_attribute("value") not in ("", "0")
               and option.is_enabled()
        ]

        if not options:
            raise Exception("No enabled options available.")

        random_option = random.choice(options)

        select.select_by_visible_text(random_option.text.strip())

        selected_item = random_option.text.strip()

        print(f"Selected Item: {selected_item}")

        return selected_item


    def click_move_right_btn(self):

        move_right_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Move right']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            move_right_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            move_right_btn
        )

    def click_OK_btn(self):

        ok_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'justify-content-center')]//button[@title='OK' and normalize-space()='OK']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            ok_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            ok_btn
        )

    def enter_required_quantity_for_all_rows(self, qty):
        # Wait until all Req Qty input fields are visible
        qty_inputs = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(
                (
                    By.XPATH,
                    "//tbody[@class='ant-table-tbody']//tr[contains(@class,'ant-table-row')]//input[@placeholder='Enter Req Qty']"
                )
            )
        )

        for index, input_box in enumerate(qty_inputs, start=1):
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                input_box
            )

            input_box.clear()
            input_box.send_keys(str(qty))

            print(f"Entered {qty} in row {index}")

        return len(qty_inputs)


    def enter_remarks(self, text):

        remarks = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='remarks']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            remarks
        )

        self.driver.execute_script(
            "arguments[0].click();",
            remarks
        )

        remarks.send_keys(text)


    def click_save_btn(self):

        save_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'add-blue-button') and normalize-space()='Save']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            save_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

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

    def get_first_indent_number(self):
        indent_number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//tr[@rowindex='0']/td[1]/span"
                )
            )
        ).text.strip()

        print(f"Indent Number: {indent_number}")
        return indent_number


    def click_order_management_option(self):
        order_mang = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Order Management']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            order_mang
        )


    def click_po_desk_option(self):
        po_desk = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='PO Desk']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            po_desk
        )

    def select_store_for_po(self, store_name):

        wait = WebDriverWait(self.driver, 10)

        # Wait for the dropdown to be visible
        dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='storeName']")
            )
        )

        # Select the option
        Select(dropdown).select_by_visible_text(store_name)

        print(f"Selected Store: {store_name}")

    def select_po_type(self, po_type):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='poType']")
            )
        )

        Select(dropdown).select_by_visible_text(po_type)

        print(f"Selected PO Type: {po_type}")

    def select_po_status(self,status):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select[@name='poStatus']"))
        )

        Select(dropdown).select_by_visible_text(status)


    def click_po_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[.//*[contains(@class,'fa-plus')]]"))
        )

        add_btn.click()

    def search_indent_number(self, indent_number):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='Search']")
            )
        )

        search_box.clear()
        search_box.send_keys(indent_number)

    def click_compile_btn(self):
        compile_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Compile']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            compile_btn
        )

        time.sleep(0.5)  # Optional: allows scrolling animation to complete

        compile_btn.click()

    def click_save_draft_btn(self):
        save_draft_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Save Draft']")
            )
        )

        save_draft_btn.click()

    def get_first_draft_po_number(self):
        po_number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "(//tbody[@class='ant-table-tbody']//tr//td[1]//span)[1]"
                )
            )
        )
        return po_number.text.strip()

    def click_first_po_action_btn(self):
        action_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//tr[@rowindex='0']/td[last()]//span[contains(@class,'ant-dropdown-trigger')]"
                )
            )
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", action_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", action_btn)


    def click_finalize_po(self):
        finalize_po = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Finalize PO']")
            )
        )
        finalize_po.click()

    def save_after_po(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Save']")
            )
        )

        self.driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'instant',
                block: 'center'
            });
        """, save_btn)

        time.sleep(1)  # Optional: let the scrolling finish

        save_btn.click()

    def get_first_po_number(self):
        po_number = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//tbody[@class='ant-table-tbody']/tr[@rowindex='0']/td[1]//span"
                )
            )
        ).text.strip()

        return po_number


    def click_receive_option(self):
        rec = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Receive']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            rec
        )

    def click_challan_receive_option(self):
        challan_receive = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Challan Receive Process']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            challan_receive
        )

    def search_po_number_challan(self,no):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'table-filter-content')]//input[@placeholder='Search']")
            )
        )

        search_box.click()

        search_box.clear()
        search_box.send_keys(no)

    def click_direct_receive_btn(self):
        direct_receive_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//*[name()='svg' and @data-icon='hand-holding-medical']]")
            )
        )

        direct_receive_btn.click()

    def select_received_date_today(self):
        # Open calendar
        date_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[normalize-space()='Received Date']/following::input[@placeholder='Select a date'][1]"
                )
            )
        )
        date_field.click()

        # Click today's date
        today = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//td[contains(@class,'ant-picker-cell-today')]//div[contains(@class,'ant-picker-cell-inner')]"
                )
            )
        )
        today.click()

    def select_random_received_by(self):
        dropdown = Select(
            self.driver.find_element(By.NAME, "receivedByCombo")
        )

        # Exclude the first placeholder option (value="")
        valid_options = [option for option in dropdown.options if option.get_attribute("value").strip()]

        random_option = random.choice(valid_options)

        dropdown.select_by_value(random_option.get_attribute("value"))

        print(f"Selected: {random_option.text}")
        return random_option.text


    def enter_challan_number(self, challan_number):
        challan_no = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@name='supplierReceiptNo']")
            )
        )
        challan_no.send_keys(challan_number)


    def select_supplier_date(self):
        # Select 3 days ago (change 3 to 2 if needed)
        previous_date = (datetime.now() - timedelta(days=3)).strftime("%d-%b-%Y")

        date_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[label[contains(.,'Supplier Receipt Date')]]//input[@placeholder='Select a date']"
            ))
        )

        date_field.clear()
        date_field.send_keys(previous_date)

        print(f"Selected Date: {previous_date}")

    def enter_no_of_batches(self, batch_no):
        batch_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@name='noOfBatches']"
            ))
        )

        batch_input.clear()
        batch_input.send_keys(batch_no)

    def click_add_btn(self):
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[@title='Add']"
            ))
        )
        add_btn.click()

    def enter_batch_no(self,batch_no):
        batch_number = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='batchNo']"))
        )
        batch_number.clear()
        batch_number.send_keys(batch_no)

    def select_mfg_date_today(self):
        wait = WebDriverWait(self.driver, 10)

        # Click on the Mfg Date input
        mfg_date = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[contains(.,'Mfg Date')]/ancestor::div[contains(@class,'d-flex')]/following-sibling::div//input[@placeholder='Select a date'][1]"
            ))
        )
        mfg_date.click()

        # Click Today's date from the calendar popup
        today = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'ant-picker-dropdown') and not(contains(@class,'ant-picker-dropdown-hidden'))]//td[contains(@class,'ant-picker-cell-today')]"
            ))
        )
        today.click()

    def select_exp_date_after_4_5_days(self):
        wait = WebDriverWait(self.driver, 10)

        # Click Exp Date field (2nd date picker)
        exp_date = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "(//div[contains(@class,'add-item-row')]//input[@placeholder='Select a date'])[2]"
            ))
        )
        exp_date.click()

        # Today's day number
        target_day = datetime.now().day + 4  # Change to +5 if needed

        # Wait until the target day is visible and click it
        target_date = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//div[contains(@class,'ant-picker-dropdown') and not(contains(@class,'hidden'))]"
                f"//td[not(contains(@class,'ant-picker-cell-disabled')) "
                f"and not(contains(@class,'ant-picker-cell-out-view'))]"
                f"//div[@class='ant-picker-cell-inner' and text()='{target_day}']"
            ))
        )

        self.driver.execute_script("arguments[0].click();", target_date)

    def enter_quantity(self,quantity):
        qty = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'add-item-row')]//input[@name='totalQty']"
            ))
        )

        qty.clear()
        qty.send_keys(quantity)


    def enter_rate(self, rate):
        cost = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'add-item-row')]//input[@name='cost']"
            ))
        )

        cost.clear()
        cost.send_keys(rate)

    def enter_discount(self, percent):
        discount = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'add-item-row')]//input[@name='discount']"
            ))
        )

        discount.clear()
        discount.send_keys(percent)

    def enter_gst(self, tax):
        gst = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'add-item-row')]//input[@name='tax']"
            ))
        )

        gst.clear()
        gst.send_keys(tax)

    def schedule_item_ok_btn(self):
        ok_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[@title='OK' and normalize-space()='OK']"
            ))
        )
        ok_btn.click()

    def challan_save_btn(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//i[.//*[name()='svg' and @data-icon='floppy-disk']]"
            ))
        )
        save_btn.click()

    def click_approval_option(self):
        approval = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Approval']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            approval
        )

    def click_challan_approval_option(self):
        challan_approval = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Challan approval']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            challan_approval
        )

    def select_challan_store_searchable_dropdown(self, item_name):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@role='combobox']")
            )
        )

        dropdown.click()
        dropdown.clear()
        dropdown.send_keys(item_name)

        # Wait for dropdown options to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@role='option']")
            )
        )

        # Select highlighted/first matching option
        dropdown.send_keys(Keys.ENTER)

    def select_po_by_value(self, po_number):

        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "(//input[contains(@class,'searchable-dropdown__input') and @role='combobox'])[2]"
                )
            )
        )

        dropdown.click()
        dropdown.clear()
        dropdown.send_keys(str(po_number))

        time.sleep(1)

        dropdown.send_keys(Keys.ENTER)

    def click_challan_approve_btn(self):
        approve_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//li[@role='menuitem'][.//span[contains(normalize-space(),'Approve')]]"
            ))
        )

        self.driver.execute_script("arguments[0].click();", approve_btn)

    def enter_description(self,description):
        des = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@name='description']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            des
        )

        self.driver.execute_script(
            "arguments[0].click();",
            des
        )

        des.send_keys(description)


    def click_challan_approval_save_btn(self):

        save_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(@class,'blue-button') and contains(@class,'btn-primary')]")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            save_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

    def select_random_supplier(self):
        wait = WebDriverWait(self.driver, 10)

        dropdown = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//td//select[contains(@class,'form-select')]")
            )
        )

        select = Select(dropdown)

        valid_options = [
            option for option in select.options
            if option.get_attribute("value") != "0"
        ]

        random_option = random.choice(valid_options)

        # Store both name and value
        self.selected_supplier_name = random_option.text.strip()
        self.selected_supplier_value = random_option.get_attribute("value")

        # Select using value
        select.select_by_value(self.selected_supplier_value)

        print(f"Selected Supplier: {self.selected_supplier_name}")
        print(f"Selected Supplier Value: {self.selected_supplier_value}")

        return self.selected_supplier_value

    def select_supplier_name_po_desk(self, supplier_value):
        supplier_dropdown = Select(
            self.driver.find_element(By.XPATH, "//select[@name='supplier']")
        )

        supplier_dropdown.select_by_value(supplier_value)

        print("Selected Supplier Value:", supplier_value)

    def select_issuing_store(self, store_name):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='issuingStore']")
            )
        )

        Select(dropdown).select_by_visible_text(store_name)

        print(f"Selected Issuing Store: {store_name}")

    def select_random_received_by_in_challan(self):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//select[@name='receivedBy']")
            )
        )

        select = Select(dropdown)

        # Exclude the "Select" option
        valid_options = [
            option for option in select.options
            if option.get_attribute("value") != ""
        ]

        random_option = random.choice(valid_options)

        select.select_by_value(random_option.get_attribute("value"))

        print(f"Selected Received By: {random_option.text}")

        return random_option.text


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


    def click_issue_desk_option(self):
        issue = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[normalize-space()='Issue Desk']")
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

    def select_issuing_store_for_issue_desk(self, store_name):
        # Locate the searchable dropdown input
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[contains(@class,'searchable-dropdown__input') and @role='combobox']"
                )
            )
        )

        dropdown.click()
        dropdown.clear()
        dropdown.send_keys(str(store_name))

        # Select matching option dynamically
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[@role='option' and normalize-space(.)='{store_name}']"
                )
            )
        )

        option.click()

    def select_indent_type(self, indent_type):
        dropdown = Select(
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//select[@name='indenttype']")
                )
            )
        )

        dropdown.select_by_visible_text(indent_type)
        print(f"Selected Indent Type: {indent_type}")


    def click_issue_indent_desk(self):
        issue = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[@role='menuitem'][.//span[normalize-space()='Issue']]")
            )
        )
        issue.click()


    def click_swal_ok_btn(self):

        swal_ok = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and normalize-space()='OK']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            swal_ok
        )

        self.driver.execute_script(
            "arguments[0].click();",
            swal_ok
        )

    def get_issue_report_details(self):
        """
        Fetches Issue Report Details and returns them as a dictionary.
        """

        report = {}

        wait = WebDriverWait(self.driver, 10)

        report["issue_number"] = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[normalize-space()='Issue No.:']/following-sibling::span")
            )
        ).text.strip()

        report["request_number"] = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[normalize-space()='Request No.:']/following-sibling::span")
            )
        ).text.strip()

        report["issue_to"] = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[normalize-space()='Issue To :']/following-sibling::span")
            )
        ).text.strip()

        print("Report Details:")
        for key, value in report.items():
            print(f"{key}: {value}")

        return report


    def click_approval_desk_option(self):
        approval = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Approval Desk']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            approval
        )


    def select_approval_request_type(self, request_type):
        dropdown = Select(
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//select[@name='requestId']")
                )
            )
        )

        dropdown.select_by_visible_text(request_type)
        print(f"Selected Indent Type: {request_type}")


    def click_approval(self):
        approval = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Approval']")
            )
        )
        approval.click()


    def close_btn(self):
        close_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Close']")
            )
        )
        close_btn.click()


    def click_ack_desk_option(self):
        rec = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'menu-level-1')]//a[text()='Acknowledgement Desk']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            rec
        )

    def select_ack_store(self, store_name):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[contains(@class,'searchable-dropdown__input') and @role='combobox']"
                )
            )
        )

        dropdown.click()
        dropdown.clear()
        dropdown.send_keys(str(store_name))

        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[@role='option' and normalize-space(.)='{store_name}']"
                )
            )
        )

        option.click()

    def click_acknowledge(self):
        ack = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Acknowledge']")
            )
        )
        ack.click()

    def enter_comments(self,comm):
        comment = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@name='comments']")))
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            comment
        )

        self.driver.execute_script(
            "arguments[0].click();",
            comment
        )

        comment.send_keys(comm)

    def select_searchable_dropdown(self, value):
        # Click dropdown
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'searchable-dropdown__control')]")
            )
        )
        dropdown.click()

        # Enter value
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@role='combobox' and contains(@class,'searchable-dropdown__input')]")
            )
        )
        search_input.send_keys(value)

        # Select matching option dynamically
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[contains(@class,'searchable-dropdown__option') and normalize-space()='{value}']"
                )
            )
        )
        option.click()















