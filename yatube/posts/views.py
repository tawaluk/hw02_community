from django.shortcuts import render, get_object_or_404
from . models import Post, Group


def index(request):
    template = 'posts/index.html'
    title = 'Yatube'
    posts = Post.objects.order_by('-pub_date')[:10]
    context_title = {
        'title': title,
        'posts': posts
    }
    return render(request, template, context_title)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
