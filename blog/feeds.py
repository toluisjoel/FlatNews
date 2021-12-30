from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from blog.models import Post


class LatestPostFeed(Feed):
    link = reverse_lazy('blog:post_list')
    description = 'My latest posts'
    