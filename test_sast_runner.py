import pytest
import re

# Test cases for validating the updated whitelist patterns

# Test for valid usernames
valid_usernames = ['user_name', 'username123', 'user.name', 'user-name']
invalid_usernames = ['!@#$', '12345678901234567890', '']

@pytest.mark.parametrize('username', valid_usernames)
def test_valid_usernames(username):
    assert re.match(r'^[a-zA-Z0-9._%+-]+$', username) is not None

@pytest.mark.parametrize('username', invalid_usernames)
def test_invalid_usernames(username):
    assert re.match(r'^[a-zA-Z0-9._%+-]+$', username) is None

# Test for valid phone numbers
valid_phone_numbers = ['+1234567890', '1234567890']
invalid_phone_numbers = ['12345', '123456789012345', 'abc123']

@pytest.mark.parametrize('phone', valid_phone_numbers)
def test_valid_phone_numbers(phone):
    assert re.match(r'^\+?[1-9]\d{1,14}$', phone) is not None

@pytest.mark.parametrize('phone', invalid_phone_numbers)
def test_invalid_phone_numbers(phone):
    assert re.match(r'^\+?[1-9]\d{1,14}$', phone) is None

# Test for valid emails
valid_emails = ['test@example.com', 'user.name@domain.co', 'user-name@domain.com']
invalid_emails = ['plainaddress', '@missingusername.com', 'username@.com']

@pytest.mark.parametrize('email', valid_emails)
def test_valid_emails(email):
    assert re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

@pytest.mark.parametrize('email', invalid_emails)
def test_invalid_emails(email):
    assert re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is None

# Test for valid addresses
valid_addresses = ['123 Main St', '456 Elm St, Apt 2', '789 Oak St.']
invalid_addresses = ['!@#$%', '', '1234\invalid_address']

@pytest.mark.parametrize('address', valid_addresses)
def test_valid_addresses(address):
    assert re.match(r'^[\d\s\w,.-]+$', address) is not None

@pytest.mark.parametrize('address', invalid_addresses)
def test_invalid_addresses(address):
    assert re.match(r'^[\d\s\w,.-]+$', address) is None
