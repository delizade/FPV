#!/usr/bin/env python3
import urllib.request
import json

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
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def main():
    print("Fetching tasks from list...")
    res = api_call(f"/list/{LIST_ID}/task?subtasks=true&include_closed=true")
    tasks = res.get("tasks", [])
    
    page = 1
    while True:
        next_res = api_call(f"/list/{LIST_ID}/task?subtasks=true&include_closed=true&page={page}")
        next_tasks = next_res.get("tasks", [])
        if not next_tasks:
            break
        tasks.extend(next_tasks)
        page += 1
        
    print(f"Total tasks: {len(tasks)}")
    for t in tasks:
        # Check if "Roadmap" or "Production" in name
        if "roadmap" in t["name"].lower() or "production" in t["name"].lower():
            print(f"- {t['name']} (ID: {t['id']})")
        # Let's also print top level tasks that might contain subtasks
        if not t.get("parent"):
            print(f"Top-level: {t['name']} (ID: {t['id']})")

if __name__ == "__main__":
    main()
