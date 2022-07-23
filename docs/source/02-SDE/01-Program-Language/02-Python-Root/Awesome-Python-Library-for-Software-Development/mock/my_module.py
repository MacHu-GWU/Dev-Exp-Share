# -*- coding: utf-8 -*-

def get_status(name: str) -> str:
    raise NotImplementedError
    return f"status of {name}: GOOD"


def get_status_api(name: str) -> str:
    return get_status(name)


if __name__ == "__main__":
    print(get_status_api(name="alice"))
