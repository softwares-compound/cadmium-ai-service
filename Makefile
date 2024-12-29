APP_MAIN=app.main
PORT=6970
VENV_DIR=env
BIN_DIR=bin

.PHONY: start install compile

start:
	. $(VENV_DIR)/bin/activate && (ollama start > /dev/null 2>&1 &) && uvicorn $(APP_MAIN):app --port $(PORT)

install:
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt

compile:
	. $(VENV_DIR)/bin/activate && nuitka --standalone --output-dir=$(BIN_DIR) app/main.py
