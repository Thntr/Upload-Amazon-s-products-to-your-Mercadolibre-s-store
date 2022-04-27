from .meli import Meli
import asyncio
from urllib.parse import urlparse
import urllib3

def refreshToken():
    meli = Meli(client_id="7933855856355346", client_secret="SxETU1znPagO0pM9BJsE5q1B4oiY5Uzz")
    redirectUrl = str(meli.auth_url(redirect_URI="https://winktechnologies.herokuapp.com/"))

    print("Da click en el siguiente enlace:\n")
    print(redirectUrl)

    print("\n\nPega el código que aparece en el URL, aquí:")
    the_received_code = str(input())
    access_token = meli.authorize(code=the_received_code, redirect_URI="https://winktechnologies.herokuapp.com/")
    refresh_token = meli.get_refresh_token()
    meli = Meli(client_id="7933855856355346", client_secret="SxETU1znPagO0pM9BJsE5q1B4oiY5Uzz", access_token=access_token, refresh_token=refresh_token)

    #Quit the hashes (#) and run the "winkSynchTest" at winkscraper/spiders/botsStarters to create your own test_user (just for user's with an mercadolibre's account)
    params = {'access_token': access_token}
    body = {'site_id': "MLM"}
    new_user = meli.post(path="/users/test_user",body=body, params=params)
    print(new_user.content)

    return meli

meli = refreshToken()

print("Do you wanna add the pictures update function? " + "Press [Y/n]")
pictures_function = input()

if pictures_function == "Y" or "y":
    pictureFunc = True

