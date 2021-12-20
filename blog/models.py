from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    status_choices = (('draft', 'draft'), ('published', 'published'),)
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=225, unique_for_date='published_date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='unknown')
    published_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_choices, default='draft')
    objects = models.Manager() 
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.published_date.year, self.published_date.month, self.published_date.day, self.slug])

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
