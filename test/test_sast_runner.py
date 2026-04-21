import unittest
from scanners.sast_runner import get_user_data

class TestSASTRunner(unittest.TestCase):

    def test_valid_username(self):
        result = get_user_data('valid_user')  # This should be a valid user in the database
        self.assertIsNotNone(result)

    def test_empty_username(self):
        with self.assertRaises(ValueError) as context:
            get_user_data('')
        self.assertEqual(str(context.exception), "Invalid username input. Must be a non-empty string with a maximum length of 50 characters.")

    def test_invalid_username_type(self):
        with self.assertRaises(ValueError) as context:
            get_user_data(123)
        self.assertEqual(str(context.exception), "Invalid username input. Must be a non-empty string with a maximum length of 50 characters.")

    def test_long_username(self):
        long_username = 'u' * 51  # 51 characters long
        with self.assertRaises(ValueError) as context:
            get_user_data(long_username)
        self.assertEqual(str(context.exception), "Invalid username input. Must be a non-empty string with a maximum length of 50 characters.")

if __name__ == '__main__':
    unittest.main()