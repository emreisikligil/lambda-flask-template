export FLASK_APP=application.app

.PHONY: deploy-dev
deploy-dev: deref-spec doc
	serverless deploy -s dev

.PHONY: deploy-staging
deploy-staging: deref-spec doc
	serverless deploy -s staging

.PHONY: deploy-prod
deploy-prod: deref-spec doc
	serverless deploy -s prod

.PHONY: run
run: deref-spec doc
	python -m flask run

.PHONY: test
test: deref-spec
	pytest -s -v -p no:cacheprovider

.PHONY: deref-spec
deref-spec:
	@swagger-cli bundle --dereference -o application/spec/swagger-flat.yml -t yaml application/spec/swagger.yml

.PHONY: doc
doc:
	@redoc-cli bundle application/spec/swagger.yml -o docs/index.html --options.pathInMiddlePanel
