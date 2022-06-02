from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeCategory, RecipeImage

# Register your models here.

admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeCategory)
admin.site.register(RecipeImage)
