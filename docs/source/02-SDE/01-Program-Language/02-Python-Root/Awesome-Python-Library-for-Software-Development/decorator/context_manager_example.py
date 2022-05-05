from typing import Generator, ContextManager
from contextlib import contextmanager


class Session:
    def __init__(self):
        self.is_live = False

    def start(self):
        self.is_live = True

    def close(self):
        self.is_live = False

    def execute(self, msg):
        print(f"execute: {msg}")

    def error(self):
        raise ValueError("something wrong!")


class Connection:
    @contextmanager
    def session(self) -> ContextManager[Session]:
        session = Session()
        try:
            session.start()
            yield session
        finally:
            session.close()


conn = Connection()
with conn.session() as ses:
    print(ses.is_live)
    ses.execute("1")

print(ses.is_live)
