# Variables
APP_MAIN=app.main
PORT=6970
VENV_DIR=env
BIN_DIR=bin
FRONTEND_DIR=../cadmium-electron-app

# Default target
.PHONY: start install compile frontend clean help run

# Help target (default action if no target is specified)
help:
	@echo "Available make targets:"
	@echo "  start      - Start the backend server and Ollama service"
	@echo "  install    - Install Python dependencies from requirements.txt"
	@echo "  compile    - Compile the backend into a standalone binary using Nuitka"
	@echo "  frontend   - Start the Electron frontend"
	@echo "  run        - Start both backend and frontend concurrently"
	@echo "  clean      - Remove build artifacts"
	@echo "  help       - Display this help message"

# Start backend server and Ollama service
start:
	@echo "Starting backend server and Ollama service..."
	. $(VENV_DIR)/bin/activate && \
	(ollama start > /dev/null 2>&1 &) && \
	uvicorn $(APP_MAIN):app --port $(PORT)

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt

# Compile backend into a standalone binary
compile:
	@echo "Compiling backend with Nuitka..."
	. $(VENV_DIR)/bin/activate && \
	nuitka --standalone --include-package=websockets --include-package=websockets.asyncio.client \
	       --output-dir=$(BIN_DIR) app/main.py

# Start frontend (Electron app)
frontend:
	@echo "Starting frontend..."
	cd $(FRONTEND_DIR) && npm start

# Clean up build artifacts
clean:
	@echo "Cleaning up build artifacts..."
	rm -rf $(BIN_DIR) *.dist *.build

# Run both backend and frontend concurrently
run:
	@echo "Starting both backend and frontend..."
	@make start & \
	make frontend
