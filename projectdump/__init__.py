"""
ProjectDump - A CLI tool to aggregate project source code
"""

__version__ = "1.0.0"
__author__ = "Henry Vo"
__email__ = "levuthanhtung11@gmail.com"

from projectdump.aggregator import aggregate_code
from projectdump.detector import detect_project_tech, get_extensions_by_tech
from projectdump.tree_generator import generate_directory_tree
from projectdump.filters import get_essential_files, get_exclude_patterns, should_exclude_path, should_exclude_file
from projectdump.constants import MAX_FILE_SIZE, TEXT_VI, TEXT_EN

__all__ = [
    'aggregate_code',
    'detect_project_tech',
    'get_extensions_by_tech',
    'generate_directory_tree',
    'get_essential_files',
    'get_exclude_patterns',
    'should_exclude_path',
    'should_exclude_file',
    'MAX_FILE_SIZE',
    'TEXT_VI',
    'TEXT_EN',
]