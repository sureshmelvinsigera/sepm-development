from game.utilities import censor_word
from tests.base.BaseTestCase import BaseTestCase


class TestCensorship(BaseTestCase):
    def test_if_censors_static_input_correctly(self):
        """Test if the censorship function correctly amends text."""
        self.assertEqual(
            "f**k", censor_word("fuck"), "fuck is not correctly being censored to f**k."
        )
        self.assertEqual(
            "b******s",
            censor_word("bollocks"),
            "bollocks is not correctly being censored to b*****s.",
        )
        self.assertEqual(
            "if", censor_word("if"), "A 2 character string has been incorrectly mutated"
        )
