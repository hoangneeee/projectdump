import os
import sys
from pathlib import Path
import fnmatch

MAX_FILE_SIZE = 100 * 1024 * 1024   # 100 MB

# --- DETECTOR LOGIC (from detector.py) ---
def detect_project_tech(project_path):
    """Tự động phát hiện công nghệ dự án dựa trên các file đặc trưng, hỗ trợ glob"""
    tech_indicators = {
        'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', '*.py', '*.ipynb'],
        'javascript': ['package.json', '*.js'],
        'typescript': ['tsconfig.json', '*.ts'],
        'react': ['*.jsx', '*.tsx', 'react.config.js'],
        'vue': ['vue.config.js', '*.vue'],
        'svelte': ['svelte.config.js', '*.svelte'],
        'nextjs': ['next.config.js', 'pages/**/*.js', 'pages/**/*.jsx', 'pages/**/*.ts', 'pages/**/*.tsx'],
        'nuxt': ['nuxt.config.js'],
        'angular': ['angular.json', 'main.ts'],

        'flutter': ['pubspec.yaml', '*.dart'],
        'android': ['build.gradle', 'AndroidManifest.xml'],
        'ios': ['*.xcodeproj', '*.xcworkspace'],

        'java': ['pom.xml', '*.java'],
        'kotlin': ['*.kt'],
        'csharp': ['*.csproj', 'Program.cs'],
        'php': ['composer.json'],
        'ruby': ['Gemfile'],
        'go': ['go.mod', '*.go'], # Added *.go for better go detection
        'rust': ['Cargo.toml'],
        'elixir': ['mix.exs'],
        'dart': ['pubspec.yaml'], # Dart is listed twice, once general, once for flutter. Fine.
        'r': ['*.R', '*.Rproj'],
        'scala': ['build.sbt'],
        'docker': ['Dockerfile'],
        'kubernetes': ['k8s/', 'helm/'], # These are directory patterns
        'terraform': ['*.tf'],
        'ansible': ['ansible.cfg'],
        'github_actions': ['.github/workflows/'], # Directory pattern
        'gitlab_ci': ['.gitlab-ci.yml'],
        'circleci': ['.circleci/config.yml'],
        'deno': ['deno.json'],
        'bun': ['bun.lockb'],

        'c': ['*.c', '*.h'],
        'cpp': ['*.cpp', '*.hpp']
    }

    detected_techs = set()

    for root, dirs, files in os.walk(project_path):
        # To handle directory patterns like 'k8s/', '.github/workflows/'
        # We need to check both files and directories against patterns.
        # For simplicity, current logic mostly relies on file patterns.
        # Adding directory check for patterns ending with /
        current_items = files + [d + "/" for d in dirs] # Add / to dirs for matching
        
        rel_root = os.path.relpath(root, project_path)
        if rel_root == ".": # Handle root path case for rel_root
            rel_root = ""
            
        for tech, patterns in tech_indicators.items():
            for pattern in patterns:
                # Handle directory patterns from tech_indicators (e.g., 'k8s/')
                if pattern.endswith('/'):
                    # This pattern is for a directory
                    for d_name in dirs: # Check against actual directory names
                        dir_path_to_check = Path(rel_root, d_name).as_posix() + "/"
                        if fnmatch.fnmatchcase(dir_path_to_check, pattern) or \
                           fnmatch.fnmatchcase(Path(rel_root, d_name).as_posix(), pattern[:-1]): # Match 'k8s' if pattern is 'k8s/'
                            detected_techs.add(tech)
                            break # Found for this tech pattern
                    if tech in detected_techs: continue # Move to next tech

                # Handle file patterns (glob or exact)
                for item_name in files: # Only check files for file patterns
                    # Construct full relative path for item for glob matching
                    # item_path_for_glob = Path(rel_root, item_name).as_posix()
                    # Simpler for now: match glob patterns against filenames within any dir
                    # More complex globs like 'pages/**/*.js' need full path matching.

                    # Path for fnmatch needs to be relative to project_path for patterns like 'pages/**/*.js'
                    item_rel_path = Path(rel_root, item_name).as_posix()

                    if fnmatch.fnmatchcase(item_rel_path, pattern): # Match 'pages/index.js' against 'pages/**/*.js'
                        detected_techs.add(tech)
                        break 
                    elif "/" not in pattern and fnmatch.fnmatchcase(item_name, pattern): # Match '*.js' against 'index.js'
                        detected_techs.add(tech)
                        break
                if tech in detected_techs: continue # Move to next tech


        # Extra logic: add implied techs
        if 'nextjs' in detected_techs:
            detected_techs.update(['react', 'javascript', 'typescript'])
        if 'nuxt' in detected_techs:
            detected_techs.update(['vue', 'javascript', 'typescript'])

    return sorted(list(detected_techs))


