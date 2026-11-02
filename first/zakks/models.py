from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Zakk(models.Model):
    # 1. Связь с автором твита.
    # models.ForeignKey означает связь "Один ко многим" (у одного пользователя может быть много твитов).
    # on_delete=models.CASCADE означает: если удалить пользователя, удалятся и все его твиты.
    # related_name='tweets' позволит нам позже легко получать твиты юзера через код: user.tweets.all()
    THEME_CHOICES = [
        ('math', '📐 Математика'),
        ('philosophy', '🧠 Философия'),
        ('it', '💻 IT'),
        ('art', '🎨 Искусство'),
        ('literature', '📚 Литература'),
        ('history', '📜 История'),
        ('physics', '🔭 Физика'),
        ('chemistry', '🔬 Химия'),
        ('biology', '🌱 Биология'),
        ('music', '🎸 Музыка'),
        ('sport', '🏀 Спорт'),
        ('other', '📝 Другое'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zakks')
    title = models.CharField(max_length=100)
    content = models.TextField()
    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default='other',
        verbose_name='Тема',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Настройка, чтобы в админке Django твит отображался текстом, а не просто как "Tweet object"
    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # Связь с автором комментария
    zakk = models.ForeignKey(Zakk, on_delete=models.CASCADE, related_name='comments')  # Связь с закком (к какому закку комментарий)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}..."


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    zakk = models.ForeignKey(Zakk, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'zakk')

    def __str__(self):
        return f'{self.user.username} ❤ {self.zakk.id}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    xp = models.IntegerField(default=0, verbose_name='Опыт (XP)')

    def __str__(self):
        return f'Профиль {self.user.username} (XP:{self.xp}'

    def get_level(self):
        if self.xp < 50:
            return 'Слабак'
        elif self.xp < 150:
            return 'Новичок'
        elif self.xp < 300:
            return 'Нормис'
        elif self.xp < 500:
            return 'Мастхэндр'
        elif self.xp < 1000:
            return 'Мыслитель'
        elif self.xp < 3000:
            return 'Крутой Заккер'
        else:
            return 'Крутая Патя'

    def get_progress_percent(self):
        if self.xp < 50:
            return int((self.xp/50)*100)
        elif self.xp < 150:
            return int(((self.xp - 50) / 100) * 100)
        elif self.xp < 300:
            return int(((self.xp - 150) / 150) * 100)
        elif self.xp < 500:
            return int(((self.xp - 300) / 200) * 100)
        elif self.xp < 1000:
            return int(((self.xp - 500) / 500) * 100)
        elif self.xp < 3000:
            return int(((self.xp - 1000) / 2000) * 100)
        else:
            return 100


# Create your models here.
