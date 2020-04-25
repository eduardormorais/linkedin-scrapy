import os
from scrapy.http import FormRequest, Request, Response
from scrapy.crawler import CrawlerProcess
from scrapy import Spider
from bs4 import BeautifulSoup
import argparse
import json
from linkedin_selenium import LinkedinSelenium

parser = argparse.ArgumentParser(description="Headless Browser to Crawler Linkedin.")
parser.add_argument("--v", default=None, type=str, help="Dados para realizar pesquisa aqui.")
parser.add_argument("--o", default=None, type=str, help="Arquivo para salvar dados recolhidos aqui.")

args = parser.parse_args()
valor_pesquisa = json.loads(args.v)
arquivo_output = args.o
linkedin_selenium = LinkedinSelenium()
linkedin_selenium.set_output_file(arquivo_output)
linkedin_selenium.start_searching(valor_pesquisa)





        
