from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.shortcuts import render
from pathlib import Path
from .models import Post, Comment

#views 

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts':posts, 'page':page}
    return render(request, 'blog/post/post_list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
    status='published',
    publish__year = year,
    publish__month = month,
    publish__day = day,
    )
    comments = Comment.objects.all()
    for comment in comments:
        comment = comment

    context = {'post': post, 'comment': comment}
    return render(request, 'blog/post/post_detail.html', context)
