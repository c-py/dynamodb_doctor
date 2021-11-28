.PHONY: db
db:
	docker-compose up -d

.PHONY: install
install:
	pipenv install --dev

.PHONY: test
test: db
	pipenv run pytest $(TESTS)