from django import template

register = template.Library()

@register.filter
def is_liked_by(zakk, user):
    if not user.is_authenticated:
        return False
    return zakk.likes.filter(user=user).exists()