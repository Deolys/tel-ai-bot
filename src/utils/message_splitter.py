"""
Утилита для разбиения длинных сообщений на части для отправки в Telegram.
"""
from typing import List

TELEGRAM_MAX_MESSAGE_LENGTH = 4096


def split_message(text: str, max_length: int = TELEGRAM_MAX_MESSAGE_LENGTH) -> List[str]:
    """
    Разбивает длинное сообщение на части, не превышающие максимальную длину.
    Старается разбивать по абзацам и предложениям для сохранения читабельности.
    
    Args:
        text: Текст для разбиения
        max_length: Максимальная длина одной части (по умолчанию 4096 для Telegram)
    
    Returns:
        Список строк, каждая не превышает max_length
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        if len(paragraph) > max_length:
            sentences = paragraph.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
            
            for sentence in sentences:
                if len(sentence) > max_length:
                    words = sentence.split(' ') if ' ' in sentence else []
                    
                    if words:
                        temp_sentence = ""
                        for word in words:
                            if len(temp_sentence) + len(word) + 1 <= max_length:
                                temp_sentence += (word + ' ')
                            else:
                                if temp_sentence:
                                    chunks.append(temp_sentence.rstrip())
                                if len(word) > max_length:
                                    for i in range(0, len(word), max_length):
                                        chunks.append(word[i:i + max_length])
                                    temp_sentence = ""
                                else:
                                    temp_sentence = word + ' '
                        
                        if temp_sentence:
                            if current_chunk and len(current_chunk) + len(temp_sentence) <= max_length:
                                current_chunk += temp_sentence
                            else:
                                if current_chunk:
                                    chunks.append(current_chunk.rstrip())
                                current_chunk = temp_sentence
                    else:
                        for i in range(0, len(sentence), max_length):
                            chunks.append(sentence[i:i + max_length])
                else:
                    if current_chunk and len(current_chunk) + len(sentence) + 1 <= max_length:
                        current_chunk += (sentence + ' ')
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.rstrip())
                        current_chunk = sentence + ' '
        else:
            if current_chunk and len(current_chunk) + len(paragraph) + 2 <= max_length:
                current_chunk += (paragraph + '\n\n')
            else:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                current_chunk = paragraph + '\n\n'
    
    if current_chunk:
        chunks.append(current_chunk.rstrip())
    
    return chunks
