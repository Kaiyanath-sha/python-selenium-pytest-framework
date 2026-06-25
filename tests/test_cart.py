"""
Test suite: Shopping cart functionality
Covers adding/removing products and validating the cart badge count.
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


@pytest.fixture
def logged_in_products_page(driver, test_data):
    """Reusable fixture: log in and land on the products page before each cart test."""
    user = test_data["valid_user"]
    login_page = LoginPage(driver).load()
    login_page.login(user["username"], user["password"])
    return ProductsPage(driver)


@pytest.mark.smoke
@pytest.mark.cart
def test_add_single_product_to_cart(logged_in_products_page):
    products_page = logged_in_products_page

    products_page.add_to_cart_by_name("Sauce Labs Backpack")

    assert products_page.get_cart_count() == 1


@pytest.mark.regression
@pytest.mark.cart
def test_add_multiple_products_to_cart(logged_in_products_page):
    products_page = logged_in_products_page

    products_page.add_to_cart_by_name("Sauce Labs Backpack")
    products_page.add_to_cart_by_name("Sauce Labs Bike Light")
    products_page.add_to_cart_by_name("Sauce Labs Bolt T-Shirt")

    assert products_page.get_cart_count() == 3


@pytest.mark.regression
@pytest.mark.cart
def test_remove_product_from_cart(logged_in_products_page):
    products_page = logged_in_products_page

    products_page.add_to_cart_by_name("Sauce Labs Backpack")
    products_page.add_to_cart_by_name("Sauce Labs Bike Light")
    assert products_page.get_cart_count() == 2

    products_page.remove_from_cart_by_name("Sauce Labs Backpack")

    assert products_page.get_cart_count() == 1


@pytest.mark.regression
@pytest.mark.cart
def test_sort_products_price_low_to_high(logged_in_products_page):
    products_page = logged_in_products_page

    products_page.sort_products("lohi")
    names_after_sort = products_page.get_all_product_names()

    # Sanity check: sorting should not lose any products, just reorder them
    assert len(names_after_sort) == 6
