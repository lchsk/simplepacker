.PHONY: check clean

check:
	python -m nose --with-coverage -s --cover-package simplepacker

clean:
	rm *.log
