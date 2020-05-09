
import time
import os
from os import path
import json
import unidecode
from flask_restful import Resource
from bs4 import BeautifulSoup
from url_filter_generator import UrlFilterGenerator
from selenium import webdriver
import requests
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LinkedinSelenium(Resource):
    def __init__(self):
        self.logger = logging.getLogger("LinkedinSelenium")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.zerobounce_url = "https://api.zerobounce.net/v2/validate"
        self.login_url = "https://www.linkedin.com/login"
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.headless = True
        self.chrome_driver_path = os.environ.get("CHROMEDRIVER_PATH", "./chromedriver")
        self.url_filter_generator = UrlFilterGenerator()
        self.chrome_driver = None

    def sign_in(self, driver):
        driver.get(self.login_url)
        username = driver.find_element_by_name("session_key")
        password = driver.find_element_by_name("session_password")
        username.send_keys(os.environ['email'])
        password.send_keys(os.environ['senha'])
        button_login = driver.find_elements_by_xpath(
            "//button[@type='submit']")[0]
        button_login.click()
    
    def set_code(self, code):
        pin = self.chrome_driver.find_element_by_name("pin")
        pin.send_keys(code)
        button_submit_pin = self.chrome_driver.find_elements_by_id("email-pin-submit-button")[0]
        button_submit_pin.click()
        if 'feed' in self.chrome_driver.current_url:
            self.logger.info('Pin submitado, login bem-sucedido')

    def save_session_cookies(self, driver):
        self.logger.info('Salvando cookies...')
        with open('cookies.json', 'w') as cookie_file:
            json.dump(driver.get_cookies(), cookie_file)

    def read_session_cookies(self):
        with open('cookies.json', 'r') as cookie_file:
            cookies = json.load(cookie_file)

        return cookies
    
    def get_chrome_options(self):
        return self.chrome_options
    
    def set_output_file(self, output_file):
        self.output_file = output_file
    
    def get_users_elements(self, page_content):
        users_elements = []
        required_elements_json = ['included', 'navigationUrl', 'trackingUrn']
        if self.is_json(page_content.text) == True:
            search_data_tag_code = json.loads(page_content.text)
            if all(tag_element in str(search_data_tag_code) for tag_element in required_elements_json):
                for element_json in search_data_tag_code['data']['elements']:
                    if 'targetUrn' in str(element_json):
                        users_elements = element_json['elements']
                        break
        return users_elements
    
    def is_authenticated(self):
        logged = False
        if path.exists('cookies.json'):
            self.chrome_driver.get(self.login_url)
            cookies = self.read_session_cookies()
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                self.chrome_driver.add_cookie(cookie)
            self.chrome_driver.get(self.login_url)
        else:
            self.sign_in(self.chrome_driver)

        current_url = self.chrome_driver.current_url
        if '/feed' in current_url:
            self.logger.info('Rota /feed encontrada..')
            self.save_session_cookies(self.chrome_driver)
            logged = True
        
        if '/login' in current_url:
            self.logger.info('/login encontrado.')
            self.sign_in(self.chrome_driver)
            self.save_session_cookies(self.chrome_driver)
        
        if '/check/challenge' in current_url:
            self.logger.info('/challenge encontrado.')
            logged = False
        
        return logged

    def initialize_driver(self):
        self.chrome_driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.chrome_options)
        
    def start_searching(self, valor_pesquisa):
        self.logger.info('Iniciando pesquisa...')
        self.initialize_driver()
        status = self.is_authenticated()
        if status is True:
            main_search_url = self.url_filter_generator.create_url(valor_pesquisa)
            profile_users = []
            next_page_number = 1
            search_url = main_search_url
            fixed_number_of_pages = 100

            while next_page_number <= fixed_number_of_pages: # Número de páginas que o script irá percorrer.
                self.chrome_driver.get(search_url)
                beautiful_soup = BeautifulSoup(self.chrome_driver.page_source)
                search_page_tags_code = beautiful_soup.find_all("code")
                for search_page_tag_code in search_page_tags_code:
                    users_elements = self.get_users_elements(search_page_tag_code)
                    if len(users_elements) > 0:
                        break

                if len(users_elements) == 0: break

                for user_element in users_elements:
                    if len(profile_users) == (valor_pesquisa['qtd']):
                        next_page_number = fixed_number_of_pages
                        break

                    self.chrome_driver.get(user_element['navigationUrl'])
                    profile_user = self.get_profile_data(self.chrome_driver.page_source)

                    if self.repeated_user(profile_users, profile_user) is True:
                        next_page_number = fixed_number_of_pages
                        break

                    if profile_user['empregado'] is True:
                        self.append_users(profile_users, self.chrome_driver, profile_user)

                next_page_number += 1
                search_url = self.url_filter_generator.next_page(main_search_url, next_page_number)
            self.chrome_driver.close()
            self.save_search_result(profile_users)
    
    def repeated_user(self, profile_users, new_user):
        repeated_user = False
        if 'primeiroNome' in new_user and 'sobrenome' in new_user:
            for profile_user in profile_users:
                if new_user['primeiroNome'] == profile_user['primeiroNome'] and new_user['sobrenome'] == profile_user['sobrenome']:
                    repeated_user = True
                    break

        return repeated_user
    
    def append_users(self, profile_users, chrome_driver, profile_user):
        chrome_driver.get(profile_user['empresa_linkedin_url'])
        company_website_url = self.get_company_url(chrome_driver.page_source)
        if company_website_url is not None:
            profile_user['dominio_empresa'] = self.url_filter_generator.get_domain(company_website_url)
            self.create_email(profile_user)
            profile_users.append(profile_user)

    def get_profile_data(self, html_page):
        profile_data = {}
        included_elements_user = {}
        required_elements_json = ['included', 'firstName', 'lastName', 'dateRange']
        beautiful_soup = BeautifulSoup(html_page)
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
            
        self.logger.info("\nProfile user: {}".format(profile_data))
        return profile_data
    
    def get_company_url(self, company_page):
        company_url = ''
        included_elements_company = ''
        required_elements_json = ['data', 'meta', 'included', 'companyPageUrl', 'universalName']
        beautiful_soup_company_page = BeautifulSoup(company_page)
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
        self.logger.info("Iniciando criação de e-mail.")
        email_address = ''
        name_variations = self.create_name_variations(user_profile)   
        user_profile['email'] = "teste@gmail.com"
        user_profile['email_status'] = "valid" 
        # for name_variation in name_variations:
        #     email_address = (name_variation + user_profile['dominio_empresa'])
        #     response_email_status = self.connect_to_zerobounce(email_address)
        #     user_profile['email'] = email_address
        #     user_profile['email_status'] = response_email_status['status']
        #     if response_email_status['status'] == "valid":
        #         break


    def connect_to_zerobounce(self, email):
        params = {"email": email, "api_key": os.environ['api_key_zerobounce'], "ip_address": ''}
        json_response = json.loads(requests.get(self.zerobounce_url, params=params).content)
        self.logger.info("\nEmail: {}.\nStatus: {}".format(email, json_response['status']))
        return json_response

    def save_search_result(self, search_response):
        self.logger.info('Pesquisa finalizada, salvando conteúdo em arquivo.')
        os.makedirs("files", exist_ok=True) 
        with open(f"files/{self.output_file}", 'w') as output_content_file:
            json.dump(search_response, output_content_file, ensure_ascii=False)
    
    def delete_search_file(self, filename):
        self.logger.info('Realizando exclusão de arquivo.')
        os.makedirs("files", exist_ok=True)
        os.remove(f"files/{filename}")
        
    def create_name_variations(self, user_profile):
        name_variations = []
        first_name = (unidecode.unidecode(user_profile['primeiroNome'].split(' ')[0].lower())).replace(".", "")
        last_name = (unidecode.unidecode(user_profile['sobrenome'].split(' ')[0].lower())).replace(".", "")

        name_variations.append('{}'.format(first_name))
        name_variations.append('{}{}'.format(first_name[0], last_name))
        name_variations.append('{}.{}'.format(first_name[0], last_name))
        name_variations.append('{}_{}'.format(first_name[0], last_name))
        name_variations.append('{}{}'.format(first_name, last_name[0]))
        name_variations.append('{}.{}'.format(first_name[0], last_name[0]))
        name_variations.append('{}.{}'.format(first_name[0], last_name[0]))
        name_variations.append('{}{}'.format(first_name, last_name))
        name_variations.append('{}_{}'.format(first_name, last_name))
        name_variations.append('{}.{}'.format(first_name, last_name))

        return name_variations



