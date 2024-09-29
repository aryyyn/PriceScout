from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import asyncio


class DataExtract:

    @staticmethod
    async def daraz_extract(productName) -> dict:  # changing to asynchronous function
        """
        Scrapes Daraz for product details based on the provided product name.

        Args:
            productName (str): The name of the product to search for.

        Returns:
            dict: A dictionary containing product titles, prices, and links.
        """

        # Regex pattern to extract Title and Price from given data
        pattern = r"([\w\s\-\(\)]+)Rs\.\s*([\d,]+(?:\.\d+)?)(?:\s*-\s*\d+%|\s*% Off)?"

        # Start Playwright and launch Chromium in headless mode
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # Open Daraz website
            await page.goto(
                f"https://www.daraz.com.np/catalog/?q={productName}",
                wait_until="domcontentloaded",
            )  # added wait_until cause the site was taking a long time to load, domcontentloaded basically tells it to not wait for any exrernal files, and display results as soon as the HTML has been loaded.

            # Search for the product using the provided product name
            # skipping this part because the homepage was taking a long time to load
            # await page.fill("input#q", productName)
            # await page.click("a.search-box__button--1oH7")  # Click the search button

            # Wait for product results to load
            await page.wait_for_selector(".FWSEp")
            
            # Get the HTML content of the product container
            html_content = await page.inner_html("._17mcb")
            soup = BeautifulSoup(
                html_content, "html.parser"
            )  # Initialize BeautifulSoup

            
            # Initialize dictionary to store product data
            DarazProductDict = {}

            # Scrape price and title divs
            PriceDivs = soup.find_all(class_="aBrP0")  # Price container
            TitleDivs = soup.find_all(class_="RfADt")  # Title and link container
            ImageDivs = soup.find_all(class_="picture-wrapper jBwCF")

            try:
                # Ensure there is a matching number of title and price divs
                if len(TitleDivs) == len(PriceDivs) == len(ImageDivs):
                    # Loop through title and price divs simultaneously
                    for div, div2, div3 in zip(TitleDivs, PriceDivs, ImageDivs):
                        TitleText = div.get_text(strip=True)  # Extract title
                        PriceText = div2.get_text(strip=True)  # Extract price
                        links = [
                            a["href"] for a in div.find_all("a", href=True)
                        ]  # Extract product link

                        # for image
                        # image = [img['src'] for img in div3.find_all('img') if img['src']]  #displaying image in base64 format

                        img_tag = div3.find("img")
                        if img_tag:
                            image_url = img_tag.get("data-src")
                            if not image_url:
                                image_url = img_tag.get("src")

                        # Store the title, price, and link in the dictionary
                        DarazProductDict[TitleText] = {
                            "price": PriceText,
                            "link": links,
                            "image": image_url,
                        }
            except Exception as err:
                print(f"Error: {err}")

            # Close the browser once scraping is done
            await browser.close()

            return DarazProductDict

    @staticmethod
    async def thulo_extract(productName) -> dict:
        """
        Scrapes Thulo.com for product details based on the provided product name.

        Args:
            productName (str): The name of the product to search for.

        Returns:
            dict: A dictionary containing product titles, prices, and links.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            await page.goto("https://thulo.com.np/", wait_until="domcontentloaded",)
            await page.fill("input.form-control", productName)

            await page.click('button[type="submit"]')

            await page.wait_for_selector(".container")

            html_content = await page.inner_html(".rowmk")

            soup = BeautifulSoup(html_content, "html.parser")

            PriceDiv = soup.find_all(class_="offerPrice")
            TitleDiv = soup.find_all(
                class_="global-card-contents-title text-capitalize"
            )
            ImageDiv = soup.find_all(id="productImage")

            ThuloProductDict = {}
            try:
                if len(PriceDiv) == len(TitleDiv) == len(ImageDiv):
                    for div1, div2, div3 in zip(TitleDiv, PriceDiv, ImageDiv):

                        links = [a["href"] for a in div1.find_all("a", href=True)]
                        TitleText = div1.get_text(strip=True)
                        PriceText = div2.get_text(strip=True)
                        img = div3["src"]

                        ThuloProductDict[TitleText] = {
                            "price": PriceText,
                            "link": links,
                            "image": img,
                        }

            except Exception as err:
                print(err)

            await browser.close()

            return ThuloProductDict

            # print(TitleDiv,PriceDiv)

    @staticmethod
    async def hamro_bazar_extract(productName) -> dict:
        """
        Scrapes hamrobazaar.com for product details based on the provided product name.

        Args:
            productName (str): The name of the product to search for.

        Returns:
            dict: A dictionary containing product titles, prices, and links.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            await page.goto("https://hamrobazaar.com/", wait_until="domcontentloaded",)

            # page.wait_for_timeout(2000) #debugging purposes

            await page.fill('input[name="searchValue"]', productName)
            await page.click("button.nav-searchbar-input-searchIcon")

            await page.wait_for_selector(".hb__body ")

            html_content = await page.inner_html('[data-test-id="virtuoso-item-list"]')
            soup = BeautifulSoup(html_content, "html.parser")

            TitleDiv = soup.find_all(class_="product-title")
            PriceDiv = soup.find_all(class_="regularPrice")
            LinkDiv = soup.find_all(class_="nameAndDropdown")
            ImageDiv = soup.find_all(class_="image-container")

            await page.wait_for_selector(".image-container")
            HamroBazarProductDict = {}
            try:

                for div1, div2, div3, div4 in zip(
                    TitleDiv, PriceDiv, LinkDiv, ImageDiv
                ):
                    TitleText = div1.get_text(strip=True)
                    PriceText = div2.get_text(strip=True)

                    links = [
                        a["href"] for a in div3.find_all("a", href=True)
                    ]  # finds a tag from div3 respose data, and then from there extracts the href tag

                    img_tag = div4.find(
                        "img"
                    )  # another way of extracting image from response data
                    if img_tag:
                        image_url = img_tag.get("data-src")
                        if not image_url:
                            image_url = img_tag.get("src")

                    # print(image_url)

                    HamroBazarProductDict[TitleText] = {
                        "price": PriceText,
                        "link": links,
                        "image": image_url,
                    }

            except Exception as err:
                print(err)

            await browser.close()

            return HamroBazarProductDict

    @staticmethod
    async def okdam_extraction(productName) -> dict:
        """
        Scrapes okdam.com for product details based on the provided product name.

        Args:
            productName (str): The name of the product to search for.

        Returns:
            dict: A dictionary containing product titles, prices, and links.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            await page.goto("https://www.okdam.com/", wait_until="domcontentloaded",)

            await page.fill('[placeholder="Search Products & brands"]', productName)
            await page.press('[placeholder="Search Products & brands"]', "Enter")
            await page.wait_for_selector(".feature-box1")

            html_content = await page.inner_html(".feature-box1")
            soup = BeautifulSoup(html_content, "html.parser")

            OkDamProductDict = {}

            MainDiv = soup.find_all(class_="col-6 col-sm-6 col-md-6 col-lg-3 pro-wrap")
            try:
                for div in MainDiv:
                    links = [a["href"] for a in div.find_all("a", href=True)]
                    image_url = [img["data-src"] for img in div.find_all("img")]
                    title = [img["alt"] for img in div.find_all("img")]

                    title = "".join(title)
                    pricediv = div.find("span", class_="og-price")
                    if pricediv:
                        price = pricediv.get_text(strip=True)

                    OkDamProductDict[title] = {
                        "price": price,
                        "link": links,
                        "image": image_url,
                    }

            except Exception as err:
                print(err)

            await browser.close()

            return OkDamProductDict

    @staticmethod
    async def dealayo_extraction(productName) -> dict:
        """
        Scrapes dealayo.com for product details based on the provided product name.

        Args:
            productName (str): The name of the product to search for.

        Returns:
            dict: A dictionary containing product titles, prices, and links.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            await page.goto("https://dealayo.com/", wait_until="domcontentloaded",)

            await page.fill("input#search", productName)
            await page.press("input#search", "Enter")

            DealAyoDataDict = {}
            html_content = await page.inner_html('[class="search results"]')
            soup = BeautifulSoup(html_content, "html.parser")

            MainDiv = soup.find_all(class_="item product product-item")
            ImageDiv = soup.find_all(class_="product-image-wrapper")
            LinkDiv = soup.find_all(class_="product name product-item-name")
            PriceDiv = soup.find_all(class_="price")

            try:
                for div, div2, div3, div4 in zip(MainDiv, ImageDiv, LinkDiv, PriceDiv):

                    image_url = [img["src"] for img in div2.find_all("img")]
                    links = [a["href"] for a in div3.find_all("a", href=True)]
                    price = div4.get_text(strip=True)
                    title = div3.get_text(strip=True)

                    DealAyoDataDict[title] = {
                        "price": price,
                        "link": links,
                        "image": image_url,
                    }

            except Exception as err:
                print(err)
            await browser.close()

            return DealAyoDataDict


# Instantiate the DataExtract class and scrape product data
async def main():
    DE = DataExtract()
    productName = "headphone"

#     # Gather the results from the async function
    results = await asyncio.gather(DE.daraz_extract(productName))

#     # The results will be a list with one item (the dictionary returned by daraz_extract)
    daraz_data = results[0]

    # Now we can iterate over the dictionary items
    # for title, data in daraz_data.items():
    #     price = data["price"]
    #     link = data["link"]
    #     image = data["image"]

    #     print(f"Title: {title}")
    #     print(f"Price: {price}")
    #     print(f"Link: {link}")
    #     print(f"Image Link: {image}")
    #     print("-----")


if __name__ == "__main__":
    asyncio.run(main())
