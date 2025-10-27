import pytest

from config import USERNAME, PASSWORD


class TestLogin:
    invalid_credentials = [{'username': 'dummy_username', 'password': 'dummy_password'},
                           {'username': USERNAME, 'password': 'dummy_password'},
                           {'username': 'dummy_username', 'password': PASSWORD}]

    error_message = "Sorry, your password was incorrect. Please double-check your password."

    @pytest.mark.login
    @pytest.mark.parametrize("credentials", invalid_credentials)
    def test_login_guest_invalid_credentials(self, login_guest_page, credentials):
        login_guest_page.login_form.login(credentials['username'], credentials['password'])

        assert login_guest_page.is_text_present(self.error_message), f"Text not found: {self.error_message}"

    @pytest.mark.login
    @pytest.mark.parametrize("credentials", invalid_credentials)
    def test_login_invalid_credentials(self, login_accounts_page, credentials):
        login_accounts_page.login_form.login(credentials['username'], credentials['password'])

        assert login_accounts_page.is_text_present(self.error_message), f"Text not found: {self.error_message}"
