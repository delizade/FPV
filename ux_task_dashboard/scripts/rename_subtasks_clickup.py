#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import time
import os

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
BASE = "https://api.clickup.com/api/v2"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def api_call(method, path, body=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    
    # Handle rate-limit retry loop
    retries = 3
    while retries > 0:
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Rate limit hit: sleep and retry
                print("  [Rate Limit Hit] ClickUp API throttled. Sleeping 12 seconds...")
                time.sleep(12)
                retries -= 1
            else:
                err = e.read().decode()
                print(f"  HTTP {e.code}: {err[:200]}")
                return {}
        except Exception as ex:
            print(f"  Connection Error: {ex}")
            time.sleep(2)
            retries -= 1
            
    print("  [Failed after retries]")
    return {}

def update_task_name(task_id, new_name):
    path = f"/task/{task_id}"
    resp = api_call("PUT", path, {"name": new_name})
    if resp.get("id"):
        return True
    return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    preview_path = os.path.join(script_dir, "renaming_preview.json")
    
    if not os.path.exists(preview_path):
        print(f"Error: {preview_path} not found. Run preview_renaming.py first.")
        return
        
    with open(preview_path, "r", encoding="utf-8") as f:
        actions = json.load(f)
        
    total = len(actions)
    print(f"=== STARTING CLICKUP SUBTASK RENAMING ({total} tasks) ===")
    print("Each call has a safety delay of 0.65 seconds to respect rate limits.")
    print("========================================================\n")
    
    success_count = 0
    fail_count = 0
    
    for idx, a in enumerate(actions):
        tid = a["id"]
        old = a["old_name"]
        new = a["new_name"]
        
        print(f"[{idx+1}/{total}] Renaming [{tid}]...")
        print(f"  OLD: {old}")
        print(f"  NEW: {new}")
        
        success = update_task_name(tid, new)
        if success:
            print("  SUCCESS.")
            success_count += 1
        else:
            print("  FAILED.")
            fail_count += 1
            
        # Safety sleep delay
        time.sleep(0.65)
        
    print("\n========================================================")
    print("=== CLICKUP SUBTASK RENAMING PROCESS COMPLETED ===")
    print(f"Total: {total} | Success: {success_count} | Failed: {fail_count}")
    print("========================================================")

if __name__ == "__main__":
    main()
