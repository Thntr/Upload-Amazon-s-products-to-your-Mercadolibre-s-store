import scrapy
import json
from ..items import WinkscraperItem
from ..testOnMeli import meli
from ..testOnMeli import pictureFunc
import js2xml
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from googletrans import Translator
from re import sub
from decimal import Decimal
from ..calljson import get_data
from ..calljson import get_json


class megaSynchAmazonSpider(scrapy.Spider):
    name = "megaSynch"
    data = get_data("megaSynchList.json")

    start_urls = data["amazonLinks"]
    melis = data["meli"]

    def parse(self, response):

        print(r"¯\\_(ツ)_/¯ MEGA SYNCH CRAWLER ¯\\_(ツ)_/¯")

        data = get_data("megaSynchList.json")
        post = False

        def priceCalculator(priceAtYouBuy, margin, taxes, importMargin, shippingCosts):

            importCosts = priceAtYouBuy * importMargin
            additionalCosts = importCosts + shippingCosts
            marginFactor = 1 + margin
            comision = 0.175
            increaseTerm = ((1 / marginFactor) - comision - taxes)

            finalPrice = (priceAtYouBuy + additionalCosts) / increaseTerm

            return round(finalPrice, 2)

        def LinearSearch(lys, element):
            for i in range(len(lys)):
                if lys[i] == element:
                    return i
            return -1

        items = WinkscraperItem()

        price = response.css("#price_inside_buybox").css("::text").extract()
        prime = response.css("#primePopoverContent > h1").extract()
        description = response.css("#feature-bullets > ul").css("::text").extract()
        selledByAmazon = response.css("#merchant-info").css("::text").extract()
        shippingDate = response.css("#fast-track-message > div").css("::text").extract()
        tittle = response.css("#productTitle").css("::text").extract()
        availability = response.css("#availability > span").css("::text").extract()
        try:
            js = response.xpath("//script[contains(text(), 'register(\"ImageBlockATF\"')]/text()").extract_first()
            xml = js2xml.parse(js)
            selector = scrapy.Selector(root=xml)
            picture = selector.xpath(
                '//property[@name="colorImages"]//property[@name="hiRes"]/string/text()').extract()
        except:
            picture = response.css("#landingImage").css("::src").extract()

        items["price"] = price
        items["description"] = description
        items["selledByAmazon"] = selledByAmazon
        items["shippingDate"] = shippingDate
        items["tittle"] = tittle
        items["picture"] = picture
        items["availability"] = availability
        items["prime"] = prime

        if len(items["price"]) != 0:
            priceInCurrency = str(items["price"][0])
            value = float(Decimal(sub(r'[^\d.]', '', priceInCurrency)))

        else:
            value = None

        for attributes in items:
            if len(items[attributes]) is not 0:
                newStrings = []
                for strings in items[attributes]:
                    newStrings.append(strings.replace("\n", ""))
                items[attributes] = newStrings
            else:
                pass

        for attributes in items:
            if len(items[attributes]) is not 0:
                newStrings = []
                for strings in items[attributes]:
                    if len(strings) != 0:
                        newStrings.append(strings)
                    else:
                        pass
                items[attributes] = newStrings
            else:
                pass

        amazonLink = str(response.request.url)
        index = LinearSearch(data["amazonLinks"], amazonLink)
        correspondingMeli = str(data["meli"][index])

        picturesList = [{"source": str(items["picture"][i])} for i in range(0, len(items["picture"]) - 1)]

        if items["availability"][0] == "Disponible." and items["prime"] == "Amazon Prime":

            if value != None and len(items["selledByAmazon"]) == 1 and pictureFunc:
                body = {"status": "active", "price": priceCalculator(value, 0.1, 0.16, 0, 100),
                        "pictures": picturesList, "available_quantity": 10}
                petition = meli.put("/items/" + correspondingMeli, body, {'access_token': meli.access_token})
                response_var = str(petition)


            elif value != None and len(items["selledByAmazon"]) == 1 and pictureFunc == False:
                body = {"status": "active", "price": priceCalculator(value, 0.1, 0.16, 0, 100),
                        "available_quantity": 10}
                petition = meli.put("/items/" + correspondingMeli, body, {'access_token': meli.access_token})
                response_var = str(petition)


            elif value != None and len(items["selledByAmazon"]) != 1 and pictureFunc:
                body = {"status": "active", "price": priceCalculator(value, 0.3, 0.16, 0, 100),
                        "pictures": picturesList, "available_quantity": 1}
                petition = meli.put("/items/" + correspondingMeli, body, {'access_token': meli.access_token})
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print(petition)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                response_var = str(petition)


            elif value != None and len(items["selledByAmazon"]) != 1 and pictureFunc == False:
                body = {"status": "active", "price": priceCalculator(value, 0.3, 0.16, 0, 100),
                        "available_quantity": 1}
                petition = meli.put("/items/" + correspondingMeli, body, {'access_token': meli.access_token})
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print(petition)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                response_var = str(petition)


        else:
            body = {"status": "paused"}
            petition = meli.put("/items/" + correspondingMeli, body, {'access_token': meli.access_token})
            response_var = str(petition)

            # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # predictor = scrapy.Request("https://api.mercadolibre.com/sites/MLM/category_predictor/predict?title=" + str(items["tittle"][0]))
            # print(predictor.text)
            # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            return response

        if post is True:
            translator = Translator()
            translation = translator.translate(str(items["tittle"][0]), dest="es")
            tittleTraslated = translation.text

        coolDict = {"meli": correspondingMeli, "amazonLink": amazonLink, "price": items["price"], "Prime?": items["prime"],
                    "selledByAmazon": items["selledByAmazon"], "shippingDate": items["shippingDate"],
                    "availability": items["availability"], "pictures": items["picture"], "response": response_var,
                    "body": body}

        path = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\evidence__responses\amazon"
        evidenceJson = get_json("synchEvidence.json", path=path)

        with open(evidenceJson, "r+") as file:
            tmp = json.load(file)
            list = tmp["items"]
            list.append(coolDict)
            tmp["items"] = list
            file.seek(0)

        with open(evidenceJson, "w") as file:
            json.dump(tmp, file)

        yield items

