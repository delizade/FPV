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
    
    # Save the tree
    tree_path = os.path.join(os.path.dirname(script_dir), "tasks_tree.json")
    with open(tree_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)
        
    # Print summary
    def print_tree_summary(node, indent=0):
        print("  " * indent + f"- [{node['id']}] {node['name']} ({len(node['subtasks'])} subtasks)")
        for sub in node["subtasks"]:
            print_tree_summary(sub, indent + 1)
            
    print("Task Tree Summary:")
    print_tree_summary(tree)

if __name__ == "__main__":
    main()
