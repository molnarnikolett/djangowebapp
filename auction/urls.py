from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("munkatarsak/", views.staff, name="staff"),
    path("elerhetoseg/", views.contact, name="contact"),
    path("targyak/", views.items, name="items"),

    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="registration/login.html"
    ), name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("auction/start/<int:item_id>/", views.start_auction, name="start_auction"),
    path("auction/stop/<int:item_id>/", views.stop_auction, name="stop_auction"),
    path("bid/<int:item_id>/", views.bid, name="bid"),
    path("items/manage/", views.manage_items, name="manage_items"),
    path("items/manage/new/", views.create_item, name="create_item"),
    path("items/manage/<int:item_id>/edit/", views.edit_item, name="edit_item"),
    path("items/manage/<int:item_id>/delete/", views.delete_item, name="delete_item"),
]
