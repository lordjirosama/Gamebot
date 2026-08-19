import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from config import DB_PATH, STARTING_COINS, STARTING_LEVEL, STARTING_XP


# ============================================================
# DATABASE SETUP
# ============================================================

os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """Create a new SQLite connection."""

    connection = sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_db() -> None:
    """Create all required Solurix tables."""

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
                coins INTEGER DEFAULT 100,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                hunts INTEGER DEFAULT 0,
                battles INTEGER DEFAULT 0,
                messages INTEGER DEFAULT 0,
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
                PRIMARY KEY (chat_id, user_id),
                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
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
                last_claim TEXT DEFAULT ''
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
                last_used REAL DEFAULT 0,
                PRIMARY KEY (user_id, action)
            )
            """
        )

        # ----------------------------------------------------
        # GAME HISTORY
        # ----------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                result TEXT DEFAULT '',
                reward INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
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
            CREATE INDEX IF NOT EXISTS idx_game_history_user
            ON game_history(user_id)
            """
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# HELPERS
# ============================================================

def now() -> str:
    """Return current UTC time."""

    return datetime.now(timezone.utc).isoformat()


# ============================================================
# USER MANAGEMENT
# ============================================================

def create_user(
    user_id: int,
    username: str = "",
    first_name: str = "",
) -> None:
    """Create a user if they do not already exist."""

    timestamp = now()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT OR IGNORE INTO users (
                user_id,
                username,
                first_name,
                coins,
                xp,
                level,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                first_name,
                STARTING_COINS,
                STARTING_XP,
                STARTING_LEVEL,
                timestamp,
                timestamp,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def update_user_info(
    user_id: int,
    username: str = "",
    first_name: str = "",
) -> None:
    """Update basic Telegram user information."""

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET username = ?,
                first_name = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                username,
                first_name,
                now(),
                user_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def ensure_user(
    user_id: int,
    username: str = "",
    first_name: str = "",
) -> None:
    """Create the user if needed and update their information."""

    create_user(
        user_id,
        username,
        first_name,
    )

    update_user_info(
        user_id,
        username,
        first_name,
    )


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
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

        return dict(row) if row else None

    finally:
        connection.close()


# ============================================================
# COINS
# ============================================================

def add_coins(user_id: int, amount: int) -> None:
    """Add coins to a user."""

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET coins = coins + ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                amount,
                now(),
                user_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def remove_coins(user_id: int, amount: int) -> bool:
    """Remove coins if the user has enough."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE users
            SET coins = coins - ?,
                updated_at = ?
            WHERE user_id = ?
              AND coins >= ?
            """,
            (
                amount,
                now(),
                user_id,
                amount,
            ),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ============================================================
# XP & LEVEL
# ============================================================

def add_xp(user_id: int, amount: int) -> None:
    """Add XP to a user."""

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET xp = xp + ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                amount,
                now(),
                user_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def set_level(user_id: int, level: int) -> None:
    """Set a user's level."""

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET level = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                level,
                now(),
                user_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# GAME STATS
# ============================================================

def increment_stat(
    user_id: int,
    stat: str,
    amount: int = 1,
) -> bool:
    """Safely increment a supported user statistic."""

    allowed_stats = {
        "wins",
        "losses",
        "hunts",
        "battles",
        "messages",
    }

    if stat not in allowed_stats:
        return False

    connection = get_connection()

    try:
        connection.execute(
            f"""
            UPDATE users
            SET {stat} = {stat} + ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                amount,
                now(),
                user_id,
            ),
        )

        connection.commit()

        return True

    finally:
        connection.close()


# ============================================================
# GROUP MEMBERS
# ============================================================

def add_group_member(
    chat_id: int,
    user_id: int,
) -> None:
    """Register a user inside a group."""

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT OR IGNORE INTO group_members (
                chat_id,
                user_id,
                joined_at
            )
            VALUES (?, ?, ?)
            """,
            (
                chat_id,
                user_id,
                now(),
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_group_ranking(
    chat_id: int,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Return top players from a group."""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                u.user_id,
                u.username,
                u.first_name,
                u.level,
                u.xp,
                u.coins,
                u.wins,
                u.losses
            FROM users u
            INNER JOIN group_members gm
                ON gm.user_id = u.user_id
            WHERE gm.chat_id = ?
            ORDER BY
                u.level DESC,
                u.xp DESC,
                u.coins DESC
            LIMIT ?
            """,
            (
                chat_id,
                limit,
            ),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# ============================================================
# DAILY REWARD
# ============================================================

def get_last_daily_claim(
    user_id: int,
) -> Optional[str]:
    """Return the last daily reward claim time."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT last_claim
            FROM daily_rewards
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        return row["last_claim"] if row else None

    finally:
        connection.close()


def set_daily_claim(user_id: int) -> None:
    """Save the current daily reward claim time."""

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO daily_rewards (
                user_id,
                last_claim
            )
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET last_claim = excluded.last_claim
            """,
            (
                user_id,
                now(),
            ),
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# COOLDOWNS
# ============================================================

def get_cooldown(
    user_id: int,
    action: str,
) -> float:
    """Get the last usage timestamp of an action."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT last_used
            FROM cooldowns
            WHERE user_id = ?
              AND action = ?
            """,
            (
                user_id,
                action,
            ),
        ).fetchone()

        return float(row["last_used"]) if row else 0.0

    finally:
        connection.close()


def set_cooldown(
    user_id: int,
    action: str,
    timestamp: float,
) -> None:
    """Save an action cooldown timestamp."""

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO cooldowns (
                user_id,
                action,
                last_used
            )
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, action)
            DO UPDATE SET last_used = excluded.last_used
            """,
            (
                user_id,
                action,
                timestamp,
            ),
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# GAME HISTORY
# ============================================================

def add_history(
    user_id: int,
    action: str,
    result: str = "",
    reward: int = 0,
) -> None:
    """Save a game action in history."""

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO game_history (
                user_id,
                action,
                result,
                reward,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                action,
                result,
                reward,
                now(),
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_history(
    user_id: int,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Return recent game history."""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT *
            FROM game_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                user_id,
                limit,
            ),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# ============================================================
# ADMIN / RESET
# ============================================================

def reset_user(user_id: int) -> None:
    """Reset a user's game progress."""

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE users
            SET coins = ?,
                xp = ?,
                level = ?,
                wins = 0,
                losses = 0,
                hunts = 0,
                battles = 0,
                messages = 0,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                STARTING_COINS,
                STARTING_XP,
                STARTING_LEVEL,
                now(),
                user_id,
            ),
        )

        connection.execute(
            """
            DELETE FROM daily_rewards
            WHERE user_id = ?
            """,
            (user_id,),
        )

        connection.execute(
            """
            DELETE FROM cooldowns
            WHERE user_id = ?
            """,
            (user_id,),
        )

        connection.execute(
            """
            DELETE FROM game_history
            WHERE user_id = ?
            """,
            (user_id,),
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

init_db()