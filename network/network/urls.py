
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("post/<int:post_id>", views.update_post, name="update_post"),
    path("post-like/<int:post_like_id>", views.post_like, name="post_like"),
    path("profiles/post-like/<int:post_like_id>", views.post_like, name="post_like"),
    path("profiles/<str:username>", views.profiles, name="profiles"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("following", views.following, name="following")
]
