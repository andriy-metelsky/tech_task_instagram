import logging

from selenium.webdriver.common.by import By

from config import BASE_URL
from src.dto.user_account_dto import UserAccountDto
from src.pages.base_page import BasePage


class SignupPage(BasePage):
    EMAIL_OR_PHONE_INPUT = (By.NAME, "emailOrPhone")
    FULL_NAME_INPUT = (By.NAME, "fullName")
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    NEXT_BUTTON = (By.XPATH, "//button[@type='submit']")
    FACEBOOK_LOG_IN_BUTTON = (By.XPATH, "//span[text()='Log in with Facebook']")
    LOG_IN_LINK = (By.LINK_TEXT, "Log in")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{BASE_URL}/accounts/emailsignup/"

    def fill_in_sign_up_form(self, user_account: UserAccountDto):
        """Fill the sign-up form fields."""
        logging.info("Filling sign-up form.")
        if user_account.mobile_number:
            logging.debug(f"Typing mobile number: '{user_account.mobile_number}'")
            self.type_text(self.EMAIL_OR_PHONE_INPUT, user_account.mobile_number)
        if user_account.email:
            logging.debug(f"Typing email: {user_account.email}")
            self.type_text(self.EMAIL_OR_PHONE_INPUT, user_account.email)
        if user_account.password:
            logging.debug(f"Typing password: {user_account.password}")  # could be masked if needed
            self.type_text(self.PASSWORD_INPUT, user_account.password)
        if user_account.full_name:
            logging.debug(f"Typing full name: {user_account.full_name}")
            self.type_text(self.FULL_NAME_INPUT, user_account.full_name)
        if user_account.username:
            logging.debug(f"Typing username: {user_account.username}")
            self.type_text(self.USERNAME_INPUT, user_account.username)

    def click_next(self):
        """Click the Next button to submit sign-up form."""
        logging.info("Clicking Next button.")
        self.click(self.NEXT_BUTTON)
