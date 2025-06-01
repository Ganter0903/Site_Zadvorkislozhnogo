from django.contrib import admin

from .models import User, Poem, Audiobook, Story

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('id',)

@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ("title", "views_count", "author")

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "views_count", "author")

@admin.register(Audiobook)
class AudiobookAdmin(admin.ModelAdmin):
    list_display = ("title", "views_count", "author")