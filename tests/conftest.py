import pytest
from selenium import webdriver

from config import EMAIL, PASSWORD
from src.pages.home_page import HomePage
from src.pages.login_accounts_page import LoginAccountsPage
from src.pages.login_guest_page import LoginGuestPage
from src.pages.signup_page import SignupPage


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login_guest_page(driver):
    login_guest_page = LoginGuestPage(driver)
    login_guest_page.open()
    login_guest_page.allow_cookies_if_present()
    yield login_guest_page


@pytest.fixture
def login_accounts_page(driver):
    login_accounts_page = LoginAccountsPage(driver)
    login_accounts_page.open()
    login_accounts_page.allow_cookies_if_present()
    yield login_accounts_page


@pytest.fixture
def signup_page(driver):
    signup_page = SignupPage(driver)
    signup_page.open()
    signup_page.allow_cookies_if_present()
    yield signup_page


@pytest.fixture
def home_page(driver):
    login_accounts_page = LoginAccountsPage(driver)
    login_accounts_page.open()
    login_accounts_page.allow_cookies_if_present()
    login_accounts_page.login_form.login(EMAIL, PASSWORD)
    login_accounts_page.wait_for_load_spinner()
    home_page = HomePage(driver)
    home_page.skip_saving_login_info_if_present()
    yield home_page

