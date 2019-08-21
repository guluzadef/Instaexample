from django import template


register = template.Library()


@register.filter
def get_followers(user):
    return [follow.from_user for follow in user.followers.all()]