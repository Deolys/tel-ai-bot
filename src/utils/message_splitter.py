"""
Утилита для разбиения длинных сообщений на части для отправки в Telegram.
"""
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
        
        is_toggler = line.strip().startswith('```')

        closing_tags_len = 4 if is_in_code_block else 0
        
        separator_len = 1 if current_chunk else 0

        if len(current_chunk) + separator_len + len(line) > max_size - closing_tags_len:
            chunk_to_add = current_chunk
            if is_in_code_block:
                chunk_to_add += '\n```'
            
            chunks.append(chunk_to_add)

            current_chunk = '```' if is_in_code_block else ''
            
            continue

        if current_chunk:
            current_chunk += '\n'
        current_chunk += line

        if is_toggler:
            is_in_code_block = not is_in_code_block

        i += 1

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
