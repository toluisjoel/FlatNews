from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
]
