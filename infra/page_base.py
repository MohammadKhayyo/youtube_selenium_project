class BasePage:
    def __init__(self, driver, wait):
        # Constructor method for the BasePage class.
        # It initializes the class with a Selenium WebDriver instance and a WebDriverWait instance.
        # These instances are provided by the code that creates an object of this class, allowing for browser manipulation and explicit waits.
        self._driver = driver  # The WebDriver instance for browser control
        self._wait = wait  # The WebDriverWait instance for managing explicit waits

    def get_page_title(self):
        # Method to get the current page title.
        # It returns the title of the web page currently loaded in the browser.
        # This can be used in tests to verify that the correct page is loaded.
        return self._driver.title  # Returns the title of the current page
