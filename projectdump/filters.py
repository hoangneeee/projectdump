from pathlib import Path
from typing import Union, Iterable
import os
import fnmatch 

def get_essential_files():
    return set()

def get_exclude_patterns(project_path: str):
    """
    Get combined default and custom exclusion patterns.
    Custom patterns are read from .dumpignore in the project_path.
    """

    default_exclude_dirs = {
    # Dependencies & environments
    'node_modules', 'vendor', 'venv', 'env', '.venv', '.env', '.mypy_cache', '.ruff_cache', '.pytest_cache', '__pycache__', 
    '.cache', 'pip-wheel-metadata', 'site-packages', 'deps', 'packages', '.tox',

    # Build artifacts
    'dist', 'build', 'target', 'out', 'bin', 'obj', '.eggs', 'lib', 'lib64', 'generated',

    # CMake build
    'cmake-build-debug', 'cmake-build-debug-visual-studio', 'cmake-build-release-visual-studio',

    # Framework build folders
    '.next', '.nuxt', '.angular', 'coverage', '.turbo', '.vercel', '.expo', '.parcel-cache',

    # Version control & IDE tools
    '.git', '.svn', '.hg', '.idea', '.vscode', '.vs', '.history', '.vscode-test', '.windsurf'

    # Temp & OS folders
    'temp', 'tmp', '.tmp', '.DS_Store', '__MACOSX', 'Thumbs.db', 'System Volume Information',

    # CI/CD & Docker volumes
    '.github', '.gitlab', '.circleci', '.docker', 'logs', 'log', 'docker', 'containers',

    # Database & sessions
    'db', 'database', 'sqlite', 'sessions', 'flask_session', 'instance',
    }

    default_exclude_files = {
        # Logs
        '*.log', '*.log.*', '*.out',

        # Package manager lock files
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'composer.lock', 'poetry.lock', 'Cargo.lock',

        # Compiled/intermediate binaries
        '*.pyc', '*.pyo', '*.pyd', '*.class', '*.o', '*.so', '*.dll', '*.exe', '*.dylib', '*.a',

        # Media files
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.svg', '*.ico', '*.webp',
        '*.mp3', '*.wav', '*.mp4', '*.avi', '*.mov', '*.mkv', '*.flac', '*.ogg',

        # Fonts
        '*.ttf', '*.otf', '*.woff', '*.woff2',

        # Archives & compressed
        '*.zip', '*.tar', '*.gz', '*.rar', '*.7z', '*.bz2', '*.xz', '*.lz', '*.lzma',

        # Office / documents
        '*.pdf', '*.docx', '*.doc', '*.ppt', '*.pptx', '*.xls', '*.xlsx', '*.csv',

        # OS/system files
        '.DS_Store', 'Thumbs.db', 'desktop.ini', 'ehthumbs.db', 'Icon\r',

        # Misc config/cache
        '*.env', '*.env.*', '*.ini', '*.toml', '*.bak', '*.swp', '*.swo',
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
                    
                    # Normalize path separators for patterns
                    pattern = Path(line).as_posix()

                    if pattern.endswith('/'):
                        custom_exclude_dirs.add(pattern[:-1]) # Store without trailing slash
                    else:
                        custom_exclude_files.add(pattern)
        except Exception as e:
            print(f"Warning: Could not read or parse .dumpignore file at {dumpignore_path}: {e}")

    exclude_dirs = default_exclude_dirs.union(custom_exclude_dirs)
    exclude_files = default_exclude_files.union(custom_exclude_files)
    
    return exclude_dirs, exclude_files

def should_exclude_path(rel_dir_path: str, exclude_dir_patterns: Iterable[str]) -> bool:
    """
    Check if a directory path should be excluded.
    rel_dir_path: Relative path of the directory from project root.
    exclude_dir_patterns: A set of patterns.
        - Simple names (e.g., "node_modules") match if any part of rel_dir_path is that name.
        - Glob patterns or paths with "/" (e.g., "build/*", "target/classes") match rel_dir_path using fnmatch.
    """
    normalized_rel_dir_path = Path(rel_dir_path).as_posix()

    for pattern in exclude_dir_patterns:
        normalized_pattern = Path(pattern).as_posix()

        # Check for simple name match in any part of the path
        # (e.g., pattern "node_modules" should exclude "src/node_modules")
        if "/" not in normalized_pattern and "*" not in normalized_pattern and \
           "?" not in normalized_pattern and "[" not in normalized_pattern:
            # This is a simple directory name, check if it's one of the components
            if any(part.lower() == normalized_pattern.lower() for part in Path(normalized_rel_dir_path).parts):
                return True
        else:
            # This is a glob pattern or a path-like pattern (e.g., "build/", "foo/*/bar")
            # Match it against the full relative directory path
            if fnmatch.fnmatchcase(normalized_rel_dir_path, normalized_pattern):
                return True
            # Also match if pattern was `some_dir` and path is `some_dir/child_dir`
            # This requires matching prefixes for directory patterns.
            # fnmatch with `*` handles this: `fnmatch.fnmatchcase(path, pattern + '*')`
            # e.g. pattern `build` should exclude `build/foo`
            if fnmatch.fnmatchcase(normalized_rel_dir_path, normalized_pattern + ('/*' if not normalized_pattern.endswith('*') else '')):
                return True


    return False


def should_exclude_file(filename: str, rel_filepath: str, exclude_file_patterns: Iterable[str]) -> bool:
    """
    Check if a file should be excluded based on the exclusion patterns.
    
    Args:
        filename: Base name of the file (e.g., "script.py").
        rel_filepath: Relative path of the file from project root (e.g., "src/script.py").
        exclude_file_patterns: Iterable of patterns.
            - Patterns with "/" are matched against rel_filepath.
            - Patterns without "/" (e.g., "*.log", "Makefile") are matched against filename primarily,
              but also against rel_filepath to catch cases like `somedir/*.log`.
    
    Returns:
        bool: True if the file matches any exclusion pattern, False otherwise.
    """

    normalized_rel_filepath = Path(rel_filepath).as_posix()
    for pattern in exclude_file_patterns:
        normalized_pattern = Path(pattern).as_posix()
        
        # Try matching pattern against the full relative file path
        if fnmatch.fnmatchcase(normalized_rel_filepath, normalized_pattern):
            # print(f"File Exclude (rel_path): '{normalized_rel_filepath}' matches '{normalized_pattern}'")
            return True
        
        # If pattern contains no slashes, it's a filename-only pattern (e.g., "*.log", "Makefile")
        # And if the previous match failed (e.g. pattern was '*.log', rel_filepath was 'src/foo.log')
        # then we should check filename only.
        if "/" not in normalized_pattern: 
            if fnmatch.fnmatchcase(filename, normalized_pattern): # Match against basename
                # print(f"File Exclude (filename): '{filename}' matches '{normalized_pattern}'")
                return True
                
    return False

