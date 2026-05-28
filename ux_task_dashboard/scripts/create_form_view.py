#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import sys

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
LIST_ID = "901818298165"
BASE = "https://api.clickup.com/api/v2"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def create_form_view():
    print("Creating native Feedback Form view under ClickUp list...")
    url = f"{BASE}/list/{LIST_ID}/view"
    body = {
        "name": "feedback form",
        "type": "form",
        "form_settings": {
            "display": {
                "style": "simple",
                "theme": "light",
                "hide_branding": False,
                "allow_multiple_submits": False
            },
            "fields": []
        }
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read())
            view_id = res.get("view", {}).get("id", "")
            public_url = res.get("view", {}).get("public_url", "")
            print(f"✅ Success! Form View created: {res.get('view', {}).get('name')} (ID: {view_id})")
            print(f"🔗 Public Form URL: {public_url}")
            return True, res
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"❌ Failed to create form view: HTTP {e.code} - {err[:500]}")
        return False, err

if __name__ == "__main__":
    create_form_view()
