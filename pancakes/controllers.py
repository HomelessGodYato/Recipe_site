import re
from django.utils.timezone import now
from .models import RecipeIngredient, RecipeImage, RecipeStageRecipeIngredient, RecipeStage, Recipe, \
    RecipeCategory, RecipeTag, RecipeRecipeCategory, RecipeRecipeTag, Article, ArticleComment, ArticleImage
from .constant import *

SHOW_LOGGING = False


class RecipeIngredientController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeIngredientController"
        self.TITLE_MIN_LENGTH = 3
        self.TITLE_MAX_LENGTH = 254
        self.UNIT_MIN_LENGTH = 1
        self.UNIT_MAX_LENGTH = 254
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            return {
                ID: object.id,
                TITLE: object.title,
                UNIT: object.unit
            }
        else:
            return None

    def create(self, title, unit):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create", title, unit)
        return RecipeIngredient(title=title, unit=unit, status=RECIPE_INGREDIENT_STATUS_DRAFT)

    def create_and_save(self, title, unit):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create_and_save", title, unit)
        object = self.create(title=title, unit=unit)
        object = self.save(object)
        return object

    def save(self, object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "save", object)
        object.save()
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "all")
        return RecipeIngredient.objects.all()

    def find_one_by_id(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeIngredient.objects.get(id=id)
            return object
        except RecipeIngredient.DoesNotExist:
            return None

    def find_one_by_title_and_unit(self, title, unit):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_title_and_unit", title, unit)
        try:
            objects_set = RecipeIngredient.objects.filter(title=title, unit=unit)
            if len(objects_set) > 0:
                return objects_set[0]
            else:
                return None
        except RecipeIngredient.DoesNotExist:
            return None

    def delete(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeIngredient.objects.get(id=id)
            object.delete()
            return id
        except RecipeIngredient.DoesNotExist:
            return None

    def valid(self, title, unit):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid", title, unit)
        if len(title) < self.TITLE_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("tytuł", self.TITLE_MIN_LENGTH)
        if len(title) > self.TITLE_MAX_LENGTH:
            return ERROR_TOO_LONG.format("tytuł", self.TITLE_MAX_LENGTH)
        if len(unit) < self.UNIT_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("jednostka", self.UNIT_MIN_LENGTH)
        if len(unit) > self.UNIT_MAX_LENGTH:
            return ERROR_TOO_LONG.format("jednostka", self.UNIT_MAX_LENGTH)
        return ""

    def update(self, id, title, unit):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update", id, title, unit)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.title = title
            object.unit = unit
            object.status = RECIPE_INGREDIENT_STATUS_DRAFT
            self.save(object)
            return object
        else:
            return None

    def set_status(self, object, status):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "set_status", object, status)
        if object is not None:
            if status == RECIPE_INGREDIENT_STATUS_DRAFT:
                object.status = RECIPE_INGREDIENT_STATUS_DRAFT
            elif status == RECIPE_INGREDIENT_STATUS_APPROVED:
                object.status = RECIPE_INGREDIENT_STATUS_APPROVED
            self.save(object)
            return object
        else:
            return None


class RecipeImageController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeImageController"
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            return {
                ID: object.id,
                IMAGE: object.image
            }
        else:
            return None

    def create(self, image):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create", image)
        return RecipeImage(image=image)

    def create_and_save(self, image):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create_and_save", image)
        object = self.create(image=image)
        object = self.save(object)
        return object

    def save(self, object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "save", object)
        object.save()
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "all")
        return RecipeImage.objects.all()

    def find_one_by_id(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeImage.objects.get(id=id)
            return object
        except RecipeImage.DoesNotExist:
            return None

    def delete(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeImage.objects.get(id=id)
            object.delete()
            return id
        except RecipeImage.DoesNotExist:
            return None

    def valid(self, image):  # TODO
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid", image)
        return ""

    def update(self, id, image):  # TODO
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update", id, image)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.image = image
            self.save(object)
            return object
        else:
            return None


class RecipeCategoryController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeCategoryController"
        self.CATEGORY_MIN_LENGTH = 3
        self.CATEGORY_MAX_LENGTH = 254
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            return {
                ID: object.id,
                TITLE: object.title
            }
        else:
            return None

    def create(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create", title)
        return RecipeCategory(title=title)

    def create_and_save(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create_and_save", title)
        object = self.create(title=title)
        object = self.save(object)
        return object

    def save(self, object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "save", object)
        object.save()
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "all")
        return RecipeCategory.objects.all()

    def find_one_by_id(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeCategory.objects.get(id=id)
            return object
        except RecipeCategory.DoesNotExist:
            return None

    def find_one_by_title(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_title", title)
        try:
            objects_set = RecipeCategory.objects.filter(title=title)
            if len(objects_set) > 0:
                return objects_set[0]
            else:
                return None
        except RecipeCategory.DoesNotExist:
            return None

    def find_all_by_recipe(self, recipe_object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_recipe", recipe_object)
        try:
            objects_set = []
            associative_objects_set = RecipeRecipeCategory.objects.filter(recipe=recipe_object)
            for associative_object in associative_objects_set:
                category_object = self.find_one_by_id(id=associative_object.category.id)
                objects_set.append(category_object)
            return objects_set
        except RecipeRecipeCategory.DoesNotExist:
            return None

    def delete(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeCategory.objects.get(id=id)
            object.delete()
            return id
        except RecipeCategory.DoesNotExist:
            return None

    def valid(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid", title)
        if len(title) < self.CATEGORY_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("tytuł", self.CATEGORY_MIN_LENGTH)
        if len(title) > self.CATEGORY_MAX_LENGTH:
            return ERROR_TOO_LONG.format("tytuł", self.CATEGORY_MAX_LENGTH)
        return ""

    def update(self, id, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update", id, title)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.title = title
            self.save(object)
            return object
        else:
            return None


class RecipeTagController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeTagController"
        self.TITLE_MIN_LENGTH = 3
        self.TITLE_MAX_LENGTH = 254
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            return {
                ID: object.id,
                TITLE: object.title
            }
        else:
            return None

    def create(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create", title)
        return RecipeTag(title=title)

    def create_and_save(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create_and_save", title)
        object = self.create(title=title)
        object = self.save(object)
        return object

    def save(self, object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "save", object)
        object.save()
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "all")
        return RecipeTag.objects.all()

    def find_one_by_id(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeTag.objects.get(id=id)
            return object
        except RecipeTag.DoesNotExist:
            return None

    def find_one_by_title(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_title", title)
        try:
            objects_set = RecipeTag.objects.filter(title=title)
            if len(objects_set) > 0:
                return objects_set[0]
            else:
                return None
        except RecipeTag.DoesNotExist:
            return None

    def find_all_by_recipe(self, recipe_object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_recipe", recipe_object)
        try:
            objects_set = []
            associative_objects_set = RecipeRecipeTag.objects.filter(recipe=recipe_object)
            for associative_object in associative_objects_set:
                tag_object = self.find_one_by_id(id=associative_object.tag.id)
                objects_set.append(tag_object)
            return objects_set
        except RecipeRecipeTag.DoesNotExist:
            return None

    def delete(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeTag.objects.get(id=id)
            object.delete()
            return id
        except RecipeTag.DoesNotExist:
            return None

    def valid(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid", title)
        if len(title) < self.TITLE_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("tytuł", self.TITLE_MIN_LENGTH)
        if len(title) > self.TITLE_MAX_LENGTH:
            return ERROR_TOO_LONG.format("tytuł", self.TITLE_MAX_LENGTH)
        return ""

    def update(self, id, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update", id, title)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.title = title
            self.save(object)
            return object
        else:
            return None


class RecipeStageRecipeIngredientController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeStageRecipeIngredientController"
        self.TITLE_MIN_LENGTH = 3
        self.TITLE_MAX_LENGTH = 254
        self.UNIT_MIN_LENGTH = 1
        self.UNIT_MAX_LENGTH = 254
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO_extend_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO_extend(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            return {
                ID: object.id,
                STAGE_ID: object.stage.id,
                INGREDIENT_ID: object.ingredient.id,
                AMOUNT: object.amount,
                IS_REQUIRED: object.is_required
            }
        else:
            return None

    def DTO_extend(self, object):
        if object is not None:
            return {
                ID: object.id,
                STAGE_ID: object.stage.id,
                INGREDIENT_ID: object.ingredient.id,
                TITLE: object.ingredient.title,
                UNIT: object.ingredient.unit,
                AMOUNT: object.amount,
                IS_REQUIRED: object.is_required
            }
        else:
            return None

    def DTO_extend_field(self, title, unit, amount, is_required, id=0, stage_id=0, ingredient_id=0):
        return {
            ID: id,
            STAGE_ID: stage_id,
            INGREDIENT_ID: ingredient_id,
            TITLE: title,
            UNIT: unit,
            AMOUNT: amount,
            IS_REQUIRED: is_required
        }

    def create(self, stage, ingredient, amount, is_required):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create", stage, ingredient, amount, is_required)
        return RecipeStageRecipeIngredient(stage=stage,
                                           ingredient=ingredient,
                                           amount=amount,
                                           is_required=is_required)

    def create_and_save(self, stage, ingredient, amount, is_required):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create_and_save", stage, ingredient, amount, is_required)
        object = self.create(stage, ingredient, amount, is_required)
        object = self.save(object)
        return object

    def save(self, object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "save", object)
        object.save()
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "all")
        return RecipeStageRecipeIngredient.objects.all()

    def find_one_by_id(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeStageRecipeIngredient.objects.get(id=id)
            return object
        except RecipeStageRecipeIngredient.DoesNotExist:
            return None

    def find_all_by_stage(self, stage_object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_stage", stage_object)
        try:
            objects_set = RecipeStageRecipeIngredient.objects.filter(stage=stage_object)
            return objects_set
        except RecipeStageRecipeIngredient.DoesNotExist:
            return None

    def delete(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeStageRecipeIngredient.objects.get(id=id)
            object.delete()
            return id
        except RecipeStageRecipeIngredient.DoesNotExist:
            return None

    def valid(self, stage, ingredient, amount, is_required):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid", stage, ingredient, amount, is_required)
        if amount == '' or int(amount) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("ilość")
        return ""

    def valid_extend(self, title, unit, amount, is_required):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid_extend", title, unit, amount, is_required)
        if len(title) < self.TITLE_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("tytuł", self.TITLE_MIN_LENGTH)
        if len(title) > self.TITLE_MAX_LENGTH:
            return ERROR_TOO_LONG.format("tytuł", self.TITLE_MAX_LENGTH)
        if len(unit) < self.UNIT_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("jednostka", self.UNIT_MIN_LENGTH)
        if len(unit) > self.UNIT_MAX_LENGTH:
            return ERROR_TOO_LONG.format("jednostka", self.UNIT_MAX_LENGTH)
        if int(amount) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("ilość")
        return ""

    def update(self, id, stage, ingredient, amount, is_required):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update", id, stage, ingredient, amount, is_required)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.stage = stage
            object.ingredient = ingredient
            object.amount = amount
            object.is_required = is_required
            self.save(object)
            return object
        else:
            return None


class RecipeStageController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeStageController"
        self.DESCRIPTION_MIN_LENGTH = 1
        self.DESCRIPTION_MAX_LENGTH = 8191
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            ingredients_list = recipe_stage_recipe_ingredient_controller.find_all_by_stage(object)
            ingredients_DTO_list = recipe_stage_recipe_ingredient_controller.DTO_extend_list(ingredients_list)
            return {
                ID: object.id,
                COOKING_TIME: object.cooking_time,
                DESCRIPTION: object.description,
                IMAGE: object.image,
                ORDER: object.order,
                INGREDIENTS_EXTENDED_LIST: ingredients_DTO_list,
            }
        else:
            return None

    def add_ingredient_to_stage(self, stageObject, title, unit, amount, is_required):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "add_ingredient_to_stage", stageObject, title, unit, amount,
                               is_required)
        recipe_ingredient_object = recipe_ingredient_controller. \
            find_one_by_title_and_unit(title=title,
                                       unit=unit)
        if recipe_ingredient_object is None:
            recipe_ingredient_object = recipe_ingredient_controller. \
                create_and_save(title=title,
                                unit=unit)

        object = recipe_stage_recipe_ingredient_controller.create_and_save(stage=stageObject,
                                                                           ingredient=recipe_ingredient_object,
                                                                           amount=amount,
                                                                           is_required=is_required)
        return object

    def update_ingredient_in_stage(self, id, stageObject, title, unit, amount, is_required):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update_ingredient_in_stage", id, stageObject, title, unit, amount,
                               is_required)
        recipe_ingredient_object = recipe_ingredient_controller.find_one_by_title_and_unit(title=title,
                                                                                           unit=unit)
        if recipe_ingredient_object is None:
            recipe_ingredient_object = recipe_ingredient_controller.create_and_save(title=title,
                                                                                    unit=unit)

        if int(id) == 0:  # create
            return recipe_stage_recipe_ingredient_controller.create_and_save(stage=stageObject,
                                                                             ingredient=recipe_ingredient_object,
                                                                             amount=amount,
                                                                             is_required=is_required)
        else:  # update
            return recipe_stage_recipe_ingredient_controller.update(id=id,
                                                                    stage=stageObject,
                                                                    ingredient=recipe_ingredient_object,
                                                                    amount=amount,
                                                                    is_required=is_required)

    def create(self, recipe, cooking_time, description, image, order):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create", recipe, cooking_time, description, image, order)
        return RecipeStage(recipe=recipe,
                           cooking_time=cooking_time,
                           description=description,
                           image=image,
                           order=order)

    def create_and_save(self, recipe, cooking_time, description, image, order):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create_and_save", recipe, cooking_time, description, image, order)
        object = self.create(recipe, cooking_time, description, image, order)
        object = self.save(object)
        return object

    def save(self, object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "save", object)
        object.save()
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "all")
        return RecipeStage.objects.all()

    def find_one_by_id(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeStage.objects.get(id=id)
            return object
        except RecipeStage.DoesNotExist:
            return None

    def find_one_by_recipe_and_order(self, recipe, order):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_recipe_and_order", recipe, order)
        try:
            objects_set = RecipeStage.objects.filter(recipe=recipe, order=order)
            if len(objects_set) > 0:
                return objects_set[0]
            else:
                return None
        except RecipeStage.DoesNotExist:
            return None

    def find_all_by_recipe(self, recipe):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_recipe", recipe)
        try:
            objects_set = RecipeStage.objects.filter(recipe=recipe)
            return objects_set
        except RecipeStage.DoesNotExist:
            return None

    def delete(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeStage.objects.get(id=id)
            object.delete()
            return id
        except RecipeStage.DoesNotExist:
            return None

    def valid(self, recipe, cooking_time, description, image, order):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid", recipe, cooking_time, description, image, order)
        if cooking_time == '' or int(cooking_time) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("czas gotowania")
        if len(description) < self.DESCRIPTION_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("opis", self.DESCRIPTION_MIN_LENGTH)
        if len(description) > self.DESCRIPTION_MAX_LENGTH:
            return ERROR_TOO_LONG.format("opis", self.DESCRIPTION_MAX_LENGTH)
        return ""

    def update(self, id, recipe, cooking_time, description, image, order):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update", id, recipe, cooking_time, description, image, order)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.recipe = recipe
            object.cooking_time = cooking_time
            object.description = description
            object.image = image
            object.order = order
            self.save(object)
            return object
        else:
            return None


class RecipeController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeController"
        self.TITLE_MIN_LENGTH = 3
        self.TITLE_MAX_LENGTH = 254
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            stages_list = recipe_stage_controller.find_all_by_recipe(recipe=object)
            tags_list = recipe_tag_controller.find_all_by_recipe(recipe_object=object)
            categories_list = recipe_category_controller.find_all_by_recipe(recipe_object=object)
            return {
                ID: object.id,
                AUTHOR: object.author,
                TITLE: object.title,
                COOKING_TIME: object.cooking_time,
                DATA_CREATE: object.date_create,
                IMAGE: object.image,
                STATUS: object.status,
                CATEGORIES_LIST: recipe_category_controller.DTO_list(categories_list),
                TAGS_LIST: recipe_category_controller.DTO_list(tags_list),
                STAGES_LIST: recipe_stage_controller.DTO_list(stages_list),
            }
        else:
            return None

    def create(self, author, title, cooking_time, date_create, image):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create", author, title, cooking_time, date_create, image)
        return Recipe(author=author,
                      title=title,
                      cooking_time=cooking_time,
                      date_create=date_create,
                      image=image,
                      status=RECIPE_STATUS_DRAFT)

    def create_and_save(self, author, title, cooking_time, date_create, image):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "create_and_save", author, title, cooking_time, date_create, image)
        object = self.create(author, title, cooking_time, date_create, image)
        object = self.save(object)
        return object

    def save(self, object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "save", object)
        object.save()
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "all")
        return Recipe.objects.all()

    def find_all_by_category(self, category_object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_category", category_object)
        try:
            objects_set = []
            associative_objects_set = RecipeRecipeCategory.objects.filter(category=category_object)
            for associative_object in associative_objects_set:
                recipe_object = self.find_one_by_id(id=associative_object.recipe.id)
                objects_set.append(recipe_object)
            return objects_set
        except RecipeRecipeTag.DoesNotExist:
            return None

    def find_all_by_tag(self, tag_object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_tag", tag_object)
        try:
            objects_set = []
            associative_objects_set = RecipeRecipeTag.objects.filter(tag=tag_object)
            for associative_object in associative_objects_set:
                recipe_object = self.find_one_by_id(id=associative_object.recipe.id)
                objects_set.append(recipe_object)
            return objects_set
        except RecipeRecipeTag.DoesNotExist:
            return None

    def find_all_by_title(self, title):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_title", title.lower())
        try:
            objects_set = Recipe.objects.filter(title__icontains=title.lower())
            return objects_set
        except Recipe.DoesNotExist:
            return None

    def find_all_by_user(self, user):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_all_by_user", user)
        try:
            objects_set = Recipe.objects.filter(author=user)
            return objects_set
        except Recipe.DoesNotExist:
            return None


    def find_one_by_id(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = Recipe.objects.get(id=id)
            return object
        except Recipe.DoesNotExist:
            if SHOW_LOGGING: print(self.CONTROLLER_NAME, "find_one_by_id return NONE", )
            return None

    def delete(self, id):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = Recipe.objects.get(id=id)
            object.delete()
            return id
        except Recipe.DoesNotExist:
            return None

    def valid(self, author, title, cooking_time, date_create, image):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "valid", author, title, cooking_time, date_create, image)
        if len(title) < self.TITLE_MIN_LENGTH:
            return ERROR_TOO_SHORT.format("tytuł", self.TITLE_MIN_LENGTH)
        if len(title) > self.TITLE_MAX_LENGTH:
            return ERROR_TOO_LONG.format("tytuł", self.TITLE_MAX_LENGTH)
        if cooking_time == '' or int(cooking_time) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("czas gotowania")
        return ""

    def update(self, id, author, title, cooking_time, image):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "update", id, author, title, cooking_time, image)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.author = author
            object.title = title
            object.cooking_time = cooking_time
            object.image = image
            self.save(object)
            return object
        else:
            return None

    def add_category_to_recipe(self, recipeObject, categoryObject):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "add_category_to_recipe", recipeObject, categoryObject)
        RecipeRecipeCategory.objects.create(recipe=recipeObject, category=categoryObject)

    def add_tag_to_recipe(self, recipeObject, tagObject):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "add_tag_to_recipe", recipeObject, tagObject)
        RecipeRecipeTag.objects.create(recipe=recipeObject, tag=tagObject)

    def set_categories_to_recipe(self, recipe_object, categories_objects_list):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "set_categories_to_recipe", recipe_object, categories_objects_list)
        for object in categories_objects_list:
            RecipeRecipeCategory.objects.create(recipe=recipe_object, category=object)

    def remove_all_categories_from_recipe(self, recipe_object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "remove_all_categories_from_recipe", recipe_object)
        objects_set = recipe_category_controller.find_all_by_recipe(recipe_object)
        for object in objects_set:
            associative_objects_set = RecipeRecipeCategory.objects.filter(recipe=recipe_object, category=object)
            for associative_object in associative_objects_set:
                associative_object.delete()

    def set_tags_to_recipe(self, recipe_object, tags_objects_list):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "set_tags_to_recipe", recipe_object, tags_objects_list)
        for object in tags_objects_list:
            RecipeRecipeTag.objects.create(recipe=recipe_object, tag=object)

    def remove_all_tags_from_recipe(self, recipe_object):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "remove_all_tags_from_recipe", recipe_object)
        objects_set = recipe_tag_controller.find_all_by_recipe(recipe_object)
        for object in objects_set:
            associative_objects_set = RecipeRecipeTag.objects.filter(recipe=recipe_object, tag=object)
            for associative_object in associative_objects_set:
                associative_object.delete()

    def set_status(self, recipe_object, status):
        if SHOW_LOGGING: print(self.CONTROLLER_NAME, "set_status", recipe_object, status)
        if recipe_object is not None:
            if status == RECIPE_STATUS_DRAFT:
                recipe_object.status = RECIPE_STATUS_DRAFT
            elif status == RECIPE_STATUS_APPROVED:
                recipe_object.status = RECIPE_STATUS_APPROVED
            self.save(recipe_object)
            return recipe_object
        else:
            return None


recipe_controller = RecipeController()
recipe_ingredient_controller = RecipeIngredientController()
recipe_tag_controller = RecipeTagController()
recipe_category_controller = RecipeCategoryController()
recipe_image_controller = RecipeImageController()
recipe_stage_recipe_ingredient_controller = RecipeStageRecipeIngredientController()
recipe_stage_controller = RecipeStageController()


# =========================================ARTICLE==============================================


class ArticleController:
    def __init__(self):
        self.CONTROLLER_NAME = "ArticleController"
        self.TITLE_MIN_LENGTH = 3
        self.TITLE_MAX_LENGTH = 254
        self.DESCRIPTION_MIN_LENGTH = 10
        self.DESCRIPTION_MAX_LENGTH = 8191

    def DTO(self, article):
        if article is not None:
            comments = ArticleComment.objects.filter(article=article, comment=None).order_by("-date_create")
            images = ArticleImage.objects.filter(article=article)

            comments_dto = article_comment_controller.DTO_list(comments)
            images_dto = article_image_controller.DTO_list(images)

            return {
                ID: article.id,
                AUTHOR: article.author,
                TITLE: article.title,
                DESCRIPTION: article.description,
                DATE_CREATE: article.date_create,
                COMMENTS: comments_dto,
                IMAGES: images_dto,
                IS_CREATOR: False
            }

        return None

    def DTO_list(self, articles):
        return [self.DTO(article) for article in articles]

    def set_is_user_creator(self, article_dto, user):
        if article_dto[AUTHOR]== user:
            article_dto[IS_CREATOR] = True

    def get_articles_by_page_number(self, page_nr, posts_count_per_page):
        return Article.objects.all().order_by('-date_create')[
               (page_nr - 1) * posts_count_per_page:page_nr * posts_count_per_page]

    def get_articles_by_search_phrase(self, phrase):
        articles = Article.objects.all().order_by('-date_create')

        search_phrase = f".*{phrase}.*"
        matching_articles = [article for article in articles
                             if re.search(search_phrase, article.title.lower())
                             or re.search(search_phrase, article.description.lower())]

        articles_dtos = self.DTO_list(matching_articles)
        return articles_dtos

    def get_article_by_id(self, id):
        return Article.objects.get(id=id)

    def get_articles_by_user(self, user):
        return Article.objects.filter(author=user).order_by('-date_create')

    def get_count_of_all_articles(self):
        return len(Article.objects.all())

    def save_article_from_the_form(self, article_form_object, user, images):
        article = article_form_object.save(commit=False)
        article.author = user
        article.date_create = now()
        article.save()

        article_image_controller.save_images_from_the_form(article, images)


class ArticleImageController:
    def __init__(self):
        self.CONTROLLER_NAME = "ArticleImageController"
        self.IMAGES_MAX_COUNT = 6

    def DTO(self, image):
        if image is not None:

            return {
                ID: image.id,
                ARTICLE: image.article,
                IMAGE: image.image
            }

        return None

    def DTO_list(self, images):
        return [self.DTO(image) for image in images]

    def get_images_by_article(self, article):
        return ArticleImage.objects.filter(article=article)

    def save_images_from_the_form(self, article, images):
        for image in images:
            ArticleImage.objects.create(article=article, image=image)


class ArticleCommentController:
    def __init__(self):
        self.CONTROLLER_NAME = "ArticleCommentController"
        self.DESCRIPTION_MIN_LENGTH = 10
        self.DESCRIPTION_MAX_LENGTH = 8191

    def DTO(self, comment):
        if comment is not None:
            sub_comments = ArticleComment.objects.filter(comment=comment).order_by("-date_create")
            sub_comments_dto = self.DTO_list(sub_comments)

            return {
                ID: comment.id,
                AUTHOR: comment.author,
                DESCRIPTION: comment.description,
                DATE_CREATE: comment.date_create,
                SUB_COMMENTS: sub_comments_dto,
                SUB_COMMENTS_COUNT: len(sub_comments_dto),
                IS_CREATOR: False
            }

        return None

    def DTO_list(self, comments):
        return [self.DTO(comment) for comment in comments]

    def set_is_user_creator(self, comments_dtos, user):
        for comment_dto in comments_dtos:
            if comment_dto[AUTHOR] == user:
                comment_dto[IS_CREATOR] = True
            if article_comment_controller.has_sub_comments(comment_dto):
                self.set_is_user_creator(comment_dto[SUB_COMMENTS], user)

    def has_sub_comments(self, comment_dto):
        return len(comment_dto[SUB_COMMENTS]) != 0

    def get_comment_by_id(self, id):
        return ArticleComment.objects.get(id=id)

    def save_comment_from_the_form(self, comment_form_object, user, article, parent_comment):
        comment = comment_form_object.save(commit=False)
        comment.article = article
        comment.author = user
        comment.comment = parent_comment
        comment.date_create = now()
        comment.save()


article_controller = ArticleController()
article_image_controller = ArticleImageController()
article_comment_controller = ArticleCommentController()