#!/bin/bash
# ClickUp FPV App Structure Task Creator
# List ID: 901818298165 - Floor Plan Visuals Mobile App Design

TOKEN="pk_72027303_H9RE35Y52CJFDDWJBFR6SC5K7ACRB3QE"
LIST_ID="901818298165"
BASE="https://api.clickup.com/api/v2"

# Helper: Create a task, return task ID
# Usage: create_task "LIST_ID_or_PARENT" "name" "description" "time_estimate_minutes" [parent_id]
create_task() {
  local list_id="$1"
  local name="$2"
  local desc="$3"
  local time_min="$4"
  local parent="$5"
  
  # time_estimate in milliseconds
  local time_ms=$(( time_min * 60 * 1000 ))
  
  if [ -n "$parent" ]; then
    # subtask
    RESPONSE=$(curl -s -X POST "$BASE/list/$list_id/task" \
      -H "Authorization: $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"$name\",
        \"description\": \"$desc\",
        \"time_estimate\": $time_ms,
        \"parent\": \"$parent\"
      }")
  else
    RESPONSE=$(curl -s -X POST "$BASE/list/$list_id/task" \
      -H "Authorization: $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"$name\",
        \"description\": \"$desc\",
        \"time_estimate\": $time_ms
      }")
  fi
  
  echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id','ERROR: '+str(d)))"
}

echo "=== Creating FPV App Structure in ClickUp ==="
echo ""

# ==========================================
# SECTION 1: Authentication & Onboarding
# ==========================================
echo "[1/6] Creating: 1. Authentication & Onboarding..."
P1=$(create_task "$LIST_ID" "1. Authentication & Onboarding" "Login, registration, and password recovery screens for the FPV client portal." 240 "")
echo "  Parent ID: $P1"
sleep 0.5

S1_1=$(create_task "$LIST_ID" "1.1 Client Portal Login Screen" "Email & password login form. Fields: Email Address, Password, Forgot Password link. Actions: Login button, Sign in with Google, Sign in with Apple, Create Account link." 60 "$P1")
echo "  Subtask 1.1: $S1_1"
sleep 0.3

S1_2=$(create_task "$LIST_ID" "1.2 Client Portal Registration Modal" "New account creation form. Fields: First Name, Last Name, Mobile Phone, Broker Email, Password, Confirm Password, Real Estate Brokerage Agency Name, State Licensure ID. NMI Payment Terms checkbox consent." 90 "$P1")
echo "  Subtask 1.2: $S1_2"
sleep 0.3

S1_3=$(create_task "$LIST_ID" "1.3 Forgot Password / Credentials Reset Wizard" "Step 1: Email input + Send Recovery Link. Step 2: 6-digit verification code input. Step 3: New Password + Confirm Password + Reset Password button." 60 "$P1")
echo "  Subtask 1.3: $S1_3"
sleep 0.5

# ==========================================
# SECTION 2: Home Dashboard
# ==========================================
echo ""
echo "[2/6] Creating: 2. Home Dashboard..."
P2=$(create_task "$LIST_ID" "2. Home Dashboard" "Main app dashboard with order summaries, upcoming appointments, and notification alerts." 300 "")
echo "  Parent ID: $P2"
sleep 0.5

S2_1=$(create_task "$LIST_ID" "2.1 Main Dashboard Screen" "App header (Profile icon, FPV logo, Notification bell badge). Welcome Card (Taylor!). My Orders Summary Grid: Drafts, Pending Scan, Processing, Completed counters. Active Orders panel with order cards (#DEMO-001). Upcoming Appointments card. FPV Promotional Banner." 120 "$P2")
echo "  Subtask 2.1: $S2_1"
sleep 0.3

S2_2=$(create_task "$LIST_ID" "2.2 Notifications Screen / Alerts Feed" "Header: Back arrow + Notifications title. Alert feed cards showing: Scheduling alerts, Invoice billing alerts, Blueprint completion alerts. Read vs Unread visual indicators." 60 "$P2")
echo "  Subtask 2.2: $S2_2"
sleep 0.5

# ==========================================
# SECTION 3: Account Settings Suite
# ==========================================
echo ""
echo "[3/6] Creating: 3. Account Settings Suite..."
P3=$(create_task "$LIST_ID" "3. Account Settings Suite" "Full user account management: profile editing, orders history, autofill defaults, wallet, favorites, and feedback hub." 600 "")
echo "  Parent ID: $P3"
sleep 0.5

S3_1=$(create_task "$LIST_ID" "3.1 Account & Profile Menu" "Profile identity card (Taylor Morgan, Morgan Realty). Grid options: Edit Profile, My Orders, AutoFill Preferences, Payment Methods/Wallet, Favorites, Feedback Hub. Logout button (red)." 60 "$P3")
echo "  Subtask 3.1: $S3_1"
sleep 0.3

S3_2=$(create_task "$LIST_ID" "3.2 Profile Editor Modal" "Editable form fields: First Name, Last Name, Phone Number, Email Address, Company Name. Company Account toggle switch (agency-wide sharing). Actions: Save Changes, Cancel." 90 "$P3")
echo "  Subtask 3.2: $S3_2"
sleep 0.3

S3_3=$(create_task "$LIST_ID" "3.3 All Projects Ledger (My Orders Listing)" "Filter tabs: Active (scheduled/processing) and Past (completed/archived). Order cards showing: Order ID, Date, Address, Service Badges (Plans/CAD/Matterport), Status Badges (Awaiting/Completed/Cancelled)." 90 "$P3")
echo "  Subtask 3.3: $S3_3"
sleep 0.3

S3_4=$(create_task "$LIST_ID" "3.4 AutoFill Preferences" "Default POC section: Same as Account Info toggle, Name/Phone/Email fields. Blueprint Deliverables defaults: PDF format, AutoCAD version selector. Lot & Formatting: Dimension Lines, Area Sizing, Compass orientation radio (True North vs Door), Color scheme (B&W vs Color)." 120 "$P3")
echo "  Subtask 3.4: $S3_4"
sleep 0.3

S3_5=$(create_task "$LIST_ID" "3.5 Payment Methods & Credit Vault (Wallet)" "PCI/NMI security banner. Saved cards list (Visa **** 4242). Add Payment Method button. Sub-modal: Add Secure Payment Method with Cardholder Name, PAN Number, Expiry MM/YY, CVV, Set as Default toggle." 90 "$P3")
echo "  Subtask 3.5: $S3_5"
sleep 0.3

S3_6=$(create_task "$LIST_ID" "3.6 Favorites Catalog" "Pinned properties registry with repeat addresses, saved technician lockbox notes, and saved search criteria. Execute Repeat Order instant shortcut." 60 "$P3")
echo "  Subtask 3.6: $S3_6"
sleep 0.3

S3_7=$(create_task "$LIST_ID" "3.7 Beta Feedback Hub" "Ticket log feed with status badges (Open, In Review, Resolved). Developer reply threads. Submit Feedback button. Sub-modal: Subject, Description text area, Category dropdown (Bug/Suggestion/UI/Other), Attach Screenshot action." 90 "$P3")
echo "  Subtask 3.7: $S3_7"
sleep 0.5

# ==========================================
# SECTION 4: Project Logistics & Order Details
# ==========================================
echo ""
echo "[4/6] Creating: 4. Project Logistics & Order Details..."
P4=$(create_task "$LIST_ID" "4. Project Logistics & Order Details" "Detailed order status screens with logistics accordion drawers for active, scheduled, and completed projects." 420 "")
echo "  Parent ID: $P4"
sleep 0.5

S4_1=$(create_task "$LIST_ID" "4.1 Active Order Details Screen (#DEMO-001 - Pending Scan)" "Status: Pending Scan (orange badge). Order banner: Address 123 Main St, Plans+CAD services. Accordion drawers: Messages Chat Room, Contact Details (POC), Survey Units (2 stories + basement + detached garage), Site Access (lockbox code), Deliverables (PDF + AutoCAD 2020), 3D Matterport Settings (Interior+Exterior, Dollhouse, Measurement Tool)." 120 "$P4")
echo "  Subtask 4.1: $S4_1"
sleep 0.3

S4_2=$(create_task "$LIST_ID" "4.2 Scheduled Visit Screen (#DEMO-002 - Awaiting Appointment)" "Same accordion drawer structure as 4.1. Status badge: Awaiting Appointment (orange). Technician calendar slot pending confirmation." 60 "$P4")
echo "  Subtask 4.2: $S4_2"
sleep 0.3

