E2E_DIRECTORY = e2e
E2E_DOCKER_COMPOSE = $(E2E_DIRECTORY)/docker-compose.yml
SCRIPTS_DIRECTORY = scripts
NODE_MODULES_BIN = node_modules/.bin
MEDTAGGER_CONFIGURATION = $(PWD)/e2e/.medtagger.yml

NG_SERVE_PID_FILE = ng_serve.pid
REST_PID_FILE = rest.pid
WEBSOCKET_PID_FILE = websocket.pid
WORKERS_PID_FILE = workers.pid

#
# Docker - Build & Push to Docker Hub
#

docker_build:
	docker-compose build medtagger_backend_rest medtagger_frontend medtagger_backend_websocket medtagger_backend_worker medtagger_backend_database_migrations

docker_push_stable: docker_push_version
	docker push medtagger/frontend_ui:latest
	docker push medtagger/backend_rest:latest
	docker push medtagger/backend_websocket:latest
	docker push medtagger/backend_worker:latest
	docker push medtagger/backend_database_migrations:latest

docker_push_nightly: docker_push_version
	docker push medtagger/frontend_ui:nightly
	docker push medtagger/backend_rest:nightly
	docker push medtagger/backend_websocket:nightly
	docker push medtagger/backend_worker:nightly
	docker push medtagger/backend_database_migrations:nightly

docker_tag_as_stable:
	docker tag medtagger/frontend_ui:latest $(MEDTAGGER_VERSION)
	docker tag medtagger/backend_rest:latest $(MEDTAGGER_VERSION)
	docker tag medtagger/backend_websocket:latest $(MEDTAGGER_VERSION)
	docker tag medtagger/backend_worker:latest $(MEDTAGGER_VERSION)
	docker tag medtagger/backend_database_migrations:latest $(MEDTAGGER_VERSION)

docker_tag_as_latest:
	docker tag medtagger/frontend_ui:$(MEDTAGGER_VERSION) latest
	docker tag medtagger/backend_rest:$(MEDTAGGER_VERSION) latest
	docker tag medtagger/backend_websocket:$(MEDTAGGER_VERSION) latest
	docker tag medtagger/backend_worker:$(MEDTAGGER_VERSION) latest
	docker tag medtagger/backend_database_migrations:$(MEDTAGGER_VERSION) latest

docker_tag_as_nightly:
	docker tag medtagger/frontend_ui:$(MEDTAGGER_VERSION) nightly
	docker tag medtagger/backend_rest:$(MEDTAGGER_VERSION) nightly
	docker tag medtagger/backend_websocket:$(MEDTAGGER_VERSION) nightly
	docker tag medtagger/backend_worker:$(MEDTAGGER_VERSION) nightly
	docker tag medtagger/backend_database_migrations:$(MEDTAGGER_VERSION) nightly

docker_push_version:
	docker push medtagger/frontend_ui:$(MEDTAGGER_VERSION)
	docker push medtagger/backend_rest:$(MEDTAGGER_VERSION)
	docker push medtagger/backend_websocket:$(MEDTAGGER_VERSION)
	docker push medtagger/backend_worker:$(MEDTAGGER_VERSION)
	docker push medtagger/backend_database_migrations:$(MEDTAGGER_VERSION)

#
# E2E Tests
#

e2e:
	make e2e__prepare_environment
	@if ! make e2e__run; then\
		make e2e__stop_medtagger;\
		make e2e__clear_dependencies;\
		echo "E2E Tests failed!";\
		exit 1;\
	fi
	make e2e__delete_environment
	echo "E2E Tests passed!"

e2e_docker:
	docker-compose -f $(E2E_DOCKER_COMPOSE) up --build -d
	cd e2e && npm install
	@if ! make e2e__run_docker; then\
	    docker-compose -f $(E2E_DOCKER_COMPOSE) logs e2e_medtagger_backend_database_migrations;\
		docker-compose -f $(E2E_DOCKER_COMPOSE) down;\
		echo "E2E Tests failed!";\
		exit 1;\
	fi
	docker-compose -f $(E2E_DOCKER_COMPOSE) down
	echo "E2E Tests passed!"

