import logging
import os
from typing import Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import ai_features
from finance_db import (
    add_transaction,
    get_all_transactions,
    get_monthly_report,
    init_db,
    parse_month_or_current,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


HELP_TEXT = (
    "Finance Bot Commands:\n"
    "/start - Show welcome message\n"
    "/help - Show this help\n"
    "/add <income|expense> <amount> <category> [note]\n"
    "Example: /add expense 120 food lunch\n"
    "/report [YYYY-MM] - Monthly summary (default: current month)\n"
    "/ai <text> - Add transaction via natural language\n"
    '  Example: /ai spent 50 on lunch yesterday\n'
    "/insights [YYYY-MM] - AI spending comparison vs previous month\n"
    "/predict - AI predicts next month's spending\n"
    "/autocat <description> - AI suggests a category for a description"
)


def _to_float(raw: str) -> float:
    value = float(raw.replace(",", "."))
    if value <= 0:
        raise ValueError("Amount must be greater than zero.")
    return value


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name if update.effective_user else "there"
    await update.message.reply_text(
        f"Welcome {user_name}!\nTrack your income and expenses directly in Telegram.\n\n{HELP_TEXT}"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)


async def add_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None:
        await update.message.reply_text("Could not identify user.")
        return

    args = context.args
    if len(args) < 3:
        await update.message.reply_text(
            "Usage: /add <income|expense> <amount> <category> [note]"
        )
        return

    tx_type = args[0].strip().lower()
    if tx_type not in {"income", "expense"}:
        await update.message.reply_text("Type must be income or expense.")
        return

    try:
        amount = _to_float(args[1])
    except ValueError:
        await update.message.reply_text("Amount must be a positive number.")
        return

    category = args[2].strip().lower()
    note = " ".join(args[3:]).strip() if len(args) > 3 else None

    tx_id = add_transaction(
        user_id=user.id,
        tx_type=tx_type,
        amount=amount,
        category=category,
        note=note,
    )
    response = f"Saved #{tx_id}: {tx_type} {amount:.2f} in {category}."

    all_tx = get_all_transactions(user.id)
    anomaly = ai_features.check_anomaly(all_tx, amount, category, tx_type)
    if anomaly:
        response += f"\n\n{anomaly}"

    await update.message.reply_text(response)


def _format_report(month: str, report: dict) -> str:
    lines = [
        f"Report for {month}",
        f"Income: {report['income_total']:.2f}",
        f"Expense: {report['expense_total']:.2f}",
        f"Balance: {report['balance']:.2f}",
        "",
        "By category:",
    ]
    by_category = report["by_category"]
    if not by_category:
        lines.append("- No transactions in this month.")
    else:
        for tx_type, category, total in by_category:
            lines.append(f"- {tx_type:<7} | {category:<15} | {total:.2f}")
    return "\n".join(lines)


async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None:
        await update.message.reply_text("Could not identify user.")
        return

    month_input: Optional[str] = context.args[0] if context.args else None
    try:
        month = parse_month_or_current(month_input)
    except ValueError:
        await update.message.reply_text("Month format must be YYYY-MM. Example: /report 2026-03")
        return

    report = get_monthly_report(user_id=user.id, month=month)
    await update.message.reply_text(_format_report(month, report))


async def ai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None:
        await update.message.reply_text("Could not identify user.")
        return

    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /ai <description>\nExample: /ai spent 50 on lunch yesterday")
        return

    parsed = ai_features.parse_natural_language(text)
    if parsed is None:
        await update.message.reply_text("Could not understand the transaction. Try: /ai spent 50 on lunch")
        return

    tx_id = add_transaction(
        user_id=user.id,
        tx_type=parsed["tx_type"],
        amount=parsed["amount"],
        category=parsed["category"],
        note=parsed["note"],
    )

    response = f"Saved #{tx_id}: {parsed['tx_type']} {parsed['amount']:.2f} in {parsed['category']}"
    if parsed.get("note"):
        response += f" ({parsed['note']})"

    all_tx = get_all_transactions(user.id)
    anomaly = ai_features.check_anomaly(all_tx, parsed["amount"], parsed["category"], parsed["tx_type"])
    if anomaly:
        response += f"\n\n{anomaly}"

    await update.message.reply_text(response)


async def predict_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None:
        await update.message.reply_text("Could not identify user.")
        return

    all_tx = get_all_transactions(user.id)
    prediction = ai_features.predict_next_month(all_tx)

    lines = ["AI Spending Prediction", ""]
    lines.append(f"Predicted income:  {prediction['predicted_income']:.2f}")
    lines.append(f"Predicted expense: {prediction['predicted_expense']:.2f}")
    lines.append(f"Predicted balance: {prediction['predicted_balance']:.2f}")
    lines.append(f"Confidence: {prediction['confidence']}")
    lines.append(f"Trend: {prediction['trend']}")
    lines.append(f"Based on {prediction['based_on_months']} month(s) of data")
    if prediction.get("note"):
        lines.append(f"\n{prediction['note']}")
    lines.append("")
    lines.append(f"Last month income:  {prediction['last_month_income']:.2f}")
    lines.append(f"Last month expense: {prediction['last_month_expense']:.2f}")

    await update.message.reply_text("\n".join(lines))


async def insights_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None:
        await update.message.reply_text("Could not identify user.")
        return

    month_input = context.args[0] if context.args else None
    try:
        current_month = parse_month_or_current(month_input)
    except ValueError:
        await update.message.reply_text("Month format must be YYYY-MM. Example: /insights 2026-03")
        return

    yr, mo = current_month.split("-")
    prev_month = f"{int(yr) - (1 if mo == '01' else 0)}-{(int(mo) - 1) if mo != '01' else 12:02d}"

    current_report = get_monthly_report(user_id=user.id, month=current_month)
    previous_report = get_monthly_report(user_id=user.id, month=prev_month)

    insights = ai_features.get_spending_insights(current_report, previous_report)

    lines = ["AI Spending Insights", f"Comparing {current_month} vs {prev_month}", ""]
    for ins in insights:
        lines.append(f"- {ins}")

    await update.message.reply_text("\n".join(lines))


async def autocat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /autocat <description>\nExample: /autocat pizza dinner")
        return

    category = ai_features.suggest_category(text)
    if category:
        await update.message.reply_text(f"Suggested category: {category.title()}")
    else:
        await update.message.reply_text("Could not determine a category. Try a more descriptive text.")


def build_application(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("add", add_cmd))
    app.add_handler(CommandHandler("report", report_cmd))
    app.add_handler(CommandHandler("ai", ai_cmd))
    app.add_handler(CommandHandler("predict", predict_cmd))
    app.add_handler(CommandHandler("insights", insights_cmd))
    app.add_handler(CommandHandler("autocat", autocat_cmd))
    return app


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        try:
            from cred import API_TOKEN
            token = API_TOKEN.strip()
        except (ImportError, AttributeError):
            pass
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable or API_TOKEN in cred.py.")

    init_db()
    app = build_application(token)
    logger.info("Starting Telegram Finance Bot polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
