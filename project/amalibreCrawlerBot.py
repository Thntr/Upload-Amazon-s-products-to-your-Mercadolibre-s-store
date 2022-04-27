import asyncio
from bs4 import BeautifulSoup
from pyppeteer import launch
import time

def amalibre_crawler(url):

    async def main():
        browser = await launch({'headless': False})
        page = await browser.newPage()
        await page.goto(url)
        print("¿Has ingresado a la sección de publicaciones?")
        print("Presiona [Y/n]...")
        boolean = input()

        if boolean == "Y":
            r = await page.content()
            print(r)

        await browser.close()

    asyncio.get_event_loop().run_until_complete(main())

r = amalibre_crawler("https://www.amalibre.com")
