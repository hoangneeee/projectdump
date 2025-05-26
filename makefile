# Makefile for ProjectDump

.PHONY: help build install clean test dev-install uninstall

BINARY_NAME = projectdump
BUILD_DIR = dist
INSTALL_DIR = /usr/local/bin
USER_INSTALL_DIR = $(HOME)/.local/bin

help: ## Show this help message
	@echo "ProjectDump Build System"
	@echo "======================="
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the binary using PyInstaller
	@echo "🚀 Building ProjectDump binary..."
	@chmod +x build.sh
	@./build.sh

install: build ## Install binary to /usr/local/bin (requires sudo)
	@echo "📦 Installing to $(INSTALL_DIR)..."
	@sudo cp $(BUILD_DIR)/$(BINARY_NAME) $(INSTALL_DIR)/
	@sudo chmod +x $(INSTALL_DIR)/$(BINARY_NAME)
	@echo "✅ Installed to $(INSTALL_DIR)/$(BINARY_NAME)"

install-user: build ## Install binary to ~/.local/bin (no sudo)
	@echo "📦 Installing to $(USER_INSTALL_DIR)..."
	@mkdir -p $(USER_INSTALL_DIR)
	@cp $(BUILD_DIR)/$(BINARY_NAME) $(USER_INSTALL_DIR)/
	@chmod +x $(USER_INSTALL_DIR)/$(BINARY_NAME)
	@echo "✅ Installed to $(USER_INSTALL_DIR)/$(BINARY_NAME)"
	@echo ""
	@echo "⚠️  Make sure $(USER_INSTALL_DIR) is in your PATH"
	@echo "Add this to your ~/.bashrc or ~/.zshrc:"
	@echo "export PATH=\"$(USER_INSTALL_DIR):\$$PATH\""

dev-install: ## Install in development mode (pip install -e .)
	@echo "📦 Installing in development mode..."
	@pip install -e .
	@echo "✅ Development installation complete"

test: ## Test the built binary
	@if [ -f "$(BUILD_DIR)/$(BINARY_NAME)" ]; then \
		echo "🧪 Testing binary..."; \
		./$(BUILD_DIR)/$(BINARY_NAME) --version; \
		echo "✅ Binary test passed"; \
	else \
		echo "❌ Binary not found. Run 'make build' first."; \
		exit 1; \
	fi

clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.spec build_env/
	@rm -rf projectdump.egg-info/
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete"

uninstall: ## Uninstall the binary
	@echo "🗑️  Uninstalling ProjectDump..."
	@sudo rm -f $(INSTALL_DIR)/$(BINARY_NAME) || true
	@rm -f $(USER_INSTALL_DIR)/$(BINARY_NAME) || true
	@echo "✅ Uninstall complete"

release: clean build test ## Create a release build
	@echo "🎯 Creating release..."
	@mkdir -p release
	@cp $(BUILD_DIR)/$(BINARY_NAME) release/
	@cd release && tar -czf $(BINARY_NAME)-$(shell uname -s)-$(shell uname -m).tar.gz $(BINARY_NAME)
	@echo "✅ Release created in release/ directory"

# Default target
all: build