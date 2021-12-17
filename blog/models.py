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
    slug = models.SlugField(max_length=225, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='unknown')
    author_picture = models.ImageField(upload_to='static/images', editable=True)
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
    # author_picture = models.ImageField(blank=True)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-published_date',)
