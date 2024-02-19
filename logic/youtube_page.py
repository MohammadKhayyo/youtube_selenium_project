from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from infra.page_base import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains


class YouTubePage(BasePage):
    # Locator tuples for various elements on the YouTube page
    SEARCH_BOX = (By.NAME, "search_query")
    VIDEO_RENDERER = (By.CSS_SELECTOR, "ytd-video-renderer,#video-title")
    FULL_SCREEN_BUTTON = (By.CSS_SELECTOR, "button.ytp-fullscreen-button")
    MUTE_BUTTON = (By.CSS_SELECTOR, "button.ytp-mute-button")
    PLAY_BUTTON = (By.CSS_SELECTOR, "button.ytp-play-button")
    MINIPLAYER_BUTTON = (By.CSS_SELECTOR, "button.ytp-miniplayer-button")
    MINIPLAYER_EXPAND = (By.CSS_SELECTOR, ".ytp-miniplayer-expand-watch-page-button")
    SETTINGS_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Settings']")
    APPEARANCE_MENU_ITEM_TEXT = "Appearance: Device theme"
    DARK_THEME_TEXT = "Dark theme"
    LIGHT_THEME_TEXT = "Light theme"
    DEVICE_THEME_TEXT = "Use device theme"
    APPEARANCE_MENU_ITEM = (By.XPATH, "//tp-yt-paper-item[@role='menuitem']")
    VIDEO_PLAYER = (By.CSS_SELECTOR, "video")
    PLAY_BUTTON_IN_EXPAND = (By.CSS_SELECTOR, "button[aria-label='Play keyboard shortcut k']")
    VIDEO_IN_MINIPLAYER_ELEMENT = (By.CLASS_NAME, "ytp-miniplayer-scrim")
    VIDEO_ELEMENT = (By.XPATH, "//video[@class = 'video-stream html5-main-video']")

    def __init__(self, driver, wait):
        # Call the constructor of BasePage
        super().__init__(driver, wait)

    def play_video(self):
        """Play the video on the current page by clicking the play button."""
        play_button = self._wait.until(EC.element_to_be_clickable(self.PLAY_BUTTON))
        play_button.click()
        # Wait for the play button to become clickable again as an indication of state change
        self._wait.until(EC.element_to_be_clickable(self.PLAY_BUTTON))

    def search(self, search_term):
        """Search for a video using the provided search term."""
        search_box = self._driver.find_element(*self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        # Wait until the page title contains the search term, indicating search completion
        self._wait.until(lambda d: search_term.lower() in d.title.lower())

    def is_video_found(self):
        """Check if any video is found after a search by looking for video renderer elements."""
        self._wait.until(EC.presence_of_element_located(self.VIDEO_RENDERER))
        videos = self._driver.find_elements(*self.VIDEO_RENDERER)
        return len(videos) > 0

    def toggle_mute(self):
        """Toggle the mute state of the video and return the new mute state."""
        self._wait.until(EC.element_to_be_clickable(self.MUTE_BUTTON)).click()
        return self.is_video_muted()

    def is_video_muted(self):
        """Check if the video is currently muted by evaluating JavaScript."""
        return self._driver.execute_script("return document.querySelector('video').muted;")

    def full_screen(self):
        """Enter full screen mode by clicking the full screen button."""
        full_screen_button = self._wait.until(EC.element_to_be_clickable(self.FULL_SCREEN_BUTTON))
        full_screen_button.click()
        # Wait until the document enters full screen mode
        self._wait.until(lambda d: self._driver.execute_script("return document.fullscreenElement != null;"))

    def is_full_screen_mode(self):
        """Check if the browser is in full screen mode by evaluating JavaScript."""
        return self._driver.execute_script("return document.fullscreenElement != null;")

    def exit_full_screen(self):
        """Exit full screen mode if currently in it."""
        if self.is_full_screen_mode():
            self._driver.execute_script("document.exitFullscreen();")
            # Wait until the document exits full screen mode
            self._wait.until(lambda d: self._driver.execute_script("return document.fullscreenElement == null;"))

    def is_exist_full_screen_mode(self):
        """Check if the browser has exited full screen mode."""
        return self._driver.execute_script("return document.fullscreenElement == null;")

    def use_miniplayer(self):
        """Activate the miniplayer mode."""
        self.move_to("video")
        self._wait.until(EC.element_to_be_clickable(self.MINIPLAYER_BUTTON)).click()
        # Wait until the miniplayer expand button is visible as an indication of miniplayer mode activation
        self.move_to("expand_button")
        self._wait.until(EC.visibility_of_element_located(self.MINIPLAYER_EXPAND))
        return True

    def expand_from_miniplayer(self):
        """Return to the regular video view from miniplayer mode."""
        self.move_to("expand_button")
        self._wait.until(EC.element_to_be_clickable(self.MINIPLAYER_EXPAND)).click()
        # Wait until the miniplayer button is visible again as an indication of returning to normal view
        self.move_to("video")
        self._wait.until(EC.visibility_of_element_located(self.MINIPLAYER_BUTTON))
        return True

    def move_to(self, to):
        if to == "expand_button":
            # Wait for the miniplayer element to be present on the page
            to_element = self._wait.until(EC.presence_of_element_located(self.VIDEO_IN_MINIPLAYER_ELEMENT))
        elif to == "video":
            to_element = self._wait.until(EC.element_to_be_clickable(self.VIDEO_ELEMENT))
        else:
            raise Exception
            # Create an ActionChains object
        actions = ActionChains(self._driver)
        # Move the mouse to the miniplayer element
        actions.move_to_element(to_element).perform()

    def click_settings_button(self):
        # Waits for the settings button to be clickable and then clicks it.
        self._wait.until(EC.element_to_be_clickable(self.SETTINGS_BUTTON)).click()

    def appearance_menu_item_button(self, previous_theme):
        # Returns a clickable element for the appearance menu item based on the previous theme.
        return self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@id='label' and contains(text(), 'Appearance: {previous_theme}')]")))

    def theme_option_button(self, theme_element):
        # Returns a clickable element for a theme option based on the theme_element argument.
        return self._wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//tp-yt-paper-item[@role='link' and contains(., '{theme_element}')]")))

    def switch_theme(self, theme, previous_theme="Device theme"):
        # Switches the application's theme to the specified theme.
        # Determines the theme_element based on the provided theme argument.
        theme_element = ""
        if theme == "Dark":
            theme_element = self.DARK_THEME_TEXT
        elif theme == "Light":
            theme_element = self.LIGHT_THEME_TEXT
        elif theme == "Device theme":
            theme_element = self.DEVICE_THEME_TEXT

        self.click_settings_button()

        appearance_menu_item = self.appearance_menu_item_button(previous_theme)
        appearance_menu_item.click()

        theme_option = self.theme_option_button(theme_element)
        theme_option.click()

    def is_theme_set(self, theme):
        # Checks if the specified theme is currently set.
        # Opens the settings menu to access the theme settings.
        self.click_settings_button()
        try:
            self.appearance_menu_item_button(theme)
        except TimeoutException:
            # If the timeout exception is caught, the theme has not been set correctly
            return False
        finally:
            # Close settings to return to the normal page state
            self.click_settings_button()

        return True
