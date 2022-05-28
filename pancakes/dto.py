from pancakes.models import RecipeRecipeCategory, RecipeStage, Ingredient, RecipeImage, Recipe, RecipeCategory, \
    RecipeRecipeTag
from typing import TypedDict, List


class RecipeImageDTO(TypedDict):
    id: int
    image: str


class RecipeCategoryDTO(TypedDict):
    id: int
    title: str


class RecipeTagDTO(TypedDict):
    id: int
    title: str


class IngredientDTO(TypedDict):
    id: int
    title: str
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
    title: str
    date_create: str
    cooking_time: str
    image: RecipeImageDTO
    categories: List[RecipeCategoryDTO]
    tags: List[RecipeTagDTO]
    stages: List[StageDTO]


class RecipeSimpleDTO(TypedDict):
    id: int
    title: str
    date_create: str
    cooking_time: str
    image: RecipeImageDTO
    categories: List[RecipeCategoryDTO]
    tags: List[RecipeTagDTO]


def getRecipeDTO(recipe):
    # categoires
    categories_list = []
    for recipeRecipeCategoryObject in RecipeRecipeCategory.objects.filter(recipe=recipe):
        categories_list.append(getCategoryDTO(recipeRecipeCategoryObject.category))
    # tags
    tags_list = []
    for recipeRecipeTagObject in RecipeRecipeTag.objects.filter(recipe=recipe):
        tags_list.append(getTagDTO(recipeRecipeTagObject.tag))
    # stages
    stages_list = []
    for recipeStageObject in RecipeStage.objects.filter(recipe=recipe):
        stages_list.append(getStageDTO(recipeStageObject))
    recipe = RecipeDTO(
        id=recipe.id,
        title=recipe.title,
        date_create=recipe.date_create,
        cooking_time=recipe.cooking_time,
        image=getRecipeImageDTO(recipe.image),
        categories=categories_list,
        tags = tags_list,
        stages=stages_list
    )
    return recipe


def getRecipeSimpleDTO(recipe):
    # categoires
    categories_list = []
    for recipeRecipeCategoryObject in RecipeRecipeCategory.objects.filter(recipe=recipe):
        categories_list.append(getCategoryDTO(recipeRecipeCategoryObject.category))
    # tags
    tags_list = []
    for recipeRecipeTagObject in RecipeRecipeTag.objects.filter(recipe=recipe):
        tags_list.append(getTagDTO(recipeRecipeTagObject.tag))
    recipe = RecipeSimpleDTO(
        id=recipe.id,
        title=recipe.title,
        date_create=recipe.date_create,
        cooking_time=recipe.cooking_time,
        image=getRecipeImageDTO(recipe.image),
        categories=categories_list,
        tags=tags_list
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
        title=category.title
    )
    return category


def getTagDTO(tag):
    tag = RecipeTagDTO(
        id=tag.id,
        title=tag.title
    )
    return tag


def getIngredientDTO(ingredient):
    ingredient = IngredientDTO(
        id=ingredient.id,
        title=ingredient.title,
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
