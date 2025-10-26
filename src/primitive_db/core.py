from src.primitive_db.constants import DATA_TYPES, ID_COLUMN


def create_table(metadata, table_name: str, columns):
    """Создание таблицы"""

    if metadata.get(table_name):
        print(f'Ошибка: Таблица "{table_name}" уже существует')
        return

    if any(column.type not in DATA_TYPES for column in columns):
        print("Ошибка: Некорректный тип данных")
        return

    # Добавляем первую колонку по-умолчанию
    columns.insert(0, ID_COLUMN)

    # Обновляем metadata
    metadata[table_name] = columns

    columns_str = ", ".join(
        f"{column.get('name')}:{column.get('type')}" for column in columns
    )
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')

    return metadata


def drop_table(metadata, table_name: str):
    if not metadata.get(table_name):
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata
