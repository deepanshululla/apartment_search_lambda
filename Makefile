deploy:
	sls deploy -v

invoke:
	sls invoke -f hello

build:
	npm init
	sls plugin install -n serverless-python-requirements