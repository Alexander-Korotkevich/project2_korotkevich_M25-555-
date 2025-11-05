from typing import List

from prettytable import PrettyTable

from src.primitive_db.constants import (
    DATA_TYPES,
    ID_COL_DATA,
    ID_COL_NAME,
)
from src.primitive_db.types import ColumnType, MetadataType, TableType
from src.primitive_db.utils import check_val_type, delete_table, save_table_data


def create_table(
    metadata: MetadataType, table_name: str, columns: List[ColumnType]
) -> MetadataType:
    """Создание таблицы"""

    if metadata.get(table_name):
        print(f'Ошибка: Таблица "{table_name}" уже существует')
        return

    if any(column.get("type") not in DATA_TYPES for column in columns):
        print("Ошибка: Некорректный тип данных")
        return

    # Добавляем колонку ID, если она не была указана пользователем
    if ID_COL_NAME not in columns:
        columns.insert(0, ID_COL_DATA)

    # Обновляем metadata
    metadata[table_name] = columns

    columns_str = ", ".join(
        f"{column.get('name')}:{column.get('type')}" for column in columns
    )

    # Сохраняем таблицу
    is_success = save_table_data(
        table_name, {"name": table_name, "columns": columns, "rows": []}
    )

    if is_success:
        print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    else:
        del metadata[table_name]

    return metadata


def drop_table(metadata: MetadataType, table_name: str) -> MetadataType:
    """Удаление таблицы"""

    if not metadata.get(table_name):
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    del metadata[table_name]
    delete_table(table_name)

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def list_tables(metadata: MetadataType):
    """Получение списка таблиц"""

    tables = list(metadata.keys())
    title = "Список таблиц:\n"
    tables_list = ",\n".join(f"{table}" for table in tables)

    print(title + (tables_list or "пусто"))


def insert(tabledata: TableType, values: List[str | int | bool]):
    """Создание новой записи в таблицу"""

    columns = tabledata.get("columns")
    col_without_id = list(filter(lambda x: x.get("name") != ID_COL_NAME, columns))
    rows = tabledata.get("rows")

    if len(values) != (len(col_without_id)):
        print("Ошибка: Некорректное количество значений")
        return

    row = {ID_COL_NAME: len(rows) + 1}

    for i, val in enumerate(values):
        column_type = col_without_id[i].get("type")
        column_name = col_without_id[i].get("name")

        if check_val_type(val, column_type) is False:
            print(f'Ошибка: Значение {val} не соответствует типу "{column_type}"')
            return

        row[column_name] = val

    tabledata["rows"].append(row)

    print(
        f'Запись с ID={row.get(ID_COL_NAME)} успешно добавлена в таблицу "{tabledata.get("name")}".'  # noqa: E501
    )

    return tabledata


def select(table_data: TableType, where_clause=None):
    columns_names = [column.get("name") for column in table_data.get("columns")]
    rows = table_data.get("rows")

    if where_clause:
        rows = [
            row
            for row in rows
            if row.get(where_clause.get("column")) == where_clause.get("value")
        ]

    table = PrettyTable()

    table.field_names = columns_names

    for row in rows:
        table.add_row([row.get(column) for column in columns_names])

    print(table)


def update(tabledata: TableType, set_clause, where_clause):
    rows = tabledata.get("rows")

    for row in rows:
        if row.get(where_clause.get("column")) == where_clause.get("value"):
            row[set_clause.get("column")] = set_clause.get("value")
            print(
                f'Запись с ID={row.get(ID_COL_NAME)} в таблице "{tabledata.get("name")}" успешно обновлена.'  # noqa: E501
            )
            return tabledata

    print("Запись не найдена")


def delete(tabledata: TableType, where_clause):
    rows = tabledata.get("rows")

    for row in rows:
        if row.get(where_clause.get("column")) == where_clause.get("value"):
            rows.remove(row)
            print(
                f'Запись с ID={row.get(ID_COL_NAME)} в таблице "{tabledata.get("name")}" успешно удалена.'  # noqa: E501
            )

            return tabledata

    print("Запись не найдена")


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись."  # noqa: E501
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию."  # noqa: E501
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись."  # noqa: E501
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись."  # noqa: E501
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def exit() -> bool:
    """Выход из программы"""

    print("Программа завершена")
    return False
