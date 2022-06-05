from pancakes.models import RecipeIngredient, RecipeImage, RecipeStageRecipeIngredient, RecipeStage, Recipe

ERROR_TOO_SHORT = "{} musi mieć przynajmniej {} znaki"
ERROR_IS_LESS_THAN_ZERO = "{} musi być dodatnie"


class RecipeIngredientController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeIngredientController"
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            return {
                "id": object.id,
                "title": object.title,
                "unit": object.unit
            }
        else:
            return None

    def create(self, title, unit):
        print(self.CONTROLLER_NAME, "create", title, unit)
        return RecipeIngredient(title=title, unit=unit)

    def create_and_save(self, title, unit):
        print(self.CONTROLLER_NAME, "create_and_save", title, unit)
        object = self.create(title=title, unit=unit)
        object = self.save(object)
        return object

    def save(self, object):
        print(self.CONTROLLER_NAME, "save", object)
        object.save()
        print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        print(self.CONTROLLER_NAME, "all")
        return RecipeIngredient.objects.all()

    def find_one_by_id(self, id):
        print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeIngredient.objects.get(id=id)
            return object
        except RecipeIngredient.DoesNotExist:
            return None

    def find_one_by_title_and_unit(self, title, unit):
        print(self.CONTROLLER_NAME, "find_one_by_title_and_unit", title, unit)
        try:
            objects_set = RecipeIngredient.objects.filter(title=title, unit=unit)
            if len(objects_set) > 0:
                return objects_set[0]
            else:
                return None
        except RecipeIngredient.DoesNotExist:
            return None

    def delete(self, id):
        print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeIngredient.objects.get(id=id)
            object.delete()
            return id
        except RecipeIngredient.DoesNotExist:
            return None

    def valid(self, title, unit):
        if len(title) < 3:
            return ERROR_TOO_SHORT.format("tytuł", 3)
        elif len(unit) < 1:
            return ERROR_TOO_SHORT.format("jednostak", 1)
        return ""

    def update(self, id, title, unit):
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.title = title
            object.unit = unit
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
                "id": object.id,
                "image": object.image
            }
        else:
            return None

    def create(self, image):
        print(self.CONTROLLER_NAME, "create", image)
        return RecipeImage(image=image)

    def create_and_save(self, image):
        print(self.CONTROLLER_NAME, "create_and_save", image)
        object = self.create(image=image)
        object = self.save(object)
        return object

    def save(self, object):
        print(self.CONTROLLER_NAME, "save", object)
        object.save()
        print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        print(self.CONTROLLER_NAME, "all")
        return RecipeImage.objects.all()

    def find_one_by_id(self, id):
        print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeImage.objects.get(id=id)
            return object
        except RecipeImage.DoesNotExist:
            return None

    def delete(self, id):
        print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeImage.objects.get(id=id)
            object.delete()
            return id
        except RecipeImage.DoesNotExist:
            return None

    def valid(self, image):
        return ""

    def update(self, id, image):  # TODO nie wiem czy działa
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.image = image
            self.save(object)
            return object
        else:
            return None


