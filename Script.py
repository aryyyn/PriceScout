from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re


def DarazExtract(productName) -> list:

    pattern = r'([\w\s\-\(\)]+)Rs\.\s*([\d,]+(?:\.\d+)?)(?:\s*-\s*\d+%|\s*% Off)?' #generated from chatgpt to extract Title and Price from given data

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.daraz.com.np/")
        
    
        page.fill('input#q', productName)
        page.click('a.search-box__button--1oH7') #searches for the product Name using the variable productName
        
    
        page.wait_for_selector('.FWSEp')  

        
        html_content = page.inner_html('._17mcb')  #product container
        soup = BeautifulSoup(html_content, 'html.parser') #initializing bs

                
        #didnt work for some reason, will try to fix this later 

        # divs_playwright = page.query_selector_all('.Bm3ON')
        # for div in divs_playwright:
        #     content = div.text_content()
        #     print(content)  

        productData = {}
    
        PriceDivs = soup.find_all(class_='aBrP0')  # contains the Price of the product
        TitleDivs = soup.find_all(class_='RfADt')  # Contains Title and Link to the product
        DarazProductDict = {}
        try:
            if len(TitleDivs) == len(PriceDivs):
                for div, div2 in zip(TitleDivs, PriceDivs):

                    TitleText = div.get_text(strip=True)  #only extracts the title, so we need to find another way of extracting the link
                    PriceText = div2.get_text(strip=True) 
                    links = [a['href'] for a in div.find_all('a', href=True)]   #extracts link from TitleDivs which contains title and links

                    # print(TitleText, PriceText, links) #for testing
                    DarazProductDict[TitleText] = {'price': PriceText, 'link': links}
                   
        except Exception as err:
            print(err)
    



        browser.close() 

        return DarazProductDict


productName = "Headphone"
productData = DarazExtract(productName)


#for testing
for title, data in productData.items():
    price = data['price']
    link = data['link']

    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Link: {link}")
    print("-----") 


