from django.shortcuts import render, get_object_or_404

from . models import Group, Post

NUM_OF_POSTS = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.select_related()[:NUM_OF_POSTS]
    context_title = {
        'posts': posts
    }
    return render(request, template, context_title)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:NUM_OF_POSTS]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
