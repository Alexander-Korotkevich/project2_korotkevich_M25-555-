from typing import List

from src.decorators import handle_db_errors
from src.primitive_db.constants import (
    COLUMN_DEFINE_SEP,
    COMPLEX_CMD,
    KEY_WORD_SET,
    KEY_WORD_VALUES,
    KEY_WORD_WHERE,
)
from src.primitive_db.types import ColumnType
from src.primitive_db.utils import convert_value


@handle_db_errors
def parse_set_condition(clause: str):
    clause = clause.split(KEY_WORD_WHERE)

    if len(clause) != 2:
        raise ValueError("Неверный формат условия")

    clause = clause[0].strip()

    return parse_key_word_condition(clause, KEY_WORD_SET)


@handle_db_errors
def parse_key_word_condition(clause: str, key_word: str):
    """Парсит условие по ключевому слову"""

    clause = clause.split(key_word)
    if len(clause) != 2:
        return

    clause = clause[1].strip()

    # Разделяем по оператору =
    if "=" not in clause:
        raise ValueError("Не найден оператор = в условии")

    parts = clause.split("=", 1)
    if len(parts) != 2:
        raise ValueError("Неверный формат условия")

    column = parts[0].strip()
    value_str = parts[1].strip()

    value = convert_value(value_str)

    return {"column": column, "value": value}


def parse_values(content):
    """Парсит список значений, разделенных запятыми"""
    if not content:
        return []

    values = []
    current = []
    in_string = False
    quote_char = None

    for char in content:
        if char in ("'", '"') and not in_string:
            # Начало строки
            in_string = True
            quote_char = char
            current.append(char)
        elif char == quote_char and in_string:
            # Конец строки
            in_string = False
            current.append(char)
        elif char == "," and not in_string:
            # Конец значения
            value_str = "".join(current).strip()
            if value_str:
                values.append(convert_value(value_str))
            current = []
        else:
            current.append(char)

    # Обрабатываем последнее значение
    if current:
        value_str = "".join(current).strip()
        if value_str:
            values.append(convert_value(value_str))

    return values


@handle_db_errors
def parse_insert(query):
    # Находим VALUES и скобки
    sql_lower = query.lower()
    values_idx = sql_lower.find(KEY_WORD_VALUES)
    if values_idx == -1:
        raise ValueError("Неверный формат запроса")

    # Ищем скобки с значениями
    open_bracket = query.find("(", values_idx)
    close_bracket = query.rfind(")")

    if open_bracket == -1 or close_bracket == -1:
        raise ValueError("Неверный формат запроса")

    # Извлекаем содержимое скобок
    content = query[open_bracket + 1 : close_bracket].strip()

    return parse_values(content)


@handle_db_errors
def parse_table_columns(list: List[str]) -> List[ColumnType] | str:
    """Получение колонок из списка аргументов"""

    if len(list) < 3:
        return []

    columns = list[2:]

    parsed_columns: List[ColumnType] = []

    for i, column in enumerate(columns):
        splitted = column.split(COLUMN_DEFINE_SEP)

        if len(splitted) != 2:
            raise ValueError("Неверный формат колонки")

        parsed_columns.append({"name": splitted[0], "type": splitted[1]})

    return parsed_columns


def parse_table_name(list: List[str], command: str) -> str | None:
    """Получение названия таблицы из списка аргументов"""
    length = len(list)
    if length < 2:
        return

    # В случае комплексной команды ищем 3-ий аргумент
    if command in COMPLEX_CMD:
        return None if length < 3 else list[2]

    return list[1]
