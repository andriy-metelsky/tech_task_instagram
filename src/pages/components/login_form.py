import logging

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class LoginForm(BasePage):
    MOB_NUMBER_OR_EMAIL_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOG_IN_BUTTON = (By.XPATH, "//button[@type='submit']")
    FACEBOOK_LOG_IN_BUTTON = (By.XPATH, "//span[text()='Log in with Facebook']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot password?")
    SIGN_UP_LINK = (By.LINK_TEXT, "Sign up")

    def login(self, username: str, password: str):
        """Fill credentials and submit."""
        logging.info(f"Loging in as '{username}'")
        self.type_text(self.MOB_NUMBER_OR_EMAIL_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOG_IN_BUTTON)

