# Velocity Check Rules for Fraud Detection

## Introduction
Velocity checks monitor the frequency of transactions or actions within a specified time window to detect potentially fraudulent behavior such as rapid repeat transactions or abuse.

## Velocity Check Rule Templates

### 1. Basic Velocity Limit Rule
- **Description:** Limit number of transactions per user account within a time window.
- **Threshold:** 5 transactions per 1 minute.
- **Action:** Flag for manual review or temporarily block.

```yaml
rule:
  name: user_transaction_velocity_limit
  description: Limit user transactions to 5 per minute
  conditions:
    - type: transaction_count
      scope: user_account
      threshold: 5
      window: 1m
  actions:
    - type: flag
      severity: medium
``` 

### 2. IP Address Velocity Rule
- **Description:** Detect excessive transactions from a single IP address.
- **Threshold:** 20 transactions per 5 minutes.
- **Action:** Block or throttle transactions.

```yaml
rule:
  name: ip_address_velocity_limit
  description: Limit transactions from single IP to 20 per 5 minutes
  conditions:
    - type: transaction_count
      scope: ip_address
      threshold: 20
      window: 5m
  actions:
    - type: block
      duration: 15m
```

### 3. Device Fingerprint Velocity Rule
- **Description:** Monitor transactions from a device fingerprint.
- **Threshold:** 10 transactions per 10 minutes.
- **Action:** Require additional verification.

```yaml
rule:
  name: device_fingerprint_velocity
  description: Limit transactions per device fingerprint
  conditions:
    - type: transaction_count
      scope: device_fingerprint
      threshold: 10
      window: 10m
  actions:
    - type: require_additional_verification
```

### 4. Adaptive Velocity Rule (Conceptual)
- **Description:** Adjust velocity thresholds based on user behavior patterns.
- **Implementation:** Use machine learning anomaly detection models.

## Implementation Recommendations
- Integrate rules with real-time transaction monitoring.
- Maintain logs of all velocity violations.
- Combine velocity checks with other fraud signals.
- Regularly tune thresholds based on fraud trends.

---

## References
- PCI-DSS Guidance on Fraud Detection
- OWASP Fraud Prevention Cheat Sheet
- Industry Best Practices for Velocity Checks

*This document serves as a template for implementing velocity check rules to enhance fraud detection in payment and transaction systems.*
