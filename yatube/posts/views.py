from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
#from .utils import utils
from .models import Group, Post, User

NUM_OF_POSTS = 10

def utils(queryset, request):
    paginator = Paginator(queryset, NUM_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_obj': page_obj,
        'page_number': page_number
    }


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    posts = Post.objects.all()[:NUM_OF_POSTS]
    context_title = {
        'page_obj': page_obj,
        'posts': posts
    }
    return render(request, template, context_title)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    goup_list_post = group.posts.all()
    paginator = Paginator(goup_list_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    posts = group.posts.all()[:NUM_OF_POSTS]
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related('author')
    template = 'posts/profile.html'
    context = {'author': author}
    context.update(utils(post_list, request))
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts_count = Post.objects.select_related('author').count()
    template = 'posts/post_detail.html'
    context = {
        'post': post, 'posts_count': posts_count}
    return render(request, template, context)

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()
        return redirect('posts:profile', create_post.author)
    template = 'posts/create_post.html'
    context = {'form': form}
    return render(request, template, context)

@login_required
def post_edit(request, post_id):
    edit_post = get_object_or_404(Post, id=post_id)
    if request.user != edit_post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=edit_post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    template = 'posts/create_post.html'
    context = {'form': form, 'is_edit': True}
    return render(request, template, context)