#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import time

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
BASE = "https://api.clickup.com/api/v2"
LIST_ID = "901818298165"
ROADMAP_TASK_ID = "86exrfkuu"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def api_call(method, path, body=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    
    retries = 3
    while retries > 0:
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("  [Rate Limit Hit] Sleeping 10s...")
                time.sleep(10)
                retries -= 1
            else:
                err = e.read().decode()
                print(f"  HTTP {e.code}: {err[:200]}")
                return {}
        except Exception as ex:
            print(f"  Connection Error: {ex}")
            time.sleep(2)
            retries -= 1
    return {}

def main():
    print("Fetching all tasks and subtasks from ClickUp...")
    # Fetch all tasks in the list
    tasks = []
    page = 0
    while True:
        res = api_call("GET", f"/list/{LIST_ID}/task?subtasks=true&include_closed=true&page={page}")
        page_tasks = res.get("tasks", [])
        if not page_tasks:
            break
        tasks.extend(page_tasks)
        print(f"Fetched page {page}, got {len(page_tasks)} tasks.")
        page += 1
        
    print(f"Total tasks fetched: {len(tasks)}")
    
    # We want to identify the main task and all subtasks of the Roadmap task
    roadmap_tasks = []
    
    # Helper to check if a task belongs to the roadmap hierarchy
    # A task belongs if its ID is ROADMAP_TASK_ID, or its parent's ID is in the set, etc.
    roadmap_ids = {ROADMAP_TASK_ID}
    
    # Since subtasks can be nested multiple levels, we loop to find all descendants
    added_any = True
    while added_any:
        added_any = False
        for t in tasks:
            tid = t["id"]
            if tid in roadmap_ids:
                continue
            parent = t.get("parent")
            if parent and parent in roadmap_ids:
                roadmap_ids.add(tid)
                added_any = True
                
    # Now collect all tasks in the roadmap hierarchy
    for t in tasks:
        if t["id"] in roadmap_ids:
            roadmap_tasks.append(t)
            
    print(f"Found {len(roadmap_tasks)} tasks in the Roadmap hierarchy:")
    for t in roadmap_tasks:
        print(f" - {t['name']} (ID: {t['id']}, Estimate: {t.get('time_estimate')})")
        
    print("\nStarting to clear time estimates (setting to null) in ClickUp...")
    success_count = 0
    for idx, t in enumerate(roadmap_tasks):
        tid = t["id"]
        tname = t["name"]
        print(f"[{idx+1}/{len(roadmap_tasks)}] Clearing estimate for '{tname}' (ID: {tid})...")
        # ClickUp API: PUT /task/{task_id} with {"time_estimate": None} (which is null in JSON)
        # Note: If that fails or does not clear it, we could try {"time_estimate": 0}. Let's try null first.
        res = api_call("PUT", f"/task/{tid}", {"time_estimate": None})
        if res.get("id"):
            print("   SUCCESS.")
            success_count += 1
        else:
            print("   FAILED.")
        time.sleep(0.5)
        
    print(f"\nCompleted! Successfully cleared {success_count}/{len(roadmap_tasks)} task estimates in ClickUp.")

if __name__ == "__main__":
    main()
