from django import template
from ..models import Post
import django.utils.html as django_html

register = template.Library()

@register.simple_tag
def total_posts_number():
    return Post.published.count()