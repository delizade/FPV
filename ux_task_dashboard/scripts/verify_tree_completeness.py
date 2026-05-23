#!/usr/bin/env python3
import json

def get_parent_id(task):
    parent = task.get("parent")
    if not parent:
        return None
    if isinstance(parent, dict):
        return parent.get("id")
    return parent

def main():
    with open("ux_task_dashboard/tasks_dump.json", "r", encoding="utf-8") as f:
        tasks = json.load(f)
        
    tasks_by_id = {t["id"]: t for t in tasks}
    
    # Trace descendants of 86expucex (Product UX Improvements)
    descendants = set()
    
    def visit(task_id):
        descendants.add(task_id)
        # Find all tasks whose parent is task_id
        for t in tasks:
            pid = get_parent_id(t)
            if pid == task_id and t["id"] not in descendants:
                visit(t["id"])
                
    root_id = "86expucex"
    visit(root_id)
    
    # Trace descendants of 86expf9ee (Current App Structure)
    cas_descendants = set()
    cas_root_id = "86expf9ee"
    
    def visit_cas(task_id):
        cas_descendants.add(task_id)
        for t in tasks:
            pid = get_parent_id(t)
            if pid == task_id and t["id"] not in cas_descendants:
                visit_cas(t["id"])
                
    visit_cas(cas_root_id)
    
    print(f"Total tasks in dump: {len(tasks)}")
    print(f"Tasks under Product UX (86expucex): {len(descendants)} (including root)")
    print(f"Tasks under Current App Structure (86expf9ee): {len(cas_descendants)} (including root)")
    
    # Check if there are tasks that belong to neither
    other_tasks = []
    for t in tasks:
        tid = t["id"]
        if tid not in descendants and tid not in cas_descendants:
            other_tasks.append(t)
            
    print(f"Tasks belonging to NEITHER root: {len(other_tasks)}")
    for t in other_tasks:
        print(f"- [{t['id']}] Name: {t['name']}, Parent: {get_parent_id(t)}")

if __name__ == "__main__":
    main()
