# Telegram Finance Bot

Simple Telegram bot to track income and expenses with SQLite.

## Features

- `/add income|expense amount category [note]`
- `/report [YYYY-MM]` monthly report
- Per-user data (each Telegram user sees only their own records)

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Set environment variable:
   - `TELEGRAM_BOT_TOKEN=<your_token>`
4. Run:
   - `python mainn.py`

## Commands

- `/start`
- `/help`
- `/add expense 120 food lunch`
- `/report`
- `/report 2026-03`
