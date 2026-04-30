# Test file to trigger security scanners for PR comment posting

def test_trigger_security_scan():
    # This dummy test function is designed to trigger security scanners
    # It contains typical patterns that scanners might detect as issues

    # Example of a high severity issue for Bandit: use of assert in production code
    assert False, "Trigger Bandit high severity issue"

    # Example secret pattern that might be picked up by secrets scanner
    secret = "SECRET_API_KEY=123456789"
    print(secret)

    # Example usage that might trigger DAST if applicable
    # Here we just simulate a vulnerable call
    user_input = "<script>alert('xss')</script>"
    print(user_input)

    assert True
