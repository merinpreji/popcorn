from django.contrib import admin

from . models import Category, Movie


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'release_date', 'actors', 'category', 'trailer_link']
    prepopulated_fields = {'slug': ('movie_title',)}
    list_per_page = 20
admin.site.register(Movie, MovieAdmin)
