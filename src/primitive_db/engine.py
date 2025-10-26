import shlex

import prompt

import src.primitive_db.constants as const
import src.primitive_db.core as core
import src.primitive_db.utils as utils


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def exit() -> bool:
    """Выход из программы"""

    print("Программа завершена")
    return False


def run():
    is_active = True

    # Показываем команды при запуске
    print_help()

    while is_active:
        changed_data = None
        metadata = utils.load_metadata(const.METADATA_PATH)
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        command = args[0]
        table_name = utils.parse_table_name(args)

        if not table_name and (
            command in [const.CMD_CREATE_TABLE, const.CMD_DROP_TABLE]
        ):
            print("Укажите название таблицы.")
            continue

        match (command):
            case const.CMD_CREATE_TABLE:
                columns = utils.parse_table_columns(args)
                if columns is None:
                    continue

                changed_data = core.create_table(metadata, table_name, columns)
            case const.CMD_DROP_TABLE:
                changed_data = core.drop_table(metadata, table_name)
            case const.CMD_LIST_TABLES:
                core.list_tables(metadata)
                continue
            case const.CMD_EXIT:
                is_active = exit()
                continue
            case const.CMD_HELP:
                print_help()
                continue
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")
                continue

        if changed_data:
            utils.save_metadata(const.METADATA_PATH, changed_data)
