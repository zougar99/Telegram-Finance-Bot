# 🤖 Telegram Finance Bot — مدير ميزانيتك على تيليغرام

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-26A5E4) ![License](https://img.shields.io/badge/License-MIT-green)

> **تطبيق تيليغرام لتتبع الدخل والمصاريف بالذكاء الاصطناعي**
> Track your income & expenses directly in Telegram — with AI-powered insights! 🚀

---

## 📋 Contents / المحتويات

- [Overview / نظرة عامة](#-overview--نظرة-عامة)
- [✨ Features / المميزات](#-features--المميزات)
- [🤖 AI Features / ميزات الذكاء الاصطناعي](#-ai-features--ميزات-الذكاء-الاصطناعي)
- [📦 Installation / التنصيب](#-installation--التنصيب)
- [⚙️ Configuration / الإعدادات](#️-configuration--الإعدادات)
- [🚀 How to Run / كيفية التشغيل](#-how-to-run--كيفية-التشغيل)
- [📖 Commands Guide / دليل الأوامر](#-commands-guide--دليل-الأوامر)
- [🧠 AI Commands in Detail / شرح أوامر الذكاء الاصطناعي](#-ai-commands-in-detail--شرح-أوامر-الذكاء-الاصطناعي)
- [📊 Database / قاعدة البيانات](#-database--قاعدة-البيانات)
- [🛠️ Project Structure / هيكل المشروع](#️-project-structure--هيكل المشروع)
- [🔒 Privacy / الخصوصية](#-privacy--الخصوصية)
- [🐛 Troubleshooting / حل المشاكل](#-troubleshooting--حل-المشاكل)

---

## 📖 Overview / نظرة عامة

**Telegram Finance Bot** is a smart personal finance tracker that lives inside your Telegram chat. You don't need to install any app — just add the bot on Telegram and start tracking your money immediately! 💰

**What makes it special?** 🤔

| Feature | Description |
|---------|-------------|
| 🗣️ **Natural Language** | Type "spent 30 on lunch" — the bot understands you! |
| 🤖 **AI Insights** | Get smart analysis of your spending habits |
| 🔮 **Predictions** | AI predicts your future expenses |
| 🚨 **Anomaly Detection** | Flags unusual transactions automatically |
| 🔒 **Private** | Each user sees only their own data |
| 💾 **Local Storage** | All data stored in SQLite on your server |

---

## ✨ Features / المميزات

### 📌 Basic Features
| Command | Description | Example |
|---------|-------------|---------|
| `/add` | Add a transaction manually | `/add expense 50 food lunch` |
| `/report` | View monthly summary | `/report` or `/report 2026-03` |
| `/start` | Welcome message | `/start` |
| `/help` | Show all commands | `/help` |

### 🤖 AI Features (New!)
| Command | Description | Example |
|---------|-------------|---------|
| `/ai` | Add via natural language | `/ai spent 30 on lunch yesterday` |
| `/predict` | Predict next month | `/predict` |
| `/insights` | Smart spending analysis | `/insights 2026-03` |
| `/autocat` | Suggest a category | `/autocat pizza dinner` |

### 🧠 Smart Detection
- ✅ **Anomaly Detection** — Alerts you if a transaction is unusually high/low
- ✅ **Auto-Categorization** — Suggests the right category automatically
- ✅ **Date Parsing** — Understands "yesterday", "today", "last week"

---

## 🤖 AI Features / ميزات الذكاء الاصطناعي

### 🗣️ 1. Natural Language Entry (`/ai`)

Turn plain English into structured transactions! The AI parser understands:

**Input examples:**
```
/ai spent 50 on lunch yesterday
/ai bought groceries for 200 MAD
/ai received salary 5000
/ai paid 30 for taxi this morning
/ai dépensé 100 في السوق
/ai pizza 25$ last night
```

**What it understands:**
- ✅ Amounts with or without currency (`50`, `200 MAD`, `25$`, `30dh`)
- ✅ Transaction type (`spent` = expense, `received` = income, `salary` = income)
- ✅ Categories (food, transport, shopping, bills, etc.) — auto-suggested from keywords
- ✅ Dates (`yesterday`, `today`, `last week`, `on 15/03`)
- ✅ French & Arabic words mixed in (dépensé, hier, salaire, سوق)

### 📊 2. Spending Insights (`/insights`)

Compare any month with the previous month and get AI-generated insights:

```
/insights 2026-03
```
```
📊 AI Spending Insights
Comparing 2026-03 vs 2026-02

- ⚠️ Spending increased by 15.3% compared to last month (+230.00)
- 📈 Income increased by 8.2% compared to last month
- 🔺 Food: spending increased by 40% (now 1200.00)
- 🔻 Transport: spending decreased by 25% (now 300.00)
- 📊 Top expense category: Food (1200.00)
```

### 🔮 3. Spending Prediction (`/predict`)

Predicts next month's income & expenses using moving average over your last 3 months:

```
/predict
```
```
🔮 AI Spending Prediction
- Predicted income:  8,500.00
- Predicted expense: 5,200.00
- Predicted balance: 3,300.00
- Confidence: high
- Trend: stable
- Based on 3 month(s) of data
- Last month income:  8,200.00
- Last month expense: 5,000.00
```

### 🚨 4. Anomaly Detection (Automatic!)

Every time you add a transaction (via `/add` or `/ai`), the bot checks if it's unusual:

```
Saved #42: expense 5,000.00 in food

⚠️ Anomaly detected: This food transaction (5000.00) is higher than usual (avg: 320.00)
```

### 🏷️ 5. Auto-Categorization (`/autocat`)

Not sure what category to use? Let AI suggest one:

```
/autocat pizza dinner with friends
→ Suggested category: Food

/autocat uber ride to work
→ Suggested category: Transport

/autocat bought medicine
→ Suggested category: Health

/autocat netflix subscription
→ Suggested category: Entertainment
```

**Supported categories & keywords:**
| Category | Keywords (EN) | Keywords (FR/AR) |
|----------|---------------|------------------|
| 🍔 Food | food, lunch, dinner, pizza, groceries, restaurant | marché, manger |
| 🚗 Transport | taxi, bus, gas, fuel, uber, parking | essence, transport |
| 🛍️ Shopping | clothes, shopping, store, mall, amazon | achats |
| 🎬 Entertainment | movie, netflix, concert, game, cinema | |
| 💡 Bills | electricity, water, internet, rent, insurance | facture |
| 💊 Health | doctor, pharmacy, medicine, hospital | hopital, docteur |
| 📚 Education | school, course, books, university | école, livres |
| 💰 Salary | salary, income, bonus, freelance | salaire, revenu |
| 💳 Transfer | bank, transfer, wire, send | virement |

---

## 📦 Installation / التنصيب

### Prerequisites / المتطلبات
- **Python 3.8+** installed
- A **Telegram Bot Token** from [@BotFather](https://t.me/BotFather) 🤖
- Internet connection 🌐

### Step 1: Clone the Repository
```bash
git clone https://github.com/zougar99/Telegram-Finance-Bot.git
cd Telegram-Finance-Bot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

That's it! Only `python-telegram-bot` is needed — the AI features are pure Python, no extra dependencies! 🎉

### Step 3: Set Your Bot Token

**Option A — Environment Variable (Recommended):**
```bash
# Windows PowerShell
$env:TELEGRAM_BOT_TOKEN="your_token_here"

# Linux / Mac
export TELEGRAM_BOT_TOKEN="your_token_here"
```

**Option B — Edit `cred.py`:**
Open `cred.py` and replace the token:
```python
API_TOKEN = "your_token_here"
```

> ⚠️ **Important**: `cred.py` is in `.gitignore` — it won't be committed to GitHub. Your token stays safe! 🔒

---

## 🚀 How to Run / كيفية التشغيل

```bash
python mainn.py
```

That's it! The bot will start polling and you'll see:
```
2026-05-31 16:53:36 - finance_bot - INFO - Starting Telegram Finance Bot polling...
```

Now open Telegram, find your bot, and start chatting! 🎊

### Running 24/7 / تشغيل دائم

**On a VPS with `screen`:**
```bash
screen -S finance-bot
python mainn.py
# Press Ctrl+A then D to detach
```

**On Windows:**
```powershell
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "mainn.py"
```

**On systemd (Linux):**
```ini
[Unit]
Description=Telegram Finance Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/Telegram-Finance-Bot
Environment=TELEGRAM_BOT_TOKEN=your_token
ExecStart=/usr/bin/python3 /path/to/Telegram-Finance-Bot/mainn.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📖 Commands Guide / دليل الأوامر

### 📝 `/add` — Add Transaction Manually

**Usage:**
```
/add <income|expense> <amount> <category> [note...]
```

**Examples:**
```
/add expense 120 food lunch at restaurant
/add income 5000 salary monthly payment
/add expense 350 transport uber ride
/add expense 2000 bills electricity
```

**Response:**
```
Saved #1: expense 120.00 in food (lunch at restaurant)
```

If the amount is unusual, an anomaly alert will appear automatically! 🚨

### 📊 `/report` — Monthly Report

**Usage:**
```
/report [YYYY-MM]
```

**Examples:**
```
/report          → Current month summary
/report 2026-03  → March 2026 summary
```

**Sample Response:**
```
📊 Report for 2026-03
Income:  12,500.00
Expense: 8,200.00
Balance: 4,300.00

By category:
- expense | food            | 2,500.00
- expense | transport       | 1,200.00
- expense | bills           | 1,800.00
- expense | entertainment   | 700.00
- expense | shopping        | 2,000.00
- income  | salary          | 10,000.00
- income  | freelance       | 2,500.00
```

---

## 🧠 AI Commands in Detail / شرح أوامر الذكاء الاصطناعي

### 🗣️ `/ai` — Natural Language Entry

**How it works:**

The parser breaks your text into parts:
1. **Type detection** — Looks for keywords like `spent`, `paid`, `bought` (expense) or `received`, `salary` (income)
2. **Amount extraction** — Finds numbers, with or without currency symbols (`$`, `€`, `MAD`, `dh`)
3. **Category suggestion** — Matches remaining text against keyword database
4. **Date parsing** — Understands relative dates (`yesterday`, `today`, `last week`) and absolute dates (`on 15/03`)

**More examples:**
```
/ai spent 25 on pizza with friends            → expense, 25.00, food 🍕
/ai received 5000 salary for March            → income, 5000.00, salary 💰
/ai paid 150 for electricity bill             → expense, 150.00, bills 💡
/ai bought groceries 300 yesterday            → expense, 300.00, food 🛒
/ai uber ride cost 45                         → expense, 45.00, transport 🚗
/ai netflix 15$                               → expense, 15.00, entertainment 🎬
/ai dépensé 200 في السوق hier                → expense, 200.00, food (Arabic/French support) 🌍
/ai salary 8000 received                      → income, 8000.00, salary 💵
```

### 📊 `/insights` — AI Insights

**How it works:**
The bot compares the selected month against the previous month and generates bullet-point insights:

- **Overall spending**: Up/down/stable percentage
- **Income changes**: Notable income changes
- **Category breakdown**: Which categories changed significantly (+20% or more)
- **Top category**: Your biggest expense category

### 🔮 `/predict` — AI Prediction

**How it works:**
Uses **simple moving average** — averages your last 3 months of income/expenses to predict next month.

- **High confidence**: 3+ months of data available
- **Medium confidence**: 2 months of data
- **Low confidence**: Only 1 month (just shows last month's numbers)

The prediction also shows a **trend** indicator:
- 📈 **Increasing** — expenses are growing month over month
- 📉 **Decreasing** — expenses are shrinking
- ➡️ **Stable** — expenses are consistent

### 🏷️ `/autocat` — Category Suggestion

Just type a description and get a category suggestion instantly:

```
/autocat whisky bar
→ Suggested category: Food (matches "bar")

/autocat hospital visit
→ Suggested category: Health
```

### 🚨 Anomaly Detection (Automatic)

Every transaction triggers a check:
1. Fetch all your previous transactions in the same category
2. Calculate the average and standard deviation
3. If the new amount is > 2 standard deviations from the mean → ALERT!

**Example:**
If your average lunch expense is 50 MAD and suddenly you add 500 MAD:
```
⚠️ Anomaly detected: This food transaction (500.00) is higher than usual (avg: 50.00)
```

---

## 📊 Database / قاعدة البيانات

### Technology
- **SQLite** — Lightweight, no setup required, file-based 📁
- File: `finance_bot.db` (auto-created when bot runs)

### Tables

**`transactions` table:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Auto-increment ID |
| `user_id` | INTEGER | Telegram user ID |
| `tx_type` | TEXT | `income` or `expense` |
| `amount` | REAL | Positive number |
| `category` | TEXT | Category name |
| `note` | TEXT | Optional note |
| `created_at` | TEXT | ISO timestamp |

### User Isolation
Each Telegram user **only sees their own data**. The `user_id` column separates data automatically. 🔒

---

## 🛠️ Project Structure / هيكل المشروع

```
Telegram-Finance-Bot/
│
├── 📄 mainn.py                  # 🚀 Entry point — just calls finance_bot.main()
├── 📄 finance_bot.py            # 🤖 Bot core — commands, handlers, Telegram integration
├── 📄 finance_db.py             # 🗄️ Database layer — SQLite CRUD operations
├── 📄 ai_features.py            # 🧠 AI engine — NLP, predictions, insights, anomalies
├── 📄 dbase.py                  # 🔧 Another database module (for user management)
├── 📄 cred.py                   # 🔑 Token storage (EXCLUDED from git)
├── 📄 requirements.txt          # 📦 Dependencies
├── 📄 .env.example              # 📝 Environment variable template
├── 📄 .gitignore                # 🙈 Git ignore rules
├── 📄 README.md                 # 📚 You are here!
└── 📁 habit_tracker/            # 🏃 Additional modules
```

### 📄 File Details

| File | Purpose |
|------|---------|
| `mainn.py` | Entry point — just imports and calls `finance_bot.main()` |
| `finance_bot.py` | Core bot logic — all Telegram command handlers, bot initialization |
| `finance_db.py` | Database layer — handles SQLite connection, transactions, reports |
| `ai_features.py` | AI engine — natural language parsing, predictions, insights, anomaly detection, auto-categorization. Pure Python! |
| `dbase.py` | Secondary database — user management, Twilio calls tracking |
| `cred.py` | Stores bot token and Twilio credentials. **Not committed to git** 🔒 |
| `requirements.txt` | Only `python-telegram-bot` needed! |

---

## 🔒 Privacy / الخصوصية

- ✅ **Your data stays on your server** — SQLite file is local
- ✅ **No external API calls** — AI runs locally, pure Python (no OpenAI, no cloud)
- ✅ **User isolation** — Each Telegram user sees only their records
- ✅ **Token safety** — `cred.py` is gitignored, never uploaded
- ✅ **No tracking** — The bot collects no analytics or personal data

---

## 🐛 Troubleshooting / حل المشاكل

### ❌ Bot doesn't respond
**Cause:** Token is wrong or bot is not running.
**Fix:** Check `cred.py` has the correct token from [@BotFather](https://t.me/BotFather).

### ❌ Timed Out / ConnectTimeout
**Cause:** Your server can't reach Telegram API (firewall, proxy, or internet issue).
**Fix:**
```bash
# Set proxy if behind corporate firewall
$env:HTTP_PROXY="http://proxy:port"
$env:HTTPS_PROXY="http://proxy:port"
python mainn.py
```

### ❌ Conflict: terminated by other getUpdates request
**Cause:** Another instance of the bot is already running.
**Fix:** Kill the other process or wait 1 minute for the lock to expire.

### ❌ Missing TELEGRAM_BOT_TOKEN
**Cause:** Token not set anywhere.
**Fix:** Either set `$env:TELEGRAM_BOT_TOKEN` or add your token to `cred.py`.

### ❌ AI not understanding my language
**Cause:** The NLP parser has limited vocabulary.
**Fix:** Use simpler English keywords (`spent`, `paid`, `received`). More languages can be added in `ai_features.py`!

---

## 🤝 Contributing / المساهمة

Want to improve the bot? Feel free to:

1. 🍴 Fork the repo
2. 🌿 Create a branch
3. ✨ Make your changes
4. 📬 Open a Pull Request

**Ideas for improvement:**
- 🌍 More language support (Arabic, French, Spanish)
- 📊 Budget management with alerts
- 💱 Multi-currency support
- 📈 Charts & visualizations
- 🎯 Financial goals tracking
- 🔄 Recurring/auto transactions
- ☁️ Cloud sync option

---

## 📜 License / الترخيص

This project is **MIT Licensed** — use it freely for personal or commercial projects! 🎉

---

## 💖 Support / الدعم

إذا عجبك المشروع، لا تنسى تضع **⭐ ستار** على GitHub!

If you like this project, don't forget to **⭐ star** it on GitHub!

---

*Made with ❤️ for the Telegram community — تطبيق مجاني للمجتمع*
