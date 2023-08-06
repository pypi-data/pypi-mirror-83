import sqlite3
import os
from typing import *
import json

from filterlib import Filter


class Setting:
    columns = ["text_id TEXT PRIMARY KEY",
               "value",
               "readable_name TEXT",
               "description TEXT",
               ]

    def __init__(self,
                 database_name: str = ":memory:",
                 table_name: str = "user_settings"):
        self.database_name = database_name
        self.table_name = table_name
        if "/" in self.database_name:
            try:
                assert self.database_name.split("/")[-1] in os.listdir("/".join(self.database_name.split("/")[:-1]))
            except AssertionError:
                print("WARNING: Cannot find database at '" + database_name + "'. Creating.")
        self.switch_database(self.database_name)

    def __getitem__(self, item):
        return self.get_setting(text_id=item, detail="value")[0]

    def __setitem__(self,
                    key,
                    value,
                    add_new: Optional[bool] = False) -> None:
        if key in self:
            self.update_setting(text_id=key, value=value)
        elif add_new:
            self.add_setting(text_id=key, value=value)

    def __contains__(self, item) -> bool:
        db = sqlite3.connect(self.database_name)
        return item in [x[0] for x in db.execute(f"SELECT text_id FROM {self.table_name}")]

    def add_setting(self,
                    text_id: str,
                    value: Optional,
                    readable_name: Optional[str] = "",
                    description: Optional[str] = "",
                    ):
        db = sqlite3.connect(self.database_name)
        if text_id not in self:
            cols = [x.split()[0] for x in self.columns][:2]
            values = [text_id, value]
            c = ', '.join(cols)
            v = ', '.join(["'" + str(v).replace("'", "\'\'") + "'" for v in values])
            cmd = f"INSERT INTO {self.table_name}({c}) VALUES({v})"
            db.execute(cmd)
            db.commit()
            self.update_setting(text_id=text_id,
                                readable_name=readable_name,
                                description=description,
                                value=value)

    def update_setting(self,
                       text_id: str,
                       readable_name: Optional[str] = None,
                       description: Optional[str] = None,
                       value: Optional[Any] = None):
        db = sqlite3.connect(self.database_name)
        f = Filter(text_id__eq__=text_id)
        command = f"UPDATE {self.table_name} SET"  # …
        if readable_name is not None:
            cmd = f"{command} readable_name='{readable_name.strip()}' WHERE {f}"
            db.execute(cmd)
        if description is not None:
            cmd = f"{command} description='{description.strip()}' WHERE {f}"
            db.execute(cmd)
        if value is not None:
            cmd = f"{command} value='{type(value).__name__}/{str(value).strip()}' WHERE {f}"
            db.execute(cmd)
        db.commit()

    def delete_setting(self, text_id):
        db = sqlite3.connect(self.database_name)
        f = Filter(text_id__eq__=text_id)
        cmd = f"DELETE FROM {self.table_name} WHERE {f}"
        db.execute(cmd)
        db.commit()

    def switch_database(self,
                        new_db_name: Optional[str] = None,
                        table_name: Optional[str] = None) -> None:
        self.database_name = new_db_name or self.database_name
        self.table_name = table_name or self.table_name
        db = sqlite3.connect(self.database_name)
        cols = [str(x) for x in self.columns]
        cmd = f"CREATE TABLE IF NOT EXISTS {self.table_name}({', '.join(cols)})"
        db.execute(cmd)
        db.commit()
        db.close()

    def get_setting(self,
                    text_id: str,
                    detail: Optional[str] = "*",
                    additional_types: List[type] = None) -> List:
        db = sqlite3.connect(self.database_name)
        cmd = f"SELECT {detail} FROM {self.table_name} WHERE text_id='{text_id}'"
        raw = [x for x in db.execute(cmd)][0]
        try:
            values = [json.loads(x) for x in raw]
        except json.decoder.JSONDecodeError:
            values = [x for x in raw]
        except TypeError:
            values = raw
        if type(values[-1]) == str and len(values[-1].split("/")) == 2:
            accepted_types = [int, float, dict, str, bool, list] + (additional_types or [])
            if values[-1].split("/")[0] in [t.__name__ for t in accepted_types]:
                t = eval(values[-1].split("/")[0])
                v = values[-1].split("/")[1].replace("_", " ")
                c = {list: json.loads}
                if t in c:
                    values[-1] = c[t](v)
                else:
                    values[-1] = t(v)
        assert len(values) <= 1, f"There are more than one values stored for setting '{text_id}'"
        return values

    def __iter__(self, f: Filter = None) -> List[List]:
        db = sqlite3.connect(self.database_name)
        for a in [e for e in db.execute(f"SELECT * FROM {self.table_name}" + (" WHERE " + str(f) if f else ""))]:
            yield a

    def __delete__(self, instance):
        db = sqlite3.connect(self.database_name)
        db.execute(f"DROP TABLE {self.table_name}")
        db.commit()
        db.close()
