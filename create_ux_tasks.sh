#!/bin/bash
# ClickUp FPV - UX Redesign Task Creator
# List: Floor Plan Visuals Mobile App Design (901818298165)

TOKEN="pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
LIST_ID="901818298165"
BASE="https://api.clickup.com/api/v2"

# Existing 6 section task IDs (created previously)
EXISTING_1="86expf7cg"   # Auth & Onboarding
EXISTING_2="86expf7cq"   # Home Dashboard
EXISTING_3="86expf7d0"   # Account Settings
EXISTING_4="86expf7dk"   # Project Logistics
EXISTING_5="86expf7e6"   # Order Now
EXISTING_6="86expf7ek"   # About/Catalog

# Helper: create task with optional parent, returns ID
create_task() {
  local list_id="$1"
  local name="$2"
  local desc="$3"
  local time_min="$4"
  local parent="$5"
  local time_ms=$(( time_min * 60 * 1000 ))

  if [ -n "$parent" ]; then
    RESP=$(curl -s -X POST "$BASE/list/$list_id/task" \
      -H "Authorization: $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"name\":$(echo "$name" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))"),\"description\":$(echo "$desc" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))"),\"time_estimate\":$time_ms,\"parent\":\"$parent\"}")
  else
    RESP=$(curl -s -X POST "$BASE/list/$list_id/task" \
      -H "Authorization: $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"name\":$(echo "$name" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))"),\"description\":$(echo "$desc" | python3 -c "import sys,json;print(json.dumps(sys.stdin.read().strip()))"),\"time_estimate\":$time_ms}")
  fi
  echo "$RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id','ERR:'+str(d)[:120)))"
}

# Helper: update task parent
reparent_task() {
  local task_id="$1"
  local parent_id="$2"
  curl -s -X PUT "$BASE/task/$task_id" \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"parent\":\"$parent_id\"}" > /dev/null
  echo "  Reparented $task_id -> $parent_id"
}

echo "======================================================"
echo "  FPV App — Full Task Structure Setup"
echo "======================================================"
echo ""

# ======================================================
# STEP 1: Create "Current App Structure" and move existing tasks under it
# ======================================================
echo ">>> STEP 1: Creating 'Current App Structure' parent task..."
CAS=$(create_task "$LIST_ID" "Current App Structure" "Complete screen-by-screen breakdown of the existing FPV mobile app. Covers all pages, sub-pages, modals, fields, and navigation flows as analysed from app screenshots." 0 "")
echo "  ID: $CAS"
sleep 0.5

echo "  Moving existing 6 section tasks under 'Current App Structure'..."
reparent_task "$EXISTING_1" "$CAS"
sleep 0.3
reparent_task "$EXISTING_2" "$CAS"
sleep 0.3
reparent_task "$EXISTING_3" "$CAS"
sleep 0.3
reparent_task "$EXISTING_4" "$CAS"
sleep 0.3
reparent_task "$EXISTING_5" "$CAS"
sleep 0.3
reparent_task "$EXISTING_6" "$CAS"
sleep 0.5
echo "  Done. All 6 sections now live under Current App Structure."
echo ""

# ======================================================
# GROUP 1: Research & Direction  (~7h total)
# ======================================================
echo ">>> GROUP 1: Research & Direction..."
G1=$(create_task "$LIST_ID" "GROUP 1 — Research & Direction" "Initial research phase: sector trends, references, and defining the overall design direction before any screen work begins." 420 "")
echo "  ID: $G1"
sleep 0.4

T=$(create_task "$LIST_ID" "Sector & Competitor Research" "Survey modern real estate / prop-tech mobile apps. Identify best-in-class UX patterns, visual trends, and opportunities for differentiation. Produce a short findings brief." 180 "$G1")
echo "  Subtask: $T (3h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Mood Board & Visual Direction" "Curate visual references: UI styles, color palettes, typography pairings, photography and illustration approaches relevant to the FPV brand." 120 "$G1")
echo "  Subtask: $T (2h)"
sleep 0.3

T=$(create_task "$LIST_ID" "General Design Concept Definition" "Synthesise research into a single-page design brief: tone of voice, visual personality, target feel, and key design principles to guide all subsequent decisions." 120 "$G1")
echo "  Subtask: $T (2h)"
sleep 0.4
echo ""

# ======================================================
# GROUP 2: Initial Design Proposals & Revision 1  (~25h total)
# ======================================================
echo ">>> GROUP 2: Initial Design Proposals..."
G2=$(create_task "$LIST_ID" "GROUP 2 — Initial Design Proposals" "First round of design concepts presented to the client. Two alternative directions explored; one selected and refined after client feedback." 1500 "")
echo "  ID: $G2"
sleep 0.4

