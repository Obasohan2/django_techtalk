from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


def home(request):
    posts_list = Post.objects.all().order_by('-created_on')
    categories = Category.objects.all()

    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        posts_list = posts_list.filter(category__name=category_filter)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'myblog/home.html', {
        'posts': posts,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent=None).order_by('-created_on')

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user

                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent = get_object_or_404(Comment, pk=parent_id)

                comment.save()
                messages.success(request, 'Comment added successfully!')
                return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'Please login to comment.')
    else:
        comment_form = CommentForm()

    return render(request, 'myblog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'myblog/add_comment.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'myblog/create_post.html', {'form': form})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes()
        })

    return redirect('post_detail', pk=post.pk)


def category_posts(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts_list = Post.objects.filter(category=category).order_by('-created_on')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'myblog/category_posts.html', {
        'posts': posts,
        'category': category,
        'categories': Category.objects.all(),
    })

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')