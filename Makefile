.PHONY: clean
## clean : clean project files
clean:
	rm -rf build/ dist/ *.egg-info .eggs .coverage htmlcov .mypy_cache
	find . -name '*__pycache__' -exec rm -rf {} +

.PHONY: deps
## deps: install dependencies
deps:
	sudo pip3 install -r requirements.txt

.PHONY: check
## check: Use mypy to lint source codes
check:
	mypy main.py

.PHONY: run
## run: Run main.py
run:
	sudo uvicorn main:app --reload --log-level debug

.PHONY: build
## build: build a docker image for production
build:
	@if docker images | grep "azwar80/core-api"; then\
		docker rmi azwar80/core-api;\
	fi
	docker build -t azwar80/core-api -f prod.Dockerfile .

.PHONY: dockerun
## dokerun: docker run container
dockerun:
	docker run --net=host --rm -p 8000:8000 azwar80/core-api uvicorn main:app --reload --log-level debug

.PHONY: push
## push: push a docker image to registry
push:
	docker push azwar80/core-api


.PHONY: help
all:help
#hel: show this  help message
help: Makefile
	@echo
	@echo " Choose a command to run in "$(NAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' | sed -e 's/^/ /'
	@echo