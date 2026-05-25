# Updated SQL String Concatenation Detection

SQL_CONCAT_PATTERN = r'(\w+|\'[^"]*\'|\"[^"]*\")\s*\+\s*(\w+|\'[^"]*\'|\"[^"]*\")'

# Expanded to handle complex SQL queries
# Added error logging for subprocess execution
# Improved logging levels for better traceability
