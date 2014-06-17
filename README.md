# Tulsa Crime Tracker #

This web app and Scrapy pipeline/script scrapes the [Tulsa Police Department Recent Calls Near You](https://www.tulsapolice.org/live-calls-/police-calls-near-you.aspx) page and generates a map and CSV of the results. The stack is Python, Scrapy, Flask, and Leaflet for mapping.

### Setting up ###

There are some non-Python dependencies. Specifically, in Ubuntu this will take care of those:

    $ apt-get install build-essential openssl python-dev libffi-dev libxml2 libxslt1-dev

Python dependencies are located in the requirement.txt file. To install them, use pip:

    $ pip install --requirement requirement.txt

You will also need a Google Maps API key, which you should put in api_key.py. A skeleton for this file is provided in api_key.py.example.

### Running ###

Start out by doing an initial scrape of the TPD site:

    $ scrapy crawl crimemap

That's the command (or its equivalent through scrapyd) that needs to run regularly to update the app's crime data.

For fire data, it's this command:

    $ python parse_fire.py

Then start up the Flask development server on port 5000 with:

    $ python run_web.py

### License ###

[Leaflet.label](https://github.com/Leaflet/Leaflet.label), included here, is Copyright (c) 2012 Jacob Toye, released under the MIT License.

The remainder is copyright (c) 2014 George Louthan, released under the MIT License.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.