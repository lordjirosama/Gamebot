# ⚔️ SOLURIX

<p align="center">
  <b>⚔️ SOLURIX — TELEGRAM RPG GAME BOT</b>
</p>

<p align="center">
  A powerful Telegram group RPG bot built for fun, competition and community interaction.
</p>

<p align="center">
  <a href="https://t.me/Solurix_bots">📢 Channel</a> •
  <a href="https://t.me/Solurix_Support_Group">💬 Support Group</a> •
  <a href="https://t.me/senpain_jiro">👑 Owner</a>
</p>

---

## 🌟 ABOUT SOLURIX

Solurix is a Telegram group-based RPG game bot designed to turn your community into an interactive gaming world.

Players can battle each other, hunt for rewards, train their characters, explore different locations, earn coins, gain XP, level up and compete on group leaderboards.

Solurix is built with a modular plugin-based structure, SQLite database and configurable game systems.

---

## ✨ FEATURES

- ⚔️ Player Battle System
- 🎯 Hunting System
- 🏋️ Training System
- 🗺 Exploration System
- 🎁 Daily Rewards
- 🏆 Weekly Rewards
- 💰 Coin Economy
- ✨ XP System
- ⭐ Level System
- 👤 Player Profiles
- 📊 Player Statistics
- 🏅 Group Rankings
- 📜 Game History
- 🤖 Auto Reply System
- 🛠 Owner Controls
- 🗄 SQLite Database
- 🖼 Custom Image Support
- 📋 Telegram Command Menu
- 🔧 Modular Plugin Architecture
- 🌐 Group-based Progression

---

## 🎮 COMMANDS

### 🔰 Basic

| Command | Description |
|---------|--------------|
| `/start` | Start Solurix. |
| `/help` | Show all available commands. |
| `/support` | Open Solurix support. |

---

### 👤 Profile & Player

| Command | Description |
|---------|--------------|
| `/profile` | View your player profile. |
| `/stats` | View detailed player statistics. |
| `/level` | Check your current level and XP. |
| `/coins` | Check your current coin balance. |
| `/history` | View your recent game activity. |

---

### 🎁 Rewards

| Command | Description |
|---------|--------------|
| `/daily` | Claim your daily reward. |
| `/weekly` | Claim your weekly reward. |

---

### ⚔️ Game

| Command | Description |
|---------|--------------|
| `/battle` | Battle another player and earn rewards. |
| `/hunt` | Go on a hunt and find rewards. |
| `/train` | Train your character and gain XP. |
| `/explore` | Explore the Solurix world and discover rewards. |

---

### 🏆 Ranking

| Command | Description |
|---------|--------------|
| `/rank` | View the leaderboard of your current Telegram group. |

Every group can have its own Solurix ranking.

---

### 🛠 Owner

**`/reset`**

Reset a player's game progress.

You can reset using a user ID:
```
/reset USER_ID
```

Or reply to a user's message with:
```
/reset
```

Only the configured `OWNER_ID` can use this command.

---

## 📋 TELEGRAM COMMAND MENU

Solurix automatically registers its commands with Telegram.

When you type `/`, Telegram will display the available Solurix commands.

---

## 🖼 CUSTOM IMAGE SYSTEM

Solurix supports optional Telegram images for different sections.

Available image settings:

```
START_IMAGE=
HELP_IMAGE=
PROFILE_IMAGE=
RANKING_IMAGE=
BATTLE_IMAGE=
DAILY_IMAGE=
SHOP_IMAGE=
QUEST_IMAGE=
EVENT_IMAGE=
```

You can add Telegram `file_id` values later.

Example:
```
START_IMAGE=YOUR_TELEGRAM_FILE_ID
```

If an image is not configured, Solurix automatically uses the normal text interface.

---

## ⚙️ CONFIGURATION

Create a `.env` file in the project root.

Required configuration:

```env
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_USER_ID

BOT_NAME=Solurix
BOT_USERNAME=SolurixBot

SUPPORT_CHANNEL=https://t.me/Solurix_bots
SUPPORT_GROUP=https://t.me/Solurix_Support_Group

OWNER_USERNAME=@senpain_jiro
OWNER_LINK=https://t.me/senpain_jiro

REPOSITORY_URL=https://github.com/lordjirosama/Gamebot

DB_PATH=data/solurix.db

START_IMAGE=
HELP_IMAGE=
PROFILE_IMAGE=
RANKING_IMAGE=
BATTLE_IMAGE=
DAILY_IMAGE=
SHOP_IMAGE=
QUEST_IMAGE=
EVENT_IMAGE=

STARTING_COINS=100
STARTING_LEVEL=1
STARTING_XP=0

XP_PER_MESSAGE=5
XP_COOLDOWN=30

DAILY_REWARD=100
WEEKLY_REWARD=500

BATTLE_COOLDOWN=30
BATTLE_MIN_REWARD=10
BATTLE_MAX_REWARD=100

HUNT_COOLDOWN=60
HUNT_MIN_REWARD=5
HUNT_MAX_REWARD=75

AUTO_REPLY_ENABLED=True
AUTO_REPLY_COOLDOWN=20

SET_COMMANDS=True

LOG_LEVEL=INFO
```

⚠️ Never publish your real `BOT_TOKEN`.

---

## 🗄 DATABASE

Solurix uses SQLite as its database.

Default database:
```
data/solurix.db
```

The database stores:

