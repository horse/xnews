import unittest

from tools.wordpress_publish_safe import normalize_application_password


class WordpressPublishSafeTests(unittest.TestCase):
    def test_normalize_application_password_removes_all_whitespace(self):
        self.assertEqual(
            normalize_application_password("abcd efgh\nijkl\tmnop"),
            "abcdefghijklmnop",
        )


if __name__ == "__main__":
    unittest.main()
