from django.shortcuts import render, get_object_or_404
from . models import Movie
from django.db.models import F, Sum, Max, Min, Count, Avg, Value
# Create your views here.
def show_all_movie(request):
    # movies = Movie.objects.all()
    # movies = Movie.objects.order_by('rating', 'budget') # сортировка
    f_mov = Movie.objects.filter(name__contains='a')
    #movies = Movie.objects.order_by(F('year').asc(nulls_last=True), 'rating')
    movies = Movie.objects.annotate( # можно в одном анотате все прописать
        true_bool=Value(True),
        false_bool=Value(False),
        str_field=Value('Hello'),
        int_field=Value(123),
        new_budget=F('budget') + 100,
    ).annotate(ffff=F('rating') * F('year')) # можно добавлять разные анототы, всё сольётся в один
    agg =  movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    #for movie in movies:
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
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })
