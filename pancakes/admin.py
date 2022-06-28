from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeCategory, RecipeImage,UserProfile, Article, ArticleComment, \
    ArticleImage

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeCategory)
admin.site.register(RecipeImage)

admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(ArticleImage)