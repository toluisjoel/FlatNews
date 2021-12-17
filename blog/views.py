from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.shortcuts import render
from .models import Post, Comment
from .forms import EmailPostForm


# Template Views 

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
    published_date__year = year,
    published_date__month = month,
    published_date__day = day,
    )
    comments = Comment.objects.all()
    for comment in comments:
        comment = comment

    context = {'post': post, 'comment': comment}
    return render(request, 'blog/post/post_detail.html', context)


# Forms views

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if post.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
    else:
        return EmailPostForm()
    context = {'post': post, 'form': form}
    return render(request, 'blog/post/share.html', context)
