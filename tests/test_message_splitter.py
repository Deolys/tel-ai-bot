"""
Тесты для утилиты разбиения сообщений.
"""
import pytest
from src.utils.message_splitter import split_message, TELEGRAM_MAX_MESSAGE_LENGTH


def test_split_message_short_text():
    """Короткий текст не должен разбиваться"""
    text = "Короткое сообщение"
    result = split_message(text)
    assert len(result) == 1
    assert result[0] == text


def test_split_message_exact_limit():
    """Текст ровно на границе лимита не должен разбиваться"""
    text = "a" * TELEGRAM_MAX_MESSAGE_LENGTH
    result = split_message(text)
    assert len(result) == 1


def test_split_message_over_limit():
    """Текст превышающий лимит должен разбиваться"""
    text = "a" * (TELEGRAM_MAX_MESSAGE_LENGTH + 100)
    result = split_message(text)
    assert len(result) > 1
    for part in result:
        assert len(part) <= TELEGRAM_MAX_MESSAGE_LENGTH


def test_split_message_by_paragraphs():
    """Разбиение должно происходить по абзацам"""
    paragraph1 = "Первый абзац. " * 500
    paragraph2 = "Второй абзац. " * 500
    text = paragraph1 + "\n\n" + paragraph2
    
    result = split_message(text)
    assert len(result) >= 2
    for part in result:
        assert len(part) <= TELEGRAM_MAX_MESSAGE_LENGTH


def test_split_message_by_sentences():
    """Разбиение длинного абзаца должно происходить по предложениям"""
    long_paragraph = "Это предложение. " * 1000
    
    result = split_message(long_paragraph)
    assert len(result) > 1
    for part in result:
        assert len(part) <= TELEGRAM_MAX_MESSAGE_LENGTH


def test_split_message_by_words():
    """Очень длинное предложение должно разбиваться по словам"""
    long_sentence = "слово " * 2000
    
    result = split_message(long_sentence)
    assert len(result) > 1
    for part in result:
        assert len(part) <= TELEGRAM_MAX_MESSAGE_LENGTH


def test_split_message_custom_max_length():
    """Проверка работы с кастомной максимальной длиной"""
    text = "a" * 200
    max_length = 50
    
    result = split_message(text, max_length)
    assert len(result) == 4
    for part in result:
        assert len(part) <= max_length


def test_split_message_preserves_content():
    """Проверка что весь контент сохраняется после разбиения"""
    text = "Тестовое сообщение. " * 500
    
    result = split_message(text)
    
    for part in result:
        assert len(part) > 0
        assert len(part) <= TELEGRAM_MAX_MESSAGE_LENGTH
    
    combined = " ".join(result)
    assert "Тестовое сообщение" in combined
    
    original_count = text.count("Тестовое сообщение")
    combined_count = combined.count("Тестовое сообщение")
    assert abs(original_count - combined_count) <= 5


def test_split_message_empty_text():
    """Пустой текст должен вернуть список с одной пустой строкой"""
    text = ""
    result = split_message(text)
    assert len(result) == 1
    assert result[0] == ""


def test_split_message_real_world_example():
    """Реальный пример длинного ответа AI"""
    text = """# Введение в Python

Python - это высокоуровневый язык программирования общего назначения.

## Основные особенности

1. Простой и понятный синтаксис
2. Динамическая типизация
3. Автоматическое управление памятью
4. Богатая стандартная библиотека

## Примеры использования

Python используется в различных областях:
- Веб-разработка
- Анализ данных
- Машинное обучение
- Автоматизация

""" * 100
    
    result = split_message(text)
    
    assert len(result) > 1
    
    for part in result:
        assert len(part) <= TELEGRAM_MAX_MESSAGE_LENGTH
    
    assert "Введение в Python" in result[0]
