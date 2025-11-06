import json
import os.path
from typing import Any, Dict

from src.decorators import handle_db_errors
from src.primitive_db.constants import (
    METADATA_NAME,
    TABLES_DIR,
)
from src.primitive_db.types import MetadataType, TableType

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


@handle_db_errors
def save_to_file(filepath: str, data: Any):
    """Сохранение данных в файл"""

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
        return True


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


@handle_db_errors
def delete_table(table_name: str):
    """Удаление файла таблицы"""

    path = os.path.join(SCRIPT_DIR, TABLES_DIR, table_name)
    os.remove(path)


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
    """Проверяет соответствие значения типу колонки"""

    if col_type == "str":
        return isinstance(val, str)
    if col_type == "int":
        return type(val) is int
    if col_type == "bool":
        return isinstance(val, bool)


def create_cacher():
    cache = {}

    def cache_result(key, value_func):

        if key in cache:
            return cache[key]
        value = value_func()
        cache[key] = value
        return value

    return cache_result
