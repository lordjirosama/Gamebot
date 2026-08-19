import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone


DB_PATH = os.getenv("DB_PATH", "data/solurix.db")


def now():
    return datetime.now(timezone.utc).isoformat()


def ensure_data_dir():
    directory = os.path.dirname(DB_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)


@contextmanager
def get_db():
    ensure_data_dir()

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    try:
        con.execute("PRAGMA foreign_keys = ON")
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_db():
    ensure_data_dir()

    with get_db() as db:

        # =========================
        # PLAYERS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT NOT NULL,

            xp INTEGER NOT NULL DEFAULT 0,
            level INTEGER NOT NULL DEFAULT 1,
            rank TEXT NOT NULL DEFAULT 'Novice',

            coins INTEGER NOT NULL DEFAULT 100,
            points INTEGER NOT NULL DEFAULT 0,

            wins INTEGER NOT NULL DEFAULT 0,
            losses INTEGER NOT NULL DEFAULT 0,
            kills INTEGER NOT NULL DEFAULT 0,

            battles INTEGER NOT NULL DEFAULT 0,
            hunts INTEGER NOT NULL DEFAULT 0,

            streak INTEGER NOT NULL DEFAULT 0,
            best_streak INTEGER NOT NULL DEFAULT 0,

            daily_claimed_at TEXT,
            weekly_claimed_at TEXT,

            last_message_at TEXT,
            last_battle TEXT,
            last_hunt TEXT,
            last_kill TEXT,
            protected_until TEXT,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)

        # =========================
        # GROUPS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            chat_id INTEGER PRIMARY KEY,
            title TEXT,
            enabled INTEGER NOT NULL DEFAULT 1,

            xp_enabled INTEGER NOT NULL DEFAULT 1,
            auto_reply_enabled INTEGER NOT NULL DEFAULT 1,
            battle_enabled INTEGER NOT NULL DEFAULT 1,
            hunting_enabled INTEGER NOT NULL DEFAULT 1,

            daily_enabled INTEGER NOT NULL DEFAULT 1,

            welcome_enabled INTEGER NOT NULL DEFAULT 0,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)

        # =========================
        # GROUP PLAYER DATA
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS group_players (
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            xp INTEGER NOT NULL DEFAULT 0,
            level INTEGER NOT NULL DEFAULT 1,
            points INTEGER NOT NULL DEFAULT 0,

            wins INTEGER NOT NULL DEFAULT 0,
            losses INTEGER NOT NULL DEFAULT 0,
            kills INTEGER NOT NULL DEFAULT 0,

            messages INTEGER NOT NULL DEFAULT 0,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            PRIMARY KEY (chat_id, user_id),

            FOREIGN KEY (chat_id)
                REFERENCES groups(chat_id)
                ON DELETE CASCADE,

            FOREIGN KEY (user_id)
                REFERENCES players(user_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # INVENTORY
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            user_id INTEGER NOT NULL,
            item_id TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            PRIMARY KEY (user_id, item_id),

            FOREIGN KEY (user_id)
                REFERENCES players(user_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # SHOP ITEMS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS shop_items (
            item_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',

            price INTEGER NOT NULL DEFAULT 0,
            item_type TEXT NOT NULL DEFAULT 'item',

            stock INTEGER NOT NULL DEFAULT -1,
            enabled INTEGER NOT NULL DEFAULT 1,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)

        # =========================
        # QUESTS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS quests (
            quest_id TEXT PRIMARY KEY,

            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',

            quest_type TEXT NOT NULL DEFAULT 'general',

            requirement INTEGER NOT NULL DEFAULT 1,
            reward_xp INTEGER NOT NULL DEFAULT 0,
            reward_coins INTEGER NOT NULL DEFAULT 0,
            reward_points INTEGER NOT NULL DEFAULT 0,

            enabled INTEGER NOT NULL DEFAULT 1,

            created_at TEXT NOT NULL
        )
        """)

        # =========================
        # PLAYER QUEST PROGRESS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS player_quests (
            user_id INTEGER NOT NULL,
            quest_id TEXT NOT NULL,

            progress INTEGER NOT NULL DEFAULT 0,
            completed INTEGER NOT NULL DEFAULT 0,
            claimed INTEGER NOT NULL DEFAULT 0,

            updated_at TEXT NOT NULL,

            PRIMARY KEY (user_id, quest_id),

            FOREIGN KEY (user_id)
                REFERENCES players(user_id)
                ON DELETE CASCADE,

            FOREIGN KEY (quest_id)
                REFERENCES quests(quest_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # ACHIEVEMENTS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id TEXT PRIMARY KEY,

            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',

            requirement_type TEXT NOT NULL,
            requirement INTEGER NOT NULL DEFAULT 1,

            reward_xp INTEGER NOT NULL DEFAULT 0,
            reward_coins INTEGER NOT NULL DEFAULT 0,
            reward_points INTEGER NOT NULL DEFAULT 0,

            enabled INTEGER NOT NULL DEFAULT 1,

            created_at TEXT NOT NULL
        )
        """)

        # =========================
        # PLAYER ACHIEVEMENTS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS player_achievements (
            user_id INTEGER NOT NULL,
            achievement_id TEXT NOT NULL,

            progress INTEGER NOT NULL DEFAULT 0,
            unlocked INTEGER NOT NULL DEFAULT 0,
            unlocked_at TEXT,

            PRIMARY KEY (user_id, achievement_id),

            FOREIGN KEY (user_id)
                REFERENCES players(user_id)
                ON DELETE CASCADE,

            FOREIGN KEY (achievement_id)
                REFERENCES achievements(achievement_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # BATTLES
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS battles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            attacker_id INTEGER NOT NULL,
            defender_id INTEGER NOT NULL,

            winner_id INTEGER,
            loser_id INTEGER,

            attacker_damage INTEGER NOT NULL DEFAULT 0,
            defender_damage INTEGER NOT NULL DEFAULT 0,

            reward_xp INTEGER NOT NULL DEFAULT 0,
            reward_coins INTEGER NOT NULL DEFAULT 0,

            created_at TEXT NOT NULL
        )
        """)

        # =========================
        # HUNT HISTORY
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS hunts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            target TEXT NOT NULL,
            result TEXT NOT NULL,

            reward_xp INTEGER NOT NULL DEFAULT 0,
            reward_coins INTEGER NOT NULL DEFAULT 0,

            created_at TEXT NOT NULL
        )
        """)

        # =========================
        # SEASONS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS seasons (
            season_id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            started_at TEXT NOT NULL,
            ends_at TEXT,

            active INTEGER NOT NULL DEFAULT 1
        )
        """)

        # =========================
        # SEASON PLAYER DATA
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS season_players (
            season_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            xp INTEGER NOT NULL DEFAULT 0,
            points INTEGER NOT NULL DEFAULT 0,
            wins INTEGER NOT NULL DEFAULT 0,
            kills INTEGER NOT NULL DEFAULT 0,

            PRIMARY KEY (season_id, user_id),

            FOREIGN KEY (season_id)
                REFERENCES seasons(season_id)
                ON DELETE CASCADE,

            FOREIGN KEY (user_id)
                REFERENCES players(user_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # EVENTS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,

            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',

            event_type TEXT NOT NULL DEFAULT 'general',

            started_at TEXT NOT NULL,
            ends_at TEXT,

            reward_xp INTEGER NOT NULL DEFAULT 0,
            reward_coins INTEGER NOT NULL DEFAULT 0,

            enabled INTEGER NOT NULL DEFAULT 1
        )
        """)

        # =========================
        # EVENT PARTICIPATION
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS event_players (
            event_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,

            progress INTEGER NOT NULL DEFAULT 0,
            score INTEGER NOT NULL DEFAULT 0,
            claimed INTEGER NOT NULL DEFAULT 0,

            PRIMARY KEY (event_id, user_id),

            FOREIGN KEY (event_id)
                REFERENCES events(event_id)
                ON DELETE CASCADE,

            FOREIGN KEY (user_id)
                REFERENCES players(user_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # CREWS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS crews (
            crew_id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL UNIQUE,
            owner_id INTEGER NOT NULL,

            level INTEGER NOT NULL DEFAULT 1,
            xp INTEGER NOT NULL DEFAULT 0,
            coins INTEGER NOT NULL DEFAULT 0,

            created_at TEXT NOT NULL
        )
        """)

        # =========================
        # CREW MEMBERS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS crew_members (
            crew_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,

            role TEXT NOT NULL DEFAULT 'member',

            joined_at TEXT NOT NULL,

            PRIMARY KEY (crew_id, user_id),

            FOREIGN KEY (crew_id)
                REFERENCES crews(crew_id)
                ON DELETE CASCADE,

            FOREIGN KEY (user_id)
                REFERENCES players(user_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # TRANSACTIONS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            transaction_type TEXT NOT NULL,

            coins INTEGER NOT NULL DEFAULT 0,
            points INTEGER NOT NULL DEFAULT 0,

            description TEXT NOT NULL DEFAULT '',

            created_at TEXT NOT NULL
        )
        """)

        # =========================
        # IMAGE SETTINGS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_key TEXT PRIMARY KEY,
            file_id TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL
        )
        """)

        # =========================
        # GROUP SETTINGS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS group_settings (
            chat_id INTEGER PRIMARY KEY,

            start_image TEXT NOT NULL DEFAULT '',
            profile_image TEXT NOT NULL DEFAULT '',
            battle_image TEXT NOT NULL DEFAULT '',
            daily_image TEXT NOT NULL DEFAULT '',
            ranking_image TEXT NOT NULL DEFAULT '',
            help_image TEXT NOT NULL DEFAULT '',
            shop_image TEXT NOT NULL DEFAULT '',
            quest_image TEXT NOT NULL DEFAULT '',
            event_image TEXT NOT NULL DEFAULT '',

            updated_at TEXT NOT NULL,

            FOREIGN KEY (chat_id)
                REFERENCES groups(chat_id)
                ON DELETE CASCADE
        )
        """)

        # =========================
        # BOT ADMINS
        # =========================
        db.execute("""
        CREATE TABLE IF NOT EXISTS bot_admins (
            user_id INTEGER PRIMARY KEY,
            added_at TEXT NOT NULL
        )
        """)

        # =========================
        # INDEXES
        # =========================
        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_players_xp
        ON players(xp DESC)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_players_coins
        ON players(coins DESC)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_group_players_xp
        ON group_players(chat_id, xp DESC)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_season_players_points
        ON season_players(season_id, points DESC)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_inventory_user
        ON inventory(user_id)
        """)

        db.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_user
        ON transactions(user_id)
        """)

    print("Solurix database initialized.")