S4_3=$(create_task "$LIST_ID" "4.3 Completed & Finalized Screen (#000-D004 - Closed)" "Status badge: Closed (green). Primary actions: View Plans button (opens blueprint PDF/AutoCAD viewer), View Invoice button (pulls receipt for printing/export)." 60 "$P4")
echo "  Subtask 4.3: $S4_3"
sleep 0.5

# ==========================================
# SECTION 5: Order Now & Wizards
# ==========================================
echo ""
echo "[5/6] Creating: 5. Order Now & Wizards..."
P5=$(create_task "$LIST_ID" "5. Order Now & Wizards" "Order creation flow: selection hub dispatcher, 11-step residential wizard, and search inventory checkout flow." 900 "")
echo "  Parent ID: $P5"
sleep 0.5

S5_1=$(create_task "$LIST_ID" "5.1 Order Selection Hub Dispatcher" "4 order type cards: Marketable Plan (Active, launches wizard), As-Built Plan (Coming Soon), 3D Renderings (Coming Soon), Site Plans (Coming Soon). Locked feature overlay modal with Coming Soon message." 60 "$P5")
echo "  Subtask 5.1: $S5_1"
sleep 0.3

S5_2=$(create_task "$LIST_ID" "5.2 Marketable Plan Residential Wizard (11-Step Flow)" "Full 11-step order form. Step 1: Contact Info (name/phone/email/brokerage). Step 2: Property Address (Google Places API autocomplete + street/city/state/zip). Step 3: Level & Structure (story count, basement Y/N finished/unfinished, attic Y/N, detached structures). Step 4: Matterport Details (include toggle, interior+exterior, dollhouse, measurement tool, 3mo hosting). Step 5: Compass Orientation (True North vs Front Door). Steps 6-9: Reserved custom spec slots. Step 10: Credit Checkout (cardholder name, PAN, MM/YY, CVV, NMI terms). Step 11: Success Confirmation (Order # + email receipt notification + Go to Active Order)." 300 "$P5")
echo "  Subtask 5.2: $S5_2"
sleep 0.3

S5_3=$(create_task "$LIST_ID" "5.3 Search Inventory & Checkout Flow" "Search Box Console: address/property ID field, State/City/Zip/SqFt/CAD-available filters. Results Page: property cards with thumbnail, sq ft, CAD badge, price, Select+Checkout button. 4-Tab Checkout Wizard: Tab1 Account Info (Same As Account toggle, POC fields, NMI consent), Tab2 Order Info (address validation, Relationship to Property dropdown, Quote Me For dropdown), Tab3 Final Steps (Co-listing Agent toggle+fields, Referral Source, Comments), Tab4 Terms (cancellation policy, no AMEX note, 3% processing fee, consent checkboxes, Submit Order + validation errors)." 300 "$P5")
echo "  Subtask 5.3: $S5_3"
sleep 0.5

# ==========================================
# SECTION 6: Catalogs, Pricing & Services (About)
# ==========================================
echo ""
echo "[6/6] Creating: 6. About, Catalogs, Pricing & Services..."
P6=$(create_task "$LIST_ID" "6. About, Catalogs, Pricing & Services" "About platform screen, service catalog with 4 category tabs, multi-state pricing grids, regional office contact directory, and support chat placeholder." 720 "")
echo "  Parent ID: $P6"
sleep 0.5

S6_1=$(create_task "$LIST_ID" "6.1 About Platform Screen" "FPV overview branding card. Main CTA buttons: Open Website (external link), Services Catalog (routes to catalog), Contact Regional Office (opens state directory). App support section: Account profile, Native ordering, Scan tools. Chat card with Coming Soon indicator." 60 "$P6")
echo "  Subtask 6.1: $S6_1"
sleep 0.3

S6_2=$(create_task "$LIST_ID" "6.2 Service Catalog - Marketable Tab" "Most Requested section: Residential Floor Plans, Site Plans, Commercial Floor Plans cards. Each card has: title, overview text, Good For checklist, View on Website button. Residential Floor Plans: MLS listings, print flyers, marketing packets use-cases." 90 "$P6")
echo "  Subtask 6.2: $S6_2"
sleep 0.3

S6_3=$(create_task "$LIST_ID" "6.3 Service Catalog - As-Built Tab" "Services: As-Built Floor Plans (engineering blueprints with wall thickness and plumbing), Exterior Elevations (building facades), Interior Elevations (kitchen cabinets, fireplace, shelving), Building Sections (cross-section framing views), Roof Plans (slopes, drainage, chimney)." 90 "$P6")
echo "  Subtask 6.3: $S6_3"
sleep 0.3

