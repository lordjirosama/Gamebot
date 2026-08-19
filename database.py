import os
import sqlite3
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from config import (
    DB_PATH,
    STARTING_COINS,
    STARTING_LEVEL,
    STARTING_XP,
)


# ============================================================
# DATABASE PATH
# ============================================================

DB_DIR = os.path.dirname(DB_PATH)

if DB_DIR:
    os.makedirs(DB_DIR, exist_ok=True)


# ============================================================
# CONNECTION
# ============================================================

def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""

    connection = sqlite3.connect(
        DB_PATH,
        timeout=30,
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db() -> None:
    """Create all Solurix database tables."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # USERS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT DEFAULT '',
                first_name TEXT DEFAULT '',

                level INTEGER NOT NULL DEFAULT 1,
                xp INTEGER NOT NULL DEFAULT 0,
                coins INTEGER NOT NULL DEFAULT 100,

                battles INTEGER NOT NULL DEFAULT 0,
                wins INTEGER NOT NULL DEFAULT 0,
                losses INTEGER NOT NULL DEFAULT 0,
                hunts INTEGER NOT NULL DEFAULT 0,
                messages INTEGER NOT NULL DEFAULT 0,

                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # GROUP MEMBERS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS group_members (
                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,

                joined_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,

                PRIMARY KEY (chat_id, user_id)
            )
            """
        )

        # ----------------------------------------------------
        # COOLDOWNS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cooldowns (
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                last_used REAL NOT NULL DEFAULT 0,

                PRIMARY KEY (user_id, action)
            )
            """
        )

        # ----------------------------------------------------
        # GAME HISTORY
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                result TEXT DEFAULT '',
                reward INTEGER NOT NULL DEFAULT 0,

                created_at TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # DAILY REWARDS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_rewards (
                user_id INTEGER PRIMARY KEY,
                last_claim TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # WEEKLY REWARDS
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weekly_rewards (
                user_id INTEGER PRIMARY KEY,
                last_claim TEXT NOT NULL
            )
            """
        )

        # ----------------------------------------------------
        # INDEXES
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_group_members_chat
            ON group_members(chat_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_group_members_user
            ON group_members(user_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_history_user
            ON history(user_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_history_created
            ON history(created_at)
            """
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# TIME HELPERS
# ============================================================

def utc_now() -> str:
    """Return the current UTC time as ISO format."""

    return datetime.now(
        timezone.utc
    ).isoformat()


# ============================================================
# USER FUNCTIONS
# ============================================================

def ensure_user(
    user_id: int,
    username: str = "",
    first_name: str = "",
) -> None:
    """
    Create the user if they don't exist.
    Otherwise update their basic information.
    """

    now = utc_now()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (
                user_id,
                username,
                first_name,
                level,
                xp,
                coins,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id)
            DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                updated_at = excluded.updated_at
            """,
            (
                user_id,
                username,
                first_name,
                STARTING_LEVEL,
                STARTING_XP,
                STARTING_COINS,
                now,
                now,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_user(
    user_id: int,
) -> Optional[Dict[str, Any]]:
    """Return a user as a dictionary."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        if not row:
            return None

        return dict(row)

    finally:
        connection.close()


# ============================================================
# COINS
# ============================================================

def add_coins(
    user_id: int,
    amount: int,
) -> None:
    """Add or remove coins from a user."""

    ensure_user(user_id)

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET
                coins = MAX(0, coins + ?),
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                amount,
                utc_now(),
                user_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_coins(
    user_id: int,
) -> int:
    """Return user's current coin balance."""

    user = get_user(user_id)

    if not user:
        return 0

    return int(
        user.get("coins", 0)
    )


# ============================================================
# XP
# ============================================================

def add_xp(
    user_id: int,
    amount: int,
) -> None:
    """Add XP to a user."""

    ensure_user(user_id)

    connection = get_connection()

    try:
       