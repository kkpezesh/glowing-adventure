# glowing-adventure
quick project to download and store RWIs of construction related webpages for further processing

### dl.py
dl.py accepts a well formatted URL as a command line argument.
prints the URL followed by a json string of a python dictionary to stdout.

### fetch.cpp
fetch.cpp takes creates ceil(# URLs in urls.txt / 3500) threads and calls dl.py on every URL in urls.txt.
It redirects the output of dl.py to data/<thread#> and blocks until every thread has completed its work.
