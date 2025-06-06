import os
from projectdump.constants import MAX_FILE_SIZE
from projectdump.detector import detect_project_tech, get_extensions_by_tech
from projectdump.filters import get_essential_files, get_exclude_patterns, should_exclude_path, should_exclude_file
from projectdump.tree_generator import generate_directory_tree
from pathlib import Path

def aggregate_code(project_path, text, output_filename="source_dump.txt"):
    """Main function to aggregate project source code"""
    if not os.path.isdir(project_path):
        print(text['not_found'].format(path=project_path))
        return False

    print(text['analyzing'] + project_path)
    print(text['scanning'])

    # Detect tech
    detected_techs = detect_project_tech(project_path)
    target_extensions = set() # Initialize

    if detected_techs:
        print(text['tech_detected'] + ', '.join(detected_techs))
        target_extensions = get_extensions_by_tech(detected_techs)
        if target_extensions:
             print(text['included_ext'] + ', '.join(sorted(list(target_extensions))))
        else:
             print(text['included_ext'] + " (none specific, may include more files based on filters)")
    else:
        print(text['no_tech'])
        # If no tech detected, target_extensions remains empty.
        # Logic below will handle including files not explicitly excluded.

    # Pass project_path to get_exclude_patterns to load .dumpignore
    exclude_dirs, exclude_files = get_exclude_patterns(project_path)

    content_lines = []
    content_lines.append("# " + "="*50)
    content_lines.append(f"# Path: {project_path}")
    content_lines.append(f"# Detected tech: {', '.join(detected_techs) if detected_techs else 'Unknown'}")
    content_lines.append("# " + "="*50)
    content_lines.append("")

    print(text['generating_tree'])
    content_lines.append("## DIRECTORY STRUCTURE")
    content_lines.append("```")
    # Pass both exclude_dirs (as dir_patterns) and exclude_files (as file_patterns)
    content_lines.append(generate_directory_tree(project_path, exclude_dirs, exclude_files))
    content_lines.append("```")
    content_lines.append("")


    print(text['processing_files'])
    content_lines.append("## FILE CONTENTS")
    content_lines.append("")

    file_count = 0
    total_size = 0

    for root, dirs, files in os.walk(project_path, topdown=True):
        # Filter directories in place using should_exclude_path
        # Pass the patterns obtained from get_exclude_patterns (which includes .dumpignore)
        dirs[:] = [d for d in dirs if not should_exclude_path(os.path.relpath(os.path.join(root, d), project_path), exclude_dirs)]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_path)

            # Use should_exclude_file with filename, relative path, and combined exclude_files patterns
            if should_exclude_file(file, rel_path, exclude_files):
                continue

            # File extension and name check logic revised
            file_ext_with_dot = Path(file).suffix.lower() # e.g., '.py', '.txt', or '' for 'Makefile'
            
            process_this_file = False
            if not detected_techs:
                # If no specific tech detected, we attempt to include "all code files".
                # This means we rely mainly on exclusion rules (size, exclude_dirs, exclude_files from .dumpignore)
                # Files already passed should_exclude_file and should_exclude_path.
                process_this_file = True
            else:
                # Techs detected, so filter by target_extensions
                # Check for full filename match (e.g. "Dockerfile" in target_extensions)
                if file in target_extensions:
                    process_this_file = True
                # Check for extension match (e.g. ".py" in target_extensions)
                elif file_ext_with_dot and file_ext_with_dot in target_extensions:
                    process_this_file = True
            
            if not process_this_file:
                continue

            try:
                file_size = os.path.getsize(file_path)
                if file_size > MAX_FILE_SIZE:
                    print(text['skip_large'].format(file=rel_path, size=file_size, limit=MAX_FILE_SIZE))
                    continue

                print(text['processing'].format(file=rel_path))
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()

                # Determine language hint for markdown code block
                lang_hint = file_ext_with_dot[1:] if file_ext_with_dot else Path(file).stem.lower()
                if lang_hint == "dockerfile": # common case
                    lang_hint = "dockerfile" 
                elif not lang_hint: # if still no hint (e.g. file is 'Makefile' -> stem is 'makefile')
                    if file.lower() == 'makefile':
                        lang_hint = 'makefile'
                    # Add other common full filename hints if needed

                content_lines.append(f"### {rel_path}")
                content_lines.append("```" + lang_hint)
                content_lines.append(file_content)
                content_lines.append("```")
                content_lines.append("")

                file_count += 1
                total_size += len(file_content) # Use actual content length for total_size

            except Exception as e:
                content_lines.append(f"### {rel_path}")
                content_lines.append(f"```\n# Error reading file: {str(e)}\n```")
                content_lines.append("")

    output_path = os.path.join(project_path, output_filename) # Use the output_filename from args
    final_content = '\n'.join(content_lines)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        # Recalculate line_count from the final_content string to be accurate
        # as content_lines might have empty strings that don't translate to lines in the file.
        # Or, more simply, use the number of elements in content_lines if each is a line.
        # However, reading the file back is most accurate for "lines in file".
        # For performance on huge files, `len(final_content.splitlines())` is better than re-read.
        line_count = len(final_content.splitlines())


        print("")
        print(text['success'] + output_path)
        print("")
        print(text['summary'])
        print(text['file_count'].format(count=file_count))
        # Use final_content length for char count, total_size for ~KB (sum of read content)
        print(text['size'].format(size=len(final_content), kb=total_size // 1024))
        print(text['line_count'].format(lines=line_count))
        return True

    except Exception as e:
        print(text['write_error'].format(error=str(e)))
        return False