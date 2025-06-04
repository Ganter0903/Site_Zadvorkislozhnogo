from django.contrib import admin

from .models import User, Poem, Audiobook, Story, Like, Comment, Blog, Subscription, Genre

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

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_id", "created_at")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_id", "created_at")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "author", "created_at")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "created_at")
    list_filter = ("from_user", "to_user")
    search_fields = ("from_user__username", "to_user__username")
    ordering = ("-created_at",)
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)