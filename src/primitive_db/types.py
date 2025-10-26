from typing import Dict, List, TypedDict


class ColumnType(TypedDict):
    name: str
    type: str


class TableMetaType(TypedDict):
    name: str
    columns: List[ColumnType]


class MetadataType(TypedDict):
    tables: Dict[str, TableMetaType]


class TableType(TableMetaType):
    rows: List[Dict[str, int | str | bool]]
