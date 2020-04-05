from django.shortcuts import render
from django.http import HttpResponse
import requests

def url_id(url, id_num=""):
  if url[-1] == "/":
    return id_num
  else:
    return url_id(url[0:-1], url[-1]+id_num)

def name_search(search_type, search_string):
    request_link = 'https://rickandmortyapi.com/api/' + search_type + '/?name=' + search_string
    response_dic = requests.get(request_link).json()
    if 'error' in response_dic.keys():
        return []
    pages = response_dic['info']['pages']
    output = []
    for _ in range(1, pages+1):
        output += response_dic['results']
        next_url = response_dic['info']['next']
        if next_url:
            response_dic = requests.get(next_url).json()
    
    return output


def index(request):
    #https://rickandmortyapi.com/api/episode/

    response = requests.get('https://rickandmortyapi.com/api/episode/')
    if response:
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
    characters_link = 'https://rickandmortyapi.com/api/character/'
    characters_id = ""
    for res in characters_links:
        if not characters_id:
            characters_id = characters_id + url_id(res)
        else:
            characters_id = characters_id + "," + url_id(res)
    characters = requests.get(characters_link + characters_id).json()
    if type(characters) == dict:
        characters = [characters]
    data = {
        'episode': response,
        'characters': characters,
    }
    return render(request, 'rickmortyapp/episode.html', data)

def character(request, character_id):
    request_link = 'https://rickandmortyapi.com/api/character/'+ str(character_id)
    character = requests.get(request_link).json()
    episodes_links = character['episode']
    episode_link = 'https://rickandmortyapi.com/api/episode/'
    episodes_id = ""

    for epi in episodes_links:
        if not episodes_id:
            episodes_id = episodes_id + url_id(epi)
        else:
            episodes_id = episodes_id + "," + url_id(epi)
    episodes = requests.get(episode_link + episodes_id).json()
    if type(episodes) == dict:
        episodes = [episodes]
    if character['origin']['name'] != 'unknown':
        character['origin']['id'] = url_id(character['origin']['url'])
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
    characters_link = 'https://rickandmortyapi.com/api/character/'
    residents_id = ""
    for res in residents_links:
        if not residents_id:
            residents_id = residents_id + url_id(res)
        else:
            residents_id = residents_id + "," + url_id(res)
    residents = requests.get(characters_link + residents_id).json()
    if type(residents) == dict:
        residents = [residents]

    data = {
        'location': location,
        'residents': residents,
    }


    return render(request, 'rickmortyapp/location.html', data)

def search(request):
    search_term = request.POST.get('search', '')
    characters = name_search('character', search_term)
    locations = name_search('location', search_term)
    episodes = name_search('episode', search_term)

    data = {
        'characters': characters,
        'locations': locations,
        'episodes': episodes,
        'search_term': search_term,
    }

    return render(request, 'rickmortyapp/search.html', data)