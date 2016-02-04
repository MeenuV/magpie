.PHONY: clean build dev tests deploy

default:

install:
	./install.sh

build:
	./build.sh

dev:
	PYTHONPATH=. python client/api.py

prod:
	PYTHONPATH=. python client/api.py

tests:
	PYTHONPATH=. nosetests test

deploy_setup:
	. ./config/deploy_config.sh
	fab prod setup

deploy:
	. ./config/deploy_config.sh
	fab prod pack deploy

clean:
	find client -name "*.pyc" -exec rm -rf {} \;

clean-logs:
	rm -r logs/*
