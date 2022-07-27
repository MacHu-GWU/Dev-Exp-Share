# -*- coding: utf-8 -*-

def get_status(name: str) -> str:
    print("real get_status() function hit")
    raise NotImplementedError
    return f"status of {name}: GOOD"


def get_status_api(name: str) -> str:
    return get_status(name)


def run_sql(sql: str) -> int:
    print("real run_sql() function hit")
    raise NotImplementedError
    return connect.execute(sql)


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id

    @property
    def n_items(self) -> int:
        sql = f"select COUNT(*) from items where items.order_id == {self.order_id}"
        return run_sql(sql)


if __name__ == "__main__":
    print(get_status_api(name="alice"))
