import json
import os.path
from typing import Any, Dict, List

from src.primitive_db.constants import (
    COLUMN_DEFINE_SEP,
    COMPLEX_CMD,
    KEY_WORD_VALUES,
    METADATA_NAME,
    TABLES_DIR,
)
from src.primitive_db.types import ColumnType, MetadataType, TableType

# Путь относительно файла скрипта
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
META_PATH = os.path.join(SCRIPT_DIR, METADATA_NAME)


def load_from_file(filepath: str) -> Dict | None:
    """Загрузка данных из файла"""

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


def save_to_file(filepath: str, data: Any):
    """Сохранение данных в файл"""

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False


def load_metadata() -> MetadataType | None:
    """Загрузка метаданных"""

    return load_from_file(META_PATH)


def save_metadata(data: MetadataType) -> bool:
    """Сохранение метаданных"""

    return save_to_file(META_PATH, data)


def load_table_data(table_name: str) -> TableType | None:
    """Загрузка данных таблицы"""

    path = os.path.join(SCRIPT_DIR, TABLES_DIR, table_name)

    return load_from_file(path)


def save_table_data(table_name: str, data: TableType) -> bool:
    """Сохранение данных таблицы"""

    path = os.path.join(SCRIPT_DIR, TABLES_DIR, table_name)

    return save_to_file(path, data)


def delete_table(table_name: str):
    """Удаление файла таблицы"""

    path = os.path.join(SCRIPT_DIR, TABLES_DIR, table_name)
    os.remove(path)


def parse_table_name(list: List[str], command: str) -> str | None:
    """Получение названия таблицы из списка аргументов"""
    length = len(list)
    if length < 2:
        return

    # В случае комплексной команды ищем 3-ий аргумент
    if command in COMPLEX_CMD:
        return None if length < 3 else list[2]

    return list[1]


def incorrect_value(value: str):
    print(f"Некорректное значение: {value}. Попробуйте снова.")


def parse_table_columns(list: List[str]) -> List[ColumnType] | str:
    """Получение колонок из списка аргументов"""

    if len(list) < 3:
        return []

    columns = list[2:]

    parsed_columns: List[ColumnType] = []

    for i, column in enumerate(columns):
        splitted = column.split(COLUMN_DEFINE_SEP)

        if len(splitted) != 2:
            incorrect_value(column)
            return

        parsed_columns.append({"name": splitted[0], "type": splitted[1]})

    return parsed_columns


def parse_insert(query):
    # Находим VALUES и скобки
    sql_lower = query.lower()
    values_idx = sql_lower.find(KEY_WORD_VALUES)
    if values_idx == -1:
       incorrect_value(query)
       return

    # Ищем скобки с значениями
    open_bracket = query.find("(", values_idx)
    close_bracket = query.rfind(")")

    if open_bracket == -1 or close_bracket == -1:
       incorrect_value(query)
       return

    # Извлекаем содержимое скобок
    content = query[open_bracket + 1 : close_bracket].strip()

    return parse_values(content)


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


def convert_value(value_str):
    """Конвертирует строку в int, str или bool"""
    value_str = value_str.strip()

    # Булевы значения
    if value_str.upper() == "TRUE":
        return True
    if value_str.upper() == "FALSE":
        return False

    # Строки в кавычках
    if (value_str.startswith("'") and value_str.endswith("'")) or (
        value_str.startswith('"') and value_str.endswith('"')
    ):
        return value_str[1:-1]  # Убираем кавычки

    # Целые числа
    if value_str.isdigit() or (value_str.startswith("-") and value_str[1:].isdigit()):
        return int(value_str)

    # Если ничего не подошло - возвращаем как строку (без кавычек)
    return value_str

def check_val_type(val: Any, col_type: str):
    if col_type == "str":
        return isinstance(val, str)
    if col_type == "int":
        return type(val) is int
    if col_type == "bool":
        return isinstance(val, bool)
