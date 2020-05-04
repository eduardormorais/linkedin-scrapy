import urllib
from urllib.parse import urlparse
import json
import tldextract

class UrlFilterGenerator():
    def __init__(self):
        self.url_to_filter = 'https://linkedin.com/search/results/people?'
    
    def create_url(self, data):
        #Origins:
        #GLOBAL_SEARCH_HEADER
        #FACETED_SEARCH
        parameters_dict = {}
        parameters_dict['origin'] = 'FACETED_SEARCH'
        
        # if data['localidade'] != None:
        #     parameters_dict['keywords'] = data['localidade']
        
        if 'setores' in data:
            array_setores = []
            setores_dict = self.read_setores_ids()
            for setor in data['setores']:
                if setor in setores_dict:
                    array_setores.append(setores_dict[setor])
            parameters_dict['facetIndustry'] = array_setores
            
        # if data['cargo'] != None:
        #     parameters_dict['title'] = data['cargo']

        url = self.url_to_filter + urllib.parse.urlencode(parameters_dict, quote_via=urllib.parse.quote).replace("%27", "\"")
        print("\nUrl: {}".format(url))
        return url
    
    def next_page(self, page_filtered, page_number):
        next_page_property = urllib.parse.urlencode({ 'page' : page_number})
        next_page_url = page_filtered + '&{}'.format(next_page_property)
        return next_page_url
    
    def read_setores_ids(self):
        with open('ids_setores.json', 'r') as all_setores_ids:
            setores_ids = json.load(all_setores_ids)
        
        return setores_ids
    
    def get_domain(self, url, remove_http=True):
        url_info = tldextract.extract(url)
        domain_info = '@{}.{}'.format(url_info.domain, url_info.suffix)

        return domain_info

        
    

        
        

