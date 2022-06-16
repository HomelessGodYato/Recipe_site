from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeCategory, RecipeImage,UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeCategory)
admin.site.register(RecipeImage)
