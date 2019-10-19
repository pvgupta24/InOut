from django import template

register = template.Library()

@register.filter(name='isAuthenticated')
def isAuthenticated(user):
    return user.is_authenticated