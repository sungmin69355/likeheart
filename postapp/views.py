from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Post, Comment
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q


def home(request):
    posts = Post.objects.order_by('-id')
    return render(request, 'home.html', {'posts': posts})

def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post': post_detail})

def new(request):
    return render(request, 'new.html')

def create(request):
    post = Post()
    post.title = request.POST['title']
    post.body = request.POST['body']
    post.pub_date = timezone.datetime.now()
    post.name = User.objects.get(username = request.user.get_username())
    
    post.images = request.FILES['images']
    post.save()
    return redirect('/post/' + str(post.id))

def comment_write(request, post_pk):
    if request.method =='POST':
        post = Post(pk=post_pk)
        comment = Comment()
        comment.post = post
        comment.comment_contents = request.POST['content']

        if not comment.comment_contents:
            messages.info(request, '댓글을 입력해 주세요')
            return redirect('detail', post_pk)

        comment.comment_date = timezone.datetime.now()
        comment.comment_writer = User.objects.get(username = request.user.get_username())
        comment.save()

        return redirect('detail', post_pk)

def delete(request, post_pk):
    post = Post.objects.get(id=post_pk)
    user = request.user.get_username()

    if post.name == user :
        post.delete()
        return redirect('home')
    else:
        messages.info(request, '아이디가 다릅니다.')
        return redirect('detail', post_pk)

def edit(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    user = request.user.get_username()

    if post.name == user :
        if request.method == 'POST':
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.pub_date = timezone.datetime.now()
            post.save()
            return redirect('detail', post_pk)

        else:
            return render(request, 'edit.html')

    else:
        messages.info(request, '아이디가 다릅니다.')
        return redirect('detail', post_pk)


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user 
        post_id = request.POST.get('pk', None)
        post = Post.objects.get(pk = post_id)

        if post.likes.filter(id = user.id).exists():
            post.likes.remove(user) 
            message = '좋아요 취소'
        else:
            post.likes.add(user)
            message = '좋아요'

    context = {'likes_count' : post.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
def comment_delete(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user.get_username()

    context = {'post': post,}
    content = request.POST.get('content')

    if user == comment.comment_writer:
        comment.delete()
        return redirect('detail', post_pk)

    else:
        messages.info(request, '아이디가 다릅니다.')
        return redirect('detail', post_pk)

def search(request):
    posts = Post.objects.order_by('-id')
    q = request.GET.get('q', '') 

    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(body__icontains=q)) 
        return render(request, 'search.html', {'posts' : posts,'q' : q})

