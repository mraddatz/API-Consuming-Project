from django.shortcuts import render
from django.http import HttpResponse
import requests

def url_id(url, id_num=""):
  if url[-1] == "/":
    return id_num
  else:
    return url_id(url[0:-1], url[-1]+id_num)

def index(request):
    #https://rickandmortyapi.com/api/episode/

    response = requests.get('https://rickandmortyapi.com/api/episode/')
    if response:
        print('Success!')
        response_dic = response.json()
        pages = response_dic['info']['pages']
        results = response_dic['results']
        episodes = []
        for episode in results:
            episode_dic = {}
            episode_dic['id'] = episode['id']
            episode_dic['name'] = episode['name']
            episode_dic['air_date'] = episode['air_date']
            episode_dic['episode'] = episode['episode']
            episodes.append(episode_dic)
        if pages > 1:
            for _ in range(2, pages+1):
                next_url = response_dic['info']['next']
                response = requests.get(next_url)
                if response:
                    response_dic = response.json()
                    results = response_dic['results']
                    for episode in results:
                        episode_dic = {}
                        episode_dic['id'] = episode['id']
                        episode_dic['name'] = episode['name']
                        episode_dic['air_date'] = episode['air_date']
                        episode_dic['episode'] = episode['episode']
                        episodes.append(episode_dic)
        print(episodes)




    else:
        print('An error has occurred.')
    
    data = {
        'episodes': episodes,
    }

    return render(request, 'rickmortyapp/home.html', data)

def episode(request, episode_id):
    request_link = 'https://rickandmortyapi.com/api/episode/'+ str(episode_id)
    response = requests.get(request_link).json()
    characters_links = response['characters']
    characters = []
    for char in characters_links:
        character = requests.get(char).json()
        character_dic = {
            'link': char,
            'name': character['name'],
            'id': character['id'],
        }
        characters.append(character_dic)
    
    data = {
        'episode': response,
        'characters': characters,
    }
    return render(request, 'rickmortyapp/episode.html', data)

def character(request, character_id):
    print("Entroo!")
    request_link = 'https://rickandmortyapi.com/api/character/'+ str(character_id)
    character = requests.get(request_link).json()
    episodes_links = character['episode']
    episodes = []
    for epi in episodes_links:
        episode = requests.get(epi).json()
        episode_dic = {
            'link': epi,
            'name': episode['name'],
            'id': episode['id'],
        }
        episodes.append(episode_dic)
    if character['origin']['name'] != 'unknown':
        character['origin']['id'] = url_id(character['origin']['url'])
        print("ORIGIN: "+character['origin']['id'])
    if character['location']['name'] != 'unknown':
        character['location']['id'] = url_id(character['location']['url'])

    

    data = {
        'character': character,
        'episodes': episodes,
    }
    return render(request, 'rickmortyapp/character.html', data)

def location(request, location_id):
    request_link = 'https://rickandmortyapi.com/api/location/'+ str(location_id)
    location = requests.get(request_link).json()
    residents_links = location['residents']
    residents = []
    print(location)
    for res in residents_links:
        resident = requests.get(res).json()
        resident_dic = {
            'link': res,
            'name': resident['name'],
            'id': resident['id'],
        }
        residents.append(resident_dic)
    
    data = {
        'location': location,
        'residents': residents,
    }


    return render(request, 'rickmortyapp/location.html', data)