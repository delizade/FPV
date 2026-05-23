#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import time

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
BASE = "https://api.clickup.com/api/v2"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# Mapping of task ID to its new name containing "PHASE" instead of "GROUP"
RENAME_MAP = {
    "86expf9fd": "PHASE 1 — Research & Direction",
    "86expf9fy": "PHASE 2 — Initial Design Proposals",
    "86expf9g8": "PHASE 3 — UX Analysis & Screen Solutions",
    "86expf9ny": "PHASE 4 — Design System & Core Branding Updates",
    "86expvbtt": "PHASE 5 — Full App Design",
    "86exq5x92": "PHASE 6 — Prototype & Mid-Review",
    "86expf9q9": "PHASE 7 — Final Review, Handoff, Other services"
}

def api_call(method, path, body=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  HTTP {e.code}: {err[:200]}")
        return {}

def update_task_name(task_id, new_name):
    print(f"Updating task [{task_id}] name to '{new_name}'...")
    resp = api_call("PUT", f"/task/{task_id}", {"name": new_name})
    if resp.get("id"):
        print(f"  SUCCESS: [{task_id}] updated successfully.")
    else:
        print(f"  FAIL: [{task_id}] failed to update. Response: {resp}")
    time.sleep(0.35)

def main():
    print("=== STARTING CLICKUP TASK RENAMING (GROUP -> PHASE) ===")
    for task_id, new_name in RENAME_MAP.items():
        update_task_name(task_id, new_name)
    print("=== ALL RENAMINGS COMPLETED ===")

if __name__ == "__main__":
    main()
