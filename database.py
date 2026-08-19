import os
import sqlite3

from config import DB_PATH


def connect():
    os.makedirs(
        os.path.dirname(DB_PATH) or ".",
        exist_ok=True,
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

        # Add missing columns to old databases
        columns = {
            "kills": "INTEGER NOT NULL DEFAULT 0",
            "deaths": "INTEGER NOT NULL DEFAULT 0",
            "protected_until": "TEXT",
            "kill_cooldown_until": "TEXT",
        }

        existing = {
            row["name"]
            for row in con.execute(
                "PRAGMA table_info(players)"
            ).fetchall()
        }

        for name, definition in columns.items():

            if name not in existing:
                con.execute(
                    f"ALTER TABLE players ADD COLUMN "
                    f"{name} {definition}"
                )

        con.commit()


def ensure_player(
    user_id,
    chat_id,
    username,
    name,
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
            name,
        ))

        con.commit()


def get_player(
    user_id,
    chat_id,
):

    with connect() as con:

        return con.execute(
            """
            SELECT *
            FROM players
            WHERE user_id=?
            AND chat_id=?
            """,
            (
                user_id,
                chat_id,
            ),
        ).fetchone()


def get_group_players(chat_id):

    with connect() as con:

        return con.execute(
            """
            SELECT *
            FROM players
            WHERE chat_id=?
            """,
            (chat_id,),
        ).fetchall()


def add_progress(
    user_id,
    chat_id,
    xp=0,
    coins=0,
    points=0,
    win=False,
    loss=False,
    kill=False,
    death=False,
):

    player = get_player(
        user_id,
        chat_id,
    )

    if not player:
        return

    new_xp = player["xp"] + xp

    new_level = max(
        1,
        new_xp // 100 + 1,
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

        WHERE user_id=?
        AND chat_id=?
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
            chat_id,
        ))

        con.commit()


def update_coins(
    user_id,
    chat_id,
    amount,
):

    with connect() as con:

        con.execute(
            """
            UPDATE players
            SET coins = MAX(0, coins + ?)
            WHERE user_id=?
            AND chat_id=?
            """,
            (
                amount,
                user_id,
                chat_id,
            ),
        )

        con.commit()


def update_points(
    user_id,
    chat_id,
    amount,
):

    with connect() as con:

        con.execute(
            """
            UPDATE players
            SET points = MAX(0, points + ?)
            WHERE user_id=?
            AND chat_id=?
            """,
            (
                amount,
                user_id,
                chat_id,
            ),
        )

        con.commit()


def set_daily(
    user_id,
    chat_id,
    stamp,
):

    with connect() as con:

        con.execute(
            """
            UPDATE players
            SET last_daily=?
            WHERE user_id=?
            AND chat_id=?
            """,
            (
                stamp,
                user_id,
                chat_id,
            ),
        )

        con.commit()


def set_protection(
    user_id,
    chat_id,
    expires,
):

    with connect() as con:

        con.execute(
            """
            UPDATE players
            SET protected_until=?
            WHERE user_id=?
            AND chat_id=?
            """,
            (
                expires,
                user_id,
                chat_id,
            ),
        )

        con.commit()


def set_kill_cooldown(
    user_id,
    chat_id,
    expires,
):

    with connect() as con:

        con.execute(
            """
            UPDATE players
            SET kill_cooldown_until=?
            WHERE user_id=?
            AND chat_id=?
            """,
            (
                expires,
                user_id,
                chat_id,
            ),
        )

        con.commit()


def top_players(
    chat_id,
    limit=10,
):

    with connect() as con:

        return con.execute(
            """
            SELECT *
            FROM players
            WHERE chat_id=?

            ORDER BY
                points DESC,
                level DESC,
                xp DESC

            LIMIT ?
            """,
            (
                chat_id,
                limit,
            ),
        ).fetchall()


def reset_chat(chat_id):

    with connect() as con:

        con.execute(
            "DELETE FROM players WHERE chat_id=?",
            (chat_id,),
        )

        con.commit()