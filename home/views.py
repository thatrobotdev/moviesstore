import random
from django.shortcuts import render
from movies.models import Movie

def index(request):
    movies = list(Movie.objects.all()) 
    random_movies = random.sample(movies, min(3, len(movies)))

    template_data = {}
    template_data['title'] = 'Movies Store'
    template_data['random_movies'] = random_movies
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data = {'title': 'About'}
    return render(request, 'home/about.html', {'template_data': template_data})
