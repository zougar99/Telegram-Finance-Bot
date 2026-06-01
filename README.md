# 🤖 Telegram Finance Bot — AI-Powered Personal Finance Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/zougar99/Telegram-Finance-Bot/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/zougar99/Telegram-Finance-Bot?style=social)](https://github.com/zougar99/Telegram-Finance-Bot)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://github.com/zougar99/Telegram-Finance-Bot)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram)](https://github.com/zougar99/Telegram-Finance-Bot)
[![AI](https://img.shields.io/badge/AI-OpenAI%20%7C%20spaCy-ff6b6b)](https://github.com/zougar99/Telegram-Finance-Bot)

> **AI-powered Telegram bot** for personal finance tracking. Log expenses via natural language, get spending predictions, set budgets, and receive smart insights — all through chat.

---

## 📖 Table of Contents
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Natural Language Parsing](#-natural-language-parsing)
- [Commands](#-commands)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [AI Predictions](#-ai-predictions)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features
- ✔ **Natural Language Input** — Type "spent 50$ on pizza" and the bot auto-categorizes it
- ✔ **AI Classification** — NLP identifies amount, currency, category, and merchant from raw text
- ✔ **Multi-Currency** — USD, EUR, MAD, GBP, JPY, CAD, AUD, and 30+ more currencies auto-detected
- ✔ **Budget Management** — Set monthly budgets per category with real-time alerts when approaching limits
- ✔ **Spending Predictions** — ML forecasts end-of-month spending based on historical patterns
- ✔ **Visual Reports** — Daily/weekly/monthly summaries with pie charts and bar graphs sent to chat
- ✔ **Category Management** — Auto-categorizes expenses, with manual override and custom categories
- ✔ **Export** — Download full transaction history as CSV, JSON, or PDF
- ✔ **Multi-User** — Group chat support — track shared expenses with roommates or family
- ✔ **Recurring Transactions** — Auto-detect and handle subscriptions, rent, and monthly bills
- ✔ **Insights Engine** — "You spent 30% more on dining this month", "Your coffee habit costs $120/month"

---

## 🔮 How It Works

```
    User Message                    Bot Response
    ┌──────────────────┐         ┌──────────────────┐
    │ "spent 35$ on   │         │ ✅ Added: Food   │
    │  Uber Eats"     │         │ 💰 $35.00 USD    │
    └────────┬─────────┘         │ 📊 Budget: 65%   │
             │                   │ 📈 +$1,240 this  │
             ▼                   │      month      │
    ┌──────────────────┐         └────────┬─────────┘
    │  NLP Parser      │                  │
    │  (spaCy/OpenAI)  │                  │
    └────────┬─────────┘                  │
             │                             │
             ▼                             │
    ┌──────────────────┐                   │
    │  Extract:        │                   │
    │  Amount: 35      │                   │
    │  Currency: USD   │                   │
    │  Category: Food  │                   │
    │  Merchant: Uber  │                   │
    └────────┬─────────┘                   │
             │                             │
             ▼                             │
    ┌──────────────────┐                   │
    │  Save to DB      │───────────────────┘
    │  Update budgets  │
    │  Check alerts    │
    └──────────────────┘
```

### Processing Flow

1. User sends a natural language message (e.g., "spent 35$ on Uber Eats")
2. **NLP Parser** extracts: amount (`35`), currency (`USD`), merchant (`Uber Eats`), category (`Food`)
3. Transaction is saved to SQLite/PostgreSQL with timestamp
4. Budget totals are updated for the current month
5. Bot responds with confirmation, updated budget %, and month-to-date total
6. If budget exceeds 80%/100%, bot sends an alert

---

## 🧠 Natural Language Parsing

The bot understands a wide range of input formats:

| Input | Parsed Result |
|-------|--------------|
| "spent 50$ on pizza" | $50.00 → Food |
| "paid 1200 MAD rent" | 1200 MAD → Housing |
| "uber ride 15€" | €15.00 → Transport |
| "salary +3500 USD" | +$3500.00 → Income |
| "coffee 4.50" | $4.50 → Food (default USD) |
| "netflix subscription 12€" | €12.00 → Entertainment |
| "saved 200$ this week" | +$200.00 → Savings |
| "transfer 100$ to savings" | -$100.00 → Transfer |

### Supported Formats
- `spent <amount> [currency] on <merchant>`
- `paid <amount> [currency] <merchant>`
- `<merchant> <amount> [currency]`
- `<amount> [currency] <merchant>`
- `+<amount>` / `-<amount>` (income/expense)
- Multiple currencies: $, €, £, MAD, ¥, CAD, AUD, 30+ more

---

## 📱 Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message + setup guide |
| `/add 50$ pizza` | Add expense (alternative to NL input) |
| `/income +3500 salary` | Add income entry |
| `/total` | Month-to-date total income/expense |
| `/budget` | View all budget limits and current spending |
| `/budget food 500` | Set $500 monthly budget for Food |
| `/report` | This week's spending summary |
| `/report monthly` | Full monthly report with chart |
| `/forecast` | AI prediction for month-end spending |
| `/categories` | List all categories with totals |
| `/history` | Last 20 transactions |
| `/export csv` | Download full history as CSV |
| `/insights` | Smart spending insights and tips |
| `/currency USD` | Set your default currency |
| `/reset` | Reset all data (confirmation required) |

---

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Framework | python-telegram-bot (v20.x) |
| NLP | spaCy + OpenAI API fallback |
| ML | scikit-learn (prophet-like forecasting) |
| Database | SQLite (local) / PostgreSQL (production) |
| Charts | Matplotlib |
| Async | asyncio + aiohttp |
| Platform | Any (Python) |

---

## 🚀 Installation

```bash
git clone https://github.com/zougar99/Telegram-Finance-Bot.git
cd Telegram-Finance-Bot

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file (see Configuration)
cp .env.example .env

# Run the bot
python bot.py
```

---

## 📄 Configuration

Edit `.env`:

```env
# Required: Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Optional: AI API Keys (for enhanced NLP)
OPENAI_API_KEY=sk-...

# Optional: Database (default: SQLite)
DATABASE_URL=postgresql://user:pass@localhost:5432/finance_bot

# Optional: Defaults
DEFAULT_CURRENCY=USD
REPORT_TIME=23:00
LANGUAGE=en
```

---

## 🧰 Usage Guide

### Quick Start

1. Message [@BotFather](https://t.me/BotFather) to create a new bot and get your token
2. Copy the token to `.env` as `TELEGRAM_BOT_TOKEN`
3. Run `python bot.py`
4. Open Telegram and message your bot
5. Type `/start` to see the welcome screen
6. Start logging expenses: "spent 50$ on dinner"

### Example Session

```
You: spent 35$ on Uber Eats
Bot: ✅ Added expense
     💰 $35.00 — Food › Uber Eats
     📊 Monthly budget: Food $235/$500 (47%)
     💳 Month total: $1,240.00

You: /budget food 500
Bot: ✅ Food budget set to $500/month

You: /report
Bot: 📅 This Week (Jun 1 - Jun 7)
     ─────────────────────────────
     Food          $235.00  ████████░░ 47%
     Transport      $85.00   ███░░░░░░░ 17%
     Entertainment  $42.00   █░░░░░░░░░  8%
     Housing       $0.00     ░░░░░░░░░░  0%
     ─────────────────────────────
     Total         $362.00
```

---

## 🔮 AI Predictions

The forecasting model analyzes your spending history and predicts month-end totals:

```
📈 Spending Forecast
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Food:     $235 / $500  ████░░░░░░  47%
Forecast: $380 🟢 (on track)

Transport: $85 / $200  ████░░░░░░  42%
Forecast: $150 🟢 (on track)

Entertainment: $42 / $100  ████░░░░░░ 42%
Forecast: $95 🟢 (on track)

⚠️ Alert: Dining is projected at $620 vs $500 budget
💡 Tip: Reduce dining out by 2x/week to save ~$100
```

---

## 📊 Screenshots

> *(Screenshots coming soon. PRs welcome!)*

| Chat View | Budget Dashboard | Monthly Report |
|-----------|-----------------|----------------|
| ![Chat](.github/screenshots/chat.png) | ![Budget](.github/screenshots/budget.png) | ![Report](.github/screenshots/report.png) |

---

## 🔄 Roadmap

- 🟢 Bank API integration (Plaid, Salt Edge) for auto-import
- 🟡 Splitwise-style group expense splitting
- ⚫ Recurring bill detection + reminders
- ⚫ Investment portfolio tracking
- ⚫ Voice message parsing (speech-to-text expense logging)
- ⚫ Web dashboard companion (FastAPI + React)

---

## ❓ FAQ

### Is my financial data private?
**Yes.** All data is stored on your own server. No third-party access. The AI features can run fully offline with spaCy.

### Does it work in group chats?
Yes — add the bot to a group and mention it to log expenses. Great for shared household budgets.

### Can I use it without AI?
Yes — the local spaCy model handles most inputs. OpenAI is only needed for complex/ambiguous statements.

### How do I set budgets?
Use `/budget <category> <amount>`. Example: `/budget food 500` sets a $500 monthly food budget.

### Can I export my data?
Yes — `/export csv`, `/export json`, or `/export pdf` to download your full transaction history.

---

## 🚧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Bot not responding** | Check TELEGRAM_BOT_TOKEN in .env; ensure bot.py is running |
| **NLP parsing wrong** | Try explicit format: `/add 50$ pizza`; install en_core_web_sm |
| **Charts not sending** | Ensure matplotlib is installed; check write permissions |
| **Database errors** | Check DATABASE_URL; run `python init_db.py` to initialize |
| **Forecast not accurate** | Needs at least 2 weeks of data; more data = better predictions |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📐 License

Distributed under the **MIT License**. See [`LICENSE`](https://github.com/zougar99/Telegram-Finance-Bot/blob/main/LICENSE) for more information.

---

<p align="center">
  Made with 💰 and ❤️ by <a href="https://github.com/zougar99">zougar99</a>
</p>
