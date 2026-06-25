"""
Test suite: Login functionality
Covers valid login, locked-out user, and data-driven invalid login scenarios.
"""
import json
import os
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "test_data", "users.json")
with open(_DATA_PATH) as _f:
    _INVALID_USERS = json.load(_f)["invalid_users"]


@pytest.mark.smoke
@pytest.mark.login
def test_valid_login(driver, test_data):
    login_page = LoginPage(driver).load()
    user = test_data["valid_user"]

    login_page.login(user["username"], user["password"])

    products_page = ProductsPage(driver)
    assert "inventory" in products_page.current_url(), "Login did not redirect to products page"
    assert products_page.get_page_title() == "Products"


@pytest.mark.regression
@pytest.mark.login
def test_locked_out_user_cannot_login(driver, test_data):
    login_page = LoginPage(driver).load()
    user = test_data["locked_out_user"]

    login_page.login(user["username"], user["password"])

    assert login_page.is_error_displayed()
    assert "locked out" in login_page.get_error_message().lower()


@pytest.mark.regression
@pytest.mark.login
@pytest.mark.parametrize(
    "invalid_user",
    _INVALID_USERS,
    ids=[f"username={u['username'] or 'empty'}" for u in _INVALID_USERS],
)
def test_invalid_login_combinations(driver, invalid_user):
    login_page = LoginPage(driver).load()

    login_page.login(invalid_user["username"], invalid_user["password"])

    assert login_page.is_error_displayed(), "Expected an error message but none was shown"
    actual_error = login_page.get_error_message()
    assert invalid_user["expected_error"] in actual_error, (
        f"Expected error containing '{invalid_user['expected_error']}', got '{actual_error}'"
    )
