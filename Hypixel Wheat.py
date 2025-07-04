import json
import requests
from discord.ext import commands
from datetime import datetime
import time
import csv

def get_uuid(username):
        url = 'https://api.mojang.com/users/profiles/minecraft/' + username
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['id']
        else:
            LookupError("Mojang Api Servers are down! Like wtf microsoft!")
            return None

with open('settings.json') as file:
        settings = json.load(file)
        print("JSON READ")

startCollecting = False
pastData = 0

key = settings["key"]
username = settings["username"]
profile = settings["profile"]
collection = settings["collection"]
uuid = get_uuid(username)

def getCollection(key, profile, uuid, collection):
    request_url = f"https://api.hypixel.net/v2/skyblock/profiles?key={key}&uuid={uuid}"
    api_response = requests.get(request_url)
    print(api_response)
    
    # TODO MAJOR: this assumes that the rank of the player using this program is MVP, doesn't account for other factors.
    # I'm just testing, so this isn't a BIG problem, but in production, this will be BAD!

    try:
        if api_response.json()["profiles"][0]["cute_name"] == profile:
            response_json = api_response.json()["profiles"][0]["members"][uuid]["collection"][collection]
        elif api_response.json()["profiles"][1]["cute_name"] == profile:
            response_json = api_response.json()["profiles"][1]["members"][uuid]["collection"][collection]
        elif api_response.json()["profiles"][2]["cute_name"] == profile:
            response_json = api_response.json()["profiles"][2]["members"][uuid]["collection"][collection]
        elif api_response.json()["profiles"][3]["cute_name"] == profile:
            response_json = api_response.json()["profiles"][3]["members"][uuid]["collection"][collection]
        else:
            return "couldn't find profile"
    except KeyError as ke:
        while True:
            time.sleep(1)
            print(f"SOMETHING WENT WRONG WITH FETCHING PROFILES, CHECK API KEY: {ke}")
    else:
        return response_json

pastData = getCollection(key, profile, uuid, collection)

def runCollectionScript():
    global startCollecting
    global pastData
    print("STARTING COLLECTION TRACKER")
    while startCollecting == True:
        current_date_and_time = str(datetime.now())[:-7]  # Remove milliseconds
        newData = getCollection(key, profile, uuid, collection)
        dataToWrite = {
            current_date_and_time: {
                "player": username,
                "uuid": uuid,
                "collection": collection,
                "data": pastData,
                "change": newData - pastData
            }
        }
        try:
            with open("collectionData.json", "r") as infile:
                existing_data = json.load(infile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing_data = {}

        existing_data.update(dataToWrite)

        with open("collectionData.json", "w") as outfile:
            json.dump(existing_data, outfile, indent=4)

        
        pastData = newData
        time.sleep(60)

startCollecting = True
runCollectionScript()