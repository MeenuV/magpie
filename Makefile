default:

install:
	./install.sh

build:
	./build.sh

dev:
	export IS_DEV=true
	PYTHONPATH=. python client/api.py

prod:
	export IS_DEV=false
	PYTHONPATH=. python client/api.py

tests:
	PYTHONPATH=. nosetests test

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

clean-logs:
	rm -r logs/*
