import re
import math
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from collections import defaultdict


CATEGORY_KEYWORDS = {
    "food": ["food", "lunch", "dinner", "breakfast", "meal", "eat", "restaurant", "cafe", "groceries", "market", "pizza", "burger", "sandwich", "tacos"],
    "transport": ["transport", "gas", "fuel", "taxi", "bus", "train", "metro", "uber", "lyft", "fare", "parking", "toll", "essence"],
    "shopping": ["shopping", "clothes", "shoes", "store", "mall", "amazon", "online", "achats"],
    "entertainment": ["entertainment", "movie", "cinema", "game", "netflix", "spotify", "concert", "music", "tickets"],
    "bills": ["bill", "electricity", "water", "internet", "phone", "rent", "insurance", "subscription", "facture"],
    "health": ["health", "doctor", "pharmacy", "medicine", "hospital", "gym", "dentist", "hopital"],
    "education": ["education", "course", "book", "books", "school", "university", "training", "class", "ecole"],
    "salary": ["salary", "income", "pay", "wage", "bonus", "freelance", "payment received", "salaire"],
    "transfer": ["transfer", "send", "received", "wire", "bank", "virement"],
}


def suggest_category(description: str) -> Optional[str]:
    desc_lower = description.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > 0:
            scores[category] = score
    if scores:
        return max(scores, key=scores.get)
    return None


def parse_natural_language(text: str) -> Optional[Dict]:
    text = text.strip()

    tx_type = "expense"

    income_patterns = [r'\b(?:received?|earned?|income|salary|bonus|got|paid\s*(?:me|to\s*me)|salaire)\b']
    for pat in income_patterns:
        if re.search(pat, text, re.IGNORECASE):
            tx_type = "income"
            break

    expense_words = [r'\bspent?\b', r'\bpaid\b', r'\bcost\b', r'\bbought?\b', r'\bexpense\b', r'\bused?\b', r'\bdépens[ée]\b']
    for pat in expense_words:
        if re.search(pat, text, re.IGNORECASE):
            tx_type = "expense"
            break

    amount_patterns = [
        r'(\d+[.,]?\d*)\s*(?:mad|dh|usd|eur|gbp|dhs?|\$|€|£)',
        r'(?:mad|dh|usd|eur|gbp|dhs?|\$|€|£)\s*(\d+[.,]?\d*)',
        r'(\d+[.,]?\d*)',
    ]
    amount_match = None
    for pat in amount_patterns:
        amount_match = re.search(pat, text, re.IGNORECASE)
        if amount_match:
            break

    if not amount_match:
        return None

    amount_str = amount_match.group(1)
    if not amount_str:
        return None
    amount = float(amount_str.replace(",", "."))
    if amount <= 0:
        return None

    remaining = re.sub(r'(?:mad|dh|usd|eur|gbp|dhs?|\$|€|£)\s*\d+[.,]?\d*|\d+[.,]?\d*\s*(?:mad|dh|usd|eur|gbp|dhs?|\$|€|£)', '', text, flags=re.IGNORECASE).strip()
    remaining = re.sub(r'\d+[.,]?\d*', '', remaining).strip()
    remaining = re.sub(r'\b(?:spent?|paid|cost|bought?|used?|received?|earned?|got|income|expense|salary|bonus|add|dépens[ée]|salaire)\b', '', remaining, flags=re.IGNORECASE).strip()

    category = suggest_category(remaining) or "other"
    note = remaining.strip() if remaining.strip() else None

    date = None
    today = datetime.now()

    date_keywords = {
        "yesterday": today - timedelta(days=1),
        "today": today,
        "this morning": today,
        "this afternoon": today,
        "last night": today - timedelta(days=1),
        "last week": today - timedelta(weeks=1),
        "last month": today - timedelta(days=30),
        "hier": today - timedelta(days=1),
        "aujourd'hui": today,
    }
    for key, dt in date_keywords.items():
        if key in text.lower():
            date = dt
            break

    if date is None:
        date_match = re.search(r'(?:on|le|du)\s+(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?', text, re.IGNORECASE)
        if date_match:
            day = int(date_match.group(1))
            month = int(date_match.group(2))
            year = int(date_match.group(3)) if date_match.group(3) else today.year
            if year < 100:
                year += 2000
            try:
                date = datetime(year, month, day)
            except ValueError:
                date = today

    return {
        "tx_type": tx_type,
        "amount": amount,
        "category": category,
        "note": note,
        "date": date.isoformat(timespec="seconds") if date else None,
    }


