#!/bin/bash

# Build script for ProjectDump
# This script will create a standalone binary using PyInstaller

set -e

echo "🚀 Building ProjectDump Binary..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the project root directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating build environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating build environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade pip
pip install pyinstaller
pip install -e .

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Create the binary
echo "🔨 Building binary with PyInstaller..."
pyinstaller \
    --onefile \
    --name projectdump \
    --console \
    --clean \
    --noconfirm \
    projectdump/cli.py

# Check if build was successful
if [ -f "dist/projectdump" ]; then
    echo "✅ Build successful!"
    echo "📁 Binary location: $(pwd)/dist/projectdump"
    echo "📏 Binary size: $(du -h dist/projectdump | cut -f1)"
    
    # Test the binary
    echo "🧪 Testing binary..."
    ./dist/projectdump --version
    
    echo ""
    echo "🎯 Installation options:"
    echo "1. Copy to /usr/local/bin (requires sudo):"
    echo "   sudo cp dist/projectdump /usr/local/bin/"
    echo ""
    echo "2. Copy to ~/.local/bin (user only):"
    echo "   mkdir -p ~/.local/bin"
    echo "   cp dist/projectdump ~/.local/bin/"
    echo "   # Add ~/.local/bin to PATH if not already added"
    echo ""
    echo "3. Run install script:"
    echo "   ./install.sh"
    
else
    echo "❌ Build failed!"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo ""
echo "🎉 Done! Binary is ready at: dist/projectdump"