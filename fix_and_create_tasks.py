#!/usr/bin/env python3
"""
ClickUp FPV — Complete task structure fixer & creator
1. Reparent Current App Structure children (6 existing sections)
2. Reparent GROUP 1-3 orphan tasks/subtasks 
3. Create GROUP 4-7 from scratch
"""
import urllib.request
import urllib.error
import json
import time

TOKEN = "pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
LIST_ID = "901818298165"
BASE = "https://api.clickup.com/api/v2"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# Known IDs from audit
CAS_ID = "86expf9ee"   # Current App Structure

# Existing 6 section parents to move under CAS
SECTION_IDS = [
    "86expf7cg",  # 1. Auth
    "86expf7cq",  # 2. Home
    "86expf7d0",  # 3. Account
    "86expf7dk",  # 4. Logistics
    "86expf7e6",  # 5. Order Now
    "86expf7ek",  # 6. About
]

# GROUP 1 orphans
G1_ID = "86expf9fd"
G1_CHILDREN = {
    "86expf9fg": "Sector & Competitor Research",
    "86expf9fm": "Mood Board & Visual Direction",
    "86expf9ft": "General Design Concept Definition",
}

# GROUP 2 orphans
G2_ID = "86expf9fy"
G2_CHILDREN = {
    "86expf9g0": "Design Proposal A",
    "86expf9g2": "Design Proposal B",
    "86expf9g3": "[REVISION 1] Client Feedback & Concept Selection",
    "86expf9g6": "Concept Revision & Refinement",
}

