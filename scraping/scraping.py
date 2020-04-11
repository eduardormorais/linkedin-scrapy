import os
from scrapy.http import FormRequest, Request, Response
from scrapy.crawler import CrawlerProcess
from scrapy import Spider
import urllib
import json

os.environ['URL_LOGIN'] = 'https://www.linkedin.com/login/'
os.environ['URL_SEARCH'] = 'https://www.linkedin.com/search/results/people/?keywords=S%C3%A3o%20paulo&origin=CLUSTER_EXPANSION'
os.environ['URL_UPDATE_FILTER'] = 'https://www.linkedin.com/voyager/api/search/history?action=update'

class Linkedin(Spider):

    name = 'linkedin'
    start_urls = [os.environ['URL_LOGIN']]
    
    def __init__(self, email='',  password='',value_search='',output_file='', **kwargs):
        self.value_search = value_search
        self.output_file = output_file
        self.EMAIL = email
        self.PASSWORD = password
        super().__init__(**kwargs)

    def parse(self, response):
        form_login = {'session_key': self.EMAIL,
                      'session_password': self.PASSWORD}
        return FormRequest.from_response(response, formdata=form_login, callback = self.start_search_scaping  )
        
    def start_search_scaping(self, response):
        yield Request(url=os.environ['URL_SEARCH'], callback = self.search)
        
    def search(self, response):
        os.makedirs("files", exist_ok=True) 
        f = open(f"files/{self.output_file}", "w")
        for resp in response.css('div').getall():
            text = resp.encode('utf-8')
            f.write(str(text))
        f.close()
        
        
    #Ideia a principio 
    def update_filter(self):
        payload = [{"filters":["geoRegion->br:0|br:6368",
                               "resultType->PEOPLE"],
                    "keywords":"São paulo",
                    "origin":"FACETED_SEARCH",
                    "searchId":"018fdc67-035e-453f-8025-fe77b9a3299b"}]
        return Request(os.environ['URL_UPDATE_FILTER'] , self.parse, method="POST", body=json.dumps(payload))
        