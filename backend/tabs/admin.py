from django.contrib import admin
from .models import Tab, Comment, Favorite

@admin.register(Tab)
class TabAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'author', 'difficulty', 'created_at')
    search_fields = ('title', 'artist', 'song')
    list_filter = ('difficulty',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'tab', 'created_at')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'tab', 'created_at')