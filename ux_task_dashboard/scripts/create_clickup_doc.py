#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import os
import sys

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
WORKSPACE_ID = "90182683899"
BASE_V3 = "https://api.clickup.com/api/v3"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def api_call_v3(method, path, body=None):
    url = f"{BASE_V3}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"HTTP {e.code}: {err[:400]}")
        return {"error": err}

def main():
    print("Attempting to create a Workspace Doc via ClickUp v3 API...")
    
    # We will format the content using Markdown block-styled text as requested:
    # 1. H4 questions (####)
    # 2. Numerical listing using actual Markdown numeric lists (1., 2.)
    # 3. Two blank lines under each question for client notes
    doc_content = (
        "# Floor Plan Visuals Mobile App Design — Client Feedback & Discovery Survey\n\n"
        "This document is prepared to align on branding, design directions, user feedback, and operational priorities. Please enter your responses directly below each question:\n\n"
        "1. #### Please share your current brand assets/documents, including the currently used wordmark/logo, emblem/symbol, colours, typography, or any existing brand-related materials.\n\n\n\n"
        "2. #### Before starting the main UX/UI production process, I believe we should first review and rework the currently used wordmark/logo and emblem structure in order to establish a stronger and more consistent visual foundation for the redesign. Do you have any concerns, limitations, or preferences regarding how far the current branding can be updated, modernized, or visually expanded?\n\n\n\n"
        "3. #### Do you currently have any specific visual style or design direction in mind regarding the redesign or are there any apps, platforms, products, or digital experiences that you personally like, admire, or would want the redesign direction to feel closer to in terms of quality, usability, atmosphere, or overall presentation?\n\n\n\n"
        "4. #### Could you please share your current competitors in order of importance from your perspective?\n\n\n\n"
        "5. #### If you currently maintain any list of customer feedback, complaints, recurring requests, or app-related issues collected from users, please share them if possible.\n\n\n\n"
        "6. #### Beyond the previously discussed needs and requests, I would appreciate it if you could internally discuss the app together with your full team and share any additional thoughts, concerns, priorities, or operational observations you collectively have regarding the current experience.\n\n\n\n"
        "7. #### Which sections, workflows, or operational areas of the app do you consider the most critical, valuable, or important from both business and user perspectives? If possible, please also prioritize them in order of importance.\n\n\n\n"
        "8. #### Who will primarily be responsible for reviewing and approving design decisions throughout the project?\n\n\n\n"
    )

    body = {
        "name": "Floor Plan Visuals Mobile App Design - Feedback Form (Wiki)",
        "content": doc_content,
        "create_page": True
    }
    
    # Let's try creating a doc under the workspace
    resp = api_call_v3("POST", f"/workspaces/{WORKSPACE_ID}/docs", body)
    
    if "error" in resp:
        print(f"❌ Failed to create Doc: {resp['error']}")
        sys.exit(1)
        
    doc_id = resp.get("id", "")
    if doc_id:
        print(f"✅ Success! Created Workspace Doc: {resp.get('name')} (ID: {doc_id})")
        print(f"🔗 ClickUp URL: {resp.get('url') or f'https://app.clickup.com/d/{doc_id}'}")
    else:
        print(f"⚠️ Doc created but no ID returned. Response: {resp}")

if __name__ == "__main__":
    main()
