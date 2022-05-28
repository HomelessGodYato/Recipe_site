from django.contrib import admin
from .models import Recipe, Ingredient, RecipeCategory, RecipeImage

# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeCategory)
admin.site.register(RecipeImage)
