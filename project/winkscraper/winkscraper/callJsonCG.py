import json

def get_json(json_file):

    incomplete_path = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders"
    theJson = "\\" + json_file
    path_of_definitiveList = str(incomplete_path + theJson).replace("\\", '/')

    return path_of_definitiveList

myJson = get_json("cgDefinitiveList.json")

with open(myJson, "r") as jsonFile:
    data = json.load(jsonFile)
