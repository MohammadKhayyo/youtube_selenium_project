import unittest
from infra.browser_wrapper import BrowserWrapper
from logic.youtube_page import YouTubePage


class YouTubePageTest(unittest.TestCase):
    def setUp(self):
        """Setup the test environment before each test."""
        # Initialize the browser wrapper
        self.browser = BrowserWrapper()
        # Start the browser and navigate to YouTube
        self.driver = self.browser.start_browser("https://www.youtube.com/")
        # Get the WebDriverWait instance for handling waits
        self.wait = self.browser.get_wait()
        # Initialize the YouTubePage object with the driver and wait objects
        self.youtube_page = YouTubePage(self.driver, self.wait)

    def test_search_on_youtube(self):
        """Test searching for a video on YouTube."""
        # Define the search term
        search_term = "Nature Documentary"
        # Use the YouTubePage object to perform a search
        self.youtube_page.search(search_term)
        # Verify that the search term is in the page title
        self.assertIn(search_term.lower(), self.youtube_page.get_page_title().lower(),
                      f"The search term '{search_term}' was not found in the page title.")
        # Verify that the expected video is found
        result = self.youtube_page.is_video_found()
        self.assertTrue(result, "Expected search results were not found.")

    def test_full_screen_and_exit(self):
        """Test entering and exiting full screen mode on a video."""
        # Navigate to a specific YouTube video
        self.browser.navigate("https://www.youtube.com/watch?v=JkaxUblCGz0")
        # Play the video
        self.youtube_page.play_video()
        # Enter full screen mode
        self.youtube_page.full_screen()
        # Verify that the video is in full screen mode
        self.assertTrue(self.youtube_page.is_full_screen_mode(), "Video is not in full screen mode.")
        # Exit full screen mode
        self.youtube_page.exit_full_screen()
        # Verify that the video exits full screen mode
        self.assertTrue(self.youtube_page.is_exist_full_screen_mode(), "Video did not exit full screen mode.")

    def test_mute_and_unmute_video(self):
        """Test muting and unmuting a video."""
        # Navigate to a specific YouTube video
        self.browser.navigate("https://www.youtube.com/watch?v=JkaxUblCGz0")
        # Play the video
        self.youtube_page.play_video()
        # Toggle mute and verify the video is muted
        is_muted = self.youtube_page.toggle_mute()
        self.assertTrue(is_muted, "Video is not muted.")
        # Toggle mute again and verify the video is unmuted
        is_muted = self.youtube_page.toggle_mute()
        self.assertFalse(is_muted, "Video is not unmuted.")

    def test_miniplayer_mode(self):
        """Test entering and exiting miniplayer mode."""
        # Navigate to a specific YouTube video
        self.browser.navigate("https://www.youtube.com/watch?v=JkaxUblCGz0")
        # Play the video
        self.youtube_page.play_video()
        # Enter miniplayer mode and verify
        result = self.youtube_page.use_miniplayer()
        self.assertTrue(result, "Miniplayer mode is not activated.")
        # Exit miniplayer mode and verify
        result = self.youtube_page.expand_from_miniplayer()
        self.assertTrue(result, "The video successfully toggled miniplayer mode and returned to full size.")
        self.assertTrue(result, "Video did not exit miniplayer mode.")

    def test_dark_mode(self):
        self.youtube_page.switch_theme(theme="Dark", previous_theme="Device theme")
        # Verify that the theme is set correctly
        is_theme_set = self.youtube_page.is_theme_set(theme="Dark")
        self.assertTrue(is_theme_set)

    def test_light_mode(self):
        self.youtube_page.switch_theme(theme="Light", previous_theme="Device theme")
        # Verify that the theme is set correctly
        is_theme_set = self.youtube_page.is_theme_set(theme="Light")
        self.assertTrue(is_theme_set)

    def test_dark_light_Device_mode(self):
        """3 Testes that switching between dark, light, and device theme modes."""
        # Define a list of themes to test
        themes = ["Dark", "Light", "Device theme"]
        # Iterate through the themes and switch to each one
        for i in range(len(themes)):
            self.youtube_page.switch_theme(theme=themes[i], previous_theme=themes[i - 1])
            # Verify that the theme is set correctly
            is_theme_set = self.youtube_page.is_theme_set(theme=themes[i])
            self.assertTrue(is_theme_set)

    def tearDown(self):
        """Tear down the test environment after each test."""
        # Close the browser
        self.browser.close_browser()


if __name__ == "__main__":
    unittest.main()
