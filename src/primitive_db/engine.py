import shlex

import prompt

import src.primitive_db.constants as const
import src.primitive_db.core as core
import src.primitive_db.utils as utils


def run():
    is_active = True

    # Показываем команды при запуске
    core.print_help()

    while is_active:
        changed_metadata = None
        changed_tabledata = None
        metadata = utils.load_metadata()
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        print(args)
        return
        command = args[0]
        table_name = utils.parse_table_name(args, command)

        if not table_name and (command in const.NEEDED_TABLE_NAME):
            print("Укажите название таблицы.")
            continue

        tabledata = (
            utils.load_table_data(table_name)
            if command in const.NEEDED_TABLE_DATA
            else None
        )

        match (command):
            case const.CMD_CREATE_TABLE:
                columns = utils.parse_table_columns(args)
                if columns is None:
                    continue

                changed_metadata = core.create_table(metadata, table_name, columns)
            case const.CMD_DROP_TABLE:
                changed_metadata = core.drop_table(metadata, table_name)
            case const.CMD_LIST_TABLES:
                core.list_tables(metadata)
                continue
            case const.CMD_INSERT:
                changed_tabledata = core.insert(tabledata)
                pass
            case const.CMD_EXIT:
                is_active = core.exit()
                continue
            case const.CMD_HELP:
                core.print_help()
                continue
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")
                continue

        if changed_metadata is not None:
            utils.save_metadata(changed_metadata)

        if changed_tabledata is not None:
            utils.save_table_data(table_name, changed_tabledata)
