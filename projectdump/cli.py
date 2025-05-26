#!/usr/bin/env python3
"""
ProjectDump CLI - Command Line Interface
"""
import sys
import os
import argparse
from .aggregator import aggregate_code
from .constants import TEXT_VI, TEXT_EN

def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='projectdump',
        description='🚀 ProjectDump - Aggregate project source code into a single file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  projectdump                    # Use current directory
  projectdump /path/to/project   # Specify project path
  projectdump . --lang en        # Use English language
  projectdump --help             # Show this help message
        """
    )
    
    parser.add_argument(
        'project_path',
        nargs='?',
        default=None,
        help='Path to the project directory (default: current directory)'
    )
    
    parser.add_argument(
        '--lang', '--language',
        choices=['en', 'vi'],
        default='en',
        help='Language for output messages (default: en)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='source_dump.txt',
        help='Output filename (default: source_dump.txt)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser

def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Select language
    text = TEXT_EN if args.lang == 'en' else TEXT_VI
    
    # Determine project path
    if args.project_path:
        project_path = args.project_path
    else:
        project_path = os.getcwd()
    
    # Convert to absolute path
    project_path = os.path.abspath(project_path)
    
    # Show banner
    print(text['app_title'])
    print("=" * 40)
    
    # Run aggregation
    success = aggregate_code(project_path, text)
    
    if success:
        print(text['done'])
        return 0
    else:
        print(text['error'])
        return 1

if __name__ == "__main__":
    sys.exit(main())