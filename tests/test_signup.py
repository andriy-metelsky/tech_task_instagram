import time

import pytest

from src.dto.user_account_dto import UserAccountDto


class TestSignup:
    @pytest.mark.signup
    def test_signup_invalid_email(self, signup_page):

        user = UserAccountDto(email="test_email@gmail")
        error_message = "Enter a valid email address."

        signup_page.fill_in_sign_up_form(user)
        signup_page.click_next()

        assert signup_page.is_text_present(error_message), f"Text not found: {error_message}"
