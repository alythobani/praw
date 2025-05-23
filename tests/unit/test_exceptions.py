import pytest

from praw.exceptions import (
    ClientException,
    DuplicateReplaceException,
    InvalidFlairTemplateID,
    InvalidImplicitAuth,
    InvalidURL,
    MediaPostFailed,
    MissingRequiredAttributeException,
    PRAWException,
    RedditAPIException,
    RedditErrorItem,
    WebSocketException,
)


class TestClientException:
    def test_inheritance(self):
        assert issubclass(ClientException, PRAWException)

    def test_str(self):
        assert str(ClientException()) == ""
        assert str(ClientException("error message")) == "error message"


class TestDuplicateReplaceException:
    def test_inheritance(self):
        assert issubclass(DuplicateReplaceException, ClientException)

    def test_message(self):
        assert (
            str(DuplicateReplaceException())
            == "A duplicate comment has been detected. Are you attempting to call 'replace_more_comments' more than once?"
        )


class TestInvalidFlairTemplateID:
    def test_inheritance(self):
        assert issubclass(InvalidFlairTemplateID, ClientException)

    def test_str(self):
        assert (
            str(InvalidFlairTemplateID("123"))
            == "The flair template ID '123' is invalid. If you are trying to create a flair, please use the 'add' method."
        )


class TestInvalidImplicitAuth:
    def test_inheritance(self):
        assert issubclass(InvalidImplicitAuth, ClientException)

    def test_message(self):
        assert (
            str(InvalidImplicitAuth())
            == "Implicit authorization can only be used with installed apps."
        )


class TestInvalidURL:
    def test_custom_message(self):
        assert (
            str(InvalidURL("https://www.google.com", message="Test custom {}"))
            == "Test custom https://www.google.com"
        )

    def test_inheritance(self):
        assert issubclass(InvalidURL, ClientException)

    def test_message(self):
        assert (
            str(InvalidURL("https://www.google.com"))
            == "Invalid URL: https://www.google.com"
        )


class TestMediaPostFailed:
    def test_inheritance(self):
        assert issubclass(MediaPostFailed, WebSocketException)

    def test_message(self):
        assert (
            str(MediaPostFailed())
            == "The attempted media upload action has failed. Possible causes include the corruption of media files. Check that the media file can be opened on your local machine."
        )


class TestMissingRequiredAttributeException:
    def test_inheritance(self):
        assert issubclass(MissingRequiredAttributeException, ClientException)

    def test_str(self):
        assert str(MissingRequiredAttributeException()) == ""
        assert (
            str(MissingRequiredAttributeException("error message")) == "error message"
        )


class TestPRAWException:
    def test_inheritance(self):
        assert issubclass(PRAWException, Exception)

    def test_str(self):
        assert str(PRAWException()) == ""
        assert str(PRAWException("foo")) == "foo"


class TestRedditAPIException:
    def test_inheritance(self):
        assert issubclass(RedditAPIException, PRAWException)

    def test_items(self):
        container = RedditAPIException(
            [
                ["BAD_SOMETHING", "invalid something", "some_field"],
                RedditErrorItem(
                    "BAD_SOMETHING", field="some_field", message="invalid something"
                ),
            ]
        )
        for exception in container.items:
            assert isinstance(exception, RedditErrorItem)


class TestRedditErrorItem:
    def test_equality(self):
        resp = {
            "error_type": "BAD_SOMETHING",
            "field": "some_field",
            "message": "invalid something",
        }
        error = RedditErrorItem(**resp)
        error2 = RedditErrorItem(**resp)
        assert error == error2
        assert error != 0

    def test_hash(self):
        resp = {
            "error_type": "BAD_SOMETHING",
            "field": "some_field",
            "message": "invalid something",
        }
        error = RedditErrorItem(**resp)
        error2 = RedditErrorItem(**resp)
        assert hash(error) == hash(error2)

    def test_property(self):
        error = RedditErrorItem(
            "BAD_SOMETHING", field="some_field", message="invalid something"
        )
        assert (
            error.error_message
            == "BAD_SOMETHING: 'invalid something' on field 'some_field'"
        )

    def test_repr(self):
        error = RedditErrorItem(
            "BAD_SOMETHING", field="some_field", message="invalid something"
        )
        assert (
            repr(error)
            == "RedditErrorItem(error_type='BAD_SOMETHING', message='invalid something', field='some_field')"
        )

    def test_str(self):
        error = RedditErrorItem(
            "BAD_SOMETHING", field="some_field", message="invalid something"
        )
        assert str(error) == "BAD_SOMETHING: 'invalid something' on field 'some_field'"


class TestWebSocketException:
    def test_inheritance(self):
        assert issubclass(WebSocketException, ClientException)

    def test_str(self):
        assert str(WebSocketException("")) == ""
        assert str(WebSocketException("error message")) == "error message"
