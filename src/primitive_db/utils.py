import json
import os.path
from typing import Any, Dict, List

from src.primitive_db.constants import (
    COLUMN_DEFINE_SEP,
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
        return None


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


def parse_table_name(list: List[str]) -> str | None:
    """Получение названия таблицы из списка аргументов"""

    if len(list) < 2:
        return None

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
            return None

        parsed_columns.append({"name": splitted[0], "type": splitted[1]})

    return parsed_columns
