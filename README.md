⚔️ Solurix

«A Telegram Group RPG Game Bot powered by SQLite»

Solurix is a clean and lightweight Telegram RPG game bot designed for groups and communities.

Build your player profile, earn XP, collect coins and points, battle, claim daily rewards, and compete with other members on group rankings.

---

🌟 Features

- ⚔️ RPG Battles
- ⭐ XP & Level System
- 🪙 Coins & Points
- 🎁 Daily Rewards
- 🏆 Group-wise Rankings
- 👤 Player Profiles
- 📊 Player Statistics
- 🛡️ Admin Group Reset
- 💾 SQLite Database
- 🧩 Modular Plugin Structure
- 🚀 VPS-friendly Polling Deployment
- 📱 Telegram Command Support

---

🎮 Commands

Type "/" in the bot's private chat or inside a Telegram group to see the available commands.

🚀 Basic

"/start"

Start the Solurix bot.

/start

Use this when you first open the bot or want to display the start message.

---

"/help"

Show the available Solurix commands and basic usage information.

/help

---

👤 Profile

"/profile"

View your Solurix player profile.

/profile

Your profile contains your game-related information.

---

"/me"

A shortcut for "/profile".

/me

---

⚔️ Game

"/daily"

Claim your daily reward.

/daily

Daily rewards help players progress through the game.

---

"/battle"

Start an RPG battle.

/battle

Battle results can affect your game progress depending on the current game mechanics.

---

🏆 Rankings

"/rank"

View the ranking for the current group.

/rank

Use this to see how you compare with other players in the group.

---

"/ranking"

Alternative command for the group ranking.

/ranking

---

🛡️ Admin

"/reset"

Reset the game data for the current group.

/reset

⚠️ Admin only

This command is restricted to group administrators.

Use it carefully because resetting game data can affect the current group's game progress.

---

📋 Complete Command List

Command| Purpose
"/start"| Start Solurix
"/help"| Show available commands
"/profile"| View your profile
"/me"| View your profile
"/daily"| Claim daily reward
"/battle"| Start a battle
"/rank"| View group ranking
"/ranking"| View group ranking
"/reset"| Reset group game data — Admin only

---

🎯 How To Play

1. Add Solurix to your Telegram group

Add the bot to your group and start the game.

2. Start

Use:

/start

3. Check your profile

Use:

/profile

or:

/me

4. Claim your daily reward

Use:

/daily

5. Battle

Use:

/battle

6. Check the leaderboard

Use:

/rank

or:

/ranking

7. Get help

Use:

/help

---

📱 Telegram Command Menu

Solurix can be used directly from Telegram's command interface.

Simply type:

/

in the bot's PM or in a group where the bot is available.

Telegram can then display the bot's available commands.

---

💾 Database

Solurix uses SQLite for storing game data.

The configured database path is:

data/solurix.db

The database allows the bot to keep player and group game information persistent between restarts.

---

🧩 Project Structure

Gamebot/
│
├── bot.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
│
└── plugins/
    ├── admin.py
    ├── game.py
    ├── help.py
    ├── profile.py
    └── ranking.py

The project uses a modular plugin structure so individual game features can be maintained separately.

---

⚙️ Requirements

- Python 3.10+
- Telegram Bot Token
- SQLite
- VPS or another Python-compatible hosting environment

---

🚀 VPS Installation

Clone the repository:

git clone https://github.com/lordjirosama/Gamebot.git Solurix

Enter the project:

cd Solurix

Create a virtual environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create the environment file:

cp .env.example .env

Edit the environment file:

nano .env

Add your bot token:

BOT_TOKEN=YOUR_BOT_TOKEN

Save the file and start the bot:

python3 bot.py

---

🔐 Configuration

Solurix reads its bot token from the ".env" file.

Example:

BOT_TOKEN=YOUR_BOT_TOKEN

The database path can also be configured:

DB_PATH=data/solurix.db

Do not publish your real bot token on GitHub.

If a real token has ever been exposed publicly, regenerate it through BotFather and update your ".env".

---

🖼️ Custom Branding & Images

Solurix is designed so additional visual branding can be added later.

Recommended image sections include:

START_IMAGE=
HELP_IMAGE=
PROFILE_IMAGE=
DAILY_IMAGE=
BATTLE_IMAGE=
RANKING_IMAGE=

You can add your preferred Telegram image "file_id" values later when image support is added to the corresponding handlers.

---

🛠️ Running Solurix on VPS

For a temporary VPS session:

python3 bot.py

For a persistent "screen" session:

screen -S solurix
python3 bot.py

Detach from the session:

CTRL + A
D

Return to the running bot:

screen -r solurix

---

🔄 Updating Solurix

Before updating, make sure your database is backed up.

Then pull the latest code:

git pull

Activate the virtual environment if required:

source .venv/bin/activate

Update dependencies:

pip install -r requirements.txt

Restart the bot:

python3 bot.py

---

🐛 Troubleshooting

Bot does not start

Check that your ".env" contains:

BOT_TOKEN=YOUR_BOT_TOKEN

Then run:

python3 bot.py

and check the terminal output.

Commands are not responding

Make sure the bot is running:

python3 bot.py

Then check the terminal for Python or Telegram API errors.

"/reset" does not work

"/reset" is an administrator-only command and is intended for use inside groups.

Database issues

Make sure the bot has permission to create and write to:

data/solurix.db

---

📢 Official Branding

Solurix Bots

Owner: Jiro

Creator / Contact: "@senpain_jiro" (https://t.me/senpain_jiro)

Official Channel: "Solurix Bots" (https://t.me/Solurix_bots)

---

🔗 Links

GitHub Repository:
https://github.com/lordjirosama/Gamebot

Official Telegram Channel:
https://t.me/Solurix_bots

Owner:
https://t.me/senpain_jiro

---

❤️ Credits

Developed and maintained by Jiro.

Built for Telegram communities, group gaming, and RPG-style entertainment.

---

⚔️ Solurix

«Play. Battle. Earn. Level Up.»

Solurix Bots — Built for Telegram Communities.