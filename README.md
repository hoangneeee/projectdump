# 🚀 ProjectDump CLI

Project fork from https://github.com/liamhnam/ProjectDump with some refactoring.

**ProjectDump** is a Python CLI tool that detects a project's technologies, filters out non-essential files, and compiles the source code and directory structure into a single readable file.

---

## 📦 Features

Support MacOS, Linux

- 🔍 Auto-detects technologies (Python, JavaScript, Java, etc.)
- 🧹 Skips dependencies, binaries, media, and config clutter
- 🌲 Generates a clean directory tree
- 📄 Dumps readable source code with syntax highlighting
- ⚡ Handles large projects and ignores huge files (>100MB)

---

## 📦 Installation

### Method 1: Install from source (Recommended)

1. Clone or download the project files
2. Navigate to the project directory
3. Install the package:

```bash
make build
./install.sh
```

---

## Usage

### Basic Usage

```bash
# Use current directory
projectdump

# Specify a project directory
projectdump /path/to/your/project

# Use Vietnamese language
projectdump . --lang vi

# Custom output filename
projectdump . --output my_dump.txt
```

### Dump ignore

You can create a `.dumpignore` file in the project root to specify patterns of files and directories to exclude from the dump.

```txt
node_modules/*
venv/*
.env
```

### Command Options

- `project_path`: Path to the project directory (optional, defaults to current directory)
- `--lang, --language`: Language for output messages (en or vi, default: en)
- `--output, -o`: Output filename (default: source_dump.txt)
- `--version`: Show version information
- `--help`: Show help message

### Examples

```bash
# Analyze current directory with English output
projectdump

# Analyze specific project with Vietnamese messages
projectdump ~/my-react-app --lang vi

# Custom output file
projectdump ~/my-python-project -o python_source.txt

# Show help
projectdump --help
```

---

## 🧑‍💻 Supported Technologies (Partial List)

- **Languages**: Python, JS/TS, Java, Kotlin, PHP, Ruby, Go, Rust, C#, Dart, R, Scala, Elixir
- **Frameworks**: React, Vue, Svelte, Angular, Next.js, Nuxt, Flutter, Android, iOS
- **Infra**: Docker, Kubernetes, Terraform, Ansible
- **CI/CD**: GitHub Actions, GitLab CI, CircleCI

---

## 📂 Output Example

```
🚀 PROJECTDUMP
========================================
🌐 Select language (en/vi): en
📂 Enter the project folder path: /path/to/your/project
🔍 Analyzing project at: /path/to/your/project
🔍 Scanning directories...
🛠️  Detected technologies: python
📁 Extensions included: .py, .pyi, .pyx
📁 Generating directory tree...
📄 Processing files...
  📝 Processing: aggregator.py
  📝 Processing: constants.py
  📝 Processing: detector.py
  📝 Processing: filters.py
  📝 Processing: one_file_version.py
  📝 Processing: tree_generator.py
  📝 Processing: __main__.py

✅ Success! File created: /path/to/your/project/source_dump.txt

📊 Summary:
   - Files processed: 7
   - Output size: 30275 characters (~28 KB)
   - Total lines: 870

🎉 Done! The source_dump.txt file is ready.
```

Inside `source_dump.txt`demo:

```text
# ==================================================
# Path: /path/to/your/project
# Detected tech: python
# ==================================================

## DIRECTORY STRUCTURE

New folder/
├── __pycache__/
├── __main__.py
├── aggregator.py
├── constants.py
├── detector.py
├── filters.py
├── one_file_version.py
├── source_dump.txt
└── tree_generator.py

## FILE CONTENTS

### __main__.py

import os
...
```

---

## 📁 What It Ignores

- **Dependency folders**: node_modules, venv, etc.

- **Media & binaries**: .jpg, .exe, .log, etc.

- **Config/IDE**: .git, .vscode, .github, etc.

- **Large files over 100MB**

## ✅ Requirements

Python 3.x

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the CLI tool
5. Submit a pull request

## License

Apache License 2.0 [LICENSE](LICENSE)
