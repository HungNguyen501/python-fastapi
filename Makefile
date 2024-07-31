ProjectName := Python-Api-Template
CiScript := ci/ci.sh
IntegrationTest := ci/integration_tests

install:
	@python3.12 --version
	@python3.12 -m pip install --upgrade pip --break-system-packages
	@python3.12 -m pip install -r ./ci/requirements.txt --break-system-packages

pep8:
	@bash ./$(CiScript) check_pep8 $(LOCATION)

test:
	@bash ./$(CiScript) run_unit_tests $(LOCATION)

check_incremental_changes:
	@bash ./$(CiScript) check_incremental_changes $(CHANGES)
	@bazel clean --async

run_integration_test:
	@bash ./$(IntegrationTest)/test_database.sh test_connection
	@bash ./$(IntegrationTest)/test_database.sh test_tables_deletion
	@bash ./$(IntegrationTest)/test_database.sh test_tables_creation
	@bash ./$(IntegrationTest)/test_user_api.sh
	@bash ./$(IntegrationTest)/test_database.sh test_tables_deletion

start_docker_compose:
	@docker compose -f build/docker-compose.yaml up -d

stop_docker_compose:
	@docker compose -f build/docker-compose.yaml down --volumes --remove-orphans
