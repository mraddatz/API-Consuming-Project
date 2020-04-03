from django.shortcuts import render
from django.http import HttpResponse
import requests

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