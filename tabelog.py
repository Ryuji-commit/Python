from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject00.items import Restaurant

class TabelogSpider(CrawlSpider):
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = [
            'https://tabelog.com/rstLst/?SrtT=rt&select_sort_flg=1&Srt=D&sort_mode=1',
    ]

    rules = [
            Rule(LinkExtractor(allow=r'/\w+/rstLst/\d/')),
            Rule(LinkExtractor(allow=r'\w+/rstLst/\d/')),
            Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), callback='parse_restaurant'),
            Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/dtlrvwlst/$'), callback='parse_rvw')
    ]

    def parse_restaurant(self, response):
        item = Restaurant(
            name=response.css('.display-name').xpath('string()').get().strip(),
            ranking=response.css('span.rdheader-rating__score-val-dtl').xpath('string()').get(),
            rvwnumber=response.css('em[property="v:count"]').xpath('string()').get(),
        )

    def parse_rvw(self, response):
        item = Restaurant(
            rvwscore=response.css('b.c-rating__val.c-rating__val--strong').xpath('string()').get(),
        )
        yield item