def predict_next_month(transactions: List[Dict]) -> Dict:
    if not transactions:
        return {"predicted_income": 0, "predicted_expense": 0, "confidence": "low", "note": "No transaction data available"}

    monthly_data = defaultdict(lambda: {"income": 0, "expense": 0})
    for tx in transactions:
        created = tx.get("created_at", "")
        month_key = created[:7]
        tx_type = tx.get("tx_type", "")
        amount = tx.get("amount", 0)
        if month_key:
            monthly_data[month_key][tx_type] += amount

    months = sorted(monthly_data.keys())
    if not months:
        return {"predicted_income": 0, "predicted_expense": 0, "confidence": "low", "note": "Could not parse dates"}

    last_month = monthly_data[months[-1]]
    if len(months) < 2:
        return {
            "predicted_income": round(last_month["income"], 2),
            "predicted_expense": round(last_month["expense"], 2),
            "predicted_balance": round(last_month["income"] - last_month["expense"], 2),
            "confidence": "low",
            "note": "Need more months of data for better predictions",
            "based_on_months": 1,
        }

    recent = months[-3:] if len(months) >= 3 else months
    recent_data = [monthly_data[m] for m in recent]

    avg_income = sum(d["income"] for d in recent_data) / len(recent_data)
    avg_expense = sum(d["expense"] for d in recent_data) / len(recent_data)

    confidence = "high" if len(months) >= 3 else "medium"
    trend = "stable"
    if len(months) >= 2:
        if avg_expense > monthly_data[months[-2]]["expense"] * 1.05:
            trend = "increasing"
        elif avg_expense < monthly_data[months[-2]]["expense"] * 0.95:
            trend = "decreasing"

    return {
        "predicted_income": round(avg_income, 2),
        "predicted_expense": round(avg_expense, 2),
        "predicted_balance": round(avg_income - avg_expense, 2),
        "confidence": confidence,
        "based_on_months": len(recent),
        "last_month_income": round(last_month["income"], 2),
        "last_month_expense": round(last_month["expense"], 2),
        "trend": trend,
    }


def get_spending_insights(current_report: Dict, previous_report: Dict) -> List[str]:
    insights = []

    cur_expense = current_report.get("expense_total", 0)
    prev_expense = previous_report.get("expense_total", 0)
    cur_income = current_report.get("income_total", 0)
    prev_income = previous_report.get("income_total", 0)

    if prev_expense > 0:
        diff = cur_expense - prev_expense
        pct = (diff / prev_expense) * 100
        if abs(pct) < 5:
            insights.append("Your spending is stable compared to last month.")
        elif pct > 0:
            insights.append(f"Spending increased by {pct:.1f}% compared to last month (+{diff:.2f}).")
        else:
            insights.append(f"Great! Spending decreased by {abs(pct):.1f}% compared to last month ({diff:.2f}).")

    if prev_income > 0:
        diff = cur_income - prev_income
        pct = (diff / prev_income) * 100
        if abs(pct) > 5:
            if pct > 0:
                insights.append(f"Income increased by {pct:.1f}% compared to last month.")
            else:
                insights.append(f"Income decreased by {abs(pct):.1f}% compared to last month.")

    cur_categories = {item[1]: item[2] for item in current_report.get("by_category", []) if item[0] == "expense"}
    prev_categories = {item[1]: item[2] for item in previous_report.get("by_category", []) if item[0] == "expense"}

    for cat, amount in cur_categories.items():
        if cat in prev_categories and prev_categories[cat] > 0:
            diff = amount - prev_categories[cat]
            pct = (diff / prev_categories[cat]) * 100
            if abs(pct) > 20:
                if pct > 0:
                    insights.append(f"{cat.title()}: spending increased by {pct:.0f}% (now {amount:.2f})")
                else:
                    insights.append(f"{cat.title()}: spending decreased by {abs(pct):.0f}% (now {amount:.2f})")

    if cur_categories:
        top_cat = max(cur_categories, key=cur_categories.get)
        top_amount = cur_categories[top_cat]
        insights.append(f"Top expense category: {top_cat.title()} ({top_amount:.2f})")

    if not insights:
        insights.append("No significant changes detected.")

    return insights


def check_anomaly(user_transactions: List[Dict], amount: float, category: str, tx_type: str) -> Optional[str]:
    same_category = [
        tx for tx in user_transactions
        if tx.get("category", "").lower() == category.lower()
        and tx.get("tx_type") == tx_type
    ]

    if len(same_category) < 3:
        return None

    amounts = [tx["amount"] for tx in same_category]
    mean = sum(amounts) / len(amounts)

    if len(amounts) >= 2:
        variance = sum((x - mean) ** 2 for x in amounts) / len(amounts)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0

    if std_dev > 0 and abs(amount - mean) > 2 * std_dev:
        direction = "higher" if amount > mean else "lower"
        return f"Anomaly detected: This {category} transaction ({amount:.2f}) is {direction} than usual (avg: {mean:.2f})"

    return None
