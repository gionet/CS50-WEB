from django.urls import path
from . import views
 
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create_post", views.create_post, name="create_post"),
    path("timeFrame/<str:timeFrame>/", views.timeFrame, name="timeFrame"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("update_post", views.update_post, name="update_post"),
    path("generate_csv/", views.generate_csv, name="generate_csv"),
]