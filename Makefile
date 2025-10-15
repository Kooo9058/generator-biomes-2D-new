# Virtual environment name
VENV = venv

# Main Python command
PYTHON = $(VENV)/bin/python

# OS detection (for Windows compatibility)
ifeq ($(OS),Windows_NT)
    ACTIVATE = $(VENV)\Scripts\activate
    PYTHON = $(VENV)\Scripts\python.exe
else
    ACTIVATE = source $(VENV)/bin/activate
endif

# Install dependencies and create virtual environment
install:
	python -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

# Run the project
run:
	$(VENV)/bin/python main.py

# Remove virtual environment
clean:
	@echo "🧹 Removing virtual environment..."
	rm -rf $(VENV)

# Update dependencies
update:
	@echo "🔄 Updating dependencies..."
	$(ACTIVATE) && pip install -r requirements.txt --upgrade
