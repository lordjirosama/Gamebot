import os
import sqlite3
from config import DB_PATH


def connect():
    os.makedirs(
        os.path.dirname(DB_PATH) or ".",
        exist_ok=True
    )

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with connect() as con:

        con.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            username TEXT,
            name TEXT NOT NULL,

            xp INTEGER NOT NULL DEFAULT 0,
            level INTEGER NOT NULL DEFAULT 1,
            coins INTEGER NOT NULL DEFAULT 100,
            points INTEGER NOT NULL DEFAULT 0,

            wins INTEGER NOT NULL DEFAULT 0,
            losses INTEGER NOT NULL DEFAULT 0,
            kills INTEGER NOT NULL DEFAULT 0,
            deaths INTEGER NOT NULL DEFAULT 0,

            last_daily TEXT,
            protected_until TEXT,
            kill_cooldown_until TEXT,

            PRIMARY KEY (user_id, chat_id)
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS bot_admins (
            user_id INTEGER PRIMARY KEY
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS broadcast_users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            chat_id INTEGER PRIMARY KEY,
            title TEXT,
            added_at TEXT
        )
        """)

        con.commit()


def ensure_player(
    user_id,
    chat_id,
    username,
    name
):
    with connect() as con:

        con.execute("""
        INSERT INTO players(
            user_id,
            chat_id,
            username,
            name
        )
        VALUES(?,?,?,?)

        ON CONFLICT(user_id, chat_id)
        DO UPDATE SET
            username=excluded.username,
            name=excluded.name
        """, (
            user_id,
            chat_id,
            username,
            name
        ))

        con.execute("""
        INSERT OR REPLACE INTO broadcast_users(
            user_id,
            username,
            name
        )
        VALUES(?,?,?)
        """, (
            user_id,
            username,
            name
        ))

        con.commit()


def get_player(user_id, chat_id):
    with connect() as con:
        return con.execute(
            """
            SELECT *
            FROM players
            WHERE user_id=? AND chat_id=?
            """,
            (user_id, chat_id)
        ).fetchone()


def add_progress(
    user_id,
    chat_id,
    xp=0,
    coins=0,
    points=0,
    win=False,
    loss=False,
    kill=False,
    death=False
):
    player = get_player(user_id, chat_id)

    if not player:
        return

    new_xp = player["xp"] + xp
    new_level = max(
        1,
        new_xp // 100 + 1
    )

    with connect() as con:

        con.execute("""
        UPDATE players
        SET
            xp=?,
            level=?,
            coins=coins+?,
            points=points+?,
            wins=wins+?,
            losses=losses+?,
            kills=kills+?,
            deaths=deaths+?
        WHERE user_id=? AND chat_id=?
        """, (
            new_xp,
            new_level,
            coins,
            points,
            int(win),
            int(loss),
            int(kill),
            int(death),
            user_id,
            chat_id
        ))

        con.commit()


def update_coins(
    user_id,
    chat_id,
    amount
):
    with connect() as con:

        con.execute("""
        UPDATE players
        SET coins=MAX(0, coins+?)
        WHERE user_id=? AND chat_id=?
        """, (
            amount,
            user_id,
            chat_id
        ))

        con.commit()


def update_points(
    user_id,
    chat_id,
    amount
):
    with connect() as con:

        con.execute("""
        UPDATE players
        SET points=MAX(0, points+?)
        WHERE user_id=? AND chat_id=?
        """, (
            amount,
            user_id,
            chat_id
        ))

        con.commit()


def set_daily(
    user_id,
    chat_id,
    stamp
):
    with connect() as con:

        con.execute("""
        UPDATE players
        SET last_daily=?
        WHERE user_id=? AND chat_id=?
        """, (
            stamp,
            user_id,
            chat_id
        ))

        con.commit()


def set_protection(
    user_id,
    chat_id,
    expires_at
):
    with connect() as con:

        con.execute("""
        UPDATE players
        SET protected_until=?
        WHERE user_id=? AND chat_id=?
        """, (
            expires_at,
            user_id,
            chat_id
        ))

        con.commit()


def set_kill_cooldown(
    user_id,
    chat_id,
    expires_at
):
    with connect() as con:

        con.execute("""
        UPDATE players
        SET kill_cooldown_until=?
        WHERE user_id=? AND chat_id=?
        """, (
            expires_at,
            user_id,
            chat_id
        ))

        con.commit()


def top_players(
    chat_id,
    limit=10
):
    with connect() as con:

        return con.execute("""
        SELECT *
        FROM players
        WHERE chat_id=?
        ORDER BY
            points DESC,
            level DESC,
            xp DESC
        LIMIT ?
        """, (
            chat_id,
            limit
        )).fetchall()


def get_group_players(
    chat_id
):
    with connect() as con:

        return con.execute("""
        SELECT *
        FROM players
        WHERE chat_id=?
        ORDER BY points DESC
        """, (
            chat_id,
        )).fetchall()


def reset_chat(chat_id):
    with connect() as con:

        con.execute(
            "DELETE FROM players WHERE chat_id=?",
            (chat_id,)
        )

        con.commit()


def add_group(
    chat_id,
    title
):
    from datetime import datetime, timezone

    with connect() as con:

        con.execute("""
        INSERT OR REPLACE INTO groups(
            chat_id,
            title,
            added_at
        )
        VALUES(?,?,?)
        """, (
            chat_id,
            title,
            datetime.now(
                timezone.utc
            ).isoformat()
        ))

        con.commit()


def is_bot_admin(user_id):
    with connect() as con:

        return con.execute(
            """
            SELECT 1
            FROM bot_admins
            WHERE user_id=?
            """,
            (user_id,)
        ).fetchone() is not None


def add_bot_admin(user_id):
    with connect() as con:

        con.execute(
            """
            INSERT OR IGNORE INTO bot_admins(user_id)
            VALUES(?)
            """,
            (user_id,)
        )

        con.commit()


def remove_bot_admin(user_id):
    with connect() as con:

        con.execute(
            """
            DELETE FROM bot_admins
            WHERE user_id=?
            """,
            (user_id,)
        )

        con.commit()


def get_broadcast_users():
    with connect() as con:

        return con.execute(
            """
            SELECT *
            FROM broadcast_users
            """
        ).fetchall()