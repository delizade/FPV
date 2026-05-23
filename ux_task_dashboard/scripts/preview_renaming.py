#!/usr/bin/env python3
import json
import re

def get_parent_id(task):
    parent = task.get("parent")
    if not parent:
        return None
    if isinstance(parent, dict):
        return parent.get("id")
    return parent

def clean_task_name(name):
    # Remove surrounding brackets ONLY if they wrap the entire string
    name = name.strip()
    if name.startswith("[") and name.endswith("]"):
        name = name[1:-1].strip()
    
    # re.sub to strip prefix numbering like "1.1.1.A -", "6.2.4.E", "1.1 -", "1.1", "1.0", "1", etc.
    name = re.sub(r'^\d+(?:\.\d+)*\.[A-Z]\b\s*(?:-\s*)?', '', name)
    name = re.sub(r'^\d+(?:\.\d+)*\b\s*(?:-\s*)?', '', name)
    
    # Strip any leading spaces, dashes, dots, or colons
    name = re.sub(r'^[\s\-\.\:\)]+', '', name)
    return name.strip()

# Alphabet converter for Level 3 subtasks (A, B, C...)
def get_alpha(index):
    return chr(65 + index)

def main():
    with open("ux_task_dashboard/tasks_dump.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)
        
    tasks_by_id = {t["id"]: t for t in tasks}
    children_by_parent = {}
    for t in tasks:
        pid = get_parent_id(t)
        if pid:
            children_by_parent.setdefault(pid, []).append(t)
            
    # Define our 7 main phases in order
    PHASE_IDS = [
        ("86expf9fd", 1), # PHASE 1
        ("86expf9fy", 2), # PHASE 2
        ("86expf9g8", 3), # PHASE 3
        ("86expf9ny", 4), # PHASE 4
        ("86expvbtt", 5), # PHASE 5
        ("86exq5x92", 6), # PHASE 6
        ("86expf9q9", 7)  # PHASE 7
    ]
    
    preview_actions = []
    
    # Recursive preview generator
    def process_node(task_id, level, parent_prefix, phase_num):
        children = children_by_parent.get(task_id, [])
        if not children:
            return
            
        # Sort children by orderindex (float)
        def get_order_key(x):
            try:
                return float(x.get("orderindex") or 0)
            except ValueError:
                return 0.0
                
        children.sort(key=get_order_key)
        
        for idx, child in enumerate(children):
            cid = child["id"]
            old_name = child["name"]
            cleaned_name = clean_task_name(old_name)
            
            # Formulate new prefix based on Level
            if level == 1:
                new_prefix = f"{phase_num}.{idx+1} - "
                new_name = f"{new_prefix}{cleaned_name}"
                current_prefix = f"{phase_num}.{idx+1}"
            elif level == 2:
                new_prefix = f"{parent_prefix}.{idx+1} - "
                new_name = f"{new_prefix}{cleaned_name}"
                current_prefix = f"{parent_prefix}.{idx+1}"
            elif level == 3:
                letter = get_alpha(idx)
                new_prefix = f"{parent_prefix}.{letter} - "
                new_name = f"{new_prefix}{cleaned_name}"
                current_prefix = f"{parent_prefix}.{letter}"
            else:
                new_prefix = f"{parent_prefix}.{idx+1} - "
                new_name = f"{new_prefix}{cleaned_name}"
                current_prefix = f"{parent_prefix}.{idx+1}"
                
            preview_actions.append({
                "id": cid,
                "old_name": old_name,
                "new_name": new_name,
                "level": level
            })
            
            # Recurse next level
            process_node(cid, level + 1, current_prefix, phase_num)

    for pid, phase_num in PHASE_IDS:
        process_node(pid, 1, str(phase_num), phase_num)
        
    print(f"Total tasks targeted for renaming: {len(preview_actions)}")
    
    # Save preview
    with open("ux_task_dashboard/scripts/renaming_preview.json", "w", encoding="utf-8") as f:
        json.dump(preview_actions, f, indent=2, ensure_ascii=False)
        
    print("\nVisual Preview check for Revision 1:")
    for a in preview_actions:
        if "Revision" in a["old_name"] or "REVISION 1" in a["old_name"]:
            print(f"OLD: {a['old_name']}")
            print(f"NEW: {a['new_name']}")

if __name__ == "__main__":
    main()
