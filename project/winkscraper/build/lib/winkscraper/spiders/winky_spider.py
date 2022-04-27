import scrapy
import json
from ..items import WinkscraperItem
from ..testOnMeli import meli
import js2xml
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import math

class AmazonSpider(scrapy.Spider):

    name = "winky"

    with open(
            r"C:\Users\Usuario\Documents\MEGAsync\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\definitiveProductList.json",
            "r") as jsonFile:
        data = json.load(jsonFile)

    start_urls = data["amazonLinks"]
    melis = data["meli"]

    def parse(self, response):

        items = WinkscraperItem()

        price = response.css("#price_inside_buybox").css("::text").extract()
        description = response.css("#feature-bullets > ul").css("::text").extract()
        selledByAmazon = response.css("#merchant-info").css("::text").extract()
        shippingDate = response.css("#fast-track-message > div").css("::text").extract()
        tittle = response.css("#productTitle").css("::text").extract()
        js = response.xpath("//script[contains(text(), 'register(\"ImageBlockATF\"')]/text()").extract_first()
        xml = js2xml.parse(js)
        selector = scrapy.Selector(root=xml)
        picture = selector.xpath('//property[@name="colorImages"]//property[@name="hiRes"]/string/text()').extract()

        items["price"] = price
        items["description"] = description
        items["selledByAmazon"] = selledByAmazon
        items["shippingDate"] = shippingDate
        items["tittle"] = tittle
        items["picture"] = picture

        for attributes in items:
            if len(items[attributes]) is not 0:
                newStrings = []
                for strings in items[attributes]:
                    newStrings.append(strings.replace("\n", ""))
                items[attributes] = newStrings
            else:
                pass

        body = {"status": "active", "price": 9999}
        response = meli.put("/items/" + "MLM680120049", body, {'access_token': meli.access_token})

        yield items