def get_extensions_by_tech(techs):
    tech_extensions = {
        # Python & Data Science
        'python': ['.py', '.pyx', '.pyi'],
        'jupyter': ['.ipynb'],
        'r': ['.r', '.R', '.Rmd', '.Rproj'],

        # JavaScript & Frontend
        'javascript': ['.js', '.jsx', '.mjs', '.cjs'],
        'typescript': ['.ts', '.tsx'],
        'react': ['.jsx', '.tsx', '.js', '.ts'], # React can use .js or .ts
        'vue': ['.vue', '.js', '.ts'],
        'svelte': ['.svelte'],
        'angular': ['.ts', '.js', '.html', '.scss'], # Angular uses .html templates, .scss styles
        'nextjs': ['.js', '.jsx', '.ts', '.tsx'],
        'nuxt': ['.vue', '.js', '.ts'],

        # Mobile
        'flutter': ['.dart'],
        'android': ['.java', '.kt', '.xml'], # Android layouts are XML
        'ios': ['.swift', '.m', '.mm', '.h', '.xib', '.storyboard'], # iOS uses storyboards, xibs

        # Backend & Dev
        'java': ['.java', '.kt'], # Kotlin often used with Java
        'kotlin': ['.kt', '.kts'], # Kotlin scripts
        'csharp': ['.cs', '.vb'], # .NET can include VB
        'php': ['.php'],
        'ruby': ['.rb', '.erb'], # Ruby on Rails templates
        'go': ['.go'],
        'rust': ['.rs'],
        'elixir': ['.ex', '.exs'],
        'dart': ['.dart'],
        'scala': ['.scala', '.sc'],
        'c': ['.c', '.h'],      # Corrected
        'cpp': ['.cpp', '.hpp'], # Corrected

        # Infrastructure
        'docker': ['Dockerfile', '.dockerignore'], # Dockerfile is a full name
        'kubernetes': ['.yaml', '.yml'], # K8s configs
        'terraform': ['.tf', '.tf.json'], # Terraform files
        'ansible': ['.yml', '.yaml'], # Ansible playbooks

        # CI/CD (usually YAML)
        'github_actions': ['.yml', '.yaml'],
        'gitlab_ci': ['.yml', '.yaml'],
        'circleci': ['.yml', '.yaml'],

        # Runtime Environments (primarily JS/TS based)
        'nodejs': ['.js', '.mjs', '.cjs'],
        'bun': ['.js', '.ts', '.jsx', '.tsx'],
        'deno': ['.ts', '.tsx', '.js'],

        # Config files (generic, good to include if no specific tech or for overall context)
        'json': ['.json'],
        'yaml': ['.yml', '.yaml'],
        'toml': ['.toml'],
        'xml': ['.xml'],
        # Consider 'Makefile', 'Procfile' etc. if desired as generic inclusions
    }

    extensions = set()
    for tech in techs:
        if tech in tech_extensions:
            extensions.update(tech_extensions[tech])
    
    return extensions

