import pytest

from src.utils import utils


class TestHomePage:

    @pytest.mark.post_feed
    def test_like_unlike_post(self, home_page):
        post = home_page.get_post_by_index(0)

        post.like(set_liked=False)
        assert not post.is_liked(), "Post is expected to be unliked"

        post.like(set_liked=True)
        assert post.is_liked(), "Post is expected to be liked"

    @pytest.mark.post_feed
    def test_add_comment(self, home_page):
        test_comment = f"Test comment {utils.get_random_string('letters', 12)}"
        post = home_page.get_post_by_index(0)

        post.add_comment(test_comment)
        assert post.has_comment(test_comment), f"Comment '{test_comment}' is not present in the list"
