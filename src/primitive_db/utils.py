import json
from typing import List

from src.primitive_db.constants import COLUMN_DEFINE_SEP
from src.primitive_db.types import ColumnType, MetadataType


def load_metadata(filepath: str) -> MetadataType | None:
    """Загрузка данных из файла"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def save_metadata(filepath: str, data: MetadataType) -> bool:
    """Сохранение данных в файл"""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False


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

        if len(splitted) != 2 or (COLUMN_DEFINE_SEP not in splitted):
            incorrect_value(column)
            return None

        parsed_columns.append({"name": splitted[0], "type": splitted[1]})

    return parsed_columns
