#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

# Change directory to the root of the project
cd "$(dirname "$0")"

echo "=================================================="
echo "🔄 1/4: Fetching latest tasks from ClickUp..."
python3 ux_task_dashboard/scripts/fetch_all_tasks.py
echo "=================================================="

echo "🌲 2/4: Rebuilding relational tasks tree..."
python3 ux_task_dashboard/scripts/build_tree.py
echo "=================================================="

echo "🎨 3/4: Regenerating responsive HTML dashboard..."
python3 ux_task_dashboard/scripts/generate_html.py
echo "=================================================="

echo "📤 4/4: Pushing updates to GitHub Pages..."
git add ux_task_dashboard/tasks_dump.json \
        ux_task_dashboard/tasks_tree.json \
        ux_task_dashboard/ux_redesign_tasks.html

# Prevent committing if there are no changes
if git diff --cached --quiet; then
    echo "ℹ️ No changes detected in task data. Everything is already up to date!"
else
    git commit -m "update: refresh task data from ClickUp"
    git push origin main
    echo "✅ Dashboard successfully updated on GitHub!"
fi

echo "=================================================="
echo "🔗 Live Link: https://delizade.github.io/FPV/ux_task_dashboard/ux_redesign_tasks.html"
echo "=================================================="
