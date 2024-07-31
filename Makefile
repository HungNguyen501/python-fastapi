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

verify_changes:
	@bash ./$(CiScript) verify_changes $(CHANGES)
	@bazel clean --async

run_integration_tests:
	@bash ./$(CiScript) run_integration_tests

start_docker_compose:
	@echo "Docker compose up..."
	@docker compose -f build/docker-compose.yaml up -d

stop_docker_compose:
	@echo "Docker compose down..."
	@docker compose -f build/docker-compose.yaml down --volumes --remove-orphans
