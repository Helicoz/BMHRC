import os

class Screenshot:

    @staticmethod
    def capture(driver, test_name):

        screenshot_dir = f"screenshots/{test_name}"
        os.makedirs(screenshot_dir, exist_ok=True)

        # 🔥 Clear old screenshots for this test
        for file in os.listdir(screenshot_dir):
            file_path = os.path.join(screenshot_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        file_path = f"{screenshot_dir}/{test_name}.png"
        driver.save_screenshot(file_path)

        return file_path