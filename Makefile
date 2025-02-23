ProjectName := Python-Api-Template
CiScript := scripts/ci/ci.sh
GithookScript := scripts/githooks.sh
IntegrationTest := scripts/ci/integration_tests

install:
	@bash ./$(CiScript) install

pep8:
	@bash ./$(CiScript) check_pep8 $(LOCATION)

test:
	@bash ./$(CiScript) run_unit_tests $(LOCATION)

verify_changes:
	@bash ./$(CiScript) verify_changes $(CHANGES)
	@bazel clean --async

run_integration_tests:
	@bash ./$(CiScript) run_integration_tests

docker_compose_up:
	@docker compose -f docker-compose.yaml up -d

docker_compose_down:
	@docker compose -f docker-compose.yaml down --volumes --remove-orphans

migrate_info:
	@cd src/infrastructures/databases/sql && flyway info -user=local -password=local -url=jdbc:postgresql://localhost:5432/local && cd -

migrate:
	@cd src/infrastructures/databases/sql && flyway migrate -user=local -password=local -url=jdbc:postgresql://localhost:5432/local && cd -

clean_migrate:
	@cd src/infrastructures/databases/sql && flyway clean migrate -user=local -password=local -url=jdbc:postgresql://localhost:5432/local && cd -

githook:
	@bash ./$(GithookScript) create_pre_commit_file
