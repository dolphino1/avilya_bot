build:
	docker-compose -f docker-compose-development.yml build
view_compose:
	docker-compose -f docker-compose-development.yml up
compose:
	docker-compose -f docker-compose-development.yml up -d
dev-restart:
	docker-compose -f docker-compose-development.yml up -d
dev_build:
	docker-compose -f docker-compose-development.yml build
	docker-compose -f docker-compose-development.yml up -d
production_build:
	docker-compose -f docker-compose-production.yml build
	docker-compose -f docker-compose-production.yml up -d
test:
	docker-compose -f docker-compose.test.yml build
	docker-compose -f docker-compose.test.yml up -d
