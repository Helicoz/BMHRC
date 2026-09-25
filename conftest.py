import pytest
import base64
from pytest_html import extras
from pytest_metadata.plugin import metadata_key

from base_pages.Opd_page import Opd_Page


# Add custom command line parameters
def pytest_addoption(parser):
    parser.addoption(
        "--tester",
        action="store",
        default="Unknown Tester",
        help="Tester Name"
    )

    parser.addoption(
        "--env",
        action="store",
        default="QA",
        help="Environment Name"
    )

    parser.addoption(
        "--revisit-crn",
        action="store",
        default=None,
        help="Fallback CRN for revisit patient"
    )

    parser.addoption(
        "--abha-mobile",
        action="store",
        default=None,
        help="Mobile number for ABHA verification"
    )


# ============================================================
# HTML REPORT METADATA
# ============================================================

def pytest_configure(config):

    tester = config.getoption("--tester")
    env = config.getoption("--env")
    revisit_crn = config.getoption("--revisit-crn")
    abha_mobile = config.getoption("--abha-mobile")

    print(f"\nTester = {tester}")
    print(f"Environment = {env}")
    print(f"Fallback Revisit CRN = {revisit_crn}")
    print(f"ABHA Mobile = {abha_mobile}")

    config.stash[metadata_key]["Tester"] = tester
    config.stash[metadata_key]["Environment"] = env

    if revisit_crn:
        config.stash[metadata_key]["Fallback Revisit CRN"] = revisit_crn
    else:
        config.stash[metadata_key]["Fallback Revisit CRN"] = "Not Provided"

    if abha_mobile:
        config.stash[metadata_key]["ABHA Mobile"] = abha_mobile
    else:
        config.stash[metadata_key]["ABHA Mobile"] = "Not Provided"


# Capture screenshot on failure and quit browser
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call":

        driver = getattr(item.instance, "driver", None)

        if driver and report.failed:

            try:
                screenshot = driver.get_screenshot_as_png()

                extra = getattr(report, "extras", [])

                extra.append(
                    extras.image(
                        base64.b64encode(screenshot).decode("utf-8"),
                        mime_type="image/png"
                    )
                )

                report.extras = extra

            except Exception as e:
                print(f"Screenshot error: {e}")


import pytest
from selenium import webdriver
import time

from base_pages.Login_Admin_Page import Login_Admin_Page
from base_pages.Patient_Register_page import Patient_Register_Page
from base_pages.Opd_page import Opd_Page
from base_pages.Inventory_page import Inventory_Page


@pytest.fixture(scope="class")
def login(request):
    # ============================================================
    # CHROME OPTIONS
    # ============================================================

    chrome_options = Options()

    # ============================================================
    # DOWNLOAD DIRECTORY
    # ============================================================

    download_dir = os.path.join(
        os.path.expanduser("~"),
        "Downloads"
    )

    prefs = {

        # --------------------------------------------------------
        # DOWNLOAD SETTINGS
        # --------------------------------------------------------

        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,

        # --------------------------------------------------------
        # PASSWORD / CREDENTIAL POPUPS
        # --------------------------------------------------------

        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,

        # Disable Chrome password leak detection popup
        "profile.password_manager_leak_detection": False,

        # --------------------------------------------------------
        # PDF
        # --------------------------------------------------------

        "download.extensions_to_open": ""
    }

    chrome_options.add_experimental_option(
        "prefs",
        prefs
    )

    # ============================================================
    # ADDITIONAL CHROME FLAGS
    # ============================================================

    chrome_options.add_argument(
        "--disable-features=PasswordLeakDetection"
    )

    chrome_options.add_argument(
        "--disable-notifications"
    )

    # ============================================================
    # START CHROME
    # ============================================================

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=chrome_options
    )

    driver.maximize_window()

    # Store download directory
    driver.download_dir = download_dir
    driver.get("https://bmhrc-esushrutnx.uat.dcservices.in/")

    admin_lp = Login_Admin_Page(driver)

    admin_lp.enter_username("SUDEEP")
    admin_lp.enter_password("Cdac@2120")
    admin_lp.enter_captcha()
    admin_lp.click_login_btn()

    time.sleep(3)


    # ============================================================
    # FALLBACK FEMALE PATIENT CRN
    # ============================================================

    revisit_crn = request.config.getoption(
        "--revisit-crn"
    )

    request.cls.revisit_hardcoded_crn = revisit_crn

    print(
        f"\nFemale Patient Fallback CRN: {revisit_crn}"
    )

    # ============================================================
    # ABHA VERIFICATION MOBILE NUMBER
    # ============================================================

    abha_mobile = request.config.getoption(
        "--abha-mobile"
    )

    # Use hardcoded mobile if batch parameter is not provided
    if not abha_mobile:
        abha_mobile = "8958519719"
        print(
            "\nABHA mobile not provided from batch file."
            " Using hardcoded fallback mobile."
        )
    else:
        print(
            f"\nABHA mobile received from batch file: "
            f"{abha_mobile}"
        )

    request.cls.abha_mobile = abha_mobile

    # Make these available to all test methods
    request.cls.driver = driver
    request.cls.patient_reg = Patient_Register_Page(driver)
    request.cls.admin_lp = admin_lp
    request.cls.opd_flow = Opd_Page(driver)
    request.cls.inventory_flow = Inventory_Page(driver)

    yield

    driver.quit()



import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def setup(request):

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://bmhrc-esushrutnx.uat.dcservices.in/")

    request.cls.driver = driver

    yield

    driver.quit()

import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def setup():

    chrome_options = Options()

    # ============================================================
    # CHROME DOWNLOAD SETTINGS
    # ============================================================

    # Use Chrome's normal Windows Downloads folder
    download_dir = os.path.join(
        os.path.expanduser("~"),
        "Downloads"
    )

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "profile.password_manager_leak_detection": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "download.directory_upgrade": True,

        # Force PDF to download instead of opening in Chrome
        "plugins.always_open_pdf_externally": True,

        "download.extensions_to_open": ""
    }

    chrome_options.add_experimental_option(
        "prefs",
        prefs
    )

    # ============================================================
    # START CHROME
    # ============================================================

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=chrome_options
    )

    driver.maximize_window()

    # Store download directory in driver
    driver.download_dir = download_dir

    yield driver

    driver.quit()