class RecipeStageRecipeIngredientController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeStageRecipeIngredientController"
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
                "id": object.id,
                "stage_id": object.stage.id,
                "ingredient_id": object.ingredient.id,
                "amount": object.amount,
                "is_required": object.is_required
            }
        else:
            return None

    def DTO_extend(self, object):
        if object is not None:
            return {
                "id": object.id,
                "stage_id": object.stage.id,
                "ingredient_id": object.ingredient.id,
                "title": object.ingredient.title,
                "unit": object.ingredient.unit,
                "amount": object.amount,
                "is_required": object.is_required
            }
        else:
            return None

    def DTO_extend_field(self, title, unit, amount, is_required, id=0, stage_id=0, ingredient_id=0):
        return {
            "id": id,
            "stage_id": stage_id,
            "ingredient_id": ingredient_id,
            "title": title,
            "unit": unit,
            "amount": amount,
            "is_required": is_required
        }

    def create(self, stage, ingredient, amount, is_required):
        print(self.CONTROLLER_NAME, "create", stage, ingredient, amount, is_required)
        return RecipeStageRecipeIngredient(stage=stage,
                                           ingredient=ingredient,
                                           amount=amount,
                                           is_required=is_required)

    def create_and_save(self, stage, ingredient, amount, is_required):
        print(self.CONTROLLER_NAME, "create_and_save", stage, ingredient, amount, is_required)
        object = self.create(stage, ingredient, amount, is_required)
        object = self.save(object)
        return object

    def save(self, object):
        print(self.CONTROLLER_NAME, "save", object)
        object.save()
        print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        print(self.CONTROLLER_NAME, "all")
        return RecipeStageRecipeIngredient.objects.all()

    def find_one_by_id(self, id):
        print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeStageRecipeIngredient.objects.get(id=id)
            return object
        except RecipeStageRecipeIngredient.DoesNotExist:
            return None

    def find_all_by_stage(self, stage):
        print(self.CONTROLLER_NAME, "find_all_by_stage", stage)
        try:
            objects_set = RecipeStageRecipeIngredient.objects.filter(stage=stage)
            return objects_set
        except RecipeStageRecipeIngredient.DoesNotExist:
            return None

    def delete(self, id):
        print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeStageRecipeIngredient.objects.get(id=id)
            object.delete()
            return id
        except RecipeStageRecipeIngredient.DoesNotExist:
            return None

    def valid(self, stage, ingredient, amount, is_required):
        print(self.CONTROLLER_NAME, "valid", stage, ingredient, amount, is_required)
        # TODO
        return ""

    def valid_extend(self, title, unit, amount, is_required):
        print(self.CONTROLLER_NAME, "valid_extend", title, unit, amount, is_required)
        if len(title) < 3:
            return ERROR_TOO_SHORT.format("tytuł", 3)
        if len(unit) < 1:
            return ERROR_TOO_SHORT.format("jednostka", 1)
        if len(amount) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("ilość")
        return ""

    def update(self, id, stage, ingredient, amount, is_required):
        print(self.CONTROLLER_NAME, "update", id, stage, ingredient, amount, is_required)
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
                "id": object.id,
                "cooking_time": object.cooking_time,
                "description": object.description,
                "image": object.image,
                "ingredients_extended_list": ingredients_DTO_list,
            }
        else:
            return None

    def add_ingredient_to_stage(self, stageObject, title, unit, amount, is_required):
        print(self.CONTROLLER_NAME, "add_ingredient_to_stage", stageObject, title, unit, amount, is_required)
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
        print(self.CONTROLLER_NAME, "update_ingredient_in_stage", id, stageObject, title, unit, amount, is_required)
        recipe_ingredient_object = recipe_ingredient_controller.find_one_by_title_and_unit(title=title,
                                                                                           unit=unit)
        if recipe_ingredient_object is None:
            recipe_ingredient_object = recipe_ingredient_controller.create_and_save(title=title,
                                                                                    unit=unit)
        if id == 0:  # create
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

    def create(self, recipe, cooking_time, description, image):
        print(self.CONTROLLER_NAME, "create", recipe, cooking_time, description, image)
        return RecipeStage(recipe=recipe,
                           cooking_time=cooking_time,
                           description=description,
                           image=image)

    def create_and_save(self, recipe, cooking_time, description, image):
        print(self.CONTROLLER_NAME, "create_and_save", recipe, cooking_time, description, image)
        object = self.create(recipe, cooking_time, description, image)
        object = self.save(object)
        return object

    def save(self, object):
        print(self.CONTROLLER_NAME, "save", object)
        object.save()
        print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        print(self.CONTROLLER_NAME, "all")
        return RecipeStage.objects.all()

    def find_one_by_id(self, id):
        print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = RecipeStage.objects.get(id=id)
            return object
        except RecipeStage.DoesNotExist:
            print(self.CONTROLLER_NAME, "find_one_by_id return NONE", )
            return None

    def delete(self, id):
        print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = RecipeStage.objects.get(id=id)
            object.delete()
            return id
        except RecipeStage.DoesNotExist:
            return None

    def valid(self, recipe, cooking_time, description, image):
        print(self.CONTROLLER_NAME, "valid", recipe, cooking_time, description, image)
        # TODO valid recipe
        if int(cooking_time) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("czas gotowania")
        if len(description) < 3:
            return ERROR_TOO_SHORT.format("opis", 3)
        return ""

    def update(self, id, recipe, cooking_time, description, image):
        print(self.CONTROLLER_NAME, "update", id, recipe, cooking_time, description, image)
        object = self.find_one_by_id(id=id)
        if object is not None:
            object.recipe = recipe
            object.cooking_time = cooking_time
            object.description = description
            object.image = image
            self.save(object)
            return object
        else:
            return None