T=$(create_task "$LIST_ID" "Design Proposal A — Concept 1" "Full design concept A applied to key screens (Home, Order Now hub, a detail screen). Presents a distinct visual language, color palette and component feel." 480 "$G2")
echo "  Subtask: $T (8h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Design Proposal B — Concept 2" "Full design concept B as an alternative direction. Same key screens as Proposal A to allow direct side-by-side comparison by the client." 480 "$G2")
echo "  Subtask: $T (8h)"
sleep 0.3

T=$(create_task "$LIST_ID" "[REVISION 1] Client Feedback & Concept Selection" "Present both proposals to the client. Collect structured feedback, align on the chosen direction, and document change requests. Output: approved concept brief + revision notes." 120 "$G2")
echo "  Subtask: $T (2h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Concept Revision & Refinement" "Apply revision notes to the selected concept. Refine typography, spacing, colour, and component style until the design language is locked and approved." 300 "$G2")
echo "  Subtask: $T (5h)"
sleep 0.4
echo ""

# ======================================================
# GROUP 3: UX Analysis & Screen Solutions  (~21h total)
# ======================================================
echo ">>> GROUP 3: UX Analysis & Screen Solutions..."
G3=$(create_task "$LIST_ID" "GROUP 3 — UX Analysis & Screen Solutions" "Deep-dive into every app screen to identify UX problems and define layout and component solutions before full visual design begins." 1260 "")
echo "  ID: $G3"
sleep 0.4

T=$(create_task "$LIST_ID" "UX Audit — Current App Flow Review" "Screen-by-screen review of the existing FPV app. Flag friction points, confusing flows, hierarchy issues, missing feedback states, and navigation gaps." 240 "$G3")
echo "  Subtask: $T (4h)"
sleep 0.3

T=$(create_task "$LIST_ID" "UX Solutions — Screen-by-Screen" "For each identified pain point, define the UX solution: restructured flow, simplified interaction, clearer labelling, or removed friction step." 360 "$G3")
echo "  Subtask: $T (6h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Layout & Component Proposals — Screen-by-Screen" "Annotated layout proposals for every screen: content hierarchy, component choice, grid usage, spacing, and state coverage (empty, loading, error)." 480 "$G3")
echo "  Subtask: $T (8h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Onboarding Flow Design — Splash + Feature Walkthrough" "Design splash screen and multi-step onboarding carousel showcasing key app features with illustrations or screenshots, concluding with a Get Started CTA button." 180 "$G3")
echo "  Subtask: $T (3h)"
sleep 0.4
echo ""

# ======================================================
# GROUP 4: Design System & Brand  (~32h total)
# ======================================================
echo ">>> GROUP 4: Design System & Brand..."
G4=$(create_task "$LIST_ID" "GROUP 4 — Design System & Brand" "Full brand and design system work: logo, branding renewal, component library, icon set and AI-assisted imagery." 1920 "")
echo "  ID: $G4"
sleep 0.4

T=$(create_task "$LIST_ID" "App Logo Design" "Redesign the FPV application logo. Explore mark + wordmark combinations. Deliver final logo in all required formats and colour variants." 480 "$G4")
echo "  Subtask: $T (8h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Branding Renewal" "Update full brand identity: primary and secondary colour palette, typography system, brand tone and usage guidelines aligned with the new design direction." 300 "$G4")
echo "  Subtask: $T (5h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Design System Setup — Tokens, Components & Styles" "Build the full design system: colour tokens, type scale, spacing scale, elevation, grid, and all reusable components (buttons, cards, inputs, modals, badges, nav bars etc.)." 480 "$G4")
echo "  Subtask: $T (8h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Icon System Design" "Design a consistent custom icon set covering all functional icons used across the app: navigation, actions, status indicators, and service category icons." 360 "$G4")
echo "  Subtask: $T (6h)"
sleep 0.3

T=$(create_task "$LIST_ID" "AI-Assisted Image Generation — Service Visuals & Imagery" "Use AI tools to generate high-quality visuals for: each service category (Marketable, As-Built, 3D & Media, Add-Ons), onboarding illustrations, hero banners and in-app promotional areas." 300 "$G4")
echo "  Subtask: $T (5h)"
sleep 0.4
echo ""

# ======================================================
# GROUP 5: Full Screen Design  (~32h total)
# ======================================================
echo ">>> GROUP 5: Full Screen Design..."
G5=$(create_task "$LIST_ID" "GROUP 5 — Full Screen Design" "High-fidelity UI design for every screen in the app, using the locked design system and approved UX solutions." 1980 "")
echo "  ID: $G5"
sleep 0.4

