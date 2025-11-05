DATA_TYPES = ("str", "int", "bool")

ID_COL_NAME = "ID"

ID_COL_DATA = {
    "name": "ID",
    "type": "int",
}

CMD_CREATE_TABLE = "create_table"
CMD_DROP_TABLE = "drop_table"
CMD_LIST_TABLES = "list_tables"

CMD_INSERT = "insert"
CMD_SELECT = "select"
CMD_UPDATE = "update"
CMD_DELETE = "delete"
CMD_INFO = "info"

CMD_EXIT = "exit"
CMD_HELP = "help"

COMPLEX_CMD = [CMD_INSERT, CMD_SELECT, CMD_DELETE]
NEEDED_TABLE_NAME = [
    CMD_CREATE_TABLE,
    CMD_DROP_TABLE,
    CMD_INSERT,
    CMD_SELECT,
    CMD_DELETE,
    CMD_INFO,
    CMD_UPDATE,
]
NEEDED_TABLE_DATA = [CMD_INSERT, CMD_SELECT, CMD_UPDATE, CMD_DELETE, CMD_INFO]

METADATA_NAME = "./db_meta.json"
TABLES_DIR = "data"

COLUMN_DEFINE_SEP = ":"

KEY_WORD_VALUES = "values"
KEY_WORD_WHERE = "where"
KEY_WORD_SET = "set"
