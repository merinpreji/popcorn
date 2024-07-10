from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)

    # def get_url(self):
    #     return reverse('movie:movie_by_category', args=[self.slug])

class Movie(models.Model):
    movie_title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    poster = models.ImageField(upload_to="poster", blank=True)
    description = models.TextField(blank=True)
    release_date = models.CharField(max_length=300, blank=True)
    actors = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trailer_link = models.URLField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('movie_title',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.movie_title)
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.movie_title)

    # def get_url(self):
    #     return reverse('movie:movie_by_category', args=[self.slug])

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=500, blank=True)
    review = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('movie',)
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return '{}'.format(self.review_title)

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('movie',)
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'

    def __str__(self):
        return '{}'.format(self.review_title)
