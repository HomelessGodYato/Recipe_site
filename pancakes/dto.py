from pancakes.models import RecipeRecipeCategory, RecipeStage, Ingredient


def getRecipeSimpleDTO(recipe):
    categories_list = []
    for iter in RecipeRecipeCategory.objects.filter(recipe=recipe):
        categories_list.append(getCategoryDTO(iter))
    recipe = {
        "id": recipe.id,
        "name": recipe.name,
        "date_create": recipe.date_create,
        "cooking_time": recipe.cooking_time,
        "image": recipe.image,
        "categories": categories_list,
    }
    return recipe


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
    recipe = {
        "id": recipe.id,
        "name": recipe.name,
        "date_create": recipe.date_create,
        "cooking_time": recipe.cooking_time,
        "image": recipe.image,
        "categories": categories_list,
        "stages": stages_list
    }
    return recipe


def getStageDTO(stage):
    ingredient_list = []
    for iter in Ingredient.objects.filter(recipe_stage=stage):
        ingredient_list.append(getIngredientDTO(iter))
    stage = {
        "id": stage.id,
        "cooking_time": stage.cooking_time,
        "description": stage.description,
        "image": stage.image,
        "ingredients": ingredient_list,
    }
    return stage


def getCategoryDTO(category):
    category = {
        "id": category.id,
        "name": category.name.name
    }
    return category


def getIngredientDTO(ingredient):
    ingredient = {
        "id": ingredient.id,
        "name": ingredient.name,
        "unit": ingredient.unit,
        "amount": ingredient.amount
    }
    return ingredient
