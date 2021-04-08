import scrapy
from scrapy.http import FromRequest
from scrapy.utils.response import open_in_browser
from ..items import QuotetutorialItem

class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls=[
        'http://quotes.toscrape.com/login'
    ]
    def parse(self, response):
        token = response.css('from input::attr(value)').extract_first()
        return FromRequest.from_response(response, formdata={
            'csrf_tokan' : token,
            'username' : 'your login',
            'password' : 'your password'
        }, callback = self.start_scraping)

    def start_scraping(self, response):
        open_in_browser(response)
        items = QuotetutorialItem()

        all_div_quotes=response.css("div.quote")
        
        for i in all_div_quotes:
            title=i.css('span.text::text').extract()
            author=i.css('.author::text').extract()
            tag =i.css('.tag::text').extract()

            items['title']=title
            items['author'] = author
            items['tag'] = tag

            yield items