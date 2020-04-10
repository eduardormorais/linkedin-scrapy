# Linkedin Scrapy

## Client
#### Dependencies 
  - Node: 10.18.1 
  - AngularCLI: 9.1.1 

#### Run
```
cd cliente && npm serve
```

## Scraping
#### Dependencies 
  - Python: 3.7.6 
  - Scrapy: 2.0.1

#### Run
```
scrapy runspider scraping.py -a value_search="Teste Teste" -a email="you@email.com" -a password="youpassword" 
```