# ============================================================
# PLAYER FUNCTIONS
# ============================================================

def create_player(user_id, username=None, first_name="Player"):
    timestamp = now()

    with get_db() as db:
        db.execute("""
        INSERT OR IGNORE INTO players (
            user_id,
            username,
            first_name,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            username,
            first_name,
            timestamp,
            timestamp
        ))


def get_player(user_id):
    with get_db() as db:
        row = db.execute("""
        SELECT *
        FROM players
        WHERE user_id = ?
        """, (user_id,)).fetchone()

        return dict(row) if row else None


def update_player_identity(user_id, username, first_name):
    create_player(user_id, username, first_name)

    with get_db() as db:
        db.execute("""
        UPDATE players
        SET username = ?,
            first_name = ?,
            updated_at = ?
        WHERE user_id = ?
        """, (
            username,
            first_name,
            now(),
            user_id
        ))


def add_xp(user_id, amount):
    create_player(user_id)

    with get_db() as db:
        db.execute("""
        UPDATE players
        SET xp = xp + ?,
            updated_at = ?
        WHERE user_id = ?
        """, (amount, now(), user_id))


def add_coins(user_id, amount, description=""):
    create_player(user_id)

    with get_db() as db:
        db.execute("""
        UPDATE players
        SET coins = MAX(0, coins + ?),
            updated_at = ?
        WHERE user_id = ?
        """, (
            amount,
            now(),
            user_id
        ))

        db.execute("""
        INSERT INTO transactions (
            user_id,
            transaction_type,
            coins,
            description,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            "coins",
            amount,
            description,
            now()
        ))


