from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'description',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('score', 'pub_date',)


class UserAdmin(admin.ModelAdmin):
    list_display = ("role",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
