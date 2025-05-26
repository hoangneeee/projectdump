
from projectdump.filters import get_exclude_patterns, should_exclude_file

# Test function
def test_file_validation():
    """Test the file validation functions with various file types"""
    
    exclude_dirs, exclude_files = get_exclude_patterns()
    
    # Test cases
    test_files = [
        "docs.go",           # Should be valid
        "main.py",           # Should be valid
        "config.json",       # Should be valid
        "app.log",           # Should be excluded
        "image.png",         # Should be excluded
        "package-lock.json", # Should be excluded
        "README.md",         # Should be valid
        ".DS_Store",         # Should be excluded
        "script.pyc",        # Should be excluded
        "data.csv",          # Should be excluded
    ]
    
    print("File validation test results:")
    print("-" * 40)
    
    for filename in test_files:
        should_exclude = should_exclude_file(filename, exclude_files)
        status = "✅ VALID" if not should_exclude else "❌ EXCLUDED"
        print(f"{filename:<20} | {status} | exclude={should_exclude}")


# Run the test
if __name__ == "__main__":
    test_file_validation()
