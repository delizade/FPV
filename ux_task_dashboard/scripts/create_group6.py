#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import time

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
LIST_ID = "901818298165"
BASE = "https://api.clickup.com/api/v2"
PARENT_ID = "86expucex"  # Product UX Improvements & UI Redesign

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
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

def create_task(name, description, time_minutes, parent_id=None):
    body = {
        "name": name,
        "description": description,
        "time_estimate": time_minutes * 60 * 1000,
    }
    if parent_id:
        body["parent"] = parent_id
    resp = api_call("POST", f"/list/{LIST_ID}/task", body)
    task_id = resp.get("id", "")
    if task_id:
        print(f"    OK [{task_id}] {name[:60]} ({time_minutes//60}h)")
    else:
        print(f"    FAIL: {name[:60]} — {resp}")
    time.sleep(0.35)
    return task_id

def main():
    print("Creating GROUP 6 — Prototype & Mid-Review under main task...")
    G6 = create_task(
        "GROUP 6 — Prototype & Mid-Review",
        "Interactive prototype build and mid-project client presentation. Second revision round based on client feedback on the full design.",
        1020,
        PARENT_ID
    )
    if G6:
        create_task(
            "Interactive Prototype Build",
            "Link all screens into a clickable prototype covering primary user flows: login, home, order creation wizard, order details, account settings, and about/services.",
            480,
            G6
        )
        create_task(
            "[REVISION 2] Mid-Project Client Presentation & Feedback",
            "Present the full prototype to the client. Walk through all main flows. Collect prioritised feedback and document all requested changes.",
            180,
            G6
        )
        create_task(
            "Screen Revisions Based on Mid-Review Feedback",
            "Apply all changes from the mid-review. Update screens, components and prototype links accordingly.",
            360,
            G6
        )
    print("Done creating GROUP 6.")

if __name__ == "__main__":
    main()
