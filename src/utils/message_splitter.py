"""
Утилита для разбиения длинных сообщений на части для отправки в Telegram.
"""
from typing import List

TELEGRAM_MAX_MESSAGE_LENGTH = 4096


def split_message(text: str, max_size: int = 4090) -> list[str]:
    """
    Разделяет длинное сообщение с Markdown-разметкой на части для Telegram.

    Функция разбивает текст на чанки, размер которых не превышает max_size.
    Она отслеживает состояние блоков кода (```) и, если разрыв происходит
    внутри такого блока, корректно закрывает его в текущем чанке с помощью '```
    и заново открывает в следующем.

    Args:
        text: Входной текст с Markdown-разметкой.
        max_size: Максимальный размер одного чанка (по умолчанию 4096).

    Returns:
        Список строк (чанков), готовых к отправке.
    """
    if not text:
        return []

    chunks = []
    lines = text.split('\n')
    current_chunk = ""
    is_in_code_block = False

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Определяем, является ли строка переключателем блока кода
        is_toggler = line.strip().startswith('```')

        # Заранее резервируем место для закрывающих '```
        # если мы находимся внутри блока кода. Это 4 символа: '\n' + '```'.
        closing_tags_len = 4 if is_in_code_block else 0
        
        # Длина разделителя (перенос строки)
        separator_len = 1 if current_chunk else 0

        # Проверяем, превысит ли добавление новой строки лимит
        if len(current_chunk) + separator_len + len(line) > max_size - closing_tags_len:
            # --- Чанк заполнен, финализируем его ---
            chunk_to_add = current_chunk
            if is_in_code_block:
                chunk_to_add += '\n```'
            
            chunks.append(chunk_to_add)

            # --- Начинаем новый чанк ---
            # Если мы были в блоке кода, новый чанк должен с него начинаться
            current_chunk = '```' if is_in_code_block else ''
            
            # Используем `continue`, чтобы текущая строка обработалась заново
            # и была добавлена уже в новый чанк.
            continue

        # --- Строка помещается, добавляем ее в текущий чанк ---
        if current_chunk:
            current_chunk += '\n'
        current_chunk += line

        # После добавления строки обновляем состояние блока кода, если нужно
        if is_toggler:
            is_in_code_block = not is_in_code_block

        # Переходим к следующей строке
        i += 1

    # Добавляем последний оставшийся чанк
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