# GROUP 3 orphans
G3_ID = "86expf9g8"
G3_CHILDREN = {
    "86expf9gb": "UX Audit — Current App Flow Review",
    "86expf9gg": "UX Solutions — Screen-by-Screen",
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


def reparent(task_id, parent_id):
    resp = api_call("PUT", f"/task/{task_id}", {"parent": parent_id})
    name = resp.get("name", task_id)[:50]
    if resp.get("id"):
        print(f"    Moved [{task_id}] {name} -> {parent_id}")
    else:
        print(f"    FAIL reparent {task_id}: {resp}")
    time.sleep(0.3)


# ─────────────────────────────────────────────
print("\n=== STEP 1: Reparent 6 existing sections under 'Current App Structure' ===")
for sid in SECTION_IDS:
    reparent(sid, CAS_ID)

# ─────────────────────────────────────────────
print("\n=== STEP 2: Reparent GROUP 1 children ===")
for cid in G1_CHILDREN:
    reparent(cid, G1_ID)

print("\n=== STEP 3: Reparent GROUP 2 children ===")
for cid in G2_CHILDREN:
    reparent(cid, G2_ID)

print("\n=== STEP 4: Reparent GROUP 3 children ===")
for cid in G3_CHILDREN:
    reparent(cid, G3_ID)

# ─────────────────────────────────────────────
# GROUP 3 — Missing subtasks (Layout + Onboarding)
print("\n=== STEP 5: Add missing GROUP 3 subtasks ===")
create_task(
    "Layout & Component Proposals — Screen-by-Screen",
    "Annotated layout proposals for every screen: content hierarchy, component choice, grid usage, spacing, and state coverage (empty, loading, error).",
    480, G3_ID
)
create_task(
    "Onboarding Flow Design — Splash + Feature Walkthrough",
    "Splash screen and multi-step onboarding carousel showcasing key app features with illustrations or screenshots, concluding with a Get Started CTA button.",
    180, G3_ID
)

# ─────────────────────────────────────────────
print("\n=== STEP 6: Create GROUP 4 — Design System & Brand ===")
G4 = create_task(
    "GROUP 4 — Design System & Brand",
    "Full brand and design system work: logo, branding renewal, component library, icon set and AI-assisted imagery.",
    1920
)
if G4:
    create_task("App Logo Design",
        "Redesign the FPV application logo. Explore mark + wordmark combinations. Deliver final logo in all required formats and colour variants.",
        480, G4)
    create_task("Branding Renewal",
        "Update full brand identity: primary and secondary colour palette, typography system, brand tone and usage guidelines aligned with the new design direction.",
        300, G4)
    create_task("Design System Setup — Tokens, Components & Styles",
        "Build the full design system: colour tokens, type scale, spacing scale, elevation, grid, and all reusable UI components (buttons, cards, inputs, modals, badges, nav bars etc.).",
        480, G4)
    create_task("Icon System Design",
        "Design a consistent custom icon set covering all functional icons used across the app: navigation, actions, status indicators, and service category icons.",
        360, G4)
    create_task("AI-Assisted Image Generation — Service Visuals & Imagery",
        "Generate high-quality visuals using AI tools for each service category (Marketable, As-Built, 3D & Media, Add-Ons), onboarding illustrations, hero banners and in-app promotional areas.",
        300, G4)

# ─────────────────────────────────────────────
print("\n=== STEP 7: Create GROUP 5 — Full Screen Design ===")
G5 = create_task(
    "GROUP 5 — Full Screen Design",
    "High-fidelity UI design for every screen in the app, using the locked design system and approved UX solutions.",
    1980
)
if G5:
    create_task("Authentication & Onboarding Screens",
        "Login, registration, forgot password, splash screen, and all onboarding walkthrough step screens.",
        300, G5)
    create_task("Home Dashboard Screen",
        "Main dashboard with welcome card, order summary grid, active orders list, upcoming appointments card and promotional banner.",
        240, G5)
    create_task("Account Settings Screens",
        "Profile menu, profile editor, orders list, autofill preferences, wallet and add card modal, favorites, feedback hub and submit feedback modal.",
        360, G5)
    create_task("Order Details Screens",
        "Active order detail (Pending Scan), scheduled order (Awaiting Appointment), and completed/closed order screen including all accordion drawer states.",
        300, G5)
    create_task("Order Now Wizard Screens",
        "Order selection hub, all 11 steps of the Marketable Plan wizard, Search Inventory flow, and all 4 tabs of the checkout wizard.",
        480, G5)
    create_task("About / Services / Pricing Screens",
        "About main page, service catalog (all 4 category tabs), individual service detail pages, all 4 pricing grid tables, regional contact directory, and chat placeholder screen.",
        300, G5)

# ─────────────────────────────────────────────
print("\n=== STEP 8: Create GROUP 6 — Prototype & Mid-Review ===")
G6 = create_task(
    "GROUP 6 — Prototype & Mid-Review",
    "Interactive prototype build and mid-project client presentation. Second revision round based on client feedback on the full design.",
    1020
)
if G6:
    create_task("Interactive Prototype Build",
        "Link all screens into a clickable prototype covering primary user flows: login, home, order creation wizard, order details, account settings, and about/services.",
        480, G6)
    create_task("[REVISION 2] Mid-Project Client Presentation & Feedback",
        "Present the full prototype to the client. Walk through all main flows. Collect prioritised feedback and document all requested changes.",
        180, G6)
    create_task("Screen Revisions Based on Mid-Review Feedback",
        "Apply all changes from the mid-review. Update screens, components and prototype links accordingly.",
        360, G6)

# ─────────────────────────────────────────────
print("\n=== STEP 9: Create GROUP 7 — Final Review & Handoff ===")
G7 = create_task(
    "GROUP 7 — Final Review & Handoff",
    "Final polish pass, client sign-off presentation, last-round revisions, and complete developer handoff package.",
    780
)
if G7:
    create_task("Final Design Polish & Consistency Check",
        "Full pass over every screen: spacing consistency, type hierarchy, component alignment, colour correctness, and edge case state coverage.",
        240, G7)
    create_task("[REVISION 3] Final Client Presentation & Sign-off",
        "Present polished design to client for final approval. Collect last feedback and obtain formal sign-off to proceed to handoff.",
        120, G7)
    create_task("Final Revisions",
        "Implement last-round client corrections. Verify all changes are consistent with the design system.",
        180, G7)
    create_task("Developer Handoff — Assets & Specs",
        "Export all assets (icons, images, illustrations). Annotate screens with measurements, component specs, interaction notes and token references. Deliver handoff-ready design file.",
        240, G7)

print("\n=== ALL DONE ===")
print(f"""
Summary:
  Current App Structure:  {CAS_ID}
  GROUP 1 (Research):     {G1_ID}  — 7h
  GROUP 2 (Proposals):    {G2_ID}  — 25h
  GROUP 3 (UX Analysis):  {G3_ID}  — 21h
  GROUP 4 (Brand):        {G4}  — 32h
  GROUP 5 (Screen Design):{G5}  — 33h
  GROUP 6 (Prototype):    {G6}  — 17h
  GROUP 7 (Handoff):      {G7}  — 13h
  Total estimated: ~148 hours
""")
