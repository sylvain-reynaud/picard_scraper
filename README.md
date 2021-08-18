# Picard Scraper

Python3 script aiming to scrape products of picard.fr and extracting name, price, nutriscore, kcal, kcal/price ratio, full url.

## How to use

### Setup

Install `setuptools_rust` and `Scrapy`

`pip3 install setuptools_rust Scrapy`

### Run

On Linux :

`source venv/bin/activate` if you have a venv.

`scrapy crawl plats -o out.csv -t csv`

The output file is `out.csv`
