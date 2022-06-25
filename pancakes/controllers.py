from .models import RecipeIngredient, RecipeImage, RecipeStageRecipeIngredient, RecipeStage, Recipe, \
    RecipeCategory, RecipeTag, RecipeRecipeCategory, RecipeRecipeTag
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