# --- FILTERS LOGIC (from filters.py) ---
def get_exclude_patterns(project_path: str):
    default_exclude_dirs = {
        'node_modules', 'vendor', 'venv', 'env', '.venv', '.env', '.mypy_cache', '.ruff_cache', '.pytest_cache', '__pycache__',
        '.cache', 'pip-wheel-metadata', 'site-packages', 'deps', 'packages', '.tox',
        'dist', 'build', 'target', 'out', 'bin', 'obj', '.eggs', 'lib', 'lib64', 'generated',
        'cmake-build-debug', 'cmake-build-debug-visual-studio', 'cmake-build-release-visual-studio',
        '.next', '.nuxt', '.angular', 'coverage', '.turbo', '.vercel', '.expo', '.parcel-cache',
        '.git', '.svn', '.hg', '.idea', '.vscode', '.vs', '.history', '.vscode-test', '.windsurf',
        'temp', 'tmp', '.tmp', '.DS_Store', '__MACOSX', 'Thumbs.db', 'System Volume Information',
        '.docker', 'logs', 'log', 'docker', 'containers',
        'db', 'database', 'sqlite', 'sessions', 'flask_session', 'instance',
    }
    default_exclude_files = {
        # Logs
        '*.log', '*.log.*', '*.out',
        # Package manager lock files
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'composer.lock', 'poetry.lock', 'Cargo.lock',

        # Compiled/intermediate binaries
        '*.pyc', '*.pyo', '*.pyd', '*.class', '*.o', '*.so', '*.dll', '*.exe', '*.dylib', '*.a',
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.svg', '*.ico', '*.webp',
        '*.mp3', '*.wav', '*.mp4', '*.avi', '*.mov', '*.mkv', '*.flac', '*.ogg',
        '*.ttf', '*.otf', '*.woff', '*.woff2',
        '*.zip', '*.tar', '*.gz', '*.rar', '*.7z', '*.bz2', '*.xz', '*.lz', '*.lzma',
        '*.pdf', '*.docx', '*.doc', '*.ppt', '*.pptx', '*.xls', '*.xlsx', '*.csv',
        '.DS_Store', 'Thumbs.db', 'desktop.ini', 'ehthumbs.db', 'Icon\r',
        '*.bak', '*.swp', '*.swo',
    }
    custom_exclude_dirs = set()
    custom_exclude_files = set()
    dumpignore_path = os.path.join(project_path, ".dumpignore")
    if os.path.exists(dumpignore_path):
        try:
            with open(dumpignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    pattern = Path(line).as_posix()
                    if pattern.endswith('/'):
                        custom_exclude_dirs.add(pattern[:-1])
                    else:
                        custom_exclude_files.add(pattern)
        except Exception as e:
            print(f"Warning: Could not read .dumpignore: {e}")
    return default_exclude_dirs.union(custom_exclude_dirs), default_exclude_files.union(custom_exclude_files)

def should_exclude_path(rel_dir_path: str, exclude_dir_patterns: Iterable[str]) -> bool:
    normalized_rel_dir_path = Path(rel_dir_path).as_posix()
    for pattern in exclude_dir_patterns:
        normalized_pattern = Path(pattern).as_posix()
        if "/" not in normalized_pattern and "*" not in normalized_pattern and \
           "?" not in normalized_pattern and "[" not in normalized_pattern:
            if any(part.lower() == normalized_pattern.lower() for part in Path(normalized_rel_dir_path).parts):
                return True
        else:
            if fnmatch.fnmatchcase(normalized_rel_dir_path, normalized_pattern):
                return True
            if fnmatch.fnmatchcase(normalized_rel_dir_path, normalized_pattern + ('/*' if not normalized_pattern.endswith('*') else '')):
                 return True
    return False

def should_exclude_file(filename: str, rel_filepath: str, exclude_file_patterns: Iterable[str]) -> bool:
    normalized_rel_filepath = Path(rel_filepath).as_posix()
    for pattern in exclude_file_patterns:
        normalized_pattern = Path(pattern).as_posix()
        if fnmatch.fnmatchcase(normalized_rel_filepath, normalized_pattern):
            return True
        if "/" not in normalized_pattern: 
            if fnmatch.fnmatchcase(filename, normalized_pattern):
                return True
    return False

# --- TREE GENERATOR (from tree_generator.py - assumed unchanged unless exclude_dirs logic impacted it) ---
def generate_directory_tree(project_path, exclude_dirs):
    """Tạo cây thư mục đầy đủ - thư mục thư viện chỉ hiển thị tên, không hiển thị file bên trong"""
    tree_lines = []
    project_name = os.path.basename(project_path.rstrip(os.sep))
    tree_lines.append(f"{project_name}/")
    
    def add_directory_content(current_path, prefix=""):
        try:
            items = sorted(os.listdir(current_path))
            # Filter dirs based on exclude_dirs patterns before processing
            # Note: The main os.walk loop in aggregate_code already prunes dirs.
            # This internal check is a backup or for standalone use of generate_directory_tree.
            # For consistency, use relpath for checking against exclude_dirs
            
            all_dirs_in_item = [item for item in items if os.path.isdir(os.path.join(current_path, item))]
            
            # This is tricky: exclude_dirs contains patterns. The original `dirname.lower() in exclude_dirs`
            # was for simple name checking. Now `should_exclude_path` is more complex.
            # We must pass the full relative path to should_exclude_path.
            
            # Dirs to process further (not explicitly excluded as a whole)
            # This filtering should ideally happen before iterating here if possible,
            # or use the should_exclude_path logic correctly.

            # The current tree generator logic: if dirname.lower() in exclude_dirs (simple set), then skip deeper.
            # With pattern-based exclude_dirs, this needs adjustment.
            # For simplicity, tree_generator will show the dir if it's not pruned by os.walk,
            # but won't recurse if the *name* is in the simple exclude_dirs set.
            # This is a slight divergence but might be acceptable for tree display.
            # The *content aggregation* uses the more robust should_exclude_path in os.walk.

            # Let's keep the original simple check for tree generation for excluded root folders
            # like 'node_modules/' for brevity in the tree, relying on aggregate_code's os.walk pruning for content.
            simple_exclude_names = {p for p in exclude_dirs if "/" not in p and "*" not in p and "?" not in p and "[" not in p}


            dirs_to_render = []
            files_to_render = []

            for item in items:
                item_path = os.path.join(current_path, item)
                item_rel_path = os.path.relpath(item_path, project_path)
                if os.path.isdir(item_path):
                    if not should_exclude_path(item_rel_path, exclude_dirs): # Use the robust check
                        dirs_to_render.append(item)
                    elif item.lower() in simple_exclude_names: # For top-level excluded dirs, show them but don't recurse
                        dirs_to_render.append(item) # Add to render, but recursion will be skipped below

                elif os.path.isfile(item_path):
                     if not should_exclude_file(item, item_rel_path, set()): # No specific file exclusions for tree itself
                        files_to_render.append(item)


            # Hiển thị thư mục
            for i, dirname in enumerate(dirs_to_render):
                is_last_dir = (i == len(dirs_to_render) - 1) and len(files_to_render) == 0
                dir_item_path = os.path.join(current_path, dirname)
                dir_item_rel_path = os.path.relpath(dir_item_path, project_path)

                tree_lines.append(f"{prefix}{'└── ' if is_last_dir else '├── '}{dirname}/")
                
                # Check if this directory itself (by its relative path) or its name is excluded for recursion
                if not should_exclude_path(dir_item_rel_path, exclude_dirs) and dirname.lower() not in simple_exclude_names:
                    next_prefix = prefix + ("    " if is_last_dir else "│   ")
                    add_directory_content(dir_item_path, next_prefix)
            
            # Hiển thị files
            for i, filename in enumerate(files_to_render):
                is_last = i == len(files_to_render) - 1
                tree_lines.append(f"{prefix}{'└── ' if is_last else '├── '}{filename}")
                
        except PermissionError:
            tree_lines.append(f"{prefix}├── [Permission Denied]")
    
    add_directory_content(project_path)
    return "\n".join(tree_lines)


# --- AGGREGATOR LOGIC (from aggregator.py) ---
def aggregate_code(project_path, output_filename="source_dump.txt"): # Removed 'text' as it's hardcoded VI here
    """Hàm chính để tổng hợp code"""
    if not os.path.isdir(project_path):
        print(f"❌ Lỗi: Thư mục '{project_path}' không tồn tại!")
        return False

    print(f"🔍 Đang phân tích dự án tại: {project_path}")
    print("🔍 Đang quét thư mục...")

    detected_techs = detect_project_tech(project_path)
    target_extensions = set()
    if detected_techs:
        print(f"🛠️  Phát hiện công nghệ: {', '.join(detected_techs)}")
        target_extensions = get_extensions_by_tech(detected_techs)
        if target_extensions:
            print(f"📁 Extensions sẽ được bao gồm: {', '.join(sorted(list(target_extensions)))}")
        else:
            print("📁 Extensions sẽ được bao gồm: (không có, có thể sẽ lấy nhiều file dựa trên filter)")
    else:
        print("⚠️  Không phát hiện được công nghệ cụ thể, sử dụng tất cả file code (sau khi filter)")

    exclude_dirs, exclude_files = get_exclude_patterns(project_path) # Pass project_path

    content_lines = []
    content_lines.append("# TỔNG HỢP MÃ NGUỒN DỰ ÁN") # Vietnamese default
    content_lines.append("# " + "="*50)
    content_lines.append(f"# Đường dẫn: {project_path}")
    content_lines.append(f"# Công nghệ phát hiện: {', '.join(detected_techs) if detected_techs else 'Không xác định'}")
    content_lines.append("# " + "="*50)
    content_lines.append("")

    print("📁 Đang tạo cây thư mục...")
    content_lines.append("## CẤU TRÚC THƯ MỤC")
    content_lines.append("```")
    content_lines.append(generate_directory_tree(project_path, exclude_dirs)) # Pass combined exclude_dirs
    content_lines.append("```")
    content_lines.append("")

    print("📄 Đang xử lý các tệp...")
    content_lines.append("## NỘI DUNG CÁC FILE")
    content_lines.append("")

    file_count = 0
    total_size = 0

    for root, dirs, files_in_dir in os.walk(project_path, topdown=True): # Renamed files to files_in_dir
        # Prune directories based on combined exclude_dirs patterns
        dirs[:] = [d for d in dirs if not should_exclude_path(os.path.relpath(os.path.join(root, d), project_path), exclude_dirs)]

        for file_item in files_in_dir: # Renamed file to file_item
            file_path = os.path.join(root, file_item)
            rel_path = os.path.relpath(file_path, project_path)

            if should_exclude_file(file_item, rel_path, exclude_files): # Pass file_item, rel_path
                continue

            file_ext_with_dot = Path(file_item).suffix.lower()
            process_this_file = False
            if not detected_techs:
                process_this_file = True # Include if not excluded by filters, if no tech found
            else:
                if file_item in target_extensions: # Full filename match, e.g., "Dockerfile"
                    process_this_file = True
                elif file_ext_with_dot and file_ext_with_dot in target_extensions: # Extension match, e.g., ".py"
                    process_this_file = True
            
            if not process_this_file:
                continue

            try:
                file_size_val = os.path.getsize(file_path) # Renamed file_size
                if file_size_val > MAX_FILE_SIZE:
                    print(f"⚠️  Bỏ qua {rel_path} (kích thước {file_size_val:,} byte > giới hạn {MAX_FILE_SIZE:,} byte)")
                    continue

                print(f"  📝 Xử lý: {rel_path}")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()

                lang_hint = file_ext_with_dot[1:] if file_ext_with_dot else Path(file_item).stem.lower()
                if lang_hint == "dockerfile": lang_hint = "dockerfile"
                elif not lang_hint and file_item.lower() == 'makefile': lang_hint = 'makefile'


                content_lines.append(f"### {rel_path}")
                content_lines.append("```" + lang_hint)
                content_lines.append(file_content)
                content_lines.append("```")
                content_lines.append("")

                file_count += 1
                total_size += len(file_content)

            except Exception as e:
                content_lines.append(f"### {rel_path}")
                content_lines.append(f"```\n# Lỗi đọc file: {str(e)}\n```") # Vietnamese
                content_lines.append("")

    output_path_val = os.path.join(project_path, output_filename) # Use output_filename
    final_content = '\n'.join(content_lines)

    try:
        with open(output_path_val, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        line_count = len(final_content.splitlines())
        print("")
        print(f"✅ Thành công! Đã tạo file: {output_path_val}")
        print("")
        print("📊 Thống kê:")
        print(f"   - Số file đã xử lý: {file_count}")
        print(f"   - Kích thước file đầu ra: {len(final_content):,} ký tự (~{total_size // 1024} KB)")
        print(f"   - Tổng số dòng: {line_count:,} dòng")
        return True

    except Exception as e:
        print(f"❌ Lỗi ghi file: {str(e)}")
        return False


def main():
    """Hàm main"""
    print("🚀 PROJECTDUMP (Phiên bản 1 file)")
    print("="*40)
    
    project_cli_path = None
    output_cli_filename = "source_dump.txt" # Default for one_file_version

    if len(sys.argv) > 1:
        project_cli_path = sys.argv[1]
        # Rudimentary arg parsing for one_file_version, e.g., projectdump_onefile.py <path> -o <outputfile>
        if len(sys.argv) > 3 and (sys.argv[2] == "-o" or sys.argv[2] == "--output"):
            output_cli_filename = sys.argv[3]
        elif len(sys.argv) > 2 and not (sys.argv[2] == "-o" or sys.argv[2] == "--output"):
             # If second arg is not -o, assume it's part of path or an error for this simple parser
             pass


    if not project_cli_path:
        project_cli_path = input("📂 Nhập đường dẫn thư mục dự án (để trống cho thư mục hiện tại): ").strip() # Vietnamese
        if not project_cli_path:
            project_cli_path = os.getcwd()
    
    project_cli_path = os.path.abspath(project_cli_path)
    
    success = aggregate_code(project_cli_path, output_filename=output_cli_filename)
    
    if success:
        print("\n🎉 Hoàn thành! File dump đã sẵn sàng.")
    else:
        print("\n💥 Có lỗi xảy ra trong quá trình xử lý.")
        sys.exit(1)

if __name__ == "__main__":
    main()