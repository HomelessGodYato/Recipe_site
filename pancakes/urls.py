from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import *

urlpatterns = [
                  path('', views.home_page, name="home"),
                  # -------------------------------------------USER------------------------------------------------
                  path('register/', views.register_page, name="register"),
                  path('login/', views.login_page, name="login"),
                  path('logout/', views.logout_user, name="logout"),
                  path('user/', views.user_main_page, name="user"),
                  path('user/<int:pk>/delete/',
                       CustomUSerDeleteView.as_view(template_name='user/modifications/delete.html'),
                       name="delete_user"),
                  path('activate/<uidb64>[0-9A-Za-z_\-]+/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}/$',
                       views.activation, name='activate'),
                  path('user_edit/', views.user_edit_view, name="edit_user"),
                  path('reset_password/',auth_views.PasswordResetView.as_view(template_name = 'user/reset_password/reset_password.html'),
                       name="reset_password"),
                  path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = 'user/reset_password/reset_password_sent.html'),
                       name = "password_reset_done"),
                  path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name = 'user/reset_password/reset_password_new_password.html'),
                       name = "password_reset_confirm"),
                  path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name ='user/reset_password/reset_password_complete.html' ),
                       name="password_reset_complete"),
                  # -------------------------------------------RECIPE----------------------------------------------
                  path('recipe/', views.recipe_show_all_view, name="recipe_show_all"),
                  path('recipe/<str:id>', views.recipe_show_view, name="recipe_show"),
                  path('recipes/category/<str:category_name>', views.recipe_category_name_show_all_view,
                       name="recipe_category_name_show_all"),
                  path('recipes/title/', views.recipe_title_name_from_form_show_all_view,
                       name="recipe_title_name_show_all"),
                  path('recipes/title/<str:title_name>', views.recipe_title_name_show_all_view,
                       name="recipe_title_name_show_all"),
                  path('recipes/tag/<str:tag_name>', views.recipe_tag_name_show_all_view,
                       name="recipe_tag_name_show_all"),
                  path('recipes/user/<str:id>', views.recipe_user_id_show_all_view,
                       name="recipe_user_show_all"),
                  path('recipe_form/', views.recipe_form_view, name="recipe_create"),
                  path('recipe_form/', views.recipe_form_view, name="recipe_create"),
                  path('recipe_form/<str:id>', views.recipe_form_view, name="recipe_update"),
                  path('recipe_delete/<str:id>', views.recipe_delete_view, name="recipe_delete"),

                  # -------------------------------------------INGREDIENT----------------------------------------------
                  path('ingredient/', views.ingredient_show_all_view, name="ingredient_show_all"),
                  path('ingredient/<str:id>', views.ingredient_show_view, name="ingredient_show"),
                  path('ingredient_form/', views.ingredient_form_view, name="ingredient_create"),
                  path('ingredient_form/<str:id>', views.ingredient_form_view, name="ingredient_update"),
                  path('ingredient_delete/<str:id>', views.ingredient_delete_view, name="ingredient_delete"),

                  # -------------------------------------------CATEGORY----------------------------------------------
                  path('category/', views.category_show_all_view, name="category_show_all"),
                  path('category/<str:id>', views.category_show_view, name="category_show"),
                  path('category_form/', views.category_form_view, name="category_create"),
                  path('category_form/<str:id>', views.category_form_view, name="category_update"),
                  path('category_delete/<str:id>', views.category_delete_view, name="category_delete"),

                  # -------------------------------------------TAG----------------------------------------------
                  path('tag/', views.tag_show_all_view, name="tag_show_all"),
                  path('tag/<str:id>', views.tag_show_view, name="tag_show"),
                  path('tag_form/', views.tag_form_view, name="tag_create"),
                  path('tag_form/<str:id>', views.tag_form_view, name="tag_update"),
                  path('tag_delete/<str:id>', views.tag_delete_view, name="tag_delete"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
