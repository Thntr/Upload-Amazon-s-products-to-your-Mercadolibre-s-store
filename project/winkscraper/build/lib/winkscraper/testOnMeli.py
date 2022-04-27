from .meli import Meli

meli = Meli(client_id="7933855856355346", client_secret="SxETU1znPagO0pM9BJsE5q1B4oiY5Uzz")
redirectUrl = str(meli.auth_url(redirect_URI="https://winktechnologies.herokuapp.com/"))

print("Da click en el siguiente enlace:\n\n")
print(redirectUrl)

print("\n\nPega el código que aparece en el URL, aquí:")
the_received_code = str(input())
access_token = meli.authorize(code=the_received_code, redirect_URI="https://winktechnologies.herokuapp.com/")

class heart():

    token = access_token

