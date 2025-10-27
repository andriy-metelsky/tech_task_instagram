from config import BASE_URL
from src.pages.base_page import BasePage
from src.pages.components.login_form import LoginForm


class LoginGuestPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = BASE_URL
        self.login_form = LoginForm(driver)
