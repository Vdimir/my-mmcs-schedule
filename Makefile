.PHONY = all clean folders jslib

CORE_JS_FILES = $(wildcard assets/javascript/*.js)
MIN_CORE_JS_FILES=$(CORE_JS_FILES:assets/javascript/%.js=html/js/%.js)
html/js/%.js: assets/javascript/%.js
	cp $^ $@


CORE_CSS_FILES = $(wildcard assets/stylesheet/*.css)
MIN_CORE_CSS_FILES=$(CORE_CSS_FILES:assets/stylesheet/%.css=html/css/%.css)
html/css/%.css: assets/stylesheet/%.css
	cp $^ $@

all: folders html/index.html jslib $(MIN_CORE_CSS_FILES) $(MIN_CORE_JS_FILES)


jslib: html/js/jquery.min.js html/js/moment.min.js 


html/js/jquery.min.js:
	wget http://code.jquery.com/jquery-2.1.4.min.js -O html/js/jquery.min.js

html/js/moment.min.js:
	wget http://momentjs.com/downloads/moment.min.js -O html/js/moment.min.js

html/index.html: schedule.xml template.html
	python schedule_generator.py

folders: html html/css html/js
html:
	mkdir -p html
html/js:
	mkdir -p html/js
html/css:
	mkdir -p html/css
	
clean:
	rm -f *.pyc
	rm -rf html/*

