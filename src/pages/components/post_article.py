from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class PostArticle(BasePage):
    POST_ARTICLE_BY_INDEX = "//article[{}]"
    LIKE_BUTTON = POST_ARTICLE_BY_INDEX + "//*[@aria-label='Like']//ancestor::div[@role='button']"
    UNLIKE_BUTTON = POST_ARTICLE_BY_INDEX + "//*[@aria-label='Unlike']//ancestor::div[@role='button']"
    COMMENT_BUTTON = POST_ARTICLE_BY_INDEX + "//*[@aria-label='Comment']//ancestor::div[@role='button']"
    SHARE_BUTTON = POST_ARTICLE_BY_INDEX + "//*[@aria-label='Share']//ancestor::div[@role='button']"
    SAVE_BUTTON = POST_ARTICLE_BY_INDEX + "//*[@aria-label='Save']//ancestor::div[@role='button']"
    ADD_COMMENT_INPUT = POST_ARTICLE_BY_INDEX + "//textarea[@placeholder='Add a comment…']"
    POST_COMMENT = POST_ARTICLE_BY_INDEX + "//div[@role='button' and text()='Post']"
    COMMENT_RECORD = POST_ARTICLE_BY_INDEX + "//ul//span[normalize-space(.)='{}']"

    def __init__(self, driver, index: int = 0):
        super().__init__(driver)
        self.index = index

    def inner_locator_builder(self, pattern: str, *args) -> tuple[str, str]:
        """
        Build a fresh By.XPATH locator for an element inside this post.
        Usage: self.inner_locator(self.LIKE_BUTTON)
               self.inner_locator(self.COMMENT_RECORD, "nice!")
        """
        return By.XPATH, pattern.format(self.index + 1, *args)

    def like(self, set_liked: bool = True):
        """Like or unlike the post depending on `set_liked`."""
        if set_liked and not self.is_liked():
            self._complex_click(self.inner_locator_builder(self.LIKE_BUTTON))
        elif not set_liked and self.is_liked():
            self._complex_click(self.inner_locator_builder(self.UNLIKE_BUTTON))

    def _complex_click(self, locator):
        """Scroll, hover and safely click an element by locator."""
        element = self.find_element(locator)
        self.scroll_to_web_element(element)
        self.hover(element)
        self.safe_click(locator)

    def is_liked(self) -> bool:
        """Return True if post is currently liked, else False."""
        return self.is_visible(self.inner_locator_builder(self.UNLIKE_BUTTON))

    def save(self):
        """Save (bookmark) the post."""
        self._complex_click(self.inner_locator_builder(self.SAVE_BUTTON))

    def add_comment(self, comment: str):
        """Add a comment to the post."""
        self.type_text(self.inner_locator_builder(self.ADD_COMMENT_INPUT), comment)
        self.safe_click(self.inner_locator_builder(self.POST_COMMENT))

    def open_comments(self):
        """Open the comment thread for this post."""
        self.safe_click(self.inner_locator_builder(self.COMMENT_BUTTON))

    def has_comment(self, text: str) -> bool:
        """Return True if a comment with given text is visible in the post."""
        return self.is_visible(self.inner_locator_builder(self.COMMENT_RECORD, text))
