"""
Page Object for the Products listing page and cart interactions.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    def add_to_cart_by_name(self, product_name: str):
        """
        saucedemo generates button IDs from the product name, e.g.
        'Sauce Labs Backpack' -> 'add-to-cart-sauce-labs-backpack'.
        This lets tests add items by readable name instead of hardcoded IDs.
        """
        button_id = "add-to-cart-" + product_name.lower().replace(" ", "-")
        locator = (By.ID, button_id)
        self.click(locator)

    def remove_from_cart_by_name(self, product_name: str):
        button_id = "remove-" + product_name.lower().replace(" ", "-")
        locator = (By.ID, button_id)
        self.click(locator)

    def get_cart_count(self) -> int:
        if self.is_present(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def sort_products(self, option_value: str):
        """option_value examples: 'az', 'za', 'lohi', 'hilo'"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find(self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(option_value)

    def get_all_product_names(self) -> list:
        return self.get_all_text(self.ITEM_NAMES)
