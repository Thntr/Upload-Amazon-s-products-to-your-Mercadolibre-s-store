import json

def get_json(json_file, path):

    incomplete_path = path
    theJson = "\\" + json_file
    path_of_definitiveList = str(incomplete_path + theJson).replace("\\", '/')

    return path_of_definitiveList

def get_data(json_file):

    path = r"C:\Users\ramzhacker\Documents\MEGA\Newy\Wink_Inc\WinkAI\#WinkAIMLApp\pythonSdkMaster\winktech\project\winkscraper\winkscraper\spiders\items"
    myJson = get_json(json_file, path=path)

    with open(myJson, "r") as jsonFile:
        data = json.load(jsonFile)

    return data