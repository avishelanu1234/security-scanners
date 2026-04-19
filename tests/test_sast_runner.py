import unittest
from scanners.sast_runner import check_sql_concatenation

class TestSQLConcatenationDetection(unittest.TestCase):
    def test_valid_concatenation(self):
        findings = "username + password"
        result = check_sql_concatenation(findings)
        self.assertEqual(result, [('username', 'password')])

    def test_invalid_concatenation(self):
        findings = "SELECT * FROM users"
        result = check_sql_concatenation(findings)
        self.assertEqual(result, [])

    def test_edge_case(self):
        findings = "'hello' + 'world'"
        result = check_sql_concatenation(findings)
        self.assertEqual(result, [('', 'hello'), ('', 'world')])

if __name__ == '__main__':
    unittest.main()