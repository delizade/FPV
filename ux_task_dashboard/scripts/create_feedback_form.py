#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import os
import sys

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
LIST_ID = "901818298165"
BASE = "https://api.clickup.com/api/v2"
PARENT_ID = "86expf9q2"  # 7.3 — Survey Preparation, Workflow Questions & Feedback Structures

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
        print(f"HTTP {e.code}: {err[:200]}")
        return {}

def main():
    print("Creating the Feedback Form / Survey task in ClickUp...")
    
    survey_description = (
        "# Floor Plan Visuals Mobile App Design — Client Feedback & Discovery Survey\n\n"
        "This task represents the discovery survey and feedback form prepared to align on branding, design directions, user feedback, and operational priorities. Please review and respond directly to the following questions:\n\n"
        "### 1. Brand Assets & Guidelines\n"
        "Please share your current brand assets/documents, including the currently used wordmark/logo, emblem/symbol, colours, typography, or any existing brand-related materials.\n\n"
        "### 2. Branding Rework & Scope Limitations\n"
        "Before starting the main UX/UI production process, I believe we should first review and rework the currently used wordmark/logo and emblem structure in order to establish a stronger and more consistent visual foundation for the redesign. Do you have any concerns, limitations, or preferences regarding how far the current branding can be updated, modernized, or visually expanded?\n\n"
        "### 3. Visual & Aesthetic Preferences\n"
        "Do you currently have any specific visual style or design direction in mind regarding the redesign or are there any apps, platforms, products, or digital experiences that you personally like, admire, or would want the redesign direction to feel closer to in terms of quality, usability, atmosphere, or overall presentation?\n\n"
        "### 4. Competitor Analysis\n"
        "Could you please share your current competitors in order of importance from your perspective?\n\n"
        "### 5. Existing Customer Feedback & Issues\n"
        "If you currently maintain any list of customer feedback, complaints, recurring requests, or app-related issues collected from users, please share them if possible.\n\n"
        "### 6. Team Feedback & Operational Observations\n"
        "Beyond the previously discussed needs and requests, I would appreciate it if you could internally discuss the app together with your full team and share any additional thoughts, concerns, priorities, or operational observations you collectively have regarding the current experience.\n\n"
        "### 7. Critical Sections & Operational Workflows\n"
        "Which sections, workflows, or operational areas of the app do you consider the most critical, valuable, or important from both business and user perspectives? If possible, please also prioritize them in order of importance.\n\n"
        "### 8. Project Reviewers & Approvers\n"
        "Who will primarily be responsible for reviewing and approving design decisions throughout the project?\n"
    )

    body = {
        "name": "Feedback Form & Survey Questions",
        "description": survey_description,
        "parent": PARENT_ID
    }
    
    resp = api_call("POST", f"/list/{LIST_ID}/task", body)
    task_id = resp.get("id", "")
    
    if task_id:
        print(f"✅ Success! Created ClickUp task: {resp.get('name')} (ID: {task_id})")
        print(f"🔗 ClickUp URL: {resp.get('url')}")
    else:
        print(f"❌ Failed to create task. Response: {resp}")
        sys.exit(1)

if __name__ == "__main__":
    main()
