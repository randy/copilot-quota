#!/usr/bin/env python3
"""
copilot_quota.py — GitHub Copilot Premium Request Budget Tracker
Menu bar app (rumps) that shows how much of your monthly quota you should have used by today.

Install deps:
    pip install rumps workalendar

Run:
    python copilot_quota.py
"""

import rumps
from datetime import date, timedelta
from workalendar.usa import UnitedStates

MONTHLY_REQUESTS = 300
UPDATE_INTERVAL_SECONDS = 3600  # refresh every hour


def get_budget_info(today: date = None) -> dict:
    if today is None:
        today = date.today()

    cal = UnitedStates()
    year, month = today.year, today.month

    # Build list of all working days in the month
    # Find first and last day of month
    first = date(year, month, 1)
    if month == 12:
        last = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)

    all_days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
    working_days = [d for d in all_days if cal.is_working_day(d)]
    total_workdays = len(working_days)

    # Working days elapsed (days up to and including today that are working days)
    elapsed_working_days = [d for d in working_days if d <= today]
    days_elapsed = len(elapsed_working_days)

    # Requests-per-day budget (floor to avoid overage)
    import math
    requests_per_day = MONTHLY_REQUESTS / total_workdays
    # Use floor so daily allowance never causes overage
    requests_per_day_safe = math.floor(requests_per_day * 100) / 100  # floor to 2 decimal places

    # Expected usage budget by end of today
    budget_used = round(requests_per_day * days_elapsed, 1)
    budget_pct = round((budget_used / MONTHLY_REQUESTS) * 100, 1)

    # Daily rate as percentage of monthly
    daily_pct = round((requests_per_day / MONTHLY_REQUESTS) * 100, 2)

    # Days remaining (including today if it's a workday)
    days_remaining = len([d for d in working_days if d >= today])

    return {
        "today": today,
        "month_name": today.strftime("%B %Y"),
        "total_workdays": total_workdays,
        "days_elapsed": days_elapsed,
        "days_remaining": days_remaining,
        "requests_per_day": round(requests_per_day, 2),
        "daily_pct": daily_pct,
        "budget_used": budget_used,
        "budget_pct": budget_pct,
        "monthly_requests": MONTHLY_REQUESTS,
        "is_workday": cal.is_working_day(today),
    }


def bar_chart(pct: float, width: int = 10) -> str:
    """Simple ASCII progress bar."""
    filled = round(pct / 100 * width)
    filled = max(0, min(width, filled))
    return f"[{'█' * filled}{'░' * (width - filled)}] {pct}%"


class CopilotQuotaApp(rumps.App):
    def __init__(self):
        super().__init__("🤖", title=None)
        self.info = get_budget_info()
        self._build_menu()
        self._update_title()

    def _update_title(self):
        info = self.info
        self.title = f"🤖 {info['budget_pct']}%"

    def _build_menu(self):
        info = self.info
        self.menu.clear()

        header = rumps.MenuItem(f"Copilot Budget — {info['month_name']}")
        header.set_callback(None)

        progress_label = rumps.MenuItem(bar_chart(info["budget_pct"]))
        progress_label.set_callback(None)

        detail_budget = rumps.MenuItem(
            f"Should be at: {info['budget_used']} / {info['monthly_requests']} requests  ({info['budget_pct']}%)"
        )
        detail_budget.set_callback(None)

        detail_daily = rumps.MenuItem(
            f"Rate: {info['requests_per_day']} req/day  ({info['daily_pct']}%/day)"
        )
        detail_daily.set_callback(None)

        detail_days = rumps.MenuItem(
            f"Workdays: {info['days_elapsed']} elapsed · {info['days_remaining']} remaining of {info['total_workdays']}"
        )
        detail_days.set_callback(None)

        today_status = "✅ Workday" if info["is_workday"] else "🟡 Non-workday (no quota today)"
        detail_today = rumps.MenuItem(f"Today ({info['today'].strftime('%a %b %d')}): {today_status}")
        detail_today.set_callback(None)

        self.menu = [
            header,
            None,
            progress_label,
            None,
            detail_budget,
            detail_daily,
            detail_days,
            detail_today,
            None,
            rumps.MenuItem("Refresh", callback=self.refresh),
            rumps.MenuItem("Quit", callback=lambda _: rumps.quit_application()),
        ]

    @rumps.timer(UPDATE_INTERVAL_SECONDS)
    def auto_refresh(self, _):
        self.info = get_budget_info()
        self._build_menu()
        self._update_title()

    def refresh(self, _):
        self.info = get_budget_info()
        self._build_menu()
        self._update_title()


if __name__ == "__main__":
    CopilotQuotaApp().run()
