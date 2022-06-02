from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name="home"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('user/', views.user_main_page, name="user"),
    path('activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/$',
         views.activation, name='activate'),

    path('recipe_create/', views.create_recipe_view, name="recipe_create"),
    path('recipe_simple_create/', views.recipe_create_simple_view, name="recipe_simple_create"),
    path('recipe/', views.recipe_select_all_view, name="recipe_select_all"),
    path('recipe/<str:pk>', views.recipe_select_view, name="recipe_select"),

    #-------------------------------------------INGREDIENT----------------------------------------------
    path('ingredient/', views.ingredient_show_all_view, name="ingredient_show_all"),
    path('ingredient/<str:id>', views.ingredient_show_view, name="ingredient_show"),
    path('ingredient_form/', views.ingredient_form_view, name="ingredient_create"),
    path('ingredient_form/<str:id>', views.ingredient_form_view, name="ingredient_update"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
