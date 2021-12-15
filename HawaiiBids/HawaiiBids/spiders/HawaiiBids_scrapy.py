import scrapy
import random
import time
from time import sleep


class HawaiibidsScrapySpider(scrapy.Spider):
    name = 'HawaiiBids_scrapy'
    allowed_domains = ['www.hawaiibids.us']
    base_url = "https://www.hawaiibids.us"
    start_urls = ['https://www.hawaiibids.us/hawaii-contractors/search.htm/']

    def strip_and_join(self, array):
        # array = map(lambda s: s.strip(), array)
        # string = ", ".join(array)
        string = ", ".join([i for i in array if i.strip() != ''])

        return string
    
    def parse(self, response):
        # scrapy.Request("https://www.hawaiibids.us/hawaii-contractors/search.htm?page=1")
        # last_page = response.xpath("//div[@class='list-navi']/a[@data-ci-pagination-page]").get()

        for i in range(1, 81):
            yield scrapy.Request(f"https://www.hawaiibids.us/hawaii-contractors/search.htm?page={i}", callback=self.parse_requests)
    
    def parse_requests(self, response):
        kompany_url_l = [kl for kl in response.xpath("//div[@class='lr-title lr-mar']/a/@href").extract()]
        # print(kompany_url_l)
        sleep(round(random.uniform(0.1, 0.60), 1))
        for ul in kompany_url_l:
            yield scrapy.Request(f"{self.base_url}{ul}", callback = self.parse_pages)

    def parse_pages(self, response):
        Company_Name = response.xpath("//dt[contains(text(),'Company Name:')]/following-sibling::dd[1]//text()").extract_first()
        Address = response.xpath("//dt[contains(text(),'Address:')]/following-sibling::dd[1]//text()").extract_first()
        City = response.xpath("//dt[contains(text(),'City:')]/following-sibling::dd[1]//text()").extract_first()
        State = response.xpath("//dt[contains(text(),'State:')]/following-sibling::dd[1]//text()").extract_first()
        Zip_Code = response.xpath("//dt[contains(text(),'Zip Code:')]/following-sibling::dd[1]//text()").extract_first()
        Phone = response.xpath("//dt[contains(text(),'Phone:')]/following-sibling::dd[1]//text()").extract_first()
        Fax = response.xpath("//dt[contains(text(),'Fax:')]/following-sibling::dd[1]//text()").extract_first()
        Contact_Person = response.xpath("//dt[contains(text(),'Contact Person:')]/following-sibling::dd[1]//text()").extract_first()
        Contact_Title = response.xpath("//dt[contains(text(),'Contact Title:')]/following-sibling::dd[1]//text()").extract()
        Legal_Structure = response.xpath("//dt[contains(text(),'Legal Structure:')]/following-sibling::dd[1]//text()").extract()
        Year_Established = response.xpath("//dt[contains(text(),'Year Established:')]/following-sibling::dd[1]//text()").extract()
        Business_Type = response.xpath("//dt[contains(text(),'Business Type:')]/following-sibling::dd[1]//text()").extract()
        Certification_Type = response.xpath("//dt[contains(text(),'Certification Type:')]/following-sibling::dd[1]//text()").extract()
        Sales_Service_Area = response.xpath("//dt[contains(text(),'Sales/Service Area:')]/following-sibling::dd[1]//text()").extract()
        Ownership = response.xpath("//dt[contains(text(),'Ownership:')]/following-sibling::dd[1]//text()").extract()


        print('=' * 50)

        print("Company_Name >>> ", Company_Name)
        print("Address >>> ", Address)
        print("City >>> ", City)
        print("State >>> ", State)
        print("Zip_Code >>> ", Zip_Code)
        print("Phone >>> ", Phone)
        print("Fax >>> ", Fax)
        print("Contact_Person >>> ", Contact_Person)
        print("Contact_Title >>> ", self.strip_and_join(Contact_Title))
        print("Legal_Structure >>> ", self.strip_and_join(Legal_Structure))
        print("Year_Established >>> ", self.strip_and_join(Year_Established))
        print("Business_Type >>> ", self.strip_and_join(Business_Type))
        print("Certification_Type >>> ", self.strip_and_join(Certification_Type))
        print("Sales_Service_Area >>> ", self.strip_and_join(Sales_Service_Area))
        print("Ownership >>> ", self.strip_and_join(Ownership))

        print('=' * 50)
        
        yield {
            'job_post_url': response.request.url,
            'Company_Name': Company_Name,
            'Address': Address,
            'City': City,
            'State': State,
            'Zip_Code': Zip_Code,
            'Phone': Phone,
            'Fax': Fax,
            'Contact_Person': Contact_Person,
            'Contact_Title': self.strip_and_join(Contact_Title),
            'Legal_Structure': self.strip_and_join(Legal_Structure),
            'Year_Established': self.strip_and_join(Year_Established),
            'Business_Type': self.strip_and_join(Business_Type),
            'Certification_Type': self.strip_and_join(Certification_Type),
            'Sales_Service_Area': self.strip_and_join(Sales_Service_Area),
            'Ownership': self.strip_and_join(Ownership)
            }