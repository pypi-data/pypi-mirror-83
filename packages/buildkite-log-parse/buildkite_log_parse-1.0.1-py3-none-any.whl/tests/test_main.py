import unittest

from buildkite_log_parse import main


class TestMain(unittest.TestCase):
    def test_extract_job_string(self):
        log_text = "blablac test regex a text"
        actual = main.extract_job_string(log_text, "regex (.*)", 1)
        self.assertEqual("a text", actual)
