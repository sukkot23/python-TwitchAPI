import datetime
import json

import requests
from json import loads

dir_twitch = "./twitch.json"


# Get Json Data
with open(dir_twitch, "r") as json_file:
    json_twitch = json.load(json_file)


# Getting Twitch API New Tokens
def getNewAccessToken(clientID: str, clientSecret: str):
    # Reference: https://dev.twitch.tv/docs/api/
    oauth_key = requests.post("https://id.twitch.tv/oauth2/token" +
                              "?client_id=" + clientID +
                              "&client_secret=" + clientSecret +
                              "&grant_type=client_credentials")

    return loads(oauth_key.text)["access_token"]


# Config Data Refresh
def setAccessToken(clientID: str, clientSecret: str):
    access_token = getNewAccessToken(clientID, clientSecret)
    json_twitch['twitch']['OAuth_Token'] = access_token

    with open(dir_twitch, 'w', encoding='UTF-8') as make_file:
        json.dump(json_twitch, make_file, indent="\t")

    return access_token


# Tokens Validating requests
def isValidateToken(tokens: str):
    oAuth = 'OAuth ' + tokens
    response = requests.get("https://id.twitch.tv/oauth2/validate", headers={'Authorization': oAuth})

    try:
        var = response.json()['client_id']
        return True
    except KeyError:
        return False


if __name__ == '__main__':
    logTime = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
    token = json_twitch['twitch']['OAuth_Token']

    if not token:
        # Warning: Refreshing access tokens
        print(logTime + "Warning: Refreshing access tokens")
    else:
        if isValidateToken(token):
            # Success
            print("Success")
        else:
            # Warning: Refreshing access tokens
            print(logTime + "Warning: Refreshing access tokens")
