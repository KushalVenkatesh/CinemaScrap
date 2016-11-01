# Scraps today's movies and corresponding times.
import scrapy
from scrapy.selector import Selector

class CinemaSpider(scrapy.Spider):
    name = "cinema"
    allowed_domains = ['cinemaxx.de'] #Only Scrap Cinemaxx Sites
    start_urls = [
        'https://www.cinemaxx.de/trier/programm/aktuellesprogramm?SwitchCinemaId=76', # CineMaxx Trier
    ]

    def parse(self, response):
        sel = Selector(response)
        movies = sel.xpath('.//div[contains(@class, "fx")]')

        for movie in movies:
            times = movie.xpath('.//table//td[contains(@class, "tdy")]//a/text()').extract()
            names = movie.xpath('.//h3/text()').extract()

            times_list = []

            for item in times:
                times_list.append(item)
            for name in names:
                yield {
                    'name': name,
                    'times': times_list
                }
