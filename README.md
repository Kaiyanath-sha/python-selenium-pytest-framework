# E-Commerce Test Automation Framework

A scalable UI test automation framework built with **Python + Selenium WebDriver + pytest**, following the **Page Object Model (POM)** design pattern. Built against [saucedemo.com](https://www.saucedemo.com), a public e-commerce demo application, to validate login, product catalog, cart, and checkout flows end-to-end.

## Why this project

This framework demonstrates the core skills expected of a QA Automation / SDET role:
- Designing a **maintainable, scalable** automation architecture (not just script-and-go)
- Separating test logic from page interaction logic (POM)
- Data-driven testing using external JSON test data
- Explicit waits and robust element handling (no flaky `sleep()` calls)
- Cross-browser execution (Chrome, Firefox, Edge) via config
- HTML test reporting + screenshot-on-failure for debugging
- CI/CD integration with GitHub Actions
- Clean logging for traceability

## Tech Stack

| Category | Tool |
|---|---|
| Language | Python 3.10+ |
| Browser Automation | Selenium WebDriver 4 |
| Test Runner | pytest |
| Design Pattern | Page Object Model (POM) |
| Reporting | pytest-html |
| Driver Management | webdriver-manager |
| CI/CD | GitHub Actions |
| IDE | VS Code |

## Project Structure

```
selenium-ecommerce-framework/
├── config/
│   └── config.py              # Browser, URL, timeout settings
├── pages/
│   ├── base_page.py           # Common reusable Selenium actions
│   ├── login_page.py          # Login page locators + actions
│   ├── products_page.py       # Product listing / cart page
│   └── checkout_page.py       # Checkout flow page
├── tests/
│   ├── conftest.py            # pytest fixtures (driver setup/teardown, screenshots)
│   ├── test_login.py          # Login test cases (valid/invalid/locked-out users)
│   ├── test_cart.py           # Add to cart / remove from cart tests
│   └── test_checkout.py       # End-to-end checkout flow tests
├── test_data/
│   └── users.json             # Data-driven test inputs
├── utils/
│   └── logger.py              # Centralized logging utility
├── reports/                    # Auto-generated HTML reports + failure screenshots
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions pipeline
├── requirements.txt
├── pytest.ini
└── README.md
```

## What's tested

- **Login**: valid login, invalid credentials, locked-out user, empty fields (data-driven from `users.json`)
- **Cart**: add single/multiple products, remove products, cart badge count validation
- **Checkout**: full end-to-end purchase flow, form validation, order confirmation

## How to run

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd selenium-ecommerce-framework

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run all tests (headless Chrome by default)
pytest

# 5. Run with HTML report
pytest --html=reports/report.html --self-contained-html

# 6. Run a specific test file
pytest tests/test_login.py -v

# 7. Run in a specific browser
pytest --browser=firefox
```

## Sample report output

After running, open `reports/report.html` in a browser to see pass/fail status, execution time, and embedded screenshots for any failed test.

## CI/CD

Every push triggers the GitHub Actions workflow (`.github/workflows/ci.yml`), which runs the full suite headlessly and uploads the HTML report as a build artifact.

## Possible extensions

- API layer testing with `requests` for backend validation
- Parallel execution with `pytest-xdist`
- Allure reporting integration
- Dockerized test execution

---
*Built as a personal project to demonstrate test automation framework design for QA Automation Engineer / SDET roles.*
