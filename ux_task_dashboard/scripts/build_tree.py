#!/usr/bin/env python3
import json
import os

def get_parent_id(task):
    parent = task.get("parent")
    if not parent:
        return None
    if isinstance(parent, dict):
        return parent.get("id")
    return parent

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dump_path = os.path.join(os.path.dirname(script_dir), "tasks_dump.json")
    with open(dump_path, "r", encoding="utf-8") as f:
        tasks = json.load(f)
        
    # Index tasks by ID and by parent ID
    tasks_by_id = {t["id"]: t for t in tasks}
    children_by_parent = {}
    
    for t in tasks:
        parent_id = get_parent_id(t)
        if parent_id:
            children_by_parent.setdefault(parent_id, []).append(t)
            
    # Find our root task: 86expucex
    root_id = "86expucex"
    if root_id not in tasks_by_id:
        print(f"Error: Root task {root_id} not found.")
        return
        
    root_task = tasks_by_id[root_id]
    
    # Find roadmap root task: 86exrfkuu
    roadmap_root_id = "86exrfkuu"
    roadmap_root_task = tasks_by_id.get(roadmap_root_id)
    
    def build_node(task):
        node = {
            "id": task["id"],
            "name": task.get("name"),
            "description": task.get("description", ""),
            "status": task.get("status", {}).get("status") if isinstance(task.get("status"), dict) else task.get("status"),
            "time_estimate": task.get("time_estimate"),
            "custom_fields": task.get("custom_fields", []),
            "subtasks": []
        }
        
        # Get children
        children = children_by_parent.get(task["id"], [])
        # Sort children by ID or position if available, let's sort by name or id for consistency
        children.sort(key=lambda x: x.get("name", ""))
        for child in children:
            node["subtasks"].append(build_node(child))
            
        return node

    tree = build_node(root_task)
    
    # Save the full tree
    tree_path = os.path.join(os.path.dirname(script_dir), "tasks_tree.json")
    with open(tree_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)
    print("Saved tasks_tree.json")
        
    # Save the roadmap tree if found
    if roadmap_root_task:
        roadmap_tree = build_node(roadmap_root_task)
        roadmap_path = os.path.join(os.path.dirname(script_dir), "roadmap_tree.json")
        with open(roadmap_path, "w", encoding="utf-8") as f:
            json.dump(roadmap_tree, f, indent=2, ensure_ascii=False)
        print("Saved roadmap_tree.json")
    else:
        print("Warning: Roadmap root task 86exrfkuu not found.")

if __name__ == "__main__":
    main()
