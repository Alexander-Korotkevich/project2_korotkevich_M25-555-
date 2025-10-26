from typing import List

from src.primitive_db.constants import DATA_TYPES, ID_COLUMN_DATA, ID_COLUMN_NAME
from src.primitive_db.types import ColumnType, MetadataType


def create_table(
    metadata: MetadataType, table_name: str, columns: List[ColumnType]
) -> MetadataType:
    """Создание таблицы"""

    if metadata.get(table_name):
        print(f'Ошибка: Таблица "{table_name}" уже существует')
        return

    if any(column.type not in DATA_TYPES for column in columns):
        print("Ошибка: Некорректный тип данных")
        return

    # Добавляем колонку ID, если она не была указана пользователем
    if ID_COLUMN_NAME not in columns:
        columns.insert(0, ID_COLUMN_DATA)

    # Обновляем metadata
    metadata[table_name] = columns

    columns_str = ", ".join(
        f"{column.get('name')}:{column.get('type')}" for column in columns
    )
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')

    return metadata


def drop_table(metadata: MetadataType, table_name: str) -> MetadataType:
    """Удаление таблицы"""

    if not metadata.get(table_name):
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def list_tables(metadata: MetadataType):
    """Получение списка таблиц"""

    tables = list(metadata.keys())
    title = "Список таблиц:\n"
    tables_list = ",\n".join(f"{table}" for table in tables)

    print(title + (tables_list or "пусто"))
