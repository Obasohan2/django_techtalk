from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Community


# Create your views here.

class HomeView(generic.ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'posts'
    ordering = ['-created_on']


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'myblog/post_detail.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Comment.objects.create(
            post=post,
            author=request.user,
            text=request.POST['comment']
        )
        return redirect('post_detail', pk=pk)


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('post_detail', pk=pk)

    def get(self, request, pk):
        return self.post(request, pk)


class CommunityView(generic.ListView):
    model = Post
    template_name = 'myblog/community.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.community = get_object_or_404(Community, name=self.kwargs['community_name'])
        return Post.objects.filter(community=self.community).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = self.community
        return context

