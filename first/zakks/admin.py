from django.contrib import admin
from .models import Zakk, Comment, Like


@admin.register(Zakk)
class ZakkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'theme', 'created_at')
    list_filter = ('theme', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'zakk', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'zakk', 'created_at')
    list_filter = ('created_at',)

from .models import Zakk, Comment, Like, Profile # ⬅️ Добавь Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'xp') # Показывать юзера и его XP
    search_fields = ('user__username',) # Чтобы можно было искать по нику
# Register your models here.
