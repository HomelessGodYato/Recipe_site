import pathlib
from django.db import models
import uuid


def recipe_image_upload_handler(instance, file_name):
    file_path = pathlib.Path(file_name)
    new_file_name = str(uuid.uuid1())
    return f"uploads/{new_file_name}{file_path.suffix}"


class RecipeImage(models.Model):
    image = models.ImageField(upload_to=recipe_image_upload_handler)


class RecipeCategory(models.Model):
    name = models.CharField(max_length=254)


class Recipe(models.Model):
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    date_create = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=254)
    cooking_time = models.IntegerField()
    image = models.ForeignKey(to=RecipeImage, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(to=RecipeCategory, through='RecipeRecipeCategory')


class RecipeRecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE)


class RecipeStage(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, null=False)
    cooking_time = models.IntegerField()
    description = models.CharField(max_length=8191)
    image = models.ForeignKey(to=RecipeImage, on_delete=models.CASCADE, null=True, blank=True)


class Ingredient(models.Model):
    recipe_stage = models.ForeignKey(to=RecipeStage, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=254)
    unit = models.CharField(max_length=254)
    amount = models.CharField(max_length=254)
