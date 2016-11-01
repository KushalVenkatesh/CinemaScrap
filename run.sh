#!/bin/bash

echo "Starting scraper."
scrapy runspider cinema_scrap.py -o movies.json
#scrapy runspider cinema_scrap.py -t -json --nolog -o - > "movies.json"
echo "Scrap complete. Checking movies with IMDb."
python check_imdb.py movies.json
rm movies.json
