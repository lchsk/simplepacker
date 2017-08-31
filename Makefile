.PHONY: check clean

check:
	python -m nose --with-coverage -s --cover-package simplepacker

clean:
	rm -f *.log

clean-all: clean
	rm -f *.jpg *.png
