import os
import unittest

import logging_extended as logging
from logging_extended.example import log_all_levels, log_all_levels_decorated, log_all_levels_loop
from logging_extended.example import test_default, test_basicConfig, test_dictConfig, test_add_file_handler, \
    test_load_config_from_file


class Logger(unittest.TestCase):
    def setUp(self) -> None:
        path_base = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
        os.chdir(path_base)

    def test_simple(self):
        logger = logging.getLogger(__name__)
        log_all_levels(logger)
        log_all_levels_decorated(logger)
        log_all_levels_loop(logger)

    def test_call_example_default(self):
        test_default()

    def test_call_example_basicConfig(self):
        test_basicConfig()  # not working since pytest initializes other logger first

    def test_call_example_dictConfig(self):
        test_dictConfig()

    def test_call_example_add_filehandler(self):
        test_add_file_handler()

    def test_call_example_load_config_from_file(self):
        logger = test_load_config_from_file()
        self.assertEqual(logger.root.level, logging.DEBUG)

    def test_git(self):
        logging.setGitConfig({"auto_commit": False, "commit_message": "Test"})
        logger = logging.getLogger(__name__)
        self.assertTrue(logging._configRetriever.config_dict["commit_message"] == "Test")
        self.assertFalse(logging._configRetriever.config_dict["auto_commit"])


def delete_log_files():
    log_files = [f for f in os.scandir(os.getcwd()) if f.name.endswith(".log")]
    for log_file in log_files:
        os.remove(log_file.path)


if __name__ == '__main__':
    unittest.main()