e2e__prepare_environment:
	docker-compose -f $(E2E_DOCKER_COMPOSE) up -d e2e_cassandra e2e_postgres e2e_rabbitmq
	cd e2e && npm install
	. $(E2E_DIRECTORY)/configuration.sh && cd backend && ./$(SCRIPTS_DIRECTORY)/dev__prepare_backend.sh $(MEDTAGGER_CONFIGURATION)

e2e__start_medtagger:
	@if test -f "$(NG_SERVE_PID_FILE)" || test -f "$(REST_PID_FILE)" || test -f "$(WEBSOCKET_PID_FILE)" || test -f "$(WORKERS_PID_FILE)"; then\
		echo "MedTagger is already running! Please stop it with \"make e2e__stop_medtagger\" first!";\
		exit 1;\
	fi
	cd frontend && { ng serve -c local & echo $$! > ../$(NG_SERVE_PID_FILE); }
	. $(E2E_DIRECTORY)/configuration.sh && cd backend && { make run_rest & echo $$! > ../$(REST_PID_FILE); }
	. $(E2E_DIRECTORY)/configuration.sh && cd backend && { make run_websocket & echo $$! > ../$(WEBSOCKET_PID_FILE); }
	. $(E2E_DIRECTORY)/configuration.sh && cd backend && { make run_workers & echo $$! > ../$(WORKERS_PID_FILE); }

e2e__stop_medtagger:
	@if test -f "$(NG_SERVE_PID_FILE)"; then\
		echo "Killing Ng Serve!";\
		kill `cat $(NG_SERVE_PID_FILE)` || echo "Process already killed!";\
	fi
	@if test -f "$(REST_PID_FILE)"; then\
		echo "Killing REST API!";\
		kill `cat $(REST_PID_FILE)` || echo "Process already killed!";\
	fi
	@if test -f "$(WEBSOCKET_PID_FILE)"; then\
		echo "Killing WebSocket API!";\
		kill `cat $(WEBSOCKET_PID_FILE)` || echo "Process already killed!";\
	fi
	@if test -f "$(WORKERS_PID_FILE)"; then\
		echo "Killing Worker!";\
		kill `cat $(WORKERS_PID_FILE)` || echo "Process already killed!";\
	fi
	rm -f $(NG_SERVE_PID_FILE)
	rm -f $(REST_PID_FILE)
	rm -f $(WEBSOCKET_PID_FILE)
	rm -f $(WORKERS_PID_FILE)

e2e__run:
	make e2e__start_medtagger
	sleep 30  # Let's wait a while for booting up of all services
	@if ! make e2e__execute; then \
		make e2e__stop_medtagger;\
		echo "E2E Tests failed!";\
		exit 1;\
	fi
	make e2e__stop_medtagger
	echo "E2E Tests passed!"

e2e__run_docker:
	sleep 30  # Let's wait a while for booting up of all services
	cd $(E2E_DIRECTORY) && CYPRESS_HOST_URL=http://localhost/ CYPRESS_API_URL=http://localhost/api/v1/ $(NODE_MODULES_BIN)/cypress run --record

e2e__execute:
	cd $(E2E_DIRECTORY) && $(NODE_MODULES_BIN)/cypress run

e2e__delete_environment:
	. $(E2E_DIRECTORY)/configuration.sh && cd backend && alembic downgrade base
	make e2e__clear_dependencies

e2e__clear_dependencies:
	docker-compose -f $(E2E_DOCKER_COMPOSE) down

.PHONY: docker_build docker_tag_as_latest docker_tag_as_nightly docker_push docker_push_nightly docker_push_version \
        e2e e2e_docker e2e__prepare_environment e2e__run e2e__delete_environment e2e__clear_dependencies
