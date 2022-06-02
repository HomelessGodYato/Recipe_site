from pancakes.models import RecipeIngredient

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
