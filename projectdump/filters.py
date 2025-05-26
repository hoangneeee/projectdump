from pathlib import Path
from typing import Union, Iterable
import os

def get_essential_files():
    return set()

def get_exclude_patterns():
    exclude_dirs = {
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

    exclude_files = {
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

    
    return exclude_dirs, exclude_files

def should_exclude_path(path, exclude_dirs):
    return any(part.lower() in exclude_dirs for part in Path(path).parts)

def should_exclude_file(filename: str, exclude_files: Iterable[str]) -> bool:
    """
    Check if a file should be excluded based on the exclusion patterns.
    
    Args:
        filename: Name of the file to check
        exclude_files: Iterable of patterns to match against the filename.
                     Patterns can be either exact matches (case-insensitive) or
                     wildcard patterns starting with '*.' to match file extensions.
    
    Returns:
        bool: True if the file matches any exclusion pattern, False otherwise.
    """
    # Convert filename to lowercase once for case-insensitive comparison
    filename_lower = filename.lower()
    
    for pattern in exclude_files:
        try:
            pattern_lower = pattern.lower()
            
            # Check for exact match
            if filename_lower == pattern_lower:
                print(f"Exact match: {filename} matches {pattern}")
                return True
                
            # Check for extension match (pattern starts with '*.' and file has the exact extension)
            if pattern_lower.startswith('*.'):
                pattern_ext = pattern_lower[2:]  # Remove '*.' to get extension
                # Get the actual file extension
                _, file_ext = os.path.splitext(filename_lower)
                file_ext = file_ext[1:] if file_ext.startswith('.') else file_ext  # Remove leading dot
                
                if file_ext == pattern_ext:
                    print(f"Extension match: {filename} matches {pattern}")
                    return True
                
        except Exception as e:
            print(f"Error checking pattern {pattern} against {filename}: {e}")
    
    return False
