from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('category/<str:category_name>/', views.category_posts, name='category_posts'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/', views.view_profile_by_username, name='view_profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('toggle-like/', views.toggle_like, name='toggle_like'),
]
