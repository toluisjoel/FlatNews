from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    status_choices = (('draft', 'draft'), ('published', 'published'),)
    title = models.CharField(max_length=255)
    body = models.TextField()
    slug = models.SlugField(max_length=225, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='unknown')
    # author_picture = models.ImageField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_choices, default='draft')
    objects = models.Manager() 
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title