from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Post
from .forms import EmailPostForm
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


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

    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save() 
    else:
        comment_form = CommentForm()

    context = {'post': post,'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form}
    return render(request, 'blog/post/post_detail.html', context)


# Forms views

def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    mail_is_sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{user['name']} recommends you read  {post.title}"
            message = f"Read the post '{post.title}' at {post_url}\n\n {user['name']}\'s comment {user['comments']}"
            send_mail(subject, message, user['email'], [user['to']], fail_silently=False)
            mail_is_sent = True
    else:
        form = EmailPostForm()
        user = EmailPostForm()
        
    context = {'post': post, 'form': form, 'mail_is_sent':mail_is_sent, 'user':user}
    return render(request, 'blog/post/share.html', context)