class RecipeController:
    def __init__(self):
        self.CONTROLLER_NAME = "RecipeController"
        pass

    def DTO_list(self, list):
        object_DTO_list = []
        for object in list:
            object_DTO_list.append(self.DTO(object))
        return object_DTO_list

    def DTO(self, object):
        if object is not None:
            # ingredients_list = recipe_stage_recipe_ingredient_controller.find_all_by_stage(object)
            # ingredients_DTO_list = recipe_stage_recipe_ingredient_controller.DTO_extend_list(ingredients_list)
            # recipe_stage_controller.find_all_by_recipe() #TODO
            return {
                "id": object.id,
                "author": object.author,
                "title": object.title,
                "cooking_time": object.cooking_time,
                "date_create": object.date_create,
                "image": object.image,
                "categories": [],  # TODO
                "tags": [],  # TODO
                "stages_list": [],  # TODO
            }
        else:
            return None

    def create(self, author, title, cooking_time, date_create, image, stages_list=[], categories=[], tags=[]):
        print(self.CONTROLLER_NAME, "create", author, title, cooking_time, date_create, image, stages_list, categories,
              tags)
        object = Recipe(author=author,
                        title=title,
                        cooking_time=cooking_time,
                        date_create=date_create,
                        image=image)
        # TODO
        return object

    def create_and_save(self, author, title, cooking_time, date_create, image, stages_list=[], categories=[], tags=[]):
        print(self.CONTROLLER_NAME, "create_and_save", author, title, cooking_time, date_create, image, stages_list,
              categories, tags)
        object = self.create(author, title, cooking_time, date_create, image, stages_list=[], categories=[], tags=[])
        object = self.save(object)
        return object

    def save(self, object):
        print(self.CONTROLLER_NAME, "save", object)
        object.save()
        print(self.CONTROLLER_NAME, "afrer save", object)
        return object

    def all(self):
        print(self.CONTROLLER_NAME, "all")
        return RecipeStage.objects.all()

    def find_one_by_id(self, id):
        print(self.CONTROLLER_NAME, "find_one_by_id", id)
        try:
            object = Recipe.objects.get(id=id)
            return object
        except Recipe.DoesNotExist:
            print(self.CONTROLLER_NAME, "find_one_by_id return NONE", )
            return None

    def delete(self, id):
        print(self.CONTROLLER_NAME, "delete", id)
        try:
            object = Recipe.objects.get(id=id)
            object.delete()
            return id
        except Recipe.DoesNotExist:
            return None

    def valid(self, author, title, cooking_time, date_create, image, stages_list=[], categories=[], tags=[]):
        print(self.CONTROLLER_NAME, "valid", author, title, cooking_time, date_create, image, stages_list, categories,
              tags)
        # TODO
        if int(cooking_time) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("czas gotowania")
        if len(title) < 3:
            return ERROR_TOO_SHORT.format("tytuł", 3)
        return ""

    def update(self, id, author, title, cooking_time, date_create, image, stages_list=[], categories=[], tags=[]):
        print(self.CONTROLLER_NAME, "update", id, author, title, cooking_time, date_create, image, stages_list,
              categories, tags)
        # TODO
        # object = self.find_one_by_id(id=id)
        # if object is not None:
        #     object.recipe = recipe
        #     object.cooking_time = cooking_time
        #     object.description = description
        #     object.image = image
        #     self.save(object)
        #     return object
        # else:
        #     return None


recipe_controller = RecipeController()
recipe_ingredient_controller = RecipeIngredientController()
recipe_image_controller = RecipeImageController()
recipe_stage_recipe_ingredient_controller = RecipeStageRecipeIngredientController()
recipe_stage_controller = RecipeStageController()
