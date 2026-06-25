"""
Test suite: End-to-end checkout flow
Covers the full purchase journey and checkout form validation.
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def cart_with_item(driver, test_data):
    """Log in and add one product to cart, then go to the cart page."""
    user = test_data["valid_user"]
    login_page = LoginPage(driver).load()
    login_page.login(user["username"], user["password"])

    products_page = ProductsPage(driver)
    products_page.add_to_cart_by_name("Sauce Labs Backpack")
    products_page.go_to_cart()
    return driver


@pytest.mark.smoke
@pytest.mark.checkout
def test_complete_checkout_flow_successfully(cart_with_item, test_data):
    checkout_page = CheckoutPage(cart_with_item)
    info = test_data["checkout_info"]

    checkout_page.start_checkout()
    checkout_page.fill_checkout_info(
        info["first_name"], info["last_name"], info["postal_code"]
    )
    checkout_page.finish_order()

    confirmation = checkout_page.get_confirmation_message()
    assert confirmation == "Thank you for your order!"


@pytest.mark.regression
@pytest.mark.checkout
def test_checkout_fails_without_required_fields(cart_with_item):
    checkout_page = CheckoutPage(cart_with_item)

    checkout_page.start_checkout()
    checkout_page.fill_checkout_info("", "", "")  # leave all fields blank

    assert checkout_page.is_checkout_error_displayed()
    assert "First Name is required" in checkout_page.get_checkout_error()


@pytest.mark.regression
@pytest.mark.checkout
def test_checkout_fails_without_postal_code(cart_with_item):
    checkout_page = CheckoutPage(cart_with_item)

    checkout_page.start_checkout()
    checkout_page.fill_checkout_info("Kaiyanath", "Sha", "")

    assert checkout_page.is_checkout_error_displayed()
    assert "Postal Code is required" in checkout_page.get_checkout_error()
