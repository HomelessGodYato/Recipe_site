from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('user/', views.user_main_page, name="user"),
    path('activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/$',
         views.activation, name='activate'),
]
