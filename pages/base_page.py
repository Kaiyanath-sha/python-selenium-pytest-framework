"""
BasePage centralizes every low-level Selenium interaction (clicking, typing,
waiting, reading text) so that page objects never call driver methods
directly. This means:
  - Explicit waits are applied everywhere automatically (no flaky tests)
  - If we ever swap how we wait/interact, we change it in ONE place
  - Page objects stay readable and focused on "what", not "how"
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url: str):
        self.logger.info(f"Navigating to {url}")
        self.driver.get(url)

    def find(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not found in time: {locator}")
            raise

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.logger.info(f"Clicking element: {locator}")
        element.click()

    def type_text(self, locator, text: str, clear_first: bool = True):
        element = self.find(locator)
        if clear_first:
            element.clear()
        self.logger.info(f"Typing into {locator}")
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator, timeout: int = None) -> bool:
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_present(self, locator) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def get_all_text(self, locator) -> list:
        elements = self.wait.until(EC.presence_of_all_elements_located(locator))
        return [el.text for el in elements]

    def wait_for_url_contains(self, fragment: str, timeout: int = None):
        wait_time = timeout or Config.EXPLICIT_WAIT
        WebDriverWait(self.driver, wait_time).until(EC.url_contains(fragment))

    def current_url(self) -> str:
        return self.driver.current_url
