from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

class DataExtract:
    
    @staticmethod
    def daraz_extract(productName) -> dict:
        """
        Scrapes Daraz for product details based on the provided product name.
        
        Args:
            productName (str): The name of the product to search for.
        
        Returns:
            dict: A dictionary containing product titles, prices, and links.
        """

        # Regex pattern to extract Title and Price from given data
        pattern = r'([\w\s\-\(\)]+)Rs\.\s*([\d,]+(?:\.\d+)?)(?:\s*-\s*\d+%|\s*% Off)?'

        # Start Playwright and launch Chromium in headless mode
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            # Open Daraz website
            page.goto("https://www.daraz.com.np/")
            
            # Search for the product using the provided product name
            page.fill('input#q', productName)
            page.click('a.search-box__button--1oH7')  # Click the search button
            
            # Wait for product results to load
            page.wait_for_selector('.FWSEp')  
            
            # Get the HTML content of the product container
            html_content = page.inner_html('._17mcb')
            soup = BeautifulSoup(html_content, 'html.parser')  # Initialize BeautifulSoup
            
            # Initialize dictionary to store product data
            DarazProductDict = {}
            
            # Scrape price and title divs
            PriceDivs = soup.find_all(class_='aBrP0')  # Price container
            TitleDivs = soup.find_all(class_='RfADt')  # Title and link container
            ImageDivs = soup.find_all(class_ = 'picture-wrapper jBwCF')
            
            try:
                # Ensure there is a matching number of title and price divs
                if len(TitleDivs) == len(PriceDivs) == len(ImageDivs):
                    # Loop through title and price divs simultaneously
                    for div, div2,div3 in zip(TitleDivs, PriceDivs,ImageDivs):
                        TitleText = div.get_text(strip=True)  # Extract title
                        PriceText = div2.get_text(strip=True)  # Extract price
                        links = [a['href'] for a in div.find_all('a', href=True)]  # Extract product link

                        #for image
                        # image = [img['src'] for img in div3.find_all('img') if img['src']]  #displaying image in base64 format


                        img_tag = div3.find("img")
                        if img_tag:
                            image_url = img_tag.get('data-src')
                            if not image_url:
                                image_url = img_tag.get('src')

                        # Store the title, price, and link in the dictionary
                        DarazProductDict[TitleText] = {'price': PriceText, 'link': links, 'image': image_url}
            except Exception as err:
                print(f"Error: {err}")
            
            # Close the browser once scraping is done
            browser.close()

            return DarazProductDict

    @staticmethod
    def thulo_extract(productName) -> dict:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto("https://thulo.com.np/")
            page.fill('input.form-control', productName)

            page.click('button[type="submit"]')

            page.wait_for_selector(".container")

            html_content = page.inner_html(".rowmk")
           
            soup = BeautifulSoup(html_content, "html.parser")

            PriceDiv = soup.find_all(class_ = 'offerPrice')
            TitleDiv = soup.find_all(class_ = 'global-card-contents-title text-capitalize')
            ImageDiv = soup.find_all(id = 'productImage')
            


            ThuloProductDict = {}
            try:
                if len(PriceDiv) == len(TitleDiv) == len(ImageDiv):    
                    for div1,div2,div3 in zip(TitleDiv,PriceDiv, ImageDiv):
                        
                        
                        links = [a['href'] for a in div1.find_all('a', href=True)]
                        TitleText = div1.get_text(strip=True)
                        PriceText = div2.get_text(strip=True)
                        img = div3['src'] 

                        ThuloProductDict[TitleText] = {'price': PriceText, 'link': links, 'image': img}
                        
                        
                        
            except Exception as err:
                print(err)

            
            browser.close()

            return ThuloProductDict


            # print(TitleDiv,PriceDiv)
            

    @staticmethod
    def hamro_bazar_extract(productName) -> dict:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://hamrobazaar.com/")

            page.wait_for_timeout(2000)

            page.fill('input[name="searchValue"]', productName)
            page.click('button.nav-searchbar-input-searchIcon')

            page.wait_for_selector('.hb__body ')

            html_content = page.inner_html('[data-test-id="virtuoso-item-list"]')
            soup = BeautifulSoup(html_content, 'html.parser')
            # print(html_content)

            TitleDiv = soup.find_all(class_ = "product-title")
            PriceDiv = soup.find_all(class_ = "regularPrice")
            LinkDiv = soup.find_all(class_ = "nameAndDropdown")
            ImageDiv = soup.find_all(class_ = "image-container")
            
            
            page.wait_for_selector('.image-container')
            HamroBazarProductDict = {}
            try:
                
                for div1,div2,div3,div4 in zip(TitleDiv,PriceDiv,LinkDiv,ImageDiv):
                    TitleText = div1.get_text(strip=True)
                    PriceText = div2.get_text(strip=True)

                    links = [a['href'] for a in div3.find_all('a', href=True)]
                    
                    
                    img_tag = div4.find("img")
                    if img_tag:
                        image_url = img_tag.get('data-src')
                        if not image_url:
                            image_url = img_tag.get('src')

                    # print(image_url)
                    
                    HamroBazarProductDict[TitleText] = {'price': PriceText, 'link': links, 'image': image_url}
                    
            except Exception as err:
                print(err)

            browser.close()

            return HamroBazarProductDict
        
    

# Instantiate the DataExtract class and scrape product data 
DE = DataExtract()
productName = "headphone"
# productDataHamroBazar = DE.hamro_bazar_extract(productName)
ThulorProductDict = DE.thulo_extract(productName)

# Testing the output by printing product details
for title, data in ThulorProductDict.items():
    price = data['price']
    link = data['link']
    image = data['image']

    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Link: {link}")
    print(f"Image Link: {image}")
    print("-----")


