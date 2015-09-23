all: html/index.html

html/index.html: schedule.xml
	python schedule_generator.py

clean:
	rm *.pyc
	rm html/index.html
