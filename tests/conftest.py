"""
pytest configuration and fixtures shared across all test files.

Key features:
- --browser CLI flag to switch between chrome/firefox/edge
- driver fixture that handles setup/teardown automatically for every test
- automatic screenshot capture on test failure, embedded into the HTML report
- JSON test data loader fixture

Note: driver binaries are handled automatically by Selenium Manager
(built into Selenium 4.6+), so no separate driver-management package
or manual driver downloads are required.
"""
import json
import os
import pytest
from selenium import webdriver
from config.config import Config

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=Config.DEFAULT_BROWSER,
        help="Browser to run tests on: chrome, firefox, edge",
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser").lower()

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        drv = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        drv = webdriver.Edge(options=options)

    else:  # default: chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        if Config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")
        # Disable GPU-accelerated rendering. On some machines (notably with
        # AMD graphics) Chrome's GPU process throws rendering/composition
        # errors that can desync click timing from what's visually painted,
        # causing intermittent failures in headed (non-headless) runs.
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        drv = webdriver.Chrome(options=options)

    drv.implicitly_wait(Config.IMPLICIT_WAIT)
    drv.maximize_window()

    yield drv

    drv.quit()


@pytest.fixture(scope="session")
def test_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "test_data", "users.json")
    with open(data_path, "r") as f:
        return json.load(f)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After each test, if it failed, attach a screenshot to the HTML report
    automatically. This is one of the most useful debugging features in
    any real-world automation framework.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            screenshot_name = f"{item.name}.png"
            screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
            driver.save_screenshot(screenshot_path)

            # Embed the screenshot into the pytest-html report
            extra = getattr(report, "extra", [])
            try:
                import pytest_html
                relative_path = os.path.join("screenshots", screenshot_name)
                extra.append(pytest_html.extras.image(relative_path))
                report.extra = extra
            except ImportError:
                pass
