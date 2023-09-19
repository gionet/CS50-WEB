from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:auction_id>", views.items, name="items"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("watchlist/<int:auction_id>", views.watchlist_func, name="watchlist_func"),
    path("bidding/<int:auction_id>", views.bidding, name="bidding"),
    path("watchlist", views.watchlistList, name="watchlistList"),
    path("closelisting/<int:auction_id>", views.closeListing, name="closeListing"),
    path("categories", views.categorylist, name="categorylist"),
    path("categories/<str:category_itemlist>", views.category, name="category")
]