- 👤 User profiles
- 💰 Coins
- ✨ XP
- ⭐ Levels
- ⚔️ Battles
- 🏆 Wins
- ❌ Losses
- 🎯 Hunts
- 💬 Messages
- 🏅 Group memberships
- ⏳ Cooldowns
- 🎁 Daily rewards
- 🏆 Weekly rewards
- 📜 Game history

The database is automatically created when Solurix starts.

---

## 📦 INSTALLATION

**1. Clone the repository**
```
git clone https://github.com/lordjirosama/Gamebot.git
```

**2. Enter the project**
```
cd Gamebot
```

**3. Check Python**
```
python3 --version
```
Python 3.10+ is recommended.

**4. Create virtual environment**
```
python3 -m venv venv
```

**5. Activate virtual environment**
```
source venv/bin/activate
```

**6. Install dependencies**
```
pip install -r requirements.txt
```

**7. Create .env**
```
cp .env.example .env
```

**8. Edit configuration**
```
nano .env
```
Add your real `BOT_TOKEN` and `OWNER_ID`.

---

## 🚀 START BOT

Run:
```
python3 bot.py
```

If the configuration is correct, Solurix will connect to Telegram.

---

## 🖥 VPS HOSTING

Solurix can be hosted on a Linux VPS.

Create a screen session:
```
screen -S solurix
```

Start the bot:
```
python3 bot.py
```

Detach from screen:
```
CTRL + A
D
```

The bot will continue running in the background.

---

## 🔄 RECONNECT TO BOT

```
screen -r solurix
```

---

## 🛑 STOP BOT

```
screen -r solurix
```
Then press `CTRL + C`.

---

## 🔁 RESTART BOT

```
screen -r solurix
```
Stop the running process: `CTRL + C`
Start again: `python3 bot.py`

---

## 📁 PROJECT STRUCTURE

```
Gamebot/
│
├── bot.py
├── config.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── solurix.db
│
└── plugins/
    ├── __init__.py
    ├── commands.py
    ├── start.py
    ├── help.py
    ├── game.py
    ├── profile.py
    ├── ranking.py
    ├── battle.py
    ├── hunt.py
    ├── admin.py
    ├── auto_reply.py
    ├── daily.py
    ├── weekly.py
    ├── coins.py
    ├── stats.py
    ├── level.py
    ├── history.py
    ├── explore.py
    └── train.py
```

---

## 🧩 PLUGIN SYSTEM

Solurix uses a modular plugin architecture.

Each major feature has its own plugin.

| Plugin | Description |
|--------|-------------|
| `battle.py` | Handles player battles. |
| `hunt.py` | Handles hunting. |
| `train.py` | Handles training. |
| `explore.py` | Handles exploration. |
| `daily.py` | Handles daily rewards. |
| `weekly.py` | Handles weekly rewards. |
| `profile.py` | Handles player profiles. |
| `ranking.py` | Handles group rankings. |

This makes Solurix easier to maintain and expand.

---

## 🎯 GAME FLOW

```
START
  ↓
Create Player
  ↓
Earn XP + Coins
  ↓
Battle / Hunt / Train / Explore
  ↓
Claim Daily / Weekly Rewards
  ↓
Level Up
  ↓
Compete in Group Ranking
```

---

## 🏅 GROUP RANKING

Solurix uses group-based rankings.

Players compete with other members of their Telegram group.

Each group can have its own leaderboard and competition.

---

## 🎁 REWARD SYSTEM

Players can earn virtual rewards from different activities.

- Daily rewards provide coins and XP.
- Weekly rewards provide larger rewards.
- Battles, hunts and exploration can also provide virtual coins and XP.

All rewards are part of the fictional game economy.

---

## 🤖 AUTO REPLY

Solurix includes an optional group auto-reply system.

Enable it using:
```
AUTO_REPLY_ENABLED=True
```

Configure the cooldown using:
```
AUTO_REPLY_COOLDOWN=20
```

The cooldown prevents the bot from replying repeatedly within a short period.

---

## 🔐 SECURITY

Never upload your real `.env` file to GitHub.

Your `.env` contains sensitive information including:
```
BOT_TOKEN
OWNER_ID
```

The `.gitignore` file protects the `.env` file from accidental Git commits.

If your Telegram bot token is exposed, regenerate it immediately using BotFather.

---

## 👑 OWNER

**Jiro**

Telegram: https://t.me/senpain_jiro
Username: `@senpain_jiro`

---

## 📢 OFFICIAL CHANNEL

**Solurix Bots**

https://t.me/Solurix_bots

Get:
- 📢 Updates
- 🆕 New features
- 🔧 Fixes
- 📣 Announcements
- ⚔️ Game updates

---

## 💬 SUPPORT GROUP

**Solurix Support Group**

https://t.me/Solurix_Support_Group

Use the support group for:
- 🐛 Bug reports
- 💡 Suggestions
- ❓ Questions
- 🛠 Technical help
- 📢 Feedback

---

## 📦 SOURCE CODE

GitHub Repository: https://github.com/lordjirosama/Gamebot

---

## ⚠️ DISCLAIMER

Solurix is a fictional Telegram RPG game created for entertainment and community interaction.

All coins, XP, levels, rewards, battles and rankings are virtual game elements. They have no real-world monetary value.

---

## ❤️ CREDITS

Developed and maintained by:

**Jiro**

Telegram: `@senpain_jiro`
Official Channel: https://t.me/Solurix_bots
Support Group: https://t.me/Solurix_Support_Group

---

<div align="center">

# ⚔️ SOLURIX

**Battle • Hunt • Train • Explore • Level Up**

🔥 Your adventure begins here.

</div>
