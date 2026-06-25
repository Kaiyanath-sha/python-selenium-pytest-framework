"""
Central configuration for the test framework.
Keeps environment-specific values (URLs, timeouts, browser choice) out of test code.
"""

class Config:
    BASE_URL = "https://www.saucedemo.com"
    DEFAULT_BROWSER = "chrome"
    IMPLICIT_WAIT = 5
    EXPLICIT_WAIT = 10
    HEADLESS = False

    # Window size matters for responsive elements on saucedemo
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
