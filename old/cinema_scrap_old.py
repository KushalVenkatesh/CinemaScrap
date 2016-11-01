# run with: scrapy runspider cinema_scrap.py -o movies.json
import scrapy
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Define Spider Class
class CinemaSpider(scrapy.Spider):
    name = "cinema"
    allowed_domains = ['cinemaxx.de'] #Only Scrap Cinemaxx Sites
    start_urls = [
        'https://www.cinemaxx.de/trier/programm/aktuellesprogramm?SwitchCinemaId=76', # CineMaxx Trier
    ]

    # Define Parse Function
    def parse(self, response):
        movie_names = response.css('.progtitle h2').extract()
        for movie_name in movie_names:
            yield {
                'name': movie_name.replace('<h2>', '').replace('</h2>', '')
            }
