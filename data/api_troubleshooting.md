# API Troubleshooting Guide

## 401 Unauthorized

A 401 error usually indicates:

- Invalid API key
- Expired token
- Missing Authorization header

Verify the following header:

Authorization: Bearer YOUR_TOKEN

## 500 Internal Server Error

Check:

- Application logs
- Database connectivity
- Third-party integrations
