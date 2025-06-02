from django.urls import path
from .views import HomeView, PostDetailView, LikePostView, CommunityView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('community/<str:community_name>/', CommunityView.as_view(), name='community_view'),
]