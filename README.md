# Solurix

A clean Telegram group RPG game bot with SQLite storage.

## Features

- RPG battles
- XP and levels
- Coins and points
- Daily rewards
- Group-wise rankings
- Player profiles and stats
- Admin group reset
- SQLite database
- Modular plugin structure
- VPS-friendly polling deployment

## Requirements

- Python 3.10+
- Telegram bot token

## VPS setup

```bash
git clone YOUR_REPOSITORY_URL Solurix
cd Solurix

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
nano .env

python3 bot.py
```

Set `BOT_TOKEN` in `.env`.

## Commands

`/start`
`/help`
`/profile`
`/me`
`/daily`
`/battle`
`/rank`
`/ranking`
`/reset`

`/reset` is restricted to group administrators.

## Branding

Solurix Bots: https://t.me/Solurix_bots
