import scrapy
import json
from ..items import CgWinkItem
from ..testOnMeli import meli
from ..testOnMeli import pictureFunc
from ..splitingProducts import howToSplit
from ..testOnMeli import refreshToken
import js2xml
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from googletrans import Translator
from re import sub
from decimal import Decimal
from ..calljson import get_data
from ..calljson import get_json
import time


class cgPostTestSpider(scrapy.Spider):
    name = "cgWinkPost"

    data = get_data("cgDefinitiveList.json")
    start_urls = data["startUrl"]

    print(" ͡° ͜ʖ ͡° these are the amount of urls for the cgSpider...")
    print(len(start_urls))
    print(" ͡° ͜ʖ ͡°")

    def parse(self, response):

        print(r"¯\\_(ツ)_/¯ CgWinkPost CRAWLER ¯\\_(ツ)_/¯")

        prediction = False

        def priceCalculator(priceAtYouBuy, margin, taxes, importMargin, shippingCosts, UsConvertion):

            importCosts = priceAtYouBuy * importMargin
            additionalCosts = importCosts + shippingCosts
            marginFactor = 1 + margin
            comision = 0.175
            increaseTerm = ((1 / marginFactor) - comision - taxes)

            finalPrice = (priceAtYouBuy + additionalCosts) / increaseTerm
            finalPrice = round(finalPrice, 2)

            if UsConvertion == True:
                finalPrice = round(finalPrice * 20, 2)

            return finalPrice

        def LinearSearch(lys, element):
            for i in range(len(lys)):
                if lys[i] == element:
                    return i
            return -1

        items = CgWinkItem()

        price = response.css(".product-pricing__price > span:nth-child(1) > span:nth-child(1)").css(
            "::text").extract()
        description = response.css(".product-description").css("::text").extract()
        # selledByAmazon = response.css("#merchant-info").css("::text").extract()
        # shippingDate = response.css("#fast-track-message > div").css("::text").extract()
        tittle = response.css(".product-header__title").css("::text").extract()
        # availability = response.css("#availability > span").css("::text").extract()
        # js = response.css(".gallery-container").extract_first()
        # xml = js2xml.parse(js)
        # selector = scrapy.Selector(root=xml)
        picture = response.css(".gallery-container").extract()

        items["price"] = price
        items["description"] = description
        items["tittle"] = tittle
        items["picture"] = picture
        # items["availability"] = availability
        items["description"] = description

        for attributes in items:
            print("{}".format(attributes) + " == " + str(items[attributes]))

        # This area is for chunks of code to put price, descriptions and another attributes to the products an adequate format...
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

        new_description = []
        for i in range(4, len(items["description"])):
            new_description.append(items["description"][i])

        descriptionOnString = str(new_description[0])
        for i in range(0, len(new_description) - 1):
            descriptionOnString += str(new_description[i])

        definitiveDescription = descriptionOnString

        params = {'access_token': meli.access_token, 'refresh_token': meli.refresh_token}

        # cut the tittle to acomplish the tittle requeriments for posting
        if len(str(items["tittle"])) >= 60:
            ancientTittle = str(items["tittle"])
            truncated_tittle = ancientTittle[0:60]
            newTittle = truncated_tittle

        else:
            newTittle = str(items["tittle"])

        CGLink = str(response.request.url)

        picturesList = [{"source": str(items["picture"][i])} for i in range(0, len(items["picture"]) - 1)]

        def postSet(varTittle, varCattegory, varDescription):
            theSet = {"title": varTittle,
                      "category_id": varCattegory,
                      "currency_id": "MXN",
                      "description": "ESTE ARTICULO ES DE PRUEBA, NO COMPRAR!\n" + varDescription,
                      "buying_mode": "buy_it_now",
                      "listing_type_id": "gold_premium",
                      "condition": "new",
                      "shipping": {"mode": "me1", "local_pick_up": False, "free_shipping": False,
                                   "free_methods": []},
                      "tags": ["immediate_payment"],
                      "attributes": [
                          {
                              "id": "BRAND",
                              "value_name": "0"
                          },
                          {
                              "id": "MODEL",
                              "value_name": "0"
                          }
                      ]
                      }

            return theSet

        if items["price"] != None:

            if value != None and pictureFunc:
                body = {"status": "active", "price": priceCalculator(value, 0.1, 0.16, 0, 100, UsConvertion=True),
                        "pictures": picturesList, "available_quantity": 10}
                body.update(postSet(newTittle, "MLM1912", definitiveDescription))
                petition = meli.post(path="/items", body=body, params=params)
                existenceOfMeli = True

            elif value != None and pictureFunc:
                body = {"status": "active", "price": priceCalculator(value, 0.3, 0.16, 0, 100, UsConvertion=True),
                        "pictures": picturesList, "available_quantity": 1}
                body.update(postSet(newTittle, "MLM1912", definitiveDescription))
                petition = meli.post(path="/items", body=body, params=params)
                existenceOfMeli = True

        else:
            body = {"status": "paused", "price": priceCalculator(value, 0.3, 0.16, 0, 100, UsConvertion=True),
                    "available_quantity": 0, "pictures": picturesList}
            body.update(postSet(newTittle, "MLM1912", definitiveDescription))
            petition = meli.post(path="/items", body=body, params=params)
            existenceOfMeli = False

        print(" ͡° ͜ʖ ͡°")
        print(petition.content)
        print(" ͡° ͜ʖ ͡°")
        responseVarString = petition.content.decode("utf-8")
        responseVarDict = json.loads(responseVarString)

        key = 'message'
        if key in responseVarDict:
            if responseVarDict['message'] == "invalid_token":
                print("The token has expired...\n")
                ops = input()
            else:
                pass

        if existenceOfMeli == True:
            newMeli = responseVarDict['id']

        else:
            newMeli = 0

        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        # predictor = scrapy.Request("https://api.mercadolibre.com/sites/MLB/category_predictor/predict?title=" + str(items["tittle"][0]))
        # print(predictor)
        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        if prediction is True:
            translator = Translator()
            translation = translator.translate(str(items["tittle"][0]), dest="es")
            tittleTraslated = translation.text

        coolDict = {"CGLink": CGLink, "price": items["price"], "pictures": items["picture"], "body": body,
                    "description": items["description"], "meli": newMeli}
        LennyDict = {"CGLink": CGLink, "response": responseVarString, "meli": newMeli}

        path = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\evidence__responses\cg"
        pathForStorageTheSynchItems = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\items"
        evidenceJson = get_json("cgEvidence.json", path=path)
        responses = get_json("cgResponses.json", path=path)
        synchLinks = get_json("synchAmazonList", path=pathForStorageTheSynchItems)

        # Storage the evidence of the process in a json file...
        with open(evidenceJson, "r+") as file:
            tmp = json.load(file)
            list = tmp["items"]
            list.append(coolDict)
            tmp["items"] = list
            file.seek(0)

        with open(evidenceJson, "w") as file:
            json.dump(tmp, file)

        # Storage their respective responses of the meli API request in another JSON with the string "responses" in his name...
        with open(responses, "r+") as file:
            tmp = json.load(file)
            list = tmp["items"]
            list.append(LennyDict)
            tmp["items"] = list
            file.seek(0)

        with open(responses, "w") as file:
            json.dump(tmp, file)

        # Build the synchList for the future synchronizing process...
        with open(synchLinks, "r+") as file:
            tmp = json.load(file)
            list0 = tmp["cgLink"]
            list0.append(LennyDict["cgLink"])

            list1 = tmp["meli"]
            list1.append(LennyDict["meli"])

            tmp["cgLink"] = list0
            tmp["meli"] = list1
            file.seek(0)

        with open(synchLinks, "w") as file:
            json.dump(tmp, file)

        yield items

