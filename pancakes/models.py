import pathlib
from django.db import models
from django.contrib.auth.models import User
import uuid


def recipe_image_upload_handler(instance, file_name):
    file_path = pathlib.Path(file_name)
    new_file_name = str(uuid.uuid1())
    return f"uploads/{new_file_name}{file_path.suffix}"


# =================================================================


class Article(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    description = models.CharField(max_length=8191)
    date_create = models.DateTimeField(auto_now_add=True)


class ArticleComment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, null=False)
    date_create = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=8191)


class ArticleImage(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to=recipe_image_upload_handler)


# =================================================================


class RecipeImage(models.Model):
    image = models.ImageField(upload_to=recipe_image_upload_handler)


class RecipeCategory(models.Model):
    title = models.CharField(max_length=254)


class RecipeTag(models.Model):
    title = models.CharField(max_length=254)


class Recipe(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=254)
    cooking_time = models.IntegerField()
    image = models.ForeignKey(to=RecipeImage, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(to=RecipeCategory, through='RecipeRecipeCategory')
    tags = models.ManyToManyField(to=RecipeTag, through='RecipeRecipeTag')


class RecipeRecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE)


class RecipeRecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(RecipeTag, on_delete=models.CASCADE)

#-----------------------------------------------------


class RecipeStage(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, null=False)
    cooking_time = models.IntegerField()
    description = models.CharField(max_length=8191)
    image = models.ForeignKey(to=RecipeImage, on_delete=models.CASCADE, null=True, blank=True)


class RecipeIngredient(models.Model):
    title = models.CharField(max_length=254)
    unit = models.CharField(max_length=254)


class RecipeStageRecipeIngredient(models.Model):
    stage = models.ForeignKey(RecipeStage, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(RecipeIngredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=254)
    is_required=models.BooleanField(default=True)

#-----------------------------------------------------
class RecipeLike(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, null=False)


class RecipeRatings(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, null=False)
    rating = models.IntegerField()


class RecipeComment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=8191)
    date_create = models.DateTimeField(auto_now_add=True)
