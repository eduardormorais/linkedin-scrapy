import time
import os
import json
from flask_restful import Resource
from bs4 import BeautifulSoup
from url_filter_generator import UrlFilterGenerator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class LinkedinSelenium(Resource):
    def __init__(self, output_file):
        self.login_url = "https://www.linkedin.com/login"
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_driver_path = "./chromedriver"
        self.output_file = output_file

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

    def start_searching(self, valor_pesquisa):
        url_filter_generator = UrlFilterGenerator()
        chrome_driver = webdriver.Chrome(
            executable_path=self.chrome_driver_path)
        chrome_driver.get(self.login_url)
        cookies = self.read_session_cookies()
        for cookie in cookies:
            chrome_driver.add_cookie(cookie)

        main_search_url = url_filter_generator.create_url(valor_pesquisa)
        profile_users_url = []
        next_page_number = 1
        search_url = main_search_url
        required_elements_json = ['included', 'navigationUrl', 'trackingUrn']
        while next_page_number <= 1: # Número de páginas que o script irá percorrer.
            chrome_driver.get(search_url)
            beautiful_soup = BeautifulSoup(chrome_driver.page_source)
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
                profile_users_url.append(user_element['navigationUrl'])
            next_page_number += 1
            search_url = url_filter_generator.next_page(main_search_url, next_page_number)

        print(profile_users_url)
        time.sleep(5)
        self.get_profiles_info_from_users(profile_users_url, chrome_driver)

    def get_profiles_info_from_users(self, users_url, driver):
        array_users_profile = []
        users_url = ['https://www.linkedin.com/in/luana-gabriela-a058061a']
        for user_url in users_url:
            driver.get(user_url)
            user_profile = self.get_profile_data(driver.page_source)
            self.create_email(user_profile)
            array_users_profile.append(user_profile)
        driver.close()
        print(array_users_profile)
        self.save_search_result(array_users_profile)

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

        for included_element in included_elements_user:
            if 'dateRange' in included_element:
                if 'end' not in included_element['dateRange'] and 'title' in included_element and 'companyName' in included_element:
                    profile_data['empresa'] = included_element['companyName']
                    profile_data['cargo'] = included_element['title']

            if 'firstName' in included_element:
                profile_data['primeiroNome'] = included_element['firstName']
                profile_data['sobrenome'] = included_element['lastName']

        return profile_data

    def is_json(self, string_object):
        try:
            json_object = json.loads(string_object)
        except ValueError as e:
            return False
        return True
    
    def create_email(self, user_profile):
        company_name = user_profile['empresa']
        user_first_name = user_profile['primeiroNome']
        compound_company_name = company_name.split(' ')
        if len(compound_company_name) > 1:
            company_name = compound_company_name[0]
        user_profile['email'] = f"{user_profile['primeiroNome'].lower()}@gmail.com"
    
    def save_search_result(self, search_response):
        print('Pesquisa finalizando, salvando conteúdo em arquivo.')
        os.makedirs("files", exist_ok=True) 
        with open(f"files/{self.output_file}", 'w') as output_content_file:
            json.dump(search_response, output_content_file, ensure_ascii=False)
        




