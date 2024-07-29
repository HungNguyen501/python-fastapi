ProjectName := Python-Api-Template
CiScript := ci/ci.sh
IntegrationTest := ci/integration_tests

run_api:
	@uvicorn src.api.application:get_app --host 0.0.0.0 --port 8009 --workers 1 --reload

pep8:
	@bash ./$(CiScript) check_pep8 $(location)

test:
	@bash ./$(CiScript) run_unit_tests $(location)

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
