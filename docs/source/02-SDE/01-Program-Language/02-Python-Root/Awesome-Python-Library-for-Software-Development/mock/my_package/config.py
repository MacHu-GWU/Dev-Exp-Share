# -*- coding: utf-8 -*-

import dataclasses


@dataclasses.dataclass
class Config:
    env: str = dataclasses.field()

    @property
    def project_name(self) -> str:
        return f"my-project-{self.env}"

    def make_db_table_name(self, env: str) -> str:
        return f"my_table_{env}"
