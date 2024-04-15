from django.shortcuts import render
from . import generate_rating as gr

# from django.http import JsonResponse

from . import format_rating as fr

# Create your views here.

def index(request):
    return render(request, 'spotify/index.html')

def rate(request):
    context = {}
    if request.method == 'POST':
        '''Get user input and change search type text in search box'''
        user_input = request.POST.get('user_input')
        search_type = request.POST.get('search_type')

        if len(user_input) > 50:
            context['error'] = "Search query too long, please try again with a shorter query."
            return render(request, 'spotify/rate.html', context)

        # set default search type if none provided
        if not search_type:
            search_type = 'album'

        context['search_type'] = search_type

        if search_type == 'track':
            # track search
            result = gr.get_track_popularity(user_input)
            if result is not None:
                '''get rating from api and description from json file'''
                context['rating'] = result

                desc, img = fr.format_rating(result, type = 'Track')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = gr.get_track_image(user_input)
                context['name'] = gr.get_track_name(user_input)
            else:
                context['error'] = f"No result with name {user_input} found."

        elif search_type == 'album':
            # album search
            result = gr.get_album_popularity(user_input)
            if result is not None:
                context['rating'] = result

                desc, img = fr.format_rating(result, type = 'Album')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = gr.get_album_image(user_input)
                context['name'] = gr.get_album_name(user_input)
            else:
                context['error'] = f"No result with name {user_input} found."


        elif search_type == 'playlist':
            # playlist search
            result = gr.get_playlist_popularity(user_input)
            if result is not None:
                context['rating'] = result

                desc, img = fr.format_rating(result, type = 'Playlist')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = gr.get_playlist_image(user_input)
                context['name'] = gr.get_playlist_name(user_input)
            else:
                context['error'] = f"No result with name {user_input} found."

    return render(request, 'spotify/rate.html', context)
