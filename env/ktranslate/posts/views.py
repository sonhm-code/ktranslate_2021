from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.

def index(request):
    posts = Post.objects.all()
    q = request.GET.get('q','')

    if q:
        posts = posts.filter(request__icontains=q)

    context = {
        'posts' : posts,
        'q' : q
    }

    return render(request,'posts/index.html',context)


def detail(request,post_id):
    post = Post.objects.get(id = post_id)

    if not Comment.objects.filter(post__id = post_id):
        comment = '응답없음'
    else:
        comment = Comment.objects.filter(post__id = post_id).order_by('-liked_users')[0]
    
    context = {
        'post' : post,
        'comment' : comment
    }

    return render(request, 'posts/detail.html', context)


def new(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    return render(request, 'posts/new.html')


@login_required
def create(request):

    user = request.user
    request = request.POST.get('request')
    post = Post(user=user, request=request, created_at=timezone.now())
    post.save()

    return redirect('posts:index')


@login_required
def edit(request,post_id):
    try:
        post = Post.objects.get(id = post_id, user = request.user)
        if not Comment.objects.filter(post__id = post_id):
            comment = '응답없음'
        else:
            comment = Comment.objects.filter(post__id = post_id).order_by('-liked_users')[0]
    except Post.DoesNotExist:
        return redirect('posts:index')
    context = {
        "post" : post,
        "comment" : comment
    }

    return render(request, 'posts/edit.html', context)


@login_required
def update(request, post_id):
    try:
        post = Post.objects.get(id = post_id, user = request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')
    post.request = request.POST.get('request')
    post.save()

    return redirect('posts:index')


@login_required
def delete(request, post_id):
    try:
        post = Post.objects.get(id = post_id, user = request.user)
    except Post.DoesNotExist:
        return redirect('posts:index')
    post.delete()

    return redirect('posts:index')


@login_required
def comment(request, post_id):
    post = Post.objects.get(id = post_id)
    user = request.user
    response = request.POST.get('response')
    comment = Comment(post=post, user=user, response=response, created_at=timezone.now())
    comment.save()

    return redirect('posts:detail', post_id)


@login_required
def comment_like(request, post_id, comment_id):
    try:
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)

        if request.user in comment.liked_users.all():
            comment.liked_users.remove(request.user)
        else:
            comment.liked_users.add(request.user)
        
        return redirect('posts:detail', post_id=post.id)
    
    except Post.DoesNotExist:
        pass

    return redirect('posts:detail', post_id=post.id)

