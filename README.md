# Security Scanners

## Managing False Positives
- **Configure Sensitivity Levels**: Adjust settings in the configuration file to minimize irrelevant alerts based on your project's needs. Consider setting thresholds that reflect the acceptable risk for your organization.
- **Implement a Whitelist**: Add known false positives to a whitelist for streamlined review. Below is an example of how to configure the whitelist in your `config.yaml`:
  ```yaml
  whitelist:
    - "hardcoded_api_key"
    - "known_secret"
    - "test_api_key"
    - "example_secret"
  ```

- **Review and Update Regularly**: Periodically review the whitelist and sensitivity settings to ensure they remain effective as your project evolves and new false positives may arise. Update the configurations to reflect any changes in your codebase.

- **Documentation**: Document any false positives and their corresponding whitelisting in a separate file or section within your project to maintain awareness among team members and future contributors.

## Recommendations for Improved Detection Accuracy
1. **Regularly Update Rules**: Keep your scanning rules and configurations up to date with the latest vulnerability definitions and best practices.
2. **Feedback Loop**: Implement a feedback loop where developers can report false positives, and use this information to refine scanning rules and update the whitelist accordingly.
3. **Testing Environment**: Use a dedicated testing environment for scanning to reduce the likelihood of false positives from production data.

## Conclusion
By implementing these strategies to manage false positives, you can improve the accuracy of your security scanners and reduce unnecessary alerts, allowing your team to focus on genuine vulnerabilities.