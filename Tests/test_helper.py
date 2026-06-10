import unittest
import logging
import os
import tempfile
from unittest.mock import patch


class TestTimestamp(unittest.TestCase):

    def test_format_timestamp(self):
        from Utils.helper import timestamp
        ts = timestamp()
        # Format awaited : YYYY-MM-DD HH:MM:SS
        self.assertRegex(ts, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    def test_retourne_string(self):
        from Utils.helper import timestamp
        self.assertIsInstance(timestamp(), str)


class TestLogMessage(unittest.TestCase):

    def setUp(self):
        self.tmpdir  = tempfile.mkdtemp()
        self.logfile = os.path.join(self.tmpdir, "app.log")
        self.patcher = patch("Utils.helper.DIR_LOGS_FILES", self.tmpdir)
        self.patcher.start()

        # Reinit logger to point to the temp file 
        logger = logging.getLogger()
        for h in logger.handlers[:]:
            logger.removeHandler(h)
        logging.basicConfig(
            filename=self.logfile,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def tearDown(self):
        self.patcher.stop()
        logging.getLogger().handlers.clear()
        if os.path.exists(self.logfile):
            os.unlink(self.logfile)
        os.rmdir(self.tmpdir)

    def test_log_info(self):
        from Utils.helper import log_message
        log_message("Test info", "info")   # no error

    def test_log_warning(self):
        from Utils.helper import log_message
        log_message("Test warning", "warning")

    def test_log_error(self):
        from Utils.helper import log_message
        log_message("Test error", "error")

    def test_log_level_invalide_leve_erreur(self):
        from Utils.helper import log_message
        with self.assertRaises(ValueError):
            log_message("Test", "debug")   # no supported level

    def test_log_level_insensible_casse(self):
        from Utils.helper import log_message
        log_message("Test", "INFO")        # maj accepted 


if __name__ == "__main__":
    unittest.main()
