from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.db.models import F, Sum, Max, Min, Count, Avg, Value


# Create your views here.
def show_all_movie(request):
    # movies = Movie.objects.order_by(F('year').asc(nulls_last=True), 'rating')
    movies = Movie.objects.annotate(
        true_bool=Value(True),
        fals_bool=Value(False),
        str_fielf=Value('Hellow'),
        int_field=Value(123),
        new_budget=F('budget') + 100,
        ffff =F('budget') * F('year')
    )
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg
    })


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    agg = movies.aggregate(Sum('budget'), Avg('rating'), Min('year'), Max('year'))

    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })

# from movie_app.models import Movie
