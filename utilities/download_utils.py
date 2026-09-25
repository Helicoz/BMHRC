import os
import time
import shutil

from pypdf import PdfReader


class PDFUtils:

    # ============================================================
    # GET CHROME DOWNLOAD FOLDER
    # ============================================================

    @staticmethod
    def get_download_folder():

        download_folder = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        os.makedirs(
            download_folder,
            exist_ok=True
        )

        return download_folder

    # ============================================================
    # GET EXISTING PDF FILES
    # ============================================================

    @staticmethod
    def get_existing_pdfs():

        download_folder = (
            PDFUtils.get_download_folder()
        )

        return {
            file_name
            for file_name in os.listdir(download_folder)
            if file_name.lower().endswith(".pdf")
        }

    # ============================================================
    # CLEAR OLD PDF FILES
    # ============================================================

    @staticmethod
    def clear_download_folder():

        download_folder = (
            PDFUtils.get_download_folder()
        )

        for file_name in os.listdir(download_folder):

            file_path = os.path.join(
                download_folder,
                file_name
            )

            try:

                if (
                    file_name.lower().endswith(".pdf")
                    or file_name.lower().endswith(".crdownload")
                ):
                    os.remove(file_path)

            except PermissionError:

                print(
                    f"Could not delete file: {file_path}"
                )

    # ============================================================
    # WAIT FOR NEW PDF DOWNLOAD
    # ============================================================

    @staticmethod
    def wait_for_pdf_download(
        timeout=30,
        existing_files=None
    ):

        download_folder = (
            PDFUtils.get_download_folder()
        )

        if existing_files is None:
            existing_files = set()

        end_time = time.time() + timeout

        while time.time() < end_time:

            try:

                files = os.listdir(
                    download_folder
                )

            except FileNotFoundError:

                os.makedirs(
                    download_folder,
                    exist_ok=True
                )

                time.sleep(1)
                continue

            # ====================================================
            # CHECK CHROME DOWNLOAD
            # ====================================================

            downloading_files = [
                file_name
                for file_name in files
                if file_name.lower().endswith(
                    ".crdownload"
                )
            ]

            # ====================================================
            # FIND NEW PDF
            # ====================================================

            new_pdf_files = [
                file_name
                for file_name in files
                if (
                    file_name.lower().endswith(".pdf")
                    and file_name not in existing_files
                )
            ]

            # ====================================================
            # PDF FOUND
            # ====================================================

            if new_pdf_files:

                new_pdf_files.sort(
                    key=lambda file_name:
                    os.path.getmtime(
                        os.path.join(
                            download_folder,
                            file_name
                        )
                    ),
                    reverse=True
                )

                pdf_file = new_pdf_files[0]

                pdf_path = os.path.join(
                    download_folder,
                    pdf_file
                )

                # If .crdownload exists, wait
                if downloading_files:

                    time.sleep(1)
                    continue

                # =================================================
                # MAKE SURE FILE IS COMPLETELY WRITTEN
                # =================================================

                previous_size = -1

                for _ in range(10):

                    try:

                        current_size = os.path.getsize(
                            pdf_path
                        )

                    except FileNotFoundError:

                        time.sleep(1)
                        continue

                    if current_size == previous_size:
                        break

                    previous_size = current_size

                    time.sleep(0.5)

                return pdf_path

            time.sleep(1)

        # ========================================================
        # TIMEOUT DEBUG INFORMATION
        # ========================================================

        try:
            current_files = os.listdir(
                download_folder
            )
        except Exception:
            current_files = []

        raise TimeoutError(
            f"PDF was not downloaded within "
            f"{timeout} seconds.\n"
            f"Download folder:\n"
            f"{download_folder}\n"
            f"Files currently present:\n"
            f"{current_files}"
        )

    # ============================================================
    # READ PDF
    # ============================================================

    @staticmethod
    def read_pdf(pdf_path):

        if not os.path.exists(pdf_path):

            raise FileNotFoundError(
                f"PDF file not found:\n{pdf_path}"
            )

        reader = PdfReader(
            pdf_path
        )

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    # ============================================================
    # COPY PDF TO PROJECT
    # ============================================================

    @staticmethod
    def copy_to_project_folder(
        pdf_path
    ):

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        project_download_folder = os.path.join(
            project_root,
            "downloads"
        )

        os.makedirs(
            project_download_folder,
            exist_ok=True
        )

        destination = os.path.join(
            project_download_folder,
            os.path.basename(pdf_path)
        )

        shutil.copy2(
            pdf_path,
            destination
        )

        return destination