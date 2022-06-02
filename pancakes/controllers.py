from pancakes.models import RecipeIngredient, RecipeImage, RecipeStageRecipeIngredient, RecipeStage

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
        return RecipeIngredient.objects.create(title=title, unit=unit)

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
            RecipeIngredient.objects.delete(id)
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
        return RecipeImage.objects.create(image=image)

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
            RecipeImage.objects.delete(id)
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

    def create(self, stage, ingredient, amount, is_required):
        print(self.CONTROLLER_NAME, "create", stage, ingredient, amount, is_required)
        return RecipeStageRecipeIngredient.objects.create(stage=stage,
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
            RecipeStageRecipeIngredient.objects.delete(id)
            return id
        except RecipeStageRecipeIngredient.DoesNotExist:
            return None

    def valid(self, stage, ingredient, amount, is_required):
        # TODO
        return ""

    def valid_extend(self, title, unit, amount, is_required):
        if len(title)<3:
            return ERROR_TOO_SHORT.format("tytuł", 3)
        if len(unit)<1:
            return ERROR_TOO_SHORT.format("jednostka", 1)
        if len(amount)<0:
            return ERROR_IS_LESS_THAN_ZERO.format("ilość")
        return ""

    def update(self, id, stage, ingredient, amount, is_required):
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

    def add_ingredient_to_stage(self, stageObject, ingredientObject, amount, is_required):
        print(self.CONTROLLER_NAME, "add_ingredient_to_stage", stageObject, ingredientObject, amount, is_required)
        object = recipe_stage_recipe_ingredient_controller.create_and_save(stage=stageObject,
                                                                           ingredient=ingredientObject,
                                                                           amount=amount,
                                                                           is_required=is_required)

    def create(self, recipe, cooking_time, description, image):
        print(self.CONTROLLER_NAME, "create", recipe, cooking_time, description, image)
        return RecipeStage.objects.create(recipe=recipe,
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
            return None

    def delete(self, id):
        print(self.CONTROLLER_NAME, "delete", id)
        try:
            RecipeStage.objects.delete(id)
            return id
        except RecipeStage.DoesNotExist:
            return None

    def valid(self, recipe, cooking_time, description, image):
        # TODO valid recipe
        if int(cooking_time) < 0:
            return ERROR_IS_LESS_THAN_ZERO.format("czas gotowania")
        if len(description) < 3:
            return ERROR_TOO_SHORT.format("opis", 3)
        return ""

    def update(self, id, recipe, cooking_time, description, image):
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


recipe_ingredient_controller = RecipeIngredientController()
recipe_image_controller = RecipeImageController()
recipe_stage_recipe_ingredient_controller = RecipeStageRecipeIngredientController()
recipe_stage_controller = RecipeStageController()
