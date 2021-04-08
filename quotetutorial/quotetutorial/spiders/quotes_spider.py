import scrapy
from ..items import QuotetutorialItem

class QuoteSpider(scrapy.Spider):
    name = "quotes"
    page_number = 2
    start_urls=[
        'http://quotes.toscrape.com/page/1/'
    ]
    def parse(self, response):
        items=QuotetutorialItem()
        all_div_quotes=response.css("div.quote")
        for i in all_div_quotes:
            title=i.css('span.text::text').extract()
            author=i.css('.author::text').extract()
            tag =i.css('.tag::text').extract()
            items['title']=title
            items['author'] = author
            items['tag'] = tag

            yield items
        next_page = 'http://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'
        if QuoteSpider.page_number < 11:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)