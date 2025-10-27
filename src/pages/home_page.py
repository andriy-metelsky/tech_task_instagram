import logging

from selenium.webdriver.common.by import By

from config import USERNAME
from src.pages.base_page import BasePage
from src.pages.components.post_article import PostArticle


class HomePage(BasePage):
    POST_ARTICLE = (By.XPATH, "//article")
    USER_PROFILE_LINK = (By.LINK_TEXT, USERNAME)

    def open_user_profile_page(self):
        """Open the current user's profile page."""
        logging.info(f"Opening user profile link for {USERNAME}")
        self.click(self.USER_PROFILE_LINK)

    def get_post_by_index(self, index=0) -> PostArticle:
        """Return a PostArticle component at the given index in the feed."""
        return PostArticle(self.driver, index)
