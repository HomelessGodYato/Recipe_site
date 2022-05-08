from pancakes.models import RecipeRecipeCategory, RecipeStage, Ingredient, RecipeImage, Recipe
from typing import TypedDict, List


class RecipeImageDTO(TypedDict):
    id: int
    image: str


class RecipeCategoryDTO(TypedDict):
    id: int
    name: str


class IngredientDTO(TypedDict):
    id: int
    name: str
    unit: str
    amount: str


class StageDTO(TypedDict):
    id: int
    cooking_time: str
    description: str
    image: str
    ingredients: List[IngredientDTO]


class RecipeDTO(TypedDict):
    id: int
    name: str
    date_create: str
    cooking_time: str
    image: RecipeImageDTO
    categories: List[RecipeCategoryDTO]
    stages: List[StageDTO]


class RecipeSimpleDTO(TypedDict):
    id: int
    name: str
    date_create: str
    cooking_time: str
    image: RecipeImageDTO
    categories: List[RecipeCategoryDTO]


def getRecipeDTO(recipe):
    # categoires
    categories_list = []
    for iter in RecipeRecipeCategory.objects.filter(recipe=recipe):
        categories_list.append(getCategoryDTO(iter))
    # stages
    stages_list = []
    for iter in RecipeStage.objects.filter(recipe=recipe):
        print(iter)
        stages_list.append(getStageDTO(iter))
    recipe = RecipeDTO(
        id=recipe.id,
        name=recipe.name,
        date_create=recipe.date_create,
        cooking_time=recipe.cooking_time,
        image=getRecipeImageDTO(recipe.image),
        categories=categories_list,
        stages=stages_list
    )
    return recipe


def getRecipeSimpleDTO(recipe):
    categories_list = []
    for iter in RecipeRecipeCategory.objects.filter(recipe=recipe):
        categories_list.append(getCategoryDTO(iter))
    recipe = RecipeSimpleDTO(
        id=recipe.id,
        name=recipe.name,
        date_create=recipe.date_create,
        cooking_time=recipe.cooking_time,
        image=getRecipeImageDTO(recipe.image),
        categories=categories_list
    )
    return recipe


def getStageDTO(stage):
    ingredient_list = []
    for iter in Ingredient.objects.filter(recipe_stage=stage):
        ingredient_list.append(getIngredientDTO(iter))
    stage = StageDTO(
        id=stage.id,
        cooking_time=stage.cooking_time,
        description=stage.description,
        image=stage.image,
        ingredients=ingredient_list
    )
    return stage


def getCategoryDTO(category):
    category = RecipeCategoryDTO(
        id=category.id,
        name=category.name.name
    )
    return category


def getIngredientDTO(ingredient):
    ingredient = IngredientDTO(
        id=ingredient.id,
        name=ingredient.name,
        unit=ingredient.unit,
        amount=ingredient.amount
    )
    return ingredient


def getRecipeImageDTO(image):
    imageDTO = RecipeImageDTO(
        id=image.id,
        image=image.image
    )
    return imageDTO