S6_4=$(create_task "$LIST_ID" "6.4 Service Catalog - 3D & Media Tab" "Services: 3D Walk-Through Tours (virtual Matterport models), 3D Renderings (exterior + interior high-res), 3D Animations (fly-over videos + interior walkthrough clips), Matterport Video (exported dollhouse clips)." 90 "$P6")
echo "  Subtask 6.4: $S6_4"
sleep 0.3

S6_5=$(create_task "$LIST_ID" "6.5 Service Catalog - Add-Ons Tab" "Add-on options: Exterior Add-On (backyard elevations/site plans), Square Footage Calculations (formal certificates), Furniture Add-On (interior furniture symbols overlay), CAD File Release (layered DWG file delivery), 2D/3D Plans From Scan (generated from raw Matterport data). Need Help section with Pricing and Website redirect buttons." 90 "$P6")
echo "  Subtask 6.5: $S6_5"
sleep 0.3

S6_6=$(create_task "$LIST_ID" "6.6 Pricing Grids Screen - PLANS Drafting Matrix" "State-selectable pricing (Arizona base). B&W and Color price brackets by sq ft: 0-1000sqft $150/$200, 1001-2000sqft $200/$250, 2001-3000sqft $250/$300, 3001-4000sqft $300/$350. 4000+ sqft: custom quote required." 60 "$P6")
echo "  Subtask 6.6: $S6_6"
sleep 0.3

S6_7=$(create_task "$LIST_ID" "6.7 Pricing Grids Screen - FROM EXISTING Drafting Matrix" "Conversion pricing for old/paper blueprints to layered AutoCAD+PDF. Base flat fee starting at $100. Incremental size brackets and revision review rates." 60 "$P6")
echo "  Subtask 6.7: $S6_7"
sleep 0.3

S6_8=$(create_task "$LIST_ID" "6.8 Pricing Grids Screen - RENDERINGS Visuals Matrix" "Visual rendering prices: 3D Exterior Rendering, 3D Interior Rendering (room/material), Fly-Over Animation Video (aerial), Interior Walk-Thru Animation Video. Custom quote via email CAD/PDF submission note." 60 "$P6")
echo "  Subtask 6.8: $S6_8"
sleep 0.3

S6_9=$(create_task "$LIST_ID" "6.9 Pricing Grids Screen - MATTERPORT Walk-Through Matrix" "Base services by sq ft: 0-1000sqft $250, 1001-2000sqft $300, 2001-3000sqft $350, 3001-4000sqft $400, 5000+sqft $250/hr. Add-On services: Outdoor Scans $100/hr, Detached Scan $50, Link Renewal $75/3mo, 2D Plan From Scan $150, 2D Color Plan $200, 3D Color Plan $250, Matterport Video below 1000sqft $125, above 1000sqft +$50/1000sqft." 90 "$P6")
echo "  Subtask 6.9: $S6_9"
sleep 0.3

S6_10=$(create_task "$LIST_ID" "6.10 Regional Office Contact Directory (15+ States)" "State-by-state office directory. California (SF, LA, SD), Arizona (Phoenix), Texas (Austin, Houston), Florida (Miami), Washington DC, Nevada (Reno/Tahoe), Illinois (Chicago), New York (NYC), New Jersey, Colorado (Denver), Connecticut, Oregon, Pennsylvania, Georgia (Atlanta), South Carolina (Charleston), Maryland, Virginia, Massachusetts (Boston), Washington (Seattle). Plus Other category." 90 "$P6")
echo "  Subtask 6.10: $S6_10"
sleep 0.3

S6_11=$(create_task "$LIST_ID" "6.11 Live Chat Module Placeholder Screen" "Chat placeholder page with Coming Soon status badge. Displays: future in-app live support connection queue description. Chat card with chevron arrow in About main screen." 30 "$P6")
echo "  Subtask 6.11: $S6_11"
sleep 0.3

echo ""
echo "=== ALL TASKS CREATED SUCCESSFULLY ==="
echo ""
echo "Summary of Parent Task IDs:"
echo "  Section 1 (Auth):       $P1"
echo "  Section 2 (Home):       $P2"
echo "  Section 3 (Account):    $P3"
echo "  Section 4 (Logistics):  $P4"
echo "  Section 5 (Order Now):  $P5"
echo "  Section 6 (About):      $P6"
