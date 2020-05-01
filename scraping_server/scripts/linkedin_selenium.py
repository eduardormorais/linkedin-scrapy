import time
import os
import json
import unidecode
from flask_restful import Resource
from bs4 import BeautifulSoup
from url_filter_generator import UrlFilterGenerator
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

os.environ['email'] = 'tguzenski@yahoo.com.br'
os.environ['senha'] = 'Eagorajose?'
os.environ['api_key_zerobounce'] = '4d4f257126fd4f90be05ecc1a62a2541'

class LinkedinSelenium(Resource):
    def __init__(self):
        self.login_url = "https://www.linkedin.com/login"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_driver_path = "./chromedriver"
        self.url_filter_generator = UrlFilterGenerator()

    def sign_in(self, driver):
        driver.get(self.login_url)
        username = driver.find_element_by_name("session_key")
        password = driver.find_element_by_name("session_password")
        username.send_keys(os.environ['email'])
        password.send_keys(os.environ['senha'])
        button_login = driver.find_elements_by_xpath(
            "//button[@type='submit']")[0]
        button_login.click()

    def save_session_cookies(self, driver):
        print('Salvando cookies...')
        with open('cookies.json', 'w') as cookie_file:
            json.dump(driver.get_cookies(), cookie_file)

    def read_session_cookies(self):
        with open('cookies.json', 'r') as cookie_file:
            cookies = json.load(cookie_file)

        return cookies
    
    def set_output_file(self, output_file):
        self.output_file = output_file

    def start_searching(self, valor_pesquisa):
        chrome_driver = webdriver.Chrome(
            executable_path=self.chrome_driver_path)
        chrome_driver.get(self.login_url)
        cookies = self.read_session_cookies()
        for cookie in cookies:
            chrome_driver.add_cookie(cookie)

        main_search_url = self.url_filter_generator.create_url(valor_pesquisa)
        profile_users = []
        next_page_number = 1
        search_url = main_search_url
        fixed_number_of_pages = 100
        required_elements_json = ['included', 'navigationUrl', 'trackingUrn']
        while next_page_number <= fixed_number_of_pages: # Número de páginas que o script irá percorrer.
            chrome_driver.get(search_url)
            beautiful_soup = BeautifulSoup(chrome_driver.page_source, features="html5lib")
            search_page_tags_code = beautiful_soup.find_all("code")
            for search_page_tag_code in search_page_tags_code:
                if self.is_json(search_page_tag_code.text) == True:
                    search_data_tag_code = json.loads(search_page_tag_code.text)
                    if all(tag_element in str(search_data_tag_code) for tag_element in required_elements_json):
                        for elements_json in search_data_tag_code['data']['elements']:
                            if 'targetUrn' in str(elements_json):
                                users_elements = elements_json['elements']
                                break
                        break
            
            for user_element in users_elements:
                if len(profile_users) == int(valor_pesquisa['qtd']):
                    next_page_number = fixed_number_of_pages
                    break

                chrome_driver.get(user_element['navigationUrl'])
                profile_user = self.get_profile_data(chrome_driver.page_source)
                if profile_user['empregado'] is True:
                    chrome_driver.get(profile_user['empresa_linkedin_url'])
                    company_website_url = self.get_company_url(chrome_driver.page_source)
                    if company_website_url is not None:
                        profile_user['dominio_empresa'] = self.url_filter_generator.get_domain(company_website_url)
                        self.create_fake_mail(profile_user)
                        # self.create_email(profile_user)
                        profile_users.append(profile_user)

            next_page_number += 1
            search_url = self.url_filter_generator.next_page(main_search_url, next_page_number)

        print(profile_users)
        time.sleep(5)
        self.save_search_result(profile_users)
    
    def create_fake_mail(self, profile_user):
        first_name = unidecode.unidecode(profile_user['primeiroNome'].split(' ')[0].lower())
        last_name = unidecode.unidecode(profile_user['sobrenome'].split(' ')[0].lower())
        profile_user['email'] = '{}.{}@{}'.format(first_name, last_name, profile_user['dominio_empresa'])


    def get_profile_data(self, html_page):
        profile_data = {}
        included_elements_user = {}
        required_elements_json = ['included', 'firstName', 'lastName', 'dateRange']
        beautiful_soup = BeautifulSoup(html_page, features="html5lib")
        tags_code = beautiful_soup.find_all('code')
        for tag_code in tags_code:
            if self.is_json(tag_code.text) == True:
                data_tag_code = json.loads(tag_code.text)
                if all(tag_element in str(data_tag_code) for tag_element in required_elements_json):
                    included_elements_user = data_tag_code['included']
                    break
        
        profile_data['empregado'] = False
        required_company_elements = ['url', 'industry', 'entityUrn', 'name']
        company_urn = ''
        for included_element in included_elements_user:
            if 'dateRange' in included_element:
                if 'end' not in included_element['dateRange'] and 'title' in included_element and 'companyName' in included_element and 'companyUrn' in included_element:
                    company_urn = included_element['companyUrn']
                    profile_data['empresa'] = included_element['companyName']
                    profile_data['cargo'] = included_element['title']
                    profile_data['empregado'] = True
            
            if 'firstName' in included_element:
                profile_data['primeiroNome'] = included_element['firstName']
                profile_data['sobrenome'] = included_element['lastName']
            
            if all(tag_element in (included_element) for tag_element in required_company_elements):
                if included_element['entityUrn'] == company_urn:
                    profile_data['empresa_linkedin_url'] = included_element['url']
                    
        return profile_data
    
    def get_company_url(self, company_page):
        company_url = ''
        included_elements_company = ''
        required_elements_json = ['data', 'meta', 'included', 'companyPageUrl', 'universalName']
        beautiful_soup_company_page = BeautifulSoup(company_page, features="html5lib")
        tags_code = beautiful_soup_company_page.find_all('code')
        for tag_code in tags_code:
            if self.is_json(tag_code.text) == True:
                data_tag_code = json.loads(tag_code.text)
                if all(tag_element in str(data_tag_code) for tag_element in required_elements_json):
                    included_elements_company = data_tag_code['included']
                    break
        
        for included_element_company in included_elements_company:
            if 'companyPageUrl' in included_element_company and 'universalName' in included_element_company:
                company_url = included_element_company['companyPageUrl']
        
        return company_url

    def is_json(self, string_object):
        try:
            json_object = json.loads(string_object)
        except ValueError as e:
            return False
        return True
    
    def create_email(self, user_profile):
        email_address = ''
        name_variations = self.create_name_variations(user_profile)
        for name_variation in name_variations:
            email_address = (name_variation + user_profile['dominio_empresa'])
            if self.connect_to_zerobounce(email_address) == "valid":
                user_profile['email'] = email_address
                break

    def connect_to_zerobounce(self, email):
        url = "https://api.zerobounce.net/v2/validate"
        params = {"email": email, "api_key": os.environ['api_key_zerobounce'], "ip_address": ''}
        json_response = json.loads(requests.get(url, params=params).content)
        print("\nEmail: {}.\nStatus: {}".format(email, json_response['status']))
        return json_response['status']

    def save_search_result(self, search_response):
        print('Pesquisa finalizando, salvando conteúdo em arquivo.')
        os.makedirs("files", exist_ok=True) 
        with open(f"files/{self.output_file}", 'w') as output_content_file:
            json.dump(search_response, output_content_file, ensure_ascii=False)
    
    def create_name_variations(self, user_profile):
        name_variations = []
        first_name = unidecode.unidecode(user_profile['primeiroNome'].split(' ')[0].lower())
        last_name = unidecode.unidecode(user_profile['sobrenome'].split(' ')[0].lower())

        name_variations.append('{}'.format(first_name))
        name_variations.append('{}.{}'.format(first_name, last_name))
        name_variations.append('{}_{}'.format(first_name, last_name))
        name_variations.append('{}{}'.format(first_name, last_name))
        name_variations.append('{}{}'.format(first_name[0], last_name))
        name_variations.append('{}.{}'.format(first_name[0], last_name))
        name_variations.append('{}_{}'.format(first_name[0], last_name))
        name_variations.append('{}{}'.format(first_name, last_name[0]))
        name_variations.append('{}.{}'.format(first_name[0], last_name[0]))
        name_variations.append('{}.{}'.format(first_name[0], last_name[0]))

        return name_variations




        




