import os
from .filters import should_exclude_path, should_exclude_file # Import the filter functions

def generate_directory_tree(project_path_root: str, exclude_dir_patterns: set, exclude_file_patterns: set):
    tree_lines = [f"{os.path.basename(project_path_root.rstrip(os.sep))}/"]
    _build_tree_recursive(project_path_root, "", tree_lines, project_path_root, exclude_dir_patterns, exclude_file_patterns, True)
    return "\n".join(tree_lines)

def _build_tree_recursive(current_path, prefix, tree_lines, project_root, exclude_dirs, exclude_files, is_last_call_for_level):
    try:
        items = sorted(os.listdir(current_path))
    except PermissionError:
        tree_lines.append(f"{prefix}└── [Permission Denied]") # Or use a generic prefix
        return

    # Filter and collect items to render
    renderable_entries = []
    for name in items:
        full_item_path = os.path.join(current_path, name)
        relative_item_path = os.path.relpath(full_item_path, project_root)
        
        is_dir = os.path.isdir(full_item_path)
        if is_dir:
            if not should_exclude_path(relative_item_path, exclude_dirs):
                renderable_entries.append({'name': name, 'is_dir': True, 'path': full_item_path})
        elif os.path.isfile(full_item_path):
             if not should_exclude_file(name, relative_item_path, exclude_files):
                renderable_entries.append({'name': name, 'is_dir': False, 'path': full_item_path})
    
    for i, entry in enumerate(renderable_entries):
        is_last_entry = (i == len(renderable_entries) - 1)
        
        connector = "└── " if is_last_entry else "├── "
        line = f"{prefix}{connector}{entry['name']}"
        
        if entry['is_dir']:
            line += "/"
        tree_lines.append(line)
        
        if entry['is_dir']:
            new_prefix = prefix + ("    " if is_last_entry else "│   ")
            _build_tree_recursive(entry['path'], new_prefix, tree_lines, project_root, exclude_dirs, exclude_files, is_last_entry)