#!/usr/bin/env python3
"""
copilot_quota_cli.py — CLI version of the Copilot quota tracker.

Install deps:
    pip install workalendar

Run:
    python copilot_quota_cli.py
"""

import math
from datetime import date, timedelta
from workalendar.usa import UnitedStates

MONTHLY_REQUESTS = 300


def bar_chart(pct: float, width: int = 30) -> str:
    filled = round(pct / 100 * width)
    filled = max(0, min(width, filled))
    return f"[{'█' * filled}{'░' * (width - filled)}] {pct:.1f}%"


def main():
    today = date.today()
    cal = UnitedStates()
    year, month = today.year, today.month

    first = date(year, month, 1)
    last = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year + 1, 1, 1) - timedelta(days=1)

    all_days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
    working_days = [d for d in all_days if cal.is_working_day(d)]
    total_workdays = len(working_days)

    days_elapsed = len([d for d in working_days if d <= today])
    days_remaining = len([d for d in working_days if d >= today])

    requests_per_day = MONTHLY_REQUESTS / total_workdays
    budget_used = round(requests_per_day * days_elapsed, 1)
    budget_pct = (budget_used / MONTHLY_REQUESTS) * 100
    daily_pct = (requests_per_day / MONTHLY_REQUESTS) * 100

    is_workday = cal.is_working_day(today)

    print(f"\n🤖  Copilot Premium Budget — {today.strftime('%B %Y')}")
    print("=" * 50)
    print(f"  {bar_chart(budget_pct)}")
    print(f"  Should be at : {budget_used} / {MONTHLY_REQUESTS} requests ({budget_pct:.1f}%)")
    print(f"  Rate         : {requests_per_day:.2f} req/day  ({daily_pct:.2f}%/day)")
    print(f"  Workdays     : {days_elapsed} elapsed · {days_remaining} remaining of {total_workdays}")
    today_label = "✅ Workday" if is_workday else "🟡 Non-workday (no quota today)"
    print(f"  Today        : {today.strftime('%a %b %d')} — {today_label}")
    print()


if __name__ == "__main__":
    main()
