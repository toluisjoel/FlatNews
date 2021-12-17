from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.shortcuts import render
from .models import Post, Comment
from .forms import EmailPostForm
from django.core.mail import send_mail


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
    mail_sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = f"{user['name']} recommends you read  {post.title}"
            message = f"Read the post '{post.title}' at {post_url}\n\n {user['name']}\'s comment {user['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [user['to']])
            mail_sent = True
    else:
        return EmailPostForm()

    context = {'post': post, 'form': form, 'mail_sent':mail_sent}
    return render(request, 'blog/post/share_post.html', context)
