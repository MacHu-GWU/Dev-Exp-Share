# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy_mate import EngineCreator, pt

metadata = sa.MetaData()

t_users = sa.Table(
    "users", metadata,
    sa.Column("user_id", sa.Integer),
    sa.Column("security_group_id", sa.Integer),
)

t_security_group_and_action = sa.Table(
    "security_group_and_action", metadata,
    sa.Column("security_group_id", sa.Integer),
    sa.Column("action_id", sa.Integer),
)

engine = EngineCreator.create_sqlite()
metadata.create_all(engine)

engine.execute(t_users.insert(), [
    dict(user_id=1, security_group_id=1),
    dict(user_id=2, security_group_id=1),
    dict(user_id=3, security_group_id=2),
    dict(user_id=4, security_group_id=2),
])

engine.execute(t_security_group_and_action.insert(), [
    dict(security_group_id=1, action_id=1),
    dict(security_group_id=1, action_id=2),
    dict(security_group_id=1, action_id=3),
    dict(security_group_id=2, action_id=4),
    dict(security_group_id=2, action_id=5),
    dict(security_group_id=2, action_id=6),
])


def pprint_sql(sql, engine):
    from sqlalchemy_mate.pkg.prettytable import from_db_cursor
    stmt = sa.text(sql)
    result_proxy = engine.execute(stmt)
    pretty_table = from_db_cursor(result_proxy.cursor)
    print(pretty_table)


def find_all_actions_can_be_done_by_a_user():
    # method 1
    sql = """
    SELECT
        security_group_and_action.action_id
    FROM
        security_group_and_action
    LEFT JOIN
        users
    ON
        security_group_and_action.security_group_id = users.security_group_id
    WHERE
        users.user_id = 1
    """

    pprint_sql(sql, engine)

    # method 2
    sql = """
    SELECT
        security_group_and_action.action_id
    FROM security_group_and_action
    WHERE
        security_group_and_action.security_group_id = (SELECT users.security_group_id FROM users WHERE users.user_id = 1)
    """

    pprint_sql(sql, engine)

find_all_actions_can_be_done_by_a_user()
