from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class BrowserWrapper:
    def __init__(self, browser_type='Chrome', wait_timeout=10):
        # Initialize the BrowserWrapper instance with default or specified browser type and wait timeout.
        self.driver = None  # This will hold the instance of the webdriver once it's started.
        self.wait_timeout = wait_timeout  # Duration to wait for a condition or element before timing out.
        self.browser_type = browser_type  # Type of browser to use, default is Chrome.

    def start_browser(self, url, maximize_window=True):
        # Start the browser specified by self.browser_type, navigate to the URL, and optionally maximize the window.
        if self.browser_type == 'Chrome':
            self.driver = webdriver.Chrome()  # Start Chrome WebDriver
        elif self.browser_type == 'Firefox':
            self.driver = webdriver.Firefox()  # Start Firefox WebDriver
        else:
            raise ValueError(
                f"Unsupported browser type: {self.browser_type}")  # Raise error if browser type is unsupported

        if maximize_window:
            self.driver.maximize_window()  # Maximize the browser window if specified

        self.navigate(url)  # Navigate to the specified URL
        return self.driver  # Return the driver instance for further use

    def get_wait(self):
        # Return a WebDriverWait instance for the current driver, using the specified timeout.
        return WebDriverWait(self.driver, self.wait_timeout)

    def navigate(self, url):
        # Navigate the browser to the specified URL.
        self.driver.get(url)

    def close_browser(self):
        # Close the browser and quit the webdriver session.
        if self.driver:
            self.driver.quit()