T=$(create_task "$LIST_ID" "Authentication & Onboarding Screens" "Login, registration, forgot password, splash, and all onboarding walkthrough step screens." 300 "$G5")
echo "  Subtask: $T (5h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Home Dashboard Screen" "Main dashboard with welcome card, order summary grid, active orders list, upcoming appointments card and promo banner." 240 "$G5")
echo "  Subtask: $T (4h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Account Settings Screens" "Profile menu, profile editor, orders list, autofill preferences, wallet + add card modal, favorites, feedback hub + submit modal." 360 "$G5")
echo "  Subtask: $T (6h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Order Details Screens" "Active order detail (Pending Scan), scheduled order detail (Awaiting Appointment), and completed/closed order screen including all accordion drawer states." 300 "$G5")
echo "  Subtask: $T (5h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Order Now Wizard Screens" "Order selection hub, all 11 steps of the Marketable Plan wizard, Search Inventory flow, and all 4 tabs of the checkout wizard." 480 "$G5")
echo "  Subtask: $T (8h)"
sleep 0.3

T=$(create_task "$LIST_ID" "About / Services / Pricing Screens" "About main page, service catalog (all 4 tabs), individual service detail pages, pricing grids screen (all 4 pricing tables), regional contact directory, chat placeholder." 300 "$G5")
echo "  Subtask: $T (5h)"
sleep 0.4
echo ""

# ======================================================
# GROUP 6: Prototype & Mid-Review  (~17h total)
# ======================================================
echo ">>> GROUP 6: Prototype & Mid-Review..."
G6=$(create_task "$LIST_ID" "GROUP 6 — Prototype & Mid-Review" "Interactive prototype build and mid-project client presentation. Second revision round based on client feedback on the full design." 1020 "")
echo "  ID: $G6"
sleep 0.4

T=$(create_task "$LIST_ID" "Interactive Prototype Build" "Link all screens into a clickable prototype covering the primary user flows: login, home, order creation wizard, order details, account settings, and about/services." 480 "$G6")
echo "  Subtask: $T (8h)"
sleep 0.3

T=$(create_task "$LIST_ID" "[REVISION 2] Mid-Project Client Presentation & Feedback" "Present the full prototype to the client. Walk through all main flows. Collect prioritised feedback. Document all requested changes with screenshots and notes." 180 "$G6")
echo "  Subtask: $T (3h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Screen Revisions Based on Mid-Review Feedback" "Apply all changes from the mid-review. Update screens, components and prototype links accordingly." 360 "$G6")
echo "  Subtask: $T (6h)"
sleep 0.4
echo ""

# ======================================================
# GROUP 7: Final Review & Handoff  (~13h total)
# ======================================================
echo ">>> GROUP 7: Final Review & Handoff..."
G7=$(create_task "$LIST_ID" "GROUP 7 — Final Review & Handoff" "Final polish pass, client sign-off presentation, last-round revisions, and complete developer handoff package." 780 "")
echo "  ID: $G7"
sleep 0.4

T=$(create_task "$LIST_ID" "Final Design Polish & Consistency Check" "Full pass over every screen: spacing consistency, type hierarchy, component alignment, colour correctness, and edge case state coverage." 240 "$G7")
echo "  Subtask: $T (4h)"
sleep 0.3

T=$(create_task "$LIST_ID" "[REVISION 3] Final Client Presentation & Sign-off" "Present polished design to client for final approval. Collect last feedback. Obtain formal sign-off to proceed to handoff." 120 "$G7")
echo "  Subtask: $T (2h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Final Revisions" "Implement last-round client corrections. Verify all changes are consistent with the design system." 180 "$G7")
echo "  Subtask: $T (3h)"
sleep 0.3

T=$(create_task "$LIST_ID" "Developer Handoff — Assets & Specs" "Export all assets (icons, images, illustrations). Annotate screens with measurements, component specs, interaction notes, and token references. Deliver handoff-ready design file." 240 "$G7")
echo "  Subtask: $T (4h)"
sleep 0.4
echo ""

echo "======================================================"
echo "  ALL DONE"
echo "======================================================"
echo ""
echo "Current App Structure parent: $CAS"
echo ""
echo "New UX/UI Groups created:"
echo "  GROUP 1 — Research & Direction:          $G1  (~7h)"
echo "  GROUP 2 — Initial Design Proposals:      $G2  (~25h)"
echo "  GROUP 3 — UX Analysis & Screen Solutions:$G3  (~21h)"
echo "  GROUP 4 — Design System & Brand:         $G4  (~32h)"
echo "  GROUP 5 — Full Screen Design:            $G5  (~32h)"
echo "  GROUP 6 — Prototype & Mid-Review:        $G6  (~17h)"
echo "  GROUP 7 — Final Review & Handoff:        $G7  (~13h)"
echo ""
echo "  Total estimated project time: ~147 hours"
