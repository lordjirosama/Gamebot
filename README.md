<p align="center">
    <a href="https://github.com/lordjirosama/Gamebot">
        <kbd>
            <img width="250" src="https://graph.org/file/placeholder-solurix-logo.jpg" alt="Solurix Logo">
        </kbd>
    </a>
</p><h1 align="center">⚔️ Solurix</h1><p align="center">
    <b>Telegram RPG Group Game Bot</b>
</p><p align="center">
    Earn XP • Collect Coins • Battle Players • Get Protection • Climb the Ranking
</p><div align="center">---

""Repository" (https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)" (https://github.com/lordjirosama/Gamebot)
""Telegram Channel" (https://img.shields.io/badge/Telegram-Channel-229ED9?style=for-the-badge&logo=telegram)" (https://t.me/Solurix_bots)
""Support Group" (https://img.shields.io/badge/Telegram-Support-229ED9?style=for-the-badge&logo=telegram)" (https://t.me/+1PeOFri-U2phYjd)
""Owner" (https://img.shields.io/badge/Owner-@senpain__jiro-orange?style=for-the-badge&logo=telegram)" (https://t.me/senpain_jiro)

</div>---

📖 About

Solurix is a Telegram group RPG game bot built with Python.

Players can create their own progress inside Telegram groups, earn XP, collect coins, gain points, level up, fight other players, activate protection, and compete for the top position on the group leaderboard.

Each group has its own separate player data, making every group its own Solurix RPG world.

---

✨ Features

<details>
<summary><b>⚔️ RPG Game System</b></summary>- XP progression
- Automatic level system
- Coins economy
- Points system
- Wins and losses
- Win-rate tracking
- Player profiles
- Group-based progression

</details><details>
<summary><b>🎮 Game Activities</b></summary>- Daily rewards
- Player battles
- Player kills
- Training
- Exploration
- Random rewards
- XP progression
- Coin rewards
- Point rewards

</details><details>
<summary><b>☠️ Kill System</b></summary>- Reply-based player targeting
- 24-hour kill cooldown
- Kill rewards
- Point transfer
- Coin rewards
- Protected-player detection
- Kill status tracking

</details><details>
<summary><b>🛡️ Protection System</b></summary>Players can protect themselves from the kill system.

Available protection plans:

- 1 Hour — 149 Coins
- 12 Hours — 500 Coins
- 24 Hours — 900 Coins

Protection automatically expires after the selected duration.

</details><details>
<summary><b>🏆 Ranking System</b></summary>- Group-specific leaderboard
- Top 10 players
- Medal system
- Points-based ranking
- Level and XP comparison
- Separate rankings for every group

</details><details>
<summary><b>👤 Player System</b></summary>Every player has their own profile containing:

- Name
- Username
- Level
- XP
- Coins
- Points
- Wins
- Losses
- Win rate
- XP progress

</details><details>
<summary><b>👑 Admin System</b></summary>Group administrators can manage Solurix game data.

- Admin-only reset
- Broadcast system
- Group management
- Admin permission checking

</details><details>
<summary><b>💾 Database</b></summary>Solurix uses SQLite for persistent storage.

Player data is stored separately for each Telegram group.

Stored information includes:

- User ID
- Chat ID
- Username
- Name
- XP
- Level
- Coins
- Points
- Wins
- Losses
- Daily reward status
- Kill cooldown
- Protection status

</details>---

🤖 Bot Commands

<details>
<summary><b>👤 Player Commands</b></summary>Command| Usage
"/start"| Start Solurix and open the main menu.
"/help"| Show the complete command guide.
"/profile"| View your player profile.
"/me"| Quickly view your profile.
"/stats"| View your game statistics.
"/coins"| Check your current coins.
"/level"| Check your current level and XP progress.

</details><details>
<summary><b>🎮 Game Commands</b></summary>Command| Usage
"/daily"| Claim your daily reward.
"/battle"| Fight a random enemy and earn rewards.
"/kill"| Kill another player by replying to their message.
"/protect"| Activate protection from the kill system.
"/train"| Train and earn XP, coins, and points.
"/explore"| Explore a random location and receive rewards.

</details><details>
<summary><b>🏆 Ranking Commands</b></summary>Command| Usage
"/rank"| View the current group's ranking.
"/ranking"| View the group leaderboard.

</details><details>
<summary><b>👑 Admin Commands</b></summary>Command| Usage
"/reset"| Reset Solurix data for the current group.
"/broadcast"| Send a broadcast message through the bot.

Admin commands are restricted to authorized administrators.

</details>---

🎁 Daily Reward

Use:

/daily

The current daily reward provides:

✨ +50 XP
🪙 +100 Coins
⭐ +25 Points

The reward can be claimed once per day.

---

⚔️ Battle System

Use:

/battle

The bot generates a random enemy.

Possible encounters include:

- Shadow Beast
- Iron Golem
- Void Guardian
- Crimson Wolf
- Storm Drake

A successful battle provides random XP, coins, and points.

A lost battle still provides consolation XP.

---

☠️ Kill System

Use "/kill" by replying to another player's message.

The bot checks:

1. Target player
2. Kill cooldown
3. Protection status
4. Available rewards

A successful kill rewards the attacker according to the current game rules.

Kill Cooldown

Players have a 24-hour kill cooldown.

The cooldown prevents repeated kills within the same period.

---

🛡️ Protection System

Use:

/protect

Protection prevents other players from killing you while it is active.

Protection Plans

Duration| Cost
1 Hour| 149 Coins
12 Hours| 500 Coins
24 Hours| 900 Coins

Protection expires automatically.

---

🏋️ Training

Use:

/train

Training gives random:

- XP
- Coins
- Points

Training is an easy way to progress your character.

---

🗺️ Exploration

Use:

/explore

Possible locations include:

- Mystic Forest
- Crystal Valley
- Ancient Ruins
- Moonlit Village
- Sky Island

Exploration provides random XP, coins, and points.

---

🪙 Economy

Solurix has three main progression currencies/values.

🪙 Coins

Coins are used for game features such as protection and are earned through gameplay.

✨ XP

XP determines your level.

⭐ Points

Points are used for competitive group rankings.

---

📈 Level System

Players start from Level 1.

Level progression is based on accumulated XP.

The profile displays an XP progress bar so players can track their progress.

---

🏆 Group Ranking

Use:

/rank

or:

/ranking

The leaderboard shows the top players of the current group.

Ranking prioritizes:

1. Points
2. Level
3. XP

Every group has an independent leaderboard.

---

👤 Player Profile

Use:

/profile

The profile shows:

👤 Player Name
⚔️ Level
⭐ Points
✨ XP
🪙 Coins
🏆 Wins
💫 Losses
📈 Win Rate

---

👑 Admin System

Solurix supports administrator-only game management.

"/reset"

Resets all Solurix player data for the current group.

Only group administrators can use this command.

"/broadcast"

The broadcast system allows authorized administrators to send a message through the bot.

Broadcast permissions should only be given to trusted administrators.

---

📢 Community

<div align="center">📢 Solurix Bots

""Telegram Channel" (https://img.shields.io/badge/Join%20Channel-Solurix%20Bots-229ED9?style=for-the-badge&logo=telegram)" (https://t.me/Solurix_bots)

💬 Support Group

""Support" (https://img.shields.io/badge/Join%20Support%20Group-229ED9?style=for-the-badge&logo=telegram)" (https://t.me/+1PeOFri-U2phYjd)

👑 Owner

""Owner" (https://img.shields.io/badge/@senpain__jiro-Contact-orange?style=for-the-badge&logo=telegram)" (https://t.me/senpain_jiro)

</div>---

🚀 Deployment

Requirements

- Python 3.10+
- Telegram Bot Token
- Linux VPS recommended
- SQLite
- Internet connection

---

📥 Clone Repository

git clone https://github.com/lordjirosama/Gamebot.git
cd Gamebot

---

🐍 Create Virtual Environment

python3 -m venv .venv

Activate it:

source .venv/bin/activate

---

📦 Install Requirements

pip install -r requirements.txt

---

⚙️ Configuration

Create:

.env

Add:

BOT_TOKEN=YOUR_BOT_TOKEN

Optional database path:

DB_PATH=data/solurix.db

Never publish your ".env" file.

---

▶️ Start Bot

python3 bot.py

If the terminal shows:

Application started

the bot is running successfully.

---

♾️ 24/7 VPS Hosting

For simple VPS hosting, Solurix can be run inside "screen".

Create a screen session:

screen -S solurix

Activate the environment:

source .venv/bin/activate

Start the bot:

python3 bot.py

When you see:

Application started

detach from screen:

Ctrl + A
D

The bot will continue running after you leave the SSH session.

Check Screen

screen -ls

Reopen Solurix

screen -r solurix

---

🔄 Updating the Bot

Go to the project:

cd ~/Solurix

Pull the latest changes:

git pull --ff-only

Compile the project:

python3 -m py_compile database.py bot.py plugins/*.py

Then restart the bot.

---

🗄️ Database

Default database:

data/solurix.db

SQLite is used because Solurix is designed to be lightweight and easy to deploy.

Database Backup

Before making database changes:

cp data/solurix.db data/solurix.db.backup

---

📁 Project Structure

Solurix/
│
├── bot.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
├── .env
│
├── data/
│   └── solurix.db
│
└── plugins/
    ├── admin.py
    ├── game.py
    ├── help.py
    ├── profile.py
    └── ranking.py

---

🧩 Plugin Structure

"bot.py"

Main application file.

It loads the Telegram application and registers commands.

"config.py"

Stores bot configuration such as:

- Bot token
- Bot name
- Brand channel
- Database path
- Image configuration

"database.py"

Handles SQLite database operations.

"plugins/game.py"

Contains gameplay systems such as:

- Daily rewards
- Battles
- Training
- Exploration
- Kill system
- Protection system

"plugins/profile.py"

Handles:

- Profiles
- Statistics
- Coins
- Levels

"plugins/ranking.py"

Handles group rankings and leaderboards.

"plugins/admin.py"

Handles administrator-only commands.

"plugins/help.py"

Contains start and help messages.

---

🖼️ Image Support

Solurix supports optional images for different bot sections.

Available configuration fields:

START_IMAGE
PROFILE_IMAGE
DAILY_IMAGE
BATTLE_IMAGE
TRAIN_IMAGE
EXPLORE_IMAGE
RANKING_IMAGE
HELP_IMAGE

Images can be configured later using Telegram file IDs or supported image URLs.

---

🔐 Security

Never expose your bot token publicly.

Keep:

.env

private.

If your bot token is accidentally exposed, immediately regenerate it using Telegram's BotFather and update your ".env".

Do not commit:

.env
data/solurix.db
.venv/
__pycache__/

to a public repository.

---

🛠️ Troubleshooting

Bot does not start

Check:

python3 -m py_compile database.py bot.py plugins/*.py

Then:

python3 bot.py

---

Check Python version

python3 --version

---

Check installed dependencies

pip list

---

Check Git status

git status

---

Check running screen sessions

screen -ls

---

🔗 Links

Resource| Link
GitHub Repository| "Gamebot" (https://github.com/lordjirosama/Gamebot)
Telegram Channel| "Solurix Bots" (https://t.me/Solurix_bots)
Support Group| "Solurix Support" (https://t.me/+1PeOFri-U2phYjd)
Owner| "@senpain_jiro" (https://t.me/senpain_jiro)

---

❤️ Credits

<p align="center"><b>Solurix</b><br>
Telegram RPG Group Game Bot

<br>Developed and maintained by<br>

<a href="https://t.me/senpain_jiro">
<b>@senpain_jiro</b>
</a><br><br>

<a href="https://t.me/Solurix_bots">
<b>Solurix Bots</b>
</a></p>---

📜 License

This project is maintained for the Solurix Telegram community.

© Solurix Bots