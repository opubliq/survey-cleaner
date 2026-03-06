#!/usr/bin/env python3
"""
session_cost.py — Rapport de tokens/coût pour une session opencode.

Usage:
    python scripts/session_cost.py <session_id>
    python scripts/session_cost.py ses_340661d5fffe2ZQWIoGb8I6OVG

    # Dernière session :
    python scripts/session_cost.py --last

    # Toutes les sessions du jour :
    python scripts/session_cost.py --today
"""

import json
import subprocess
import sys
from datetime import datetime, timezone


def export_session(session_id: str) -> dict:
    result = subprocess.run(
        ["opencode", "export", session_id],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def list_sessions() -> list[dict]:
    result = subprocess.run(
        ["opencode", "session", "list", "--format", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def report(data: dict) -> None:
    info = data["info"]
    messages = data.get("messages", [])

    title = info.get("title", "—")
    session_id = info.get("id", "—")
    created = datetime.fromtimestamp(
        info["time"]["created"] / 1000, tz=timezone.utc
    ).astimezone().strftime("%Y-%m-%d %H:%M")

    total_in = total_out = total_reasoning = total_cost = 0
    per_turn = []

    for msg in messages:
        i = msg.get("info", {})
        tokens = i.get("tokens", {})
        if not tokens:
            continue
        t_in = tokens.get("input", 0) or 0
        t_out = tokens.get("output", 0) or 0
        t_rea = tokens.get("reasoning", 0) or 0
        cost = i.get("cost", 0) or 0
        total_in += t_in
        total_out += t_out
        total_reasoning += t_rea
        total_cost += cost
        per_turn.append((t_in, t_out, t_rea, cost))

    grand_total = total_in + total_out + total_reasoning

    print(f"\nSession : {title}")
    print(f"ID      : {session_id}")
    print(f"Date    : {created}")
    print(f"Turns   : {len(per_turn)}")
    print()
    print(f"  Input tokens     : {total_in:>10,}")
    print(f"  Output tokens    : {total_out:>10,}")
    print(f"  Reasoning tokens : {total_reasoning:>10,}")
    print(f"  ─────────────────────────────")
    print(f"  TOTAL tokens     : {grand_total:>10,}")
    print(f"  TOTAL cost       : ${total_cost:>10.4f}")
    print()

    if per_turn:
        avg_in = total_in // len(per_turn)
        print(f"  Avg input/turn   : {avg_in:>10,}  ← context growth indicator")
    print()


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    if args[0] == "--last":
        sessions = list_sessions()
        if not sessions:
            print("Aucune session trouvée.")
            sys.exit(1)
        session_id = sessions[0]["id"]
        data = export_session(session_id)
        report(data)

    elif args[0] == "--today":
        sessions = list_sessions()
        today = datetime.now().date()
        found = False
        for s in sessions:
            created_ts = s.get("time", {}).get("created", 0) / 1000
            created_date = datetime.fromtimestamp(created_ts).date()
            if created_date == today:
                data = export_session(s["id"])
                report(data)
                found = True
        if not found:
            print("Aucune session aujourd'hui.")

    else:
        session_id = args[0]
        data = export_session(session_id)
        report(data)


if __name__ == "__main__":
    main()
