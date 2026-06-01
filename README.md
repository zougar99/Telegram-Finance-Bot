# 🤖 Telegram-Finance-Bot — Telegram Finance Bot with AI — Track income/expenses via chat, natural language entry, spending predictions, and budget management

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/zougar99/Telegram-Finance-Bot/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/zougar99/Telegram-Finance-Bot?style=social)](https://github.com/zougar99/Telegram-Finance-Bot)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue)](https://github.com/zougar99/Telegram-Finance-Bot)

> Telegram Finance Bot with AI — Track income/expenses via chat, natural language entry, spending predictions, and budget management.

---

## 📖 Table of Contents
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features
- ✔ **Chat-Based Tracking** — "Spent 50$ on pizza" — auto-categorized
- ✔ **AI Classification** — NLP identifies category, amount, and currency
- ✔ **Budget Management** — Set monthly budgets per category with alerts
- ✔ **Spending Predictions** — ML forecasts future spending trends
- ✔ **Reports** — Daily/weekly/monthly summaries with charts
- ✔ **Multi-Currency** — Supports USD, EUR, MAD, GBP, and more
- ✔ **Export** — Download transaction history as CSV

---

## 🔮 How It Works

```
  Input ──► Processing Pipeline ──► Output
  ┌────────┐   ┌────────┐   ┌────────┐
  │ Data   │──►│ Engine │──►│ Result │
  │ Source │   │ Logic  │   │        │
  └────────┘   └────────┘   └────────┘
```

1. **Input** — Load data from file, API, or user input
2. **Process** — Core engine applies logic/analysis/transformation
3. **Output** — Results displayed in UI, saved to file, or sent via API

---

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Framework | python-telegram-bot |
| AI | OpenAI / spaCy NLP |
| Database | SQLite / PostgreSQL |
| Charts | Matplotlib |

---

## 🚀 Installation

```bash
git clone https://github.com/zougar99/Telegram-Finance-Bot.git
cd Telegram-Finance-Bot
pip install -r requirements.txt
# Set TELEGRAM_BOT_TOKEN in .env
python bot.py
```

---

## 📄 Configuration

Create a `config.yaml` or `.env` file in the project root:

```yaml
# Application settings
debug: false
port: 8080
theme: dark
language: en
```

---

## 🧰 Usage Guide

1. Create a bot via @BotFather and get token
2. Add token to `.env` file
3. Run `python bot.py`
4. Open Telegram and message your bot

---

## 🖼 Screenshots

> *(Screenshots coming soon. PRs welcome!)*

---

## 🔄 Roadmap

- 🟢 Web dashboard
- 🟡 Mobile companion app
- ⚫ API access
- ⚫ Plugin system
- ⚫ Multi-language support

---

## ❓ FAQ

### Is my financial data private?
Yes — data is stored locally on your server. No third-party access.

### Can I use it with group chats?
Yes — add the bot to a group and it will track expenses for all members.

---

## 🚧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **App won't start** | Check Python version (3.10+); run `pip install -r requirements.txt` |
| **No output** | Check logs in `logs/` folder; enable debug mode in config |
| **Performance issues** | Close other applications; reduce batch size in config |
| **Dependency errors** | Create fresh venv: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |

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
  Made with ❤️ by <a href="https://github.com/zougar99">zougar99</a>
</p>
