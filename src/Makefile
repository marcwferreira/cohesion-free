PYTHON = python3

.PHONY: requirements game

RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(RUN_ARGS):;@:)

# Run the game
game:
	@echo "Starting game..."
	@$(PYTHON) main.py $(filter-out $@, $(MAKECMDGOALS))

# Compile the program
compile: clean requirements

# Install all the necessay requirements for the game
requirements:
	@echo "Installing pygame..."
	@pip install -q -r requirements.txt

# Clean cache files
clean:
	@echo "Cleaning cache files..."
	@find . | grep -E "(/__pycache__)" | xargs rm -rf
