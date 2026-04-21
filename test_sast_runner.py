# Updated test_sast_runner.py

def test_safe_sql_concatenation():
    assert safe_sql_concatenation('value1', 'value2') == "SELECT * FROM table WHERE column1 = 'value1' AND column2 = 'value2'"

# Other existing test cases...
