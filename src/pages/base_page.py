import logging

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import BASE_URL


class BasePage:
    INSTA_LOGO = (By.XPATH, "//*[@aria-label='Instagram']")
    ALLOW_COOKIES_BUTTON = (By.XPATH, "//button[text()='Allow all cookies']")
    LOGIN_INFO_NOT_NOW = (By.XPATH, "//div[@role='button' and text()='Not now']")
    LOAD_SPINNER = (By.XPATH, "//*[@role='progressbar']")

    def __init__(self, driver):
        self.driver = driver
        self.url = BASE_URL
        self.timeout = 10
        self.max_retries = 3
        self.wait = WebDriverWait(driver, self.timeout)

    def open(self):
        """Navigate to the URL."""
        logging.info(f"Opening URL: {self.url}")
        self.driver.get(self.url)

    def wait_for_load_spinner(self):
        """Wait until the loading spinner is not visible."""
        logging.debug("Waiting for load spinner to disappear")
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_SPINNER))
        except Exception as e:
            logging.exception(f"Spinner did not disappear within the timeout: {e}")

    def find_element(self, locator):
        """Find a single element with explicit wait."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Find all elements with explicit wait."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def safe_click(self, locator):
        """ Clicks on an element identified by the locator."""
        logging.info(f"Clicking element: {locator}")
        for attempt in range(self.max_retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                break
            except StaleElementReferenceException:
                logging.exception(f"StaleElementReferenceException occurred, retrying... (Attempt {attempt + 1})")
        else:
            logging.error("Failed to interact with element after multiple retries.")

    def click(self, locator):
        """ Clicks on an element identified by the locator."""
        logging.info(f"Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text: str, clear: bool = True, click_first: bool = True):
        """
        Types text into an input field identified by the locator.
        """
        logging.info(f"Typing text '{text}' into {locator}")
        for attempt in range(self.max_retries):
            try:
                element = self.wait.until(EC.visibility_of_element_located(locator))
                self.scroll_to_web_element(element)
                if click_first:
                    element.click()
                if clear:
                    element.clear()
                element.send_keys(text)
                break
            except StaleElementReferenceException:
                logging.exception(f"StaleElementReferenceException occurred, retrying... (Attempt {attempt + 1})")
        else:
            logging.error("Failed to interact with element after multiple retries.")

    def allow_cookies_if_present(self):
        try:
            self.click(self.ALLOW_COOKIES_BUTTON)
        except NoSuchElementException:
            pass

    def skip_saving_login_info_if_present(self):
        try:
            self.click(self.LOGIN_INFO_NOT_NOW)
        except NoSuchElementException:
            pass
        self.wait.until(EC.visibility_of_element_located(self.INSTA_LOGO))

    def is_text_present(self, text: str) -> bool:
        """
        Check if given text is present anywhere in the page source/visible DOM.
        Returns True if found within timeout, else False.
        """
        logging.info(f"Checking if text is present: '{text}'")
        try:
            self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "//*"), text))
            return True
        except TimeoutException:
            return False

    def scroll_to_locator(self, locator):
        """Scroll a locator into view."""
        logging.info(f"Scrolling to element by locator: {locator}")
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return element

    def scroll_to_web_element(self, element):
        """Scroll a WebElement into view."""
        logging.info(f"Scrolling to WebElement: {element}")
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return element

    def hover(self, element):
        """Hover over a WebElement."""
        logging.info(f"Hovering over element: {element}")
        ActionChains(self.driver).move_to_element(element).perform()
        return element

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        url = self.driver.current_url
        logging.info(f"Current URL: {url}")
        return url

    def is_visible(self, locator):
        """Return True if the element is visible within the timeout."""
        logging.info(f"Checking visibility of: {locator}")
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
