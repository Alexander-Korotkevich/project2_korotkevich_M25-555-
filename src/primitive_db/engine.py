import shlex
from src.primitive_db.utils import load_metadata, save_metadata
import prompt
import src.primitive_db.constants as const


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

    while is_active:
        metadata = load_metadata("./db_meta.json")
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)

        match (args[0]):
            case const.CMD_CREATE_TABLE:
                pass
            case const.CMD_LIST_TABLES:
                pass
            case const.CMD_DROP_TABLE:
                pass
            case const.CMD_EXIT:
                is_active = exit()
                continue
            case const.CMD_HELP:
                print_help()
                continue
