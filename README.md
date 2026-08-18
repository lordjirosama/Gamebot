<div align="center">

# ⚔️ SOLURIX COMBAT RPG BOT ⚔️

An advanced, feature-rich RPG Combat Telegram Bot built with Python (`python-telegram-bot`) and SQLite3. Features include monster battles, user duels, level progression, protection shields, and real-time leaderboards.

---

### 📢 Powered & Maintained By
[![Solurix Bots](https://img.shields.io/badge/Telegram-Solurix%20Bots-2CA5E0?style=for-the-badge&logo=telegram)](https://t.me/Solurix_bots)

</div>

---

## ✨ Features

* **🗡️ Combat System (`/kill`, `/attack`)**: Hunt monsters, gain EXP, earn Points and Coins with built-in cooldown management.
* **⚔️ Player vs Player (`/duel`)**: Reply to any group member to attack and steal their hard-earned points.
* **🛡️ Protection Shield (`/shield`)**: Buy 1h, 12h, or 24h immunity shields using points to protect against player attacks.
* **👤 Character Profile (`/profile`)**: Detailed statistics showing Level, EXP, Points, Coins, and Active Shield status.
* **🏆 Global Leaderboard (`/top`)**: Real-time rank tracking for the top 10 players based on total points.
* **⚡ Full Channel Branding**: Built-in interactive buttons and dynamic dynamic footers referencing **Solurix Bots**.

---

## 📁 Modular Project Architecture

```text
SolurixBot/
├── 📄 config.py          # Bot Token, Branding Links, & Global Footer Configuration
├── 📄 database.py        # SQLite Database Initialization & CRUD User Operations
├── 📄 handlers.py        # Game Logic, Combat Commands, & Callback Queries
├── 📄 main.py            # Bot Runner & Command Handler Registrations
├── 📄 requirements.txt   # Python Dependencies
└── 📄 README.md          # Official Documentation
