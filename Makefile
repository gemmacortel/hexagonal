.PHONY: help install run dev test clean health lint format

# Helper function to find the correct Python/pip
# These are evaluated dynamically when used
VENV := venv
VENV_BIN := $(VENV)/bin
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip

# Default target
help:
	@echo "🚀 Payee Onboarding Service - Available Commands:"
	@echo ""
	@echo "  make setup      - Complete setup (venv + install)"
	@echo "  make run        - Run the application"
	@echo "  make dev        - Run in development mode with auto-reload"
	@echo "  make health     - Check if the service is running"
	@echo "  make test-api   - Test API with a sample request"
	@echo "  make docs       - Show API documentation URLs"
	@echo "  make clean      - Remove cache files and build artifacts"
	@echo ""
	@echo "Advanced:"
	@echo "  make venv       - Create virtual environment only"
	@echo "  make install    - Install dependencies only"
	@echo "  make test       - Run tests (placeholder)"
	@echo "  make lint       - Run linting checks (placeholder)"
	@echo "  make format     - Format code (placeholder)"
	@echo ""
	@echo "💡 The virtual environment is automatically used when available!"
	@echo ""

# Create virtual environment
venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "📦 Creating virtual environment..."; \
		python3 -m venv $(VENV); \
		echo "✅ Virtual environment created!"; \
	else \
		echo "✅ Virtual environment already exists!"; \
	fi

# Install dependencies
install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Virtual environment not found. Run 'make venv' first."; \
		exit 1; \
	fi
	@echo "📦 Installing dependencies..."
	@$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Complete setup
setup: venv
	@echo "📦 Installing dependencies..."
	@$(PIP) install -r requirements.txt
	@echo "✅ Setup complete!"
	@echo "💡 You can now run commands with 'make run'"

# Run the application
run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@echo "🚀 Starting application..."
	@$(PYTHON) -m app.main

# Run in development mode
dev:
	@if [ ! -d "$(VENV)" ]; then \
		echo "❌ Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@echo "🚀 Starting application in development mode..."
	@$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Health check
health:
	@echo "🏥 Checking service health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Service is not running"

# Test endpoint
test-api:
	@echo "🧪 Testing API endpoint..."
	@curl -X POST http://localhost:8000/api/payees \
		-H "Content-Type: application/json" \
		-d '{"name":"Test User","email":"test@example.com","bank_account":"GB29NWBK60161331926819"}' \
		| python -m json.tool

# Placeholder for unit tests
test:
	@echo "🧪 Running tests..."
	@echo "⚠️  No tests configured yet. Add pytest and test files to implement."

# Placeholder for linting
lint:
	@echo "🔍 Running linting..."
	@echo "⚠️  No linter configured. Consider adding: pip install flake8 black mypy"

# Placeholder for formatting
format:
	@echo "✨ Formatting code..."
	@echo "⚠️  No formatter configured. Consider adding: pip install black isort"

# Clean cache and artifacts
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Show API docs URL
docs:
	@echo "📚 API Documentation:"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc:      http://localhost:8000/redoc"

