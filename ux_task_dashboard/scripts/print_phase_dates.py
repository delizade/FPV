#!/usr/bin/env python3
import json
from datetime import datetime

with open("ux_task_dashboard/roadmap_tree.json", "r", encoding="utf-8") as f:
    tree = json.load(f)

def fmt_date(ts):
    if not ts:
        return "None"
    return datetime.fromtimestamp(int(ts)/1000).strftime("%B %d, %Y")

for sub in tree["subtasks"]:
    print(f"Name: {sub['name']}")
    print(f"  Start: {fmt_date(sub.get('start_date'))} ({sub.get('start_date')})")
    print(f"  Due:   {fmt_date(sub.get('due_date'))} ({sub.get('due_date')})")
