build:
	docker-compose build
test:
	docker-compose build tests && docker-compose run --rm tests
run:
	docker-compose run tests bash
black:
	docker-compose run base_build bash -c 'black .'