#!/bin/bash

# Installation script for ProjectDump binary

set -e

BINARY_NAME="projectdump"
BINARY_PATH="dist/$BINARY_NAME"

echo "🚀 ProjectDump Installation"
echo "=========================="

# Check if binary exists
if [ ! -f "$BINARY_PATH" ]; then
    echo "❌ Error: Binary not found at $BINARY_PATH"
    echo "Please run ./build.sh first to create the binary."
    exit 1
fi

# Function to install to system path
install_system() {
    echo "📦 Installing to /usr/local/bin (requires sudo)..."
    sudo cp "$BINARY_PATH" /usr/local/bin/
    sudo chmod +x /usr/local/bin/$BINARY_NAME
    echo "✅ Installed to /usr/local/bin/$BINARY_NAME"
}

# Function to install to user path
install_user() {
    echo "📦 Installing to ~/.local/bin..."
    mkdir -p ~/.local/bin
    cp "$BINARY_PATH" ~/.local/bin/
    chmod +x ~/.local/bin/$BINARY_NAME
    echo "✅ Installed to ~/.local/bin/$BINARY_NAME"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo ""
        echo "⚠️  ~/.local/bin is not in your PATH."
        echo "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        echo "Then run: source ~/.bashrc (or ~/.zshrc)"
    fi
}

# Ask user where to install
echo "Where would you like to install projectdump?"
echo "1) System-wide (/usr/local/bin) - requires sudo"
echo "2) User only (~/.local/bin) - no sudo required"
echo "3) Exit"
echo ""
read -p "Choose option (1/2/3): " choice

case $choice in
    1)
        install_system
        ;;
    2)
        install_user
        ;;
    3)
        echo "Installation cancelled."
        exit 0
        ;;
    *)
        echo "❌ Invalid option. Please choose 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "🧪 Testing installation..."
if command -v $BINARY_NAME &> /dev/null; then
    echo "✅ Installation successful!"
    echo "📋 Version: $($BINARY_NAME --version)"
    echo ""
    echo "🎯 Usage examples:"
    echo "  $BINARY_NAME                    # Current directory"
    echo "  $BINARY_NAME /path/to/project   # Specific path"
    echo "  $BINARY_NAME --help             # Show help"
else
    echo "⚠️  Installation complete but binary not found in PATH."
    echo "You may need to:"
    echo "1. Restart your terminal"
    echo "2. Run: source ~/.bashrc (or ~/.zshrc)"
    echo "3. Check your PATH configuration"
fi

echo ""
echo "🎉 Installation complete!"