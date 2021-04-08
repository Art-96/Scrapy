import scrapy
from ..items import AmazontutorialItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    page_numers = 2
    start_urls = [
        'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&qid=1617884354&rnid=1250225011&ref=lp_1000_nr_p_n_publication_date_0'
        ]

    def parse(self, response):
        items = AmazontutorialItem()

        product_name = response.css('.a-color-base.a-text-normal::text').extract()
        product_author = [i.strip() for i in response.css('.a-letter-space~ .a-link-normal , .a-color-secondary .a-row .a-size-base:nth-child(2) , .a-size-base.a-link-normal:nth-child(2)').css('::text').extract()]
        product_price = response.xpath('//div[@class="a-section a-spacing-none a-spacing-top-small"]//span[@class="a-price-whole"]/text()').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink
        
        yield items
        
        next_page = "https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page=" + str(AmazonSpiderSpider.page_numers) + "&qid=1617884361&rnid=1250225011&ref=sr_pg_2"
        if AmazonSpiderSpider.page_numers <= 100:
            AmazonSpiderSpider.page_numers += 1 
            yield response.follow(next_page, callback = self.parse)
