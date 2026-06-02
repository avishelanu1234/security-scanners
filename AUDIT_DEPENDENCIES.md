# Audit Dependencies

## Overview
This file outlines the steps to audit project dependencies for known vulnerabilities.

## Steps to Audit
1. **Node.js Projects**: Run `npm audit` to check for vulnerabilities in dependencies.
2. **Python Projects**: Use `pip-audit` to audit installed packages.
3. **Ruby Projects**: Run `bundler-audit` to check for vulnerabilities in Gemfile.lock.

## Reporting
- Review the output and address any vulnerabilities found.
- Update dependencies as necessary to mitigate risks.