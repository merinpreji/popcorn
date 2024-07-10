from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Avg, Count, Q

from .forms import MovieForm
from .models import Movie, Category, Review, Rating


# Create your views here.

def index(request):
    film = Movie.objects.annotate(average_rating=Avg('rating__rating'))
    genre = Category.objects.all()
    context = {
        "movies": film,
        "categories": genre
    }
    return render(request, "index.html", context)

def about(request):
    return render(request, "about.html")

def help(request):
    return render(request, "faq.html")

def moviedetail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    reviews = Review.objects.filter(movie=movie_id, user=user).order_by('-date')
    user_rating = Rating.objects.filter(movie=movie, user=user).first()
    rating_data = Rating.objects.filter(movie=movie).aggregate(average_rating=Avg('rating'), rating_count=Count('id'))
    review_data = reviews.aggregate(review_count=Count('id'))

    average_rating = rating_data['average_rating'] or 0
    rating_count = rating_data['rating_count']
    review_count = review_data['review_count']

    return render(request, "moviedetail.html", {"movie": movie, "reviews": reviews, "user_rating": user_rating, "user": user, "average_rating": average_rating, "review_count": review_count, "rating_count": rating_count})

def add_movie(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        movie_title = request.POST.get("movie_title")
        slug = slugify(movie_title)
        poster = request.FILES.get("poster")
        description = request.POST.get("description")
        release_date = request.POST.get("release_date")
        actors = request.POST.get("actors")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        trailer_link = request.POST.get("trailer_link")
        user = request.user
        movie = Movie(movie_title=movie_title, slug=slug, poster=poster, description=description, release_date=release_date, actors=actors, category=category, trailer_link=trailer_link, user=user)
        movie.save()
        return redirect("/")
    return render(request, "addmovie.html", {"categories": categories})

def edit_movie(request,movie_id):
    movie = Movie.objects.get(id=movie_id)
    categories = Category.objects.all()
    if request.method == "POST":
        movie.movie_title = request.POST.get("movie_title")
        movie.slug = slugify(movie.movie_title)
        movie.poster = request.FILES.get("poster")
        movie.description = request.POST.get("description")
        movie.release_date = request.POST.get("release_date")
        movie.actors = request.POST.get("actors")
        category_id = request.POST.get("category")
        movie.category = Category.objects.get(id=category_id)
        movie.trailer_link = request.POST.get("trailer_link")
        movie.save()
        return redirect("movie:moviedetail", movie_id=movie.id)
    return render(request, 'editmovie.html', {"categories": categories})

def del_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    return redirect("/")

def write_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    if request.method == "POST":
        review_title = request.POST.get("review_title")
        review = request.POST.get("review")
        movie_review = Review(movie=movie, review_title=review_title, review=review, user=user)
        movie_review.save()
        return redirect("movie:moviedetail", movie_id=movie_id)
    return render(request, "review.html", {"movie": movie, "user": user})

def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user = request.user
    if request.method == "POST":
        rating = request.POST.get("rating")
        movie_rating = Rating(movie=movie, rating=rating, user=user)
        movie_rating.save()
        return redirect("movie:moviedetail", movie_id=movie_id)
    return render(request, "moviedetail.html", {"movie": movie})

def search_movie(request):
    movies = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        movies = Movie.objects.all().filter(Q(movie_title__icontains=query)).annotate(average_rating=Avg('rating__rating'))
    return render(request, 'search.html', {'query': query, 'movies': movies})




