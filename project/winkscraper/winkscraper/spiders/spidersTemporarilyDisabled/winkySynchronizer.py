import scrapy
import json
from ..items import WinkscraperItem
from ..testOnMeli import meli, pictureFunc, pictures_function
from ..splitingProducts import howToSplit
import js2xml
from re import sub
from decimal import Decimal
from ..calljson import get_data
from ..calljson import get_json
import time
import sys
import pandas as pd

pd.options.display.max_columns = 10000
pd.options.display.max_rows = 10000

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
    noFUrls = len(start_urls)

    print(" ͡° ͜ʖ ͡°these are the amount of urls for the megaPostSpider...")
    print(noFUrls)
    print(" ͡° ͜ʖ ͡°")

    amazonFails = []
    amazonSynch = []
    meliSynch = []
    condition = []
    counter = 0

    def parse(self, response):

        self.counter += 1

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

                self.amazonFails.append(response.url)
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

            # This area is for chunks of code to put price, descriptions and another attributes to the products in an adequate format...
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

            params = {'access_token': meli.access_token, 'refresh_token': meli.refresh_token}

            index = LinearSearch(self.data["amazonLinks"], self.amazonLink)
            correspondingMeli = str(self.data["meli"][index])

            if items["availability"][0] == "Disponible." and (items["prime"][0] == "Amazon Prime" or items["prime"][0] == "*Amazon Prime"):

                if value != None and len(items["selledByAmazon"]) == 1 and pictureFunc:
                    body = {"status": "active", "price": priceCalculator(value, 0.1, 0.16, 0, 100), "available_quantity": 10}
                    #body.update(postSet(newTittle, "MLM3530", definitiveDescription))
                    petition = meli.put(path="/items" + correspondingMeli, body=body, params=params)
                    time.sleep(0.4)
                    try:
                        responseVarString = petition.content.decode("utf-8")
                        responseVarDict = json.loads(responseVarString)
                        currentMeli = responseVarDict['id']

                        self.amazonSynch.append(response.url)
                        self.meliSynch.append(currentMeli)
                        self.condition.append("active, selled and shipped by Amazon!")
                    except:
                        print("Oops!", sys.exc_info()[0], "occurred.")
                        self.amazonSynch.append(response.url)
                        self.meliSynch.append(None)
                        self.condition.append("active, selled and shipped by Amazon!")
                        pass

                elif value != None and len(items["selledByAmazon"]) != 1 and pictureFunc:
                    body = {"status": "paused", "price": priceCalculator(value, 0.3, 0.16, 0, 100), "available_quantity": 1}
                    #body.update(postSet(newTittle, "MLM3530", definitiveDescription))
                    petition = meli.put(path="/items"+ correspondingMeli, body=body, params=params)
                    time.sleep(0.4)
                    try:
                        responseVarString = petition.content.decode("utf-8")
                        responseVarDict = json.loads(responseVarString)
                        currentMeli = responseVarDict['id']

                        self.amazonSynch.append(response.url)
                        self.meliSynch.append(currentMeli)
                        self.condition.append("active, selled and shipped by Amazon!**")
                    except:
                        print("Oops!", sys.exc_info()[0], "occurred.")
                        self.amazonSynch.append(response.url)
                        self.meliSynch.append(None)
                        self.condition.append("active, selled and shipped by Amazon!**")
                        pass

            else:
                body = {"status": "paused", "price": priceCalculator(value, 0.3, 0.16, 0, 100), "available_quantity": 0}
                #body.update(postSet(newTittle, "MLM3530", definitiveDescription))
                petition = meli.put(path="/items" + correspondingMeli, body=body, params=params)
                time.sleep(0.4)
                try:
                    responseVarString = petition.content.decode("utf-8")
                    responseVarDict = json.loads(responseVarString)
                    currentMeli = responseVarDict['id']

                    self.amazonSynch.append(response.url)
                    self.meliSynch.append(currentMeli)
                    self.condition.append("paused, not available")
                except:
                    print("Oops!", sys.exc_info()[0], "occurred.")
                    self.amazonSynch.append(response.url)
                    self.meliSynch.append(None)
                    self.condition.append("paused, not available")
                    pass

            yield items

        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("We're going to retry with the response {}... (⊙_◎)".format(response.url))

            #exec('amazonFails.append(response.url)')

            return self.parse(response)

        print("THIS IS HOW THE COUNTER LOOKS LIKE: {}".format(self.counter))
        print("THE TOTAL NOMBER OF PRODUCTS IS: {}".format(self.noFUrls))
        dictOfSynch = {"amazonLinks": self.amazonSynch, "meli": self.meliSynch, "condición": self.condition}
        dictOfFails = {"amazonFails": self.amazonFails}
        dfSynch = pd.DataFrame(dictOfSynch)
        dfFails = pd.DataFrame(dictOfFails)
        print(dfSynch)
        print(dfFails)
        if self.counter >= self.noFUrls - 8:
            dictOfSynch = {"amazonLinks": self.amazonSynch, "meli": self.meliSynch}
            dfSynch = pd.DataFrame(dictOfSynch)
            print(dfSynch)
            for _ in range(100):
                print('######################################################################')

            pathForStorageTheSynchItems = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\items"
            synchLinks = get_json("synchAmazonList" + str(self.beautifulNumber) + ".json", path=pathForStorageTheSynchItems)

            with open(synchLinks, "r+") as file:
                tmp = json.load(file)
                list0 = dfSynch["amazonLinks"]
                list1 = dfSynch["meli"]

                tmp["amazonLinks"] = self.amazonSynch
                tmp["meli"] = self.meliSynch
                file.seek(0)

            with open(synchLinks, "w") as file:
                json.dump(tmp, file)

