from django.contrib import admin

from reviews.models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'all_genres')
    list_filter = ('year', 'category', 'genre')
    search_fields = ('name', 'category__name', 'genre__name')
    filter_horizontal = ('genre',)

    @admin.display(description='Жанры')
    def all_genres(self, obj):
        genres = obj.genre.all()
        if genres:
            return ', '.join([genre.name for genre in genres])
        return '—'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    date_hierarchy = 'pub_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date')
    list_filter = ('pub_date', 'review')
    search_fields = ('text', 'author__username', 'review__text')
    date_hierarchy = 'pub_date'
