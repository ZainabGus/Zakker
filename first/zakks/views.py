from django.contrib.admin.templatetags.admin_list import search_form
from django.contrib.messages.api import success
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404  # ⬅️ добавили redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import models

from .models import Zakk, Comment, Like, Profile  # Импортируем модель зак и комментария
from .forms import ZakkForm, RegisterForm

def zakk_feed(request):
    # 1. Если пользователь отправляет данные (нажал кнопку)

    # 2. If request.method == 'GET' (пользователь просто открыл страницу)
    if request.method == 'POST':
        # Обработка добавления комментария
        if 'comment_text' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Войдите, чтобы оставить комментарий')
                return redirect('login')

            zakk_id = request.POST.get('zakk_id')
            zakk = get_object_or_404(Zakk, id=zakk_id)

            Comment.objects.create(
                user=request.user,
                zakk=zakk,
                text=request.POST.get('comment_text')
            )
            messages.success(request, 'Комментарий добавлен!')

            # Возвращаемся на ту же тему и к тому же закку
            current_theme = request.POST.get('current_theme', 'all')
            if current_theme == 'all' or not current_theme:
                return redirect(f"/#zakk-{zakk_id}")
            else:
                return redirect(f"/?theme={current_theme}#zakk-{zakk_id}")

    theme = request.GET.get('theme', 'all')
    if theme == 'all' or not theme:
        zakks = Zakk.objects.all().order_by('-created_at')
        # Забираем все твиты из базы данных и сортируем их по дате: от новых к старым (-)
    else:
        zakks = Zakk.objects.filter(theme=theme).order_by('-created_at')

    search_query = request.GET.get('search', '').strip().lower()
        # Если есть поисковый запрос — фильтруем по тексту или заголовку
    if search_query:
        # icontains означает "содержит" (без учета регистра)
        # Q позволяет сделать "ИЛИ" (текст ИЛИ заголовок)
        zakks = zakks.filter(
            models.Q(content__icontains=search_query) |
            models.Q(title__icontains=search_query)
        )

    themes = Zakk.THEME_CHOICES

    sort = request.GET.get('sort', 'new')

    if sort == 'popular':
        zakks = zakks.annotate(
            total_likes = Count('likes'),
            total_comments = Count('comments')
        ).order_by('-total_likes', '-total_comments', '-created_at')
    else:
        zakks = zakks.order_by('-created_at')

    # Отправляем эти твиты в наш HTML-шаблон
    return render(request, 'zakks/feed.html', {
        'zakks': zakks,
        'themes': themes,
        'current_theme': theme,
        'current_sort': sort,
        'search_query': search_query,
    })


def create_zakk(request):
    # Проверяем, залогинен ли пользователь
    if not request.user.is_authenticated:
        messages.error(request, 'Войдите в систему, чтобы создавать закки')
        return redirect('login')

    if request.method == 'POST':
        form = ZakkForm(request.POST)
        if form.is_valid():
            zakk = form.save(commit=False)
            zakk.user = request.user
            zakk.save()

            # Начисляем XP
            request.user.profile.xp += 10
            request.user.profile.save()

            messages.success(request, 'Закк опубликован! 🎉 +10XP')
            return redirect('feed')
    else:
        form = ZakkForm()

    return render(request, 'zakks/create_zakk.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже авторизованы')
        return redirect('feed')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, f'Добро пожаловать {user.username}!')
            return redirect('feed')

        else:
            messages.error(request, 'Ошибка! Форма заполнена неправильно')

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('feed')


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    Profile.objects.get_or_create(user=profile_user) # Если профиля нет — он создастся автоматически

    zakks = Zakk.objects.filter(user=profile_user).order_by('-created_at')

    theme = request.GET.get('theme', 'all')
    if theme != 'all' and theme:
        zakks = zakks.filter(theme=theme)

    zakks_count = Zakk.objects.filter(user=profile_user).count()
    comments_count = Comment.objects.filter(user=profile_user).count()
    likes_count = Like.objects.filter(zakk__user=profile_user).count()

    return render(request, 'zakks/profile.html', {
        'profile_user': profile_user,
        'zakks': zakks,
        'themes': Zakk.THEME_CHOICES,
        'current_theme': theme,
        'zakks_count': zakks_count,
        'comments_count': comments_count,
        'likes_count': likes_count,
        'profile_data': profile_user.profile,
    })


def toogle_like(request, zakk_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'error': 'Нужно войти в систему'
        }, status=403)

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Разрешен только POST'
        }, status=405)

    zakk = get_object_or_404(Zakk, id=zakk_id)
    like = Like.objects.filter(user=request.user, zakk=zakk).first()

    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, zakk=zakk)
        liked = True

        if zakk.user != request.user:  # Защита от накрутки (нельзя лайкать себя)
            zakk.user.profile.xp += 5
            zakk.user.profile.save()

    likes_count = zakk.likes.count()

    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': likes_count
    })


def delete_zakk(request, zakk_id):
    zakk = get_object_or_404(Zakk, id=zakk_id)

    if request.method != 'POST':
        messages.error(request, 'Неверный метод')
        return redirect('feed')

    if zakk.user != request.user:
        messages.error(request, 'Нельзя удалить чужой закк!')
        return redirect('feed')

    current_theme = request.POST.get('current_theme', 'all')

    zakk.delete()
    messages.success(request, 'Закк удален')

    if current_theme == 'all' or not current_theme:
        return redirect('feed')
    else:
        return redirect(f"/?=theme={current_theme}")
# Create your views here.


def edit_zakk(request, zakk_id):
    zakk = get_object_or_404(Zakk, id=zakk_id)

    if zakk.user != request.user:
        messages.error(request, 'Нельзя редактировать чужой закк!')
        return  redirect('feed')

    if request.method == 'POST':
        form = ZakkForm(request.POST, instance=zakk)
        if form.is_valid():
            form.save()
            messages.success(request, 'Закк изменён!')
            return redirect('feed')
    else:
        form = ZakkForm(instance=zakk)

    return render(request, 'zakks/edit_zakk.html', {
        'form': form,
        'zakk': zakk,
    })