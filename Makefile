ProjectName := Python-Api-Template
CiScript := ci/ci.sh

pep8:
	@bash ./$(CiScript) check_pep8 ./src/

