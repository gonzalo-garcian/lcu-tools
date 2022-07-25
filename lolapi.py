import json
import requests

def update_data_base(JSON_NAME, API_URL):
    
    open(JSON_NAME, 'wb').write(requests.get(API_URL, allow_redirects=True).content)


def get_game_version():

    data_base_name = 'version.json'
    update_data_base(data_base_name, API_VERSION)
    actual_summoner_data = json.loads(open(data_base_name, 'r').read())
    return actual_summoner_data[0]


def GET_PROFILE_ICON(PROFILE_ICON_ID):

    temp_API_URL = API_PROFILE_IMG + PROFILE_ICON_ID + '.png'

    r = requests.get(temp_API_URL)
    with open("profileIcon.png", "wb") as f:
        f.write(r.content)


    return "profileIcon.png"


API_VERSION = 'https://ddragon.leagueoflegends.com/api/versions.json'
API_PROFILE_IMG = f'http://ddragon.leagueoflegends.com/cdn/{get_game_version()}/img/profileicon/'