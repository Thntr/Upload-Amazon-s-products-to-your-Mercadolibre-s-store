import scrapy
import json
from ..items import WinkscraperItem
from ..testOnMeli import meli
from ..testOnMeli import pictureFunc
from ..splitingProducts import howToSplit
import js2xml
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from googletrans import Translator
from re import sub
from decimal import Decimal
from ..calljson import get_data
from ..calljson import get_json
from scrapy_splash import SplashRequest
import time
import sys


class megaPostTestSpider(scrapy.Spider):
    name = "megaTest"
    data = get_data("megaSynchList.json")
    newArray = []

    # Start a set of parallel publications
    print("¿What # of prompt is is this?\n")
    beautifulNumber = int(input())

    # Get my array of the splited list
    listOfExtremes = howToSplit()
    print(listOfExtremes)

    for i in range(int(listOfExtremes[beautifulNumber - 1]), int(listOfExtremes[beautifulNumber])):
        newArray.append(data["amazonLinks"][i])

    start_urls = newArray

    print(" ͡° ͜ʖ ͡°these are the amount of urls for the megaPostSpider...")
    print(len(start_urls))
    print(" ͡° ͜ʖ ͡°")

    counter = 0

    def parse(self, response):

        try:
            print(r"¯\\_(ツ)_/¯ MEGA POST CRAWLER ¯\\_(ツ)_/¯")
            print("͡° ͜ʖ ͡° THIS IS THE CURRENT RESPONSE -----> {}".format(response.url))

            prediction = False

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

            time.sleep(1)

            price = response.css("#price_inside_buybox").css("::text").extract()
            description = response.css("#feature-bullets > ul").css("::text").extract()
            selledByAmazon = response.css("#merchant-info").css("::text").extract()
            shippingDate = response.css("#fast-track-message > div").css("::text").extract()
            tittle = response.css("#productTitle").css("::text").extract()

            if tittle == []:
                print("(⊙_◎) THE TITTLE IS EMPTY! Retrying with the response {}...".format(response.url))
                return self.parse(response)

            availability = response.css("#availability > span").css("::text").extract()
            js_prime = response.xpath(
                "//script[contains(text(), '\"bbopRuleID\":\"Acquisition_AddToCart_PrimeBasicFreeTrialUpsellEligible\"')]/text()").extract()

            if js_prime == None:
                prime = ["It's not prime"]
            else:
                if js_prime == []:
                    prime = ["*Amazon Prime"]
                else:
                    prime = ["Amazon Prime"]

            if availability == []:
                availability = ["It's not available"]
            if price == []:
                try:
                    price = response.css("# priceblock_ourprice").css("::text").extract()
                except:
                    pass
            if price == []:
                price = ["9999"]

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

            try:
                descriptionOnString = str(new_description[0])
                for i in range(0, len(new_description) - 1):
                    descriptionOnString += str(new_description[i])

                definitiveDescription = descriptionOnString
            except:
                definitiveDescription = "None"

            if definitiveDescription.isascii():
                print("*******************+YOUR DESCRIPTION HAS AN ASCII FORMAT******")
            else:
                print("********************DESCRIPTION HAS NOT AN ASCII FORMAT******")

            params = {'access_token': meli.access_token, 'refresh_token': meli.refresh_token}

            # cut the tittle to acomplish the tittle requeriments for posting
            if len(str(items["tittle"])) >= 55:
                ancientTittle = str(items["tittle"])
                truncated_tittle = ancientTittle[0:55]
                newTittle = truncated_tittle
            else:
                newTittle = str(items["tittle"])

            amazonLink = str(response.request.url)

            picturesList = [{"source": str(items["picture"][i])} for i in range(0, len(items["picture"]) - 1)]

            def postSet(varTittle, varCattegory, varDescription):
                theSet = {"title": "l" + varTittle,
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
                              },
                              {
                                  "id": "THICKNESS",
                                  "value_name": "0 cm"
                              },
                              {
                                  "id": "MATERIAL",
                                  "value_name": "0"
                              },
                              {
                                  "id": "LENGTH",
                                  "value_name": "0 cm"
                              },
                              {
                                  "id": "WIDTH",
                                  "value_name": "0 cm"
                              }
                          ]
                          }

                return theSet

            if items["availability"][0] == "Disponible." and (
                    items["prime"][0] == "Amazon Prime" or items["prime"][0] == "*Amazon Prime"):

                if value != None and len(items["selledByAmazon"]) == 1 and pictureFunc:
                    body = {"status": "active", "price": priceCalculator(value, 0.1, 0.16, 0, 100),
                            "pictures": picturesList, "available_quantity": 10}
                    body.update(postSet(newTittle, "MLM3530", definitiveDescription))
                    petition = meli.post(path="/items", body=body, params=params)
                    existenceOfMeli = True

                elif value != None and len(items["selledByAmazon"]) != 1 and pictureFunc:
                    body = {"status": "paused", "price": priceCalculator(value, 0.3, 0.16, 0, 100),
                            "pictures": picturesList, "available_quantity": 1}
                    body.update(postSet(newTittle, "MLM3530", definitiveDescription))
                    petition = meli.post(path="/items", body=body, params=params)
                    existenceOfMeli = True

            else:
                body = {"status": "paused", "price": priceCalculator(value, 0.3, 0.16, 0, 100), "available_quantity": 0,
                        "pictures": picturesList}
                body.update(postSet(newTittle, "MLM3530", definitiveDescription))
                petition = meli.post(path="/items", body=body, params=params)

                try:
                    responseVarString = petition.content.decode("utf-8")
                    responseVarDict = json.loads(responseVarString)
                    print("Response dict: {}".format(responseVarDict['id']))
                    existenceOfMeli = True
                except:
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

            coolDict = {"amazonLink": amazonLink, "price": items["price"], "Prime?": items["prime"],
                        "selledByAmazon": items["selledByAmazon"],
                        "shippingDate": items["shippingDate"], "availability": items["availability"],
                        "pictures": items["picture"], "body": body, "fdescription": items["description"],
                        "meli": newMeli}
            LennyDict = {"amazonLink": amazonLink, "response": responseVarString, "meli": newMeli}

            path = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\evidence__responses\amazon"
            pathForStorageTheSynchItems = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\items"
            evidenceJson = get_json("postEvidence.json", path=path)
            responses = get_json("postResponses.json", path=path)
            synchLinks = get_json("synchAmazonList.json", path=pathForStorageTheSynchItems)

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
                list0 = tmp["amazonLinks"]
                list0.append(LennyDict["amazonLink"])

                list1 = tmp["meli"]
                list1.append(LennyDict["meli"])

                tmp["amazonLinks"] = list0
                tmp["meli"] = list1
                file.seek(0)

            with open(synchLinks, "w") as file:
                json.dump(tmp, file)

            yield items

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("We're going to retry with the response {}... (⊙_◎)".format(response.url))
            return self.parse(response)

