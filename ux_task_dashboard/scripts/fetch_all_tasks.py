#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import os

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
LIST_ID = "901818298165"
BASE = "https://api.clickup.com/api/v2"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def api_call(path):
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"HTTP {e.code}: {err[:200]}")
        return {}

def main():
    print("Fetching tasks from list...")
    # Page 0
    res = api_call(f"/list/{LIST_ID}/task?subtasks=true&include_closed=true")
    tasks = res.get("tasks", [])
    
    # ClickUp lists might have pagination. Let's fetch page 1, 2, 3 as well just in case.
    page = 1
    while True:
        next_res = api_call(f"/list/{LIST_ID}/task?subtasks=true&include_closed=true&page={page}")
        next_tasks = next_res.get("tasks", [])
        if not next_tasks:
            break
        tasks.extend(next_tasks)
        print(f"Fetched page {page}, got {len(next_tasks)} more tasks.")
        page += 1
        
    print(f"Total tasks fetched: {len(tasks)}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dump_path = os.path.join(os.path.dirname(script_dir), "tasks_dump.json")
    with open(dump_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    print("Saved tasks_dump.json")

if __name__ == "__main__":
    main()
