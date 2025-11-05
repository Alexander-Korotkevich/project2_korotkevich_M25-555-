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

        if (tabledata is None) and (command in const.NEEDED_TABLE_DATA):
            print("Таблица не существует.")
            continue

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
                values = utils.parse_insert(user_input)
                if values is None:
                    continue
                changed_tabledata = core.insert(tabledata, values)
                pass
            case const.CMD_SELECT:
                where_clause = utils.parse_key_word_condition(
                    user_input, const.KEY_WORD_WHERE
                )
                core.select(tabledata, where_clause)
                continue
            case const.CMD_UPDATE:
                set_clause = utils.parse_set_condition(user_input)
                where_clause = utils.parse_key_word_condition(
                    user_input, const.KEY_WORD_WHERE
                )
                changed_tabledata = core.update(tabledata, set_clause, where_clause)
            case const.CMD_DELETE:
                where_clause = utils.parse_key_word_condition(
                    user_input, const.KEY_WORD_WHERE
                )
                changed_tabledata = core.delete(tabledata, where_clause)
            case const.CMD_INFO:
                core.info(tabledata)
                continue    
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
