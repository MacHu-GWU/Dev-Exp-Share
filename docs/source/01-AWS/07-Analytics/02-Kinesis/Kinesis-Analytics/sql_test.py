# -*- coding: utf-8 -*-

import rolex
import uuid
import random
from datetime import datetime
from tabulate import tabulate


from sqlalchemy_mate import EngineCreator, ExtendedBase, pt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, text

ec = EngineCreator()
engine = ec.create_sqlite()

Base = declarative_base()


class Event(Base, ExtendedBase):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    time = Column(DateTime)
    name = Column(String)

t_event = Event.__table__

Base.metadata.create_all(engine)

n_records = 1000
event_name_pool = ["sign_in", ] * 9 + ["sign_up",]

events = [
    Event(
        id=str(uuid.uuid4()),
        time=rolex.rnd_datetime(start="2017-01-01", end="2017-01-01 23:59:59"),
        name=random.choice(event_name_pool),
    )
    for _ in range(n_records)
]
Event.smart_insert(engine, events)

sql = text("""
SELECT datetime(strftime('%s', t_E.time) / 3600 * 3600, 'unixepoch') as window, count(*)
FROM events as t_E
GROUP BY strftime('%s', t_E.time) / 3600
""")

print(pt.from_everything(sql, engine))

