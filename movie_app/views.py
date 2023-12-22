from django.shortcuts import render, get_object_or_404
from . models import Movie, Director, Actor
from django.db.models import F, Sum, Max, Min, Count, Avg, Value

# Create your views here.
def show_all_directors(request):
    '''Список всех режиссеров'''
    directors = Director.objects.all()
    # for director in directors: # для первого запуска, чтобы прописать SLUGи
    #     director.save()
    data ={
        'directors': directors
    }

    return render(request, 'movie_app/directors_list.html', context=data)
def show_one_director(request, slug_director:str):
   '''Вывод указанного режиссера'''
   director = get_object_or_404(Director, slug=slug_director)
   return render(request, 'movie_app/one_director.html',
                 context={'director': director})

def show_all_movie(request):
    # movies = Movie.objects.all()
    # movies = Movie.objects.order_by('rating', 'budget') # сортировка
    #movies = Movie.objects.order_by(F('year').asc(nulls_last=True), 'rating')
    f_mov = Movie.objects.filter(name__contains='a')
    movies = Movie.objects.annotate( # можно в одном анотате все прописать
        true_bool=Value(True),
        false_bool=Value(False),
        str_field=Value('Hello'),
        int_field=Value(123),
        new_budget=F('budget') + 100,
    ).annotate(ffff=F('rating') * F('year')) # можно добавлять разные анототы, всё сольётся в один
    agg =  movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    #for movie in movies: # для первого запуска, чтобы прописать SLUGи
    #    movie.save()
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg,
        'total': movies.count(),
        'f_mov' : f_mov,
    })

def show_one_movie(request, slug_movie:str):
    #movie = Movie.objects.get(id=id_movie)          вариант через ГЕТ, сломается если дать несуществующий ключ
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html',
                  {
                    'movie': movie,
                    })

def show_all_actors(request):
    actors = Actor.objects.all()
    # for actor in actors: # для первого запуска, чтобы прописать SLUGи
    #     actor.save()
    data = {
        'actors': actors
    }
    return render(request, 'movie_app/actors_list.html', context=data)

def show_one_actor(request, slug_actor:str):
    actor = get_object_or_404(Actor, slug=slug_actor)
    return render(request, 'movie_app/one_actor.html',
                  {
                      'actor': actor,
                  })
