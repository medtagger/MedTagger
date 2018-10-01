E2E_DIRECTORY = e2e
E2E_DOCKER_COMPOSE = $(E2E_DIRECTORY)/docker-compose.yml
SCRIPTS_DIRECTORY = scripts
NODE_MODULES_BIN = node_modules/.bin

NG_SERVE_PID_FILE = ng_serve.pid
REST_PID_FILE = rest.pid
WEBSOCKET_PID_FILE = websocket.pid
WORKERS_PID_FILE = workers.pid

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
	echo "E2E Tests passed!"
	make e2e__delete_environment

e2e_docker:
	docker-compose -f $(E2E_DOCKER_COMPOSE) up --build -d
	cd e2e && npm install
	@if ! make e2e__run_docker; then\
		docker-compose -f $(E2E_DOCKER_COMPOSE) down;\
		echo "E2E Tests failed!";\
		exit 1;\
	fi
	echo "E2E Tests passed!"
	docker-compose -f $(E2E_DOCKER_COMPOSE) down

e2e__prepare_environment:
	docker-compose -f $(E2E_DOCKER_COMPOSE) up -d cassandra postgres rabbitmq
	cd e2e && npm install
	. $(E2E_DIRECTORY)/configuration.sh && cd backend && ./$(SCRIPTS_DIRECTORY)/dev__prepare_backend.sh

e2e__start_medtagger:
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
	cd $(E2E_DIRECTORY) && $(NODE_MODULES_BIN)/cypress run
	make e2e__stop_medtagger

e2e__run_docker:
	sleep 30  # Let's wait a while for booting up of all services
	cd $(E2E_DIRECTORY) && CYPRESS_HOST_URL=http://localhost/ CYPRESS_API_URL=http://localhost/api/v1/ $(NODE_MODULES_BIN)/cypress run

e2e__delete_environment:
	. $(E2E_DIRECTORY)/configuration.sh && cd backend && alembic downgrade base
	make e2e__clear_dependencies

e2e__clear_dependencies:
	docker-compose -f $(E2E_DOCKER_COMPOSE) down

.PHONY: e2e e2e_docker e2e__prepare_environment e2e__run e2e__delete_environment e2e__clear_dependencies
