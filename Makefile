APP_MAIN=app.main:app
PORT=6970
VENV_DIR=env

.PHONY: start install

start:
	. $(VENV_DIR)/bin/activate && (ollama start > /dev/null 2>&1 &) && uvicorn $(APP_MAIN) --port $(PORT)

install:
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
