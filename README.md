# Ecommerce Web Automation

[![Python](https://img.shields.io/badge/Python-3.12.3-blue)]()
[![Pytest](https://img.shields.io/badge/pytest-8.4.1-green)]()
[![Selenium](https://img.shields.io/badge/selenium-4.34.2-orange)]()
[![Allure](https://img.shields.io/badge/allure-2.15.0-red)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey)]()
[![Tests](https://github.com/MaryRes/ecommerce-web-automation/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/MaryRes/ecommerce-web-automation/actions)

Automated test suite for e-commerce website verification using Python and Selenium WebDriver.

## 📋 Project Overview

This project contains automated tests for critical functionalities of an online shop:
- ✅ User authentication (login/logout)
- ✅ Product search and filtering
- ✅ Shopping cart management  
- ✅ Checkout process
- ✅ Order management

## 🛠️ Tech Stack

- **Programming Language:** Python 3.12.3
- **Testing Framework:** pytest 8.4.1
- **Browser Automation:** Selenium WebDriver 4.34.2
- **Reporting:** Allure Report 2.15.0
- **CI/CD:** GitHub Actions (planned)

## 🚀 Quick Start

### Prerequisites
- Python 3.12.3 or higher
- Git

### Installation & Running

```bash
# Clone the repository
git clone https://github.com/MaryRes/ecommerce-web-automation.git
cd ecommerce-web-automation

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ --alluredir=allure-results

# Run specific test category
pytest tests/ui/ -v
pytest tests/e2e/ -v
```

### Viewing Reports

```bash
# Generate Allure report (requires Allure CLI)
allure serve allure-results/
```

## 📁 Project Structure

```bash
ecommerce-web-automation/          # Root project directory
│
├── config/                        # Configuration files
│   ├── __init__.py
│   └── settings.py                # Main settings (URLs, credentials, timeouts)
│
├── data/                          # Test data
│   ├── __init__.py
│   ├── test_data.py               # Data as variables/dictionaries
│   └── test_data.json             # Data in JSON format
│
├── pages/                         # Page Object Model
│   ├── __init__.py
│   ├── base_page.py               # Base class for all pages
│   ├── main_page.py               # Main page
│   ├── catalog_page.py            # Catalog page
│   ├── product_page.py            # Product details page
│   ├── cart_page.py               # Shopping cart page
│   ├── auth_page.py               # Authentication/registration
│   ├── checkout_page.py           # Checkout page
│   └── account_page.py            # User account page
│
├── tests/                         # Test packages
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── ui/                        # UI component tests
│   └── e2e/                       # End-to-end scenarios
│
├── utils/                         # Helper utilities
│   ├── __init__.py
│   ├── helpers.py                 # Common helper functions
│   └── locators.py                # Centralized selectors
│
├── logs/                          # Test execution logs
├── screenshots/                   # Screenshots on failures
├── allure-results/                # Allure test results
├── requirements.txt               # Dependencies
├── pytest.ini                     # Pytest configuration
└── README.md                      # Project documentation
```

## 🧪 Test Cases

### Smoke Tests

- 🔐 User login with valid credentials
- 🔍 Product search functionality
- 🛒 Add product to cart
- 💳 Checkout process

### Regression Tests

- 👤 User registration
- 📊 Product filtering and sorting
- 📦 Cart quantity management
- 📋 Order history verification

## 📊 Test Management

_Test documentation, bug reports, and test plans will be added to the project Wiki soon..._

## 🤝 Contributing

This is a portfolio project. Feel free to:
- Report issues and bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

Created by MaryRes - QA Automation Engineer
Connect with me on [LinkedIn](https://www.linkedin.com/in/aija-t-08934978)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/aija-t-08934978)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/MaryRes)