def add_points(user_id, amount, description=""):
    create_player(user_id)

    with get_db() as db:
        db.execute("""
        UPDATE players
        SET points = MAX(0, points + ?),
            updated_at = ?
        WHERE user_id = ?
        """, (
            amount,
            now(),
            user_id
        ))

        db.execute("""
        INSERT INTO transactions (
            user_id,
            transaction_type,
            points,
            description,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            "points",
            amount,
            description,
            now()
        ))


def set_level(user_id, level):
    create_player(user_id)

    with get_db() as db:
        db.execute("""
        UPDATE players
        SET level = ?,
            updated_at = ?
        WHERE user_id = ?
        """, (level, now(), user_id))


def set_rank(user_id, rank):
    create_player(user_id)

    with get_db() as db:
        db.execute("""
        UPDATE players
        SET rank = ?,
            updated_at = ?
        WHERE user_id = ?
        """, (rank, now(), user_id))


# ============================================================
# BATTLE / HUNT
# ============================================================

def record_battle(
    attacker_id,
    defender_id,
    winner_id,
    loser_id,
    attacker_damage=0,
    defender_damage=0,
    reward_xp=0,
    reward_coins=0
):
    with get_db() as db:
        db.execute("""
        INSERT INTO battles (
            attacker_id,
            defender_id,
            winner_id,
            loser_id,
            attacker_damage,
            defender_damage,
            reward_xp,
            reward_coins,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attacker_id,
            defender_id,
            winner_id,
            loser_id,
            attacker_damage,
            defender_damage,
            reward_xp,
            reward_coins,
            now()
        ))

        db.execute("""
        UPDATE players
        SET battles = battles + 1,
            updated_at = ?
        WHERE user_id = ?
        """, (now(), attacker_id))

        if winner_id:
            db.execute("""
            UPDATE players
            SET wins = wins + 1,
                updated_at = ?
            WHERE user_id = ?
            """, (now(), winner_id))

        if loser_id:
            db.execute("""
            UPDATE players
            SET losses = losses + 1,
                updated_at = ?
            WHERE user_id = ?
            """, (now(), loser_id))


def record_hunt(
    user_id,
    target,
    result,
    reward_xp=0,
    reward_coins=0
):
    with get_db() as db:
        db.execute("""
        INSERT INTO hunts (
            user_id,
            target,
            result,
            reward_xp,
            reward_coins,
           