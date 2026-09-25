import logging
import os


class LogGen:

    @staticmethod
    def loggen():

        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        log_file = f"{log_dir}/automation.log"

        # Clear previous log
        if os.path.exists(log_file):
            open(log_file, "w").close()

        logging.basicConfig(
            filename=log_file,
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
            force=True
        )

        return logging.getLogger()

    # ============================================================
    # TEST START
    # ============================================================

    @staticmethod
    def start_test(logger, test_name, module_name):

        logger.info("")
        logger.info("#" * 95)
        logger.info(f"# TEST CASE : {test_name}")
        logger.info(f"# MODULE    : {module_name}")
        logger.info("# STATUS    : STARTED")
        logger.info("#" * 95)

    # ============================================================
    # TEST PASSED
    # ============================================================

    @staticmethod
    def test_passed(logger, test_name):

        logger.info("")
        logger.info("#" * 95)
        logger.info(f"# TEST CASE : {test_name}")
        logger.info("# STATUS    : PASSED")
        logger.info("#" * 95)
        logger.info("")

    # ============================================================
    # TEST FAILED
    # ============================================================

    @staticmethod
    def test_failed(logger, test_name, reason):

        logger.error("")
        logger.error("#" * 95)
        logger.error(f"# TEST CASE : {test_name}")
        logger.error("# STATUS    : FAILED")
        logger.error(f"# REASON    : {reason}")
        logger.error("#" * 95)
        logger.error("")