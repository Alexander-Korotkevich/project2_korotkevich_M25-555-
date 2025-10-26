from typing import Dict, List, TypedDict


class ColumnType(TypedDict):
    name: str
    type: str


class TableType(TypedDict):
    name: str
    columns: List[ColumnType]


class MetadataType(TypedDict):
    tables: Dict[str, TableType]
