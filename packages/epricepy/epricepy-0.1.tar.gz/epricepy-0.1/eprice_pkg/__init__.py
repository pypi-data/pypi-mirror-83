# NOTE: be aware of the region you request for because the functions retunrs the prices acording to the url the user searches for
# NOTE: be aware of the quantity while providing the link from alibaba
# NOTE: Available websites to scrape 1.Amazon 2.Flipkart 3.Alibaba 4.Snapdeal 5.Reliancedigital
import requests
import lxml
from bs4 import BeautifulSoup
import re

class eprice:
    
    @staticmethod
    def makeRequest(url):
        HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                    'Accept-Language': 'en-US, en;q=0.5'})
        source=requests.get(url, headers=HEADERS).text
        soup=BeautifulSoup(source,'lxml')
        return soup

    @staticmethod
    def getAmazon(url):
        soup=eprice.makeRequest(url)

        title=soup.find('span',id='productTitle')
        ProductTitle=title.get_text().strip()

        price=soup.find('span',id='priceblock_ourprice')
        if price == None: 
            price = soup.find('span', id ='priceblock_dealprice')
        price=price.text.replace(',','')
        price=float(re.search(r'\d+.\d+',price).group())

        return (ProductTitle,price)

    @staticmethod
    def getFlipkart(url):
        soup=eprice.makeRequest(url)

        title=soup.find('span',class_='_35KyD6')
        ProductTitle=title.get_text().strip()

        price=soup.find('div',class_='_1vC4OE _3qQ9m1')
        if price!=None:
            price=price.text.replace(',','')
            price=float(re.search(r'\d+.\d+',price).group())

        return (ProductTitle,price)

    @staticmethod
    def getAlibaba(url):
        soup=eprice.makeRequest(url)

        title=soup.find('h1',class_='ma-title')
        ProductTitle=title.get_text().strip()

        price=soup.find('div',class_="sku-price").find('div')
        if price!=None: 
            price=price.text.strip().replace(',','')
            price=float(re.search(r'\d+.\d+',price).group())

        return (ProductTitle,price)

    @staticmethod
    def getSnapdeal(url):
        soup=eprice.makeRequest(url)

        title=soup.find('div',class_='col-xs-22').find('h1').get('title')
        ProductTitle=title.strip()

        price=soup.find('span',class_='payBlkBig')
        if price!=None:
            price=price.text.replace(',','')
            price=float(re.search(r'\d+.\d+',price).group())

        return (ProductTitle,price)

    @staticmethod
    def getReliancedigital(url):
        soup=eprice.makeRequest(url)

        title=soup.find('div',class_='pdp__title')
        ProductTitle=title.get_text().strip()

        price=soup.find('span',class_='pdp__offerPrice')
        if price!=None:
            price=price.text.replace(',','')
            price=float(re.search(r'\d+.\d+',price).group())

        return (ProductTitle,price)

    

if __name__ == "__main__":
    pass
  
        


