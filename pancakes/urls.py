from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static
from .views import CustomUSerDeleteView

urlpatterns = [
    path('home/', views.home_page, name="home"),

    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('user/', views.user_main_page, name="user"),
    path('user/<int:pk>/delete/', CustomUSerDeleteView.as_view(template_name ='user/modifications/delete.html') , name="delete_user"),
    path('activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/$',
         views.activation, name='activate'),

    path('recipe_create/', views.create_recipe_view, name="recipe_create"),
    path('recipe_simple_create/', views.recipe_create_simple_view, name="recipe_simple_create"),
    path('recipe/', views.recipe_select_all_view, name="recipe_select_all"),
    path('recipe/<str:pk>', views.recipe_select_view, name="recipe_select"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
