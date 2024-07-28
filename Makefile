ProjectName := Python-Api-Template
CiScript := ci/ci.sh
IntegrationTest := ci/integration_tests

init:
	@bash ./$(CiScript) init

run_api:
	@uvicorn src.api.application:get_app --host 0.0.0.0 --port 8009 --workers 1 --reload

pep8:
	@bash ./$(CiScript) check_pep8 $(location)

test:
	@bash ./$(CiScript) run_unit_tests $(location)

test_db:
	@bash ./$(IntegrationTest)/test_database.sh $(func)

test_user_api:
	@bash ./$(IntegrationTest)/test_user_api.sh $(func)




