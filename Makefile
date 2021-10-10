.PHONY: db
db:
	docker-compose up -d

.PHONY: test
test: db
	pipenv run pytest $(TESTS)