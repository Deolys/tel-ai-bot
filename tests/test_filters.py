import pytest
from src.filters.content_filter import ContentFilter


def test_content_filter_valid_message():
    filter_instance = ContentFilter()

    is_valid, message = filter_instance.validate_message("Hello, how are you?")

    assert is_valid is True
    assert message == ""


def test_content_filter_empty_message():
    filter_instance = ContentFilter()

    is_valid, message = filter_instance.validate_message("")

    assert is_valid is False
    assert "Пустое сообщение" in message


def test_content_filter_too_long_message():
    filter_instance = ContentFilter()

    long_message = "a" * 4001

    is_valid, message = filter_instance.validate_message(long_message)

    assert is_valid is False
    assert "слишком длинное" in message


def test_content_filter_profanity_detection():
    filter_instance = ContentFilter()

    profane_text = "fuck this shit"

    assert filter_instance.contains_profanity(profane_text) is True


def test_content_filter_clean_text():
    filter_instance = ContentFilter()

    clean_text = "Hello, nice to meet you!"

    assert filter_instance.contains_profanity(clean_text) is False


def test_content_filter_censor_text():
    filter_instance = ContentFilter()

    profane_text = "fuck"

    censored = filter_instance.censor_text(profane_text)

    assert "fuck" not in censored
    assert "*" in censored


def test_content_filter_response_filtering():
    filter_instance = ContentFilter()

    clean_response = "This is a clean response"
    assert filter_instance.filter_response(clean_response) == clean_response

    profane_response = "This is a fuck response"
    filtered = filter_instance.filter_response(profane_response)
    assert "fuck" not in filtered
