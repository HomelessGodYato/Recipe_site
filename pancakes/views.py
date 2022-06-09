from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .controllers import RecipeIngredientController, recipe_ingredient_controller, recipe_image_controller, \
    recipe_stage_controller, recipe_stage_recipe_ingredient_controller, recipe_controller, recipe_tag_controller, \
    recipe_category_controller
from .dto import getRecipeDTO, getRecipeSimpleDTO
from .forms import CreateUserForm, RecipeForm, RecipeStageIngredientForm, RecipeFormFirst, RecipeFormStage, \
    RecipeFormLast
from .tokens import account_activation_token
from .models import Recipe, RecipeStage, RecipeIngredient, RecipeImage, RecipeCategory, RecipeRecipeCategory
from django.forms.models import modelformset_factory

from django.utils.timezone import now


def home_page(request):
    context = {"recipes": ['pancakes', 'donuts']}
    return render(request, 'home.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('user')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('registration_login/acc_activation.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
            else:
                form = CreateUserForm()
    context = {"form": form}
    return render(request, 'registration_login/register.html', context)


def activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'registration_login/registration_successful.html', {})
    else:
        return HttpResponse('Activation link is invalid!')


def login_page(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('user')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('user')  # any page you want @user_page just for test
            else:
                messages.info(request, 'Username or password is incorrect')
                return render(request, 'registration_login/login.html', context)

        return render(request, 'registration_login/login.html', context)


@login_required(login_url='login')
def user_main_page(request):
    return render(request, 'registration_login/user_main.html')


def logout_user(request):
    logout(request)
    return redirect('login')


INGREDIENT_ID = "ingredient_id_{}"
INGREDIENT_TITLE = "ingredient_title_{}"
INGREDIENT_AMOUNT = "ingredient_amount_{}"
INGREDIENT_UNIT = "ingredient_unit_{}"
INGREDIENT_IS_REQUIRED = "ingredient_is_required_{}"

ID = "id"
TITLE = "title"
UNIT = "unit"
IMAGE = "image"
AMOUNT = "amount"
IS_REQUIRED = "is_required"
COOKING_TIME = "cooking_time"
STAGE = "stage"
STAGES_LIST = "stages_list"
RECIPE = "recipe"
RECIPES_LIST = "recipes_list"
INGREDIENT = "ingredient"
DESCRIPTION = "description"
TAG = "tag"
CATEGORY = "category"

INGREDIENTS_LIST = "ingredients_list"
TAGS_LIST = "tags_list"
CATEGORIES_LIST = "categories_list"
INGREDIENTS_EXTENDED_LIST = "ingredients_extended_list"
INGREDIENTS_EXTENDED_LIST_LENGTH = "ingredients_extended_list_length"

ERROR = "error"

NUMBER_OF_INGREDIENTS_MAX = "numberOfIngredientsMax"
NUMBER_OF_INGREDIENTS_RANGE = "numberOfIngredientsRange"
numberOfIngredientsMax = 5
numberOfIngredientsRange = range(0, numberOfIngredientsMax)

ACTION = "ACTION"
ACTION_CREATE = "ACTION_CREATE"
ACTION_UPDATE = "ACTION_UPDATE"

RECIPE_FORM_STATE = "RECIPE_FORM_STATE"
RECIPE_FORM_STATE_FIRST = "RECIPE_FORM_STATE_FIRST"
RECIPE_FORM_STATE_STAGE = "RECIPE_FORM_STATE_STAGE"
RECIPE_FORM_STATE_LAST_STAGE = "RECIPE_FORM_STATE_LAST_STAGE"
RECIPE_FORM_STATE_LAST = "RECIPE_FORM_STATE_LAST"


# ======================================STAGE===================================================

def stage_show_all_view(request):
    object_list = recipe_stage_controller.all()
    context = {
        STAGES_LIST: recipe_stage_controller.DTO_list(object_list)
    }
    return render(request, 'stage/stage_show_all.html', context)


def stage_show_view(request, id):
    object = recipe_stage_controller.find_one_by_id(id)
    context = {
        STAGE: recipe_stage_controller.DTO(object)
    }
    return render(request, 'stage/stage_show.html', context)


def stage_form_view(request, id=0):
    if request.method == "POST":
        action = request.POST.get(ACTION)
        # image
        image = request.FILES.get(IMAGE)
        if image is None:
            image = 'default/default.PNG'
        error_image = recipe_image_controller.valid(image=image)
        # stage
        recipe_object = Recipe.objects.get(id=3)  # TODO
        cooking_time = request.POST.get(COOKING_TIME)
        description = request.POST.get(DESCRIPTION)
        error_stage = recipe_stage_controller.valid(recipe=recipe_object,
                                                    cooking_time=cooking_time,
                                                    description=description,
                                                    image=image)
        # ingredients
        ingredient_extended_list_validated = []
        ingredient_extended_list = []
        error_ingredient = ''
        for index in numberOfIngredientsRange:
            ingredient_id = request.POST.get(INGREDIENT_ID.format(index))
            ingredient_title = request.POST.get(INGREDIENT_TITLE.format(index))
            ingredient_amount = request.POST.get(INGREDIENT_AMOUNT.format(index))
            ingredient_unit = request.POST.get(INGREDIENT_UNIT.format(index))
            ingredient_is_require = request.POST.get(INGREDIENT_IS_REQUIRED.format(index))
            if ingredient_is_require is None:
                ingredient_is_require = False
            else:
                ingredient_is_require = True
            # print("--", ingredient_id, ingredient_title, ingredient_amount, ingredient_unit, ingredient_is_require)
            if ingredient_title != '' or ingredient_amount != '' or ingredient_unit != '':

                ingredient_extended_list.append(
                    recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                               title=ingredient_title,
                                                                               amount=ingredient_amount,
                                                                               unit=ingredient_unit,
                                                                               is_required=ingredient_is_require))
                if error_ingredient == '':
                    error_ingredient = recipe_stage_recipe_ingredient_controller.valid_extend(title=ingredient_title,
                                                                                              amount=ingredient_amount,
                                                                                              unit=ingredient_unit,
                                                                                              is_required=ingredient_is_require)
                    if error_ingredient == '':
                        ingredient_extended_list_validated.append(
                            recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                                       title=ingredient_title,
                                                                                       amount=ingredient_amount,
                                                                                       unit=ingredient_unit,
                                                                                       is_required=ingredient_is_require))

        if error_stage == "" and error_image == "" and error_ingredient == "":
            if action == ACTION_CREATE:
                print("ACTION_CREATE")
                # image
                image_object = recipe_image_controller.create_and_save(image=image)
                # stage
                stage_object = recipe_stage_controller.create_and_save(recipe=recipe_object,
                                                                       cooking_time=cooking_time,
                                                                       description=description,
                                                                       image=image_object)
                # ingredients
                for object in ingredient_extended_list_validated:
                    recipe_stage_controller.add_ingredient_to_stage(stageObject=stage_object,
                                                                    title=object.get(TITLE),
                                                                    unit=object.get(UNIT),
                                                                    amount=object.get(AMOUNT),
                                                                    is_required=object.get(IS_REQUIRED))

                return redirect("stage_show", id=stage_object.id)
            elif action == ACTION_UPDATE:
                print("ACTION_UPDATE", id)
                stage_object = recipe_stage_controller.find_one_by_id(id)
                # image
                image_object = recipe_image_controller.update(id=stage_object.image.id, image=image)
                # stage
                stage_object = recipe_stage_controller.update(id=id,
                                                              recipe=recipe_object,
                                                              cooking_time=cooking_time,
                                                              description=description,
                                                              image=image_object)
                # ingredients
                for object in ingredient_extended_list_validated:
                    recipe_stage_controller.update_ingredient_in_stage(id=object.get(ID),
                                                                       stageObject=stage_object,
                                                                       title=object.get(TITLE),
                                                                       unit=object.get(UNIT),
                                                                       amount=object.get(AMOUNT),
                                                                       is_required=object.get(IS_REQUIRED))
                return redirect("stage_show", id=id)
        else:
            # error
            error = ""
            if error_image != "":
                error = error_image
            elif error_stage != "":
                error = error_stage
            elif error_ingredient != "":
                error = error_ingredient
            context = {
                ERROR: error,
                ACTION: action,
                STAGE: {
                    COOKING_TIME: cooking_time,
                    DESCRIPTION: description,
                    IMAGE: image
                },
                INGREDIENTS_EXTENDED_LIST: ingredient_extended_list,
                INGREDIENTS_EXTENDED_LIST_LENGTH: len(ingredient_extended_list),
                NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), numberOfIngredientsMax),
            }
            return render(request, 'stage/stage_form.html', context)

    # data
    if id != 0:
        # update
        stage_object = recipe_stage_controller.find_one_by_id(id)

        ingredient_list = recipe_stage_recipe_ingredient_controller.find_all_by_stage(stage_object)
        ingredient_extended_list = recipe_stage_recipe_ingredient_controller.DTO_extend_list(ingredient_list)
        if stage_object is not None:
            stage = recipe_stage_controller.DTO(stage_object)
            print("stage", stage)
            context = {
                ACTION: ACTION_UPDATE,
                STAGE: stage,
                INGREDIENTS_EXTENDED_LIST: ingredient_extended_list,
                INGREDIENTS_EXTENDED_LIST_LENGTH: len(ingredient_extended_list),
                NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), numberOfIngredientsMax),
            }
            return render(request, 'stage/stage_form.html', context)
    # create
    context = {
        ACTION: ACTION_CREATE,
        NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
        NUMBER_OF_INGREDIENTS_RANGE: range(0, numberOfIngredientsMax),
        INGREDIENTS_EXTENDED_LIST_LENGTH: 0
    }
    return render(request, 'stage/stage_form.html', context)


# ======================================TAG===================================================

def tag_show_all_view(request):
    object_list = recipe_tag_controller.all()
    context = {
        TAGS_LIST: recipe_tag_controller.DTO_list(object_list)
    }
    return render(request, 'tag/tag_show_all.html', context)


def tag_show_view(request, id):
    object = recipe_tag_controller.find_one_by_id(id)
    context = {
        TAG: recipe_tag_controller.DTO(object)
    }
    return render(request, 'tag/tag_show.html', context)


def tag_form_view(request, id=0):
    if request.method == "POST":
        action = request.POST.get(ACTION)
        title = request.POST.get(TITLE)
        error = recipe_tag_controller.valid(title=title)
        if error == "":
            if action == ACTION_CREATE:
                print("ACTION_CREATE")
                object = recipe_tag_controller.create_and_save(title=title)
                return redirect("tag_show", id=object.id)
            elif action == ACTION_UPDATE:
                print("ACTION_UPDATE", id)
                recipe_tag_controller.update(id, title=title)
                return redirect("tag_show", id=id)
        else:
            context = {
                ERROR: error,
                TAG: {
                    TITLE: title
                }
            }
            return render(request, 'tag/tag_form.html', context)

    # data
    if id != 0:
        # update
        tagObj = recipe_tag_controller.find_one_by_id(id)
        if tagObj is not None:  # else create
            tag = recipe_tag_controller.DTO(tagObj)
            context = {
                ACTION: ACTION_UPDATE,
                TAG: tag,
            }
            return render(request, 'tag/tag_form.html', context)

    # create
    context = {
        ACTION: ACTION_CREATE
    }
    return render(request, 'tag/tag_form.html', context)


# ======================================CATEGORY===================================================

def category_show_all_view(request):
    object_list = recipe_category_controller.all()
    context = {
        CATEGORIES_LIST: recipe_category_controller.DTO_list(object_list)
    }
    return render(request, 'category/category_show_all.html', context)


def category_show_view(request, id):
    object = recipe_category_controller.find_one_by_id(id)
    context = {
        CATEGORY: recipe_category_controller.DTO(object)
    }
    return render(request, 'category/category_show.html', context)


def category_form_view(request, id=0):
    if request.method == "POST":
        action = request.POST.get(ACTION)
        title = request.POST.get(TITLE)
        error = recipe_category_controller.valid(title=title)
        if error == "":
            if action == ACTION_CREATE:
                print("ACTION_CREATE")
                object = recipe_category_controller.create_and_save(title=title)
                return redirect("category_show", id=object.id)
            elif action == ACTION_UPDATE:
                print("ACTION_UPDATE", id)
                recipe_category_controller.update(id, title=title)
                return redirect("category_show", id=id)
        else:
            context = {
                ERROR: error,
                CATEGORY: {
                    TITLE: title
                }
            }
            return render(request, 'category/category_form.html', context)

    # data
    if id != 0:
        # update
        categoryObj = recipe_category_controller.find_one_by_id(id)
        if categoryObj is not None:  # else create
            category = recipe_category_controller.DTO(categoryObj)
            context = {
                ACTION: ACTION_UPDATE,
                CATEGORY: category,
            }
            return render(request, 'category/category_form.html', context)

    # create
    context = {
        ACTION: ACTION_CREATE
    }
    return render(request, 'category/category_form.html', context)


# ======================================INGREDIENT===================================================

def ingredient_show_all_view(request):
    object_list = recipe_ingredient_controller.all()
    context = {
        INGREDIENTS_LIST: recipe_ingredient_controller.DTO_list(object_list)
    }
    return render(request, 'ingredient/ingredient_show_all.html', context)


def ingredient_show_view(request, id):
    object = recipe_ingredient_controller.find_one_by_id(id)
    context = {
        INGREDIENT: recipe_ingredient_controller.DTO(object)
    }
    return render(request, 'ingredient/ingredient_show.html', context)


def ingredient_form_view(request, id=0):
    if request.method == "POST":
        action = request.POST.get(ACTION)
        title = request.POST.get(TITLE)
        unit = request.POST.get(UNIT)
        error = recipe_ingredient_controller.valid(title=title, unit=unit)
        if error == "":
            if action == ACTION_CREATE:
                print("ACTION_CREATE")
                object = recipe_ingredient_controller.create_and_save(title=title, unit=unit)
                return redirect("ingredient_show", id=object.id)
            elif action == ACTION_UPDATE:
                print("ACTION_UPDATE", id)
                recipe_ingredient_controller.update(id, title=title, unit=unit)
                return redirect("ingredient_show", id=id)
        else:
            context = {
                ERROR: error,
                INGREDIENT: {
                    TITLE: title,
                    UNIT: unit
                }
            }
            return render(request, 'ingredient/ingredient_form.html', context)

    # data
    if id != 0:
        # update
        ingredientObj = recipe_ingredient_controller.find_one_by_id(id)
        if ingredientObj is not None:  # else create
            ingredient = recipe_ingredient_controller.DTO(ingredientObj)
            context = {
                ACTION: ACTION_UPDATE,
                INGREDIENT: ingredient,
            }
            return render(request, 'ingredient/ingredient_form.html', context)

    # create
    context = {
        ACTION: ACTION_CREATE
    }
    return render(request, 'ingredient/ingredient_form.html', context)


# ======================================recipe===================================================

def recipe_show_all_view(request):
    object_list = recipe_controller.all()
    context = {
        RECIPES_LIST: recipe_controller.DTO_list(object_list)
    }
    return render(request, 'recipe/recipe_show_all.html', context)


def recipe_show_view(request, id):
    object = recipe_controller.find_one_by_id(id)
    context = {
        RECIPE: recipe_controller.DTO(object)
    }
    return render(request, 'recipe/recipe_show.html', context)


def recipe_form_first_view(request, id=0):
    pass


def recipe_form_stage_view(request, recipe_id, id=0):
    if request.method == "POST":
        action = request.POST.get(ACTION)
        # image
        image = request.FILES.get(IMAGE)
        if image is None:
            image = 'default/default.PNG'
        error_image = recipe_image_controller.valid(image=image)
        # stage
        recipe_object = Recipe.objects.get(id=3)  # TODO
        cooking_time = request.POST.get(COOKING_TIME)
        description = request.POST.get(DESCRIPTION)
        error_stage = recipe_stage_controller.valid(recipe=recipe_object,
                                                    cooking_time=cooking_time,
                                                    description=description,
                                                    image=image)
        # ingredients
        ingredient_extended_list_validated = []
        ingredient_extended_list = []
        error_ingredient = ''
        for index in numberOfIngredientsRange:
            ingredient_id = request.POST.get(INGREDIENT_ID.format(index))
            ingredient_title = request.POST.get(INGREDIENT_TITLE.format(index))
            ingredient_amount = request.POST.get(INGREDIENT_AMOUNT.format(index))
            ingredient_unit = request.POST.get(INGREDIENT_UNIT.format(index))
            ingredient_is_require = request.POST.get(INGREDIENT_IS_REQUIRED.format(index))
            if ingredient_is_require is None:
                ingredient_is_require = False
            else:
                ingredient_is_require = True
            # print("--", ingredient_id, ingredient_title, ingredient_amount, ingredient_unit, ingredient_is_require)
            if ingredient_title != '' or ingredient_amount != '' or ingredient_unit != '':

                ingredient_extended_list.append(
                    recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                               title=ingredient_title,
                                                                               amount=ingredient_amount,
                                                                               unit=ingredient_unit,
                                                                               is_required=ingredient_is_require))
                if error_ingredient == '':
                    error_ingredient = recipe_stage_recipe_ingredient_controller.valid_extend(title=ingredient_title,
                                                                                              amount=ingredient_amount,
                                                                                              unit=ingredient_unit,
                                                                                              is_required=ingredient_is_require)
                    if error_ingredient == '':
                        ingredient_extended_list_validated.append(
                            recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                                       title=ingredient_title,
                                                                                       amount=ingredient_amount,
                                                                                       unit=ingredient_unit,
                                                                                       is_required=ingredient_is_require))

        if error_stage == "" and error_image == "" and error_ingredient == "":
            if action == ACTION_CREATE:
                print("ACTION_CREATE")
                # image
                image_object = recipe_image_controller.create_and_save(image=image)
                # stage
                stage_object = recipe_stage_controller.create_and_save(recipe=recipe_object,
                                                                       cooking_time=cooking_time,
                                                                       description=description,
                                                                       image=image_object)
                # ingredients
                for object in ingredient_extended_list_validated:
                    recipe_stage_controller.add_ingredient_to_stage(stageObject=stage_object,
                                                                    title=object.get(TITLE),
                                                                    unit=object.get(UNIT),
                                                                    amount=object.get(AMOUNT),
                                                                    is_required=object.get(IS_REQUIRED))

                return redirect("stage_show", id=stage_object.id)
            elif action == ACTION_UPDATE:
                print("ACTION_UPDATE", id)
                stage_object = recipe_stage_controller.find_one_by_id(id)
                # image
                image_object = recipe_image_controller.update(id=stage_object.image.id, image=image)
                # stage
                stage_object = recipe_stage_controller.update(id=id,
                                                              recipe=recipe_object,
                                                              cooking_time=cooking_time,
                                                              description=description,
                                                              image=image_object)
                # ingredients
                for object in ingredient_extended_list_validated:
                    recipe_stage_controller.update_ingredient_in_stage(id=object.get(ID),
                                                                       stageObject=stage_object,
                                                                       title=object.get(TITLE),
                                                                       unit=object.get(UNIT),
                                                                       amount=object.get(AMOUNT),
                                                                       is_required=object.get(IS_REQUIRED))
                return redirect("stage_show", id=id)
        else:
            # error
            error = ""
            if error_image != "":
                error = error_image
            elif error_stage != "":
                error = error_stage
            elif error_ingredient != "":
                error = error_ingredient
            context = {
                ERROR: error,
                ACTION: action,
                STAGE: {
                    COOKING_TIME: cooking_time,
                    DESCRIPTION: description,
                    IMAGE: image
                },
                INGREDIENTS_EXTENDED_LIST: ingredient_extended_list,
                INGREDIENTS_EXTENDED_LIST_LENGTH: len(ingredient_extended_list),
                NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), numberOfIngredientsMax),
            }
            return render(request, 'stage/stage_form.html', context)

    # data
    if id != 0:
        # update
        stage_object = recipe_stage_controller.find_one_by_id(id)

        ingredient_list = recipe_stage_recipe_ingredient_controller.find_all_by_stage(stage_object)
        ingredient_extended_list = recipe_stage_recipe_ingredient_controller.DTO_extend_list(ingredient_list)
        if stage_object is not None:
            stage = recipe_stage_controller.DTO(stage_object)
            print("stage", stage)
            context = {
                ACTION: ACTION_UPDATE,
                STAGE: stage,
                INGREDIENTS_EXTENDED_LIST: ingredient_extended_list,
                INGREDIENTS_EXTENDED_LIST_LENGTH: len(ingredient_extended_list),
                NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), numberOfIngredientsMax),
            }
            return render(request, 'stage/stage_form.html', context)
    # create
    context = {
        ACTION: ACTION_CREATE,
        NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
        NUMBER_OF_INGREDIENTS_RANGE: range(0, numberOfIngredientsMax),
        INGREDIENTS_EXTENDED_LIST_LENGTH: 0
    }
    return render(request, 'stage/stage_form.html', context)


def recipe_form_last_view(request, id=0):
    if request.method == "POST":
        action = request.POST.get(ACTION)
        # image
        image = request.FILES.get(IMAGE)
        if image is None:
            image = 'default/default.PNG'
        error_image = recipe_image_controller.valid(image=image)
        # recipe
        author_object = request.user
        cooking_time = request.POST.get(COOKING_TIME)
        title = request.POST.get(TITLE)
        date_create = now()

        error_recipe = recipe_controller.valid(author=author_object,
                                               title=title,
                                               cooking_time=cooking_time,
                                               date_create=date_create,
                                               image=image)

        if error_recipe == "" and error_image == "":
            if action == ACTION_CREATE:
                print("ACTION_CREATE")
                # image
                image_object = recipe_image_controller.create_and_save(image=image)
                # recipe
                recipe_object = recipe_controller.create_and_save(author=author_object,
                                                                  title=title,
                                                                  cooking_time=cooking_time,
                                                                  date_create=date_create,
                                                                  image=image_object)

                return redirect("stage_show")
            elif action == ACTION_UPDATE:
                # TODO
                return redirect("stage_show", id=id)
        else:
            # error
            error = ""
            if error_image != "":
                error = error_image
            elif error_recipe != "":
                error = error_recipe
            context = {
                ERROR: error,
                ACTION: action,
                RECIPE: {
                    TITLE: title,
                    COOKING_TIME: cooking_time,
                    IMAGE: image
                }
            }
            return render(request, 'recipe/recipe_form_first.html', context)

    # data
    if id != 0:
        pass
        # # update
        # stage_object = recipe_stage_controller.find_one_by_id(id)
        #
        # ingredient_list = recipe_stage_recipe_ingredient_controller.find_all_by_stage(stage_object)
        # ingredient_extended_list = recipe_stage_recipe_ingredient_controller.DTO_extend_list(ingredient_list)
        # if stage_object is not None:
        #     stage = recipe_stage_controller.DTO(stage_object)
        #     print("stage", stage)
        #     context = {
        #         ACTION: ACTION_UPDATE,
        #         STAGE: stage,
        #         INGREDIENTS_EXTENDED_LIST: ingredient_extended_list,
        #         INGREDIENTS_EXTENDED_LIST_LENGTH: len(ingredient_extended_list),
        #         NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
        #         NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), numberOfIngredientsMax),
        #     }
        #     return render(request, 'stage/stage_form.html', context)
    # create
    # first stage
    context = {
        ACTION: ACTION_CREATE
    }
    return render(request, 'recipe/recipe_form_first.html', context)


def recipe_form_view(request, id=0):
    print("----------------------RECIPE-------------------------")
    action = request.POST.get(ACTION)
    recipe_form_state = request.POST.get(RECIPE_FORM_STATE)
    recipe_id = request.POST.get("recipe_id")
    print("action,recipe_form_state,recipe_id", action, recipe_form_state, recipe_id)
    if recipe_form_state == RECIPE_FORM_STATE_FIRST:  # FIRST -> STAGE
        print("----------------------FIRST -> STAGE-------------------------")
        # save first and send stage
        if request.method == "POST":
            # image
            image = request.FILES.get(IMAGE)
            if image is None:
                image = 'default/default.PNG'
            error_image = recipe_image_controller.valid(image=image)
            # recipe
            author_object = request.user
            cooking_time = request.POST.get(COOKING_TIME)
            title = request.POST.get(TITLE)
            date_create = now()

            error_recipe = recipe_controller.valid(author=author_object,
                                                   title=title,
                                                   cooking_time=cooking_time,
                                                   date_create=date_create,
                                                   image=image)

            if error_recipe == "" and error_image == "":
                if action == ACTION_CREATE:
                    print("ACTION_CREATE")
                    # image
                    image_object = recipe_image_controller.create_and_save(image=image)
                    # recipe
                    recipe_object = recipe_controller.create_and_save(author=author_object,
                                                                      title=title,
                                                                      cooking_time=cooking_time,
                                                                      date_create=date_create,
                                                                      image=image_object)
                    print("recipe_object", recipe_object)
                    context = {
                        ACTION: ACTION_CREATE,
                        RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                        RECIPE_FORM_STATE_STAGE: RECIPE_FORM_STATE_STAGE,
                        RECIPE_FORM_STATE_LAST_STAGE: RECIPE_FORM_STATE_LAST_STAGE,

                        NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                        NUMBER_OF_INGREDIENTS_RANGE: range(0, numberOfIngredientsMax),
                        INGREDIENTS_EXTENDED_LIST_LENGTH: 0,

                        "recipe_id": recipe_object.id,
                    }
                    return render(request, 'recipe/recipe_form_stage.html', context)
            else:
                # error
                error = ""
                if error_image != "":
                    error = error_image
                elif error_recipe != "":
                    error = error_recipe
                context = {
                    ACTION: ACTION_CREATE,
                    RECIPE_FORM_STATE: RECIPE_FORM_STATE_FIRST,
                    ERROR: error,
                    RECIPE: {
                        TITLE: title,
                        COOKING_TIME: cooking_time,
                        IMAGE: image
                    }
                }
                return render(request, 'recipe/recipe_form_first.html', context)
        else:
            print("ERROR", "----------------------FIRST -> STAGE-------------------------")
            context = {
                ACTION: ACTION_CREATE,
                RECIPE_FORM_STATE: RECIPE_FORM_STATE_FIRST
            }
            return render(request, 'recipe/recipe_form_first.html', context)
    elif recipe_form_state == RECIPE_FORM_STATE_STAGE:
        print("----------------------STAGE -> STAGE-------------------------")
        if request.method == "POST":
            # image
            image = request.FILES.get(IMAGE)
            if image is None:
                image = 'default/default.PNG'
            error_image = recipe_image_controller.valid(image=image)
            # stage
            recipe_object = recipe_controller.find_one_by_id(id=recipe_id)
            cooking_time = request.POST.get(COOKING_TIME)
            description = request.POST.get(DESCRIPTION)
            error_stage = recipe_stage_controller.valid(recipe=recipe_object,
                                                        cooking_time=cooking_time,
                                                        description=description,
                                                        image=image)
            # ingredients
            ingredient_extended_list_validated = []
            ingredient_extended_list = []
            error_ingredient = ''
            for index in numberOfIngredientsRange:
                ingredient_id = request.POST.get(INGREDIENT_ID.format(index))
                ingredient_title = request.POST.get(INGREDIENT_TITLE.format(index))
                ingredient_amount = request.POST.get(INGREDIENT_AMOUNT.format(index))
                ingredient_unit = request.POST.get(INGREDIENT_UNIT.format(index))
                ingredient_is_require = request.POST.get(INGREDIENT_IS_REQUIRED.format(index))
                if ingredient_is_require is None:
                    ingredient_is_require = False
                else:
                    ingredient_is_require = True
                # print("--", ingredient_id, ingredient_title, ingredient_amount, ingredient_unit, ingredient_is_require)
                if ingredient_title != '' or ingredient_amount != '' or ingredient_unit != '':

                    ingredient_extended_list.append(
                        recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                                   title=ingredient_title,
                                                                                   amount=ingredient_amount,
                                                                                   unit=ingredient_unit,
                                                                                   is_required=ingredient_is_require))
                    if error_ingredient == '':
                        error_ingredient = recipe_stage_recipe_ingredient_controller.valid_extend(
                            title=ingredient_title,
                            amount=ingredient_amount,
                            unit=ingredient_unit,
                            is_required=ingredient_is_require)
                        if error_ingredient == '':
                            ingredient_extended_list_validated.append(
                                recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                                           title=ingredient_title,
                                                                                           amount=ingredient_amount,
                                                                                           unit=ingredient_unit,
                                                                                           is_required=ingredient_is_require))

            if error_stage == "" and error_image == "" and error_ingredient == "":
                if action == ACTION_CREATE:
                    print("ACTION_CREATE")
                    # image
                    image_object = recipe_image_controller.create_and_save(image=image)
                    # stage
                    stage_object = recipe_stage_controller.create_and_save(recipe=recipe_object,
                                                                           cooking_time=cooking_time,
                                                                           description=description,
                                                                           image=image_object)
                    # ingredients
                    for object in ingredient_extended_list_validated:
                        recipe_stage_controller.add_ingredient_to_stage(stageObject=stage_object,
                                                                        title=object.get(TITLE),
                                                                        unit=object.get(UNIT),
                                                                        amount=object.get(AMOUNT),
                                                                        is_required=object.get(IS_REQUIRED))

                    print("recipe_object", recipe_object)
                    context = {
                        ACTION: ACTION_CREATE,
                        RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                        RECIPE_FORM_STATE_STAGE: RECIPE_FORM_STATE_STAGE,
                        RECIPE_FORM_STATE_LAST_STAGE: RECIPE_FORM_STATE_LAST_STAGE,

                        NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                        NUMBER_OF_INGREDIENTS_RANGE: range(0, numberOfIngredientsMax),
                        INGREDIENTS_EXTENDED_LIST_LENGTH: 0,

                        "recipe_id": recipe_object.id,
                    }
                    return render(request, 'recipe/recipe_form_stage.html', context)
            else:
                # error
                error = ""
                if error_image != "":
                    error = error_image
                elif error_stage != "":
                    error = error_stage
                elif error_ingredient != "":
                    error = error_ingredient

                print("recipe_object", recipe_object)
                context = {
                    ERROR: error,
                    ACTION: ACTION_CREATE,
                    RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                    RECIPE_FORM_STATE_STAGE: RECIPE_FORM_STATE_STAGE,
                    RECIPE_FORM_STATE_LAST_STAGE: RECIPE_FORM_STATE_LAST_STAGE,

                    STAGE: {
                        COOKING_TIME: cooking_time,
                        DESCRIPTION: description,
                        IMAGE: image
                    },
                    INGREDIENTS_EXTENDED_LIST: ingredient_extended_list,
                    INGREDIENTS_EXTENDED_LIST_LENGTH: len(ingredient_extended_list),
                    NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                    NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), numberOfIngredientsMax),

                    "recipe_id": recipe_object.id,
                }
                return render(request, 'recipe/recipe_form_stage.html', context)
        else:
            print("ERROR", "----------------------STAGE -> STAGE-------------------------")
            context = {
                ACTION: ACTION_CREATE,
                RECIPE_FORM_STATE: RECIPE_FORM_STATE_FIRST
            }
            return render(request, 'recipe/recipe_form_first.html', context)
    elif recipe_form_state == RECIPE_FORM_STATE_LAST_STAGE:
        print("----------------------STAGE -> LAST-------------------------")
        if request.method == "POST":
            # image
            image = request.FILES.get(IMAGE)
            if image is None:
                image = 'default/default.PNG'
            error_image = recipe_image_controller.valid(image=image)
            # stage
            recipe_object = recipe_controller.find_one_by_id(id=recipe_id)
            cooking_time = request.POST.get(COOKING_TIME)
            description = request.POST.get(DESCRIPTION)
            error_stage = recipe_stage_controller.valid(recipe=recipe_object,
                                                        cooking_time=cooking_time,
                                                        description=description,
                                                        image=image)
            # ingredients
            ingredient_extended_list_validated = []
            ingredient_extended_list = []
            error_ingredient = ''
            for index in numberOfIngredientsRange:
                ingredient_id = request.POST.get(INGREDIENT_ID.format(index))
                ingredient_title = request.POST.get(INGREDIENT_TITLE.format(index))
                ingredient_amount = request.POST.get(INGREDIENT_AMOUNT.format(index))
                ingredient_unit = request.POST.get(INGREDIENT_UNIT.format(index))
                ingredient_is_require = request.POST.get(INGREDIENT_IS_REQUIRED.format(index))
                if ingredient_is_require is None:
                    ingredient_is_require = False
                else:
                    ingredient_is_require = True
                # print("--", ingredient_id, ingredient_title, ingredient_amount, ingredient_unit, ingredient_is_require)
                if ingredient_title != '' or ingredient_amount != '' or ingredient_unit != '':

                    ingredient_extended_list.append(
                        recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                                   title=ingredient_title,
                                                                                   amount=ingredient_amount,
                                                                                   unit=ingredient_unit,
                                                                                   is_required=ingredient_is_require))
                    if error_ingredient == '':
                        error_ingredient = recipe_stage_recipe_ingredient_controller.valid_extend(
                            title=ingredient_title,
                            amount=ingredient_amount,
                            unit=ingredient_unit,
                            is_required=ingredient_is_require)
                        if error_ingredient == '':
                            ingredient_extended_list_validated.append(
                                recipe_stage_recipe_ingredient_controller.DTO_extend_field(id=ingredient_id,
                                                                                           title=ingredient_title,
                                                                                           amount=ingredient_amount,
                                                                                           unit=ingredient_unit,
                                                                                           is_required=ingredient_is_require))

            if error_stage == "" and error_image == "" and error_ingredient == "":
                if action == ACTION_CREATE:
                    print("ACTION_CREATE")
                    # image
                    image_object = recipe_image_controller.create_and_save(image=image)
                    # stage
                    stage_object = recipe_stage_controller.create_and_save(recipe=recipe_object,
                                                                           cooking_time=cooking_time,
                                                                           description=description,
                                                                           image=image_object)
                    # ingredients
                    for object in ingredient_extended_list_validated:
                        recipe_stage_controller.add_ingredient_to_stage(stageObject=stage_object,
                                                                        title=object.get(TITLE),
                                                                        unit=object.get(UNIT),
                                                                        amount=object.get(AMOUNT),
                                                                        is_required=object.get(IS_REQUIRED))

                    print("recipe_object", recipe_object)
                    context = {
                        ACTION: ACTION_CREATE,
                        RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                        RECIPE_FORM_STATE_LAST: RECIPE_FORM_STATE_LAST,
                        "recipe_id": recipe_object.id,
                    }
                    return render(request, 'recipe/recipe_form_last.html', context)
            else:
                # error
                error = ""
                if error_image != "":
                    error = error_image
                elif error_stage != "":
                    error = error_stage
                elif error_ingredient != "":
                    error = error_ingredient

                print("recipe_object", recipe_object)
                context = {
                    ERROR: error,
                    ACTION: ACTION_CREATE,
                    RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                    RECIPE_FORM_STATE_STAGE: RECIPE_FORM_STATE_STAGE,
                    RECIPE_FORM_STATE_LAST_STAGE: RECIPE_FORM_STATE_LAST_STAGE,

                    STAGE: {
                        COOKING_TIME: cooking_time,
                        DESCRIPTION: description,
                        IMAGE: image
                    },
                    INGREDIENTS_EXTENDED_LIST: ingredient_extended_list,
                    INGREDIENTS_EXTENDED_LIST_LENGTH: len(ingredient_extended_list),
                    NUMBER_OF_INGREDIENTS_MAX: numberOfIngredientsMax,
                    NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), numberOfIngredientsMax),

                    "recipe_id": recipe_object.id,
                }
                return render(request, 'recipe/recipe_form_stage.html', context)
        else:
            print("ERROR", "----------------------STAGE -> LAST-------------------------")
            context = {
                ACTION: ACTION_CREATE,
                RECIPE_FORM_STATE: RECIPE_FORM_STATE_FIRST
            }
            return render(request, 'recipe/recipe_form_first.html', context)
    elif recipe_form_state == RECIPE_FORM_STATE_LAST:
        print("----------------------LAST -> END-------------------------")
        if request.method == "POST":
            pass
        else:
            print("ERROR", "----------------------LAST -> END-------------------------")
            context = {
                ACTION: ACTION_CREATE,
                RECIPE_FORM_STATE: RECIPE_FORM_STATE_FIRST
            }
            return render(request, 'recipe/recipe_form_first.html', context)
    else:
        print("----------------------NONE -> FIRST-------------------------")
        context = {
            ACTION: ACTION_CREATE,
            RECIPE_FORM_STATE: RECIPE_FORM_STATE,
            RECIPE_FORM_STATE_FIRST: RECIPE_FORM_STATE_FIRST
        }
        return render(request, 'recipe/recipe_form_first.html', context)


# =========================================================================================

def create_recipe_view(request):
    form = RecipeFormFirst()
    print("user", request.user)
    if request.method == "POST":
        if request.POST.get("ACTION") == "FIRST":
            form = RecipeFormFirst(request.POST)
            if form.is_valid():
                recipeObject = SaveRecipeSimple(
                    user=request.user,
                    title=form.cleaned_data['title'],
                    date_create=now(),
                    cooking_time=form.cleaned_data['cooking_time'],
                    image=request.FILES.get("image"),
                    categories=None)
                # data for the next stage
                recipe_stage_form = RecipeFormStage(None)
                recipeStageIngredient = modelformset_factory(RecipeIngredient, form=RecipeStageIngredientForm, extra=0)
                formset = recipeStageIngredient(None)
                context = {
                    'form': recipe_stage_form,
                    'recipe': recipeObject,
                    'formset': formset,
                }
                return render(request, 'recipe/create_recipe_stage.html', context)
            else:
                # data for the same stage
                context = {
                    'form': form,
                    'error': form.errors
                }
                return render(request, 'recipe/create_recipe_first.html', context)

        if request.POST.get("ACTION") == "STAGE":
            recipe_stage_form = RecipeFormStage(request.POST)
            recipeStageIngredient = modelformset_factory(RecipeIngredient, form=RecipeStageIngredientForm, extra=0)
            formset = recipeStageIngredient(None)
            if recipe_stage_form.is_valid():
                recipeObject, recipeStageObject = saveRecipeStage(recipe_stage_form, request)

                # data for the next stage
                recipe_stage_form = RecipeFormStage(request.POST or None)
                recipeStageIngredient = modelformset_factory(RecipeIngredient, form=RecipeStageIngredientForm, extra=0)
                formset = recipeStageIngredient(None)
                context = {
                    'form': recipe_stage_form,
                    'recipe': recipeObject,
                    'formset': formset,
                }
                return render(request, 'recipe/create_recipe_stage.html', context)
            else:
                print(recipe_stage_form.errors)
                # data for the same stage
                recipe_stage_form = RecipeFormStage(request.POST or None)
                recipeStageIngredient = modelformset_factory(RecipeIngredient, form=RecipeStageIngredientForm, extra=0)
                formset = recipeStageIngredient(request.POST or None)
                recipeObject = Recipe.objects.get(id=request.POST.get('recipe_id'))

                context = {
                    'form': recipe_stage_form,
                    'recipe': recipeObject,
                    'formset': formset,
                }
                return render(request, 'recipe/create_recipe_stage.html', context)

        if request.POST.get("ACTION") == "LAST_STAGE":
            recipe_stage_form = RecipeFormStage(request.POST)
            recipeStageIngredient = modelformset_factory(RecipeIngredient, form=RecipeStageIngredientForm, extra=0)
            formset = recipeStageIngredient(None)
            if recipe_stage_form.is_valid():
                recipeObject, recipeStageObject = saveRecipeStage(recipe_stage_form, request)

                # data to next stage
                recipe_last_form = RecipeFormLast(None)
                context = {
                    'form': recipe_last_form,
                    'recipe': recipeObject
                }
                return render(request, 'recipe/create_recipe_last.html', context)
            else:
                print(recipe_stage_form.errors)
                # data for the same stage
                recipe_stage_form = RecipeFormStage(request.POST or None)
                recipeStageIngredient = modelformset_factory(RecipeIngredient, form=RecipeStageIngredientForm, extra=0)
                formset = recipeStageIngredient(request.POST or None)
                recipeObject = Recipe.objects.get(id=request.POST.get('recipe_id'))

                context = {
                    'form': recipe_stage_form,
                    'recipe': recipeObject,
                    'formset': formset,
                }
                return render(request, 'recipe/create_recipe_stage.html', context)

        if request.POST.get("ACTION") == "LAST":
            recipe_last_form = RecipeFormLast(request.POST or None)
            if recipe_last_form.is_valid():
                recipeObject = Recipe.objects.get(id=request.POST.get('recipe_id'))
                categories = recipe_last_form.cleaned_data['categories']
                for category in categories:
                    recipeObject.categories.add(category)
                recipeObject.save()
                tags = recipe_last_form.cleaned_data['tags']
                for tag in tags:
                    recipeObject.tags.add(tag)
                recipeObject.save()
                return redirect(to="home")
            else:
                print(recipe_last_form.errors)
                recipe_last_form = RecipeFormLast(request.POST or None)
                recipeObject = Recipe.objects.get(id=request.POST.get('recipe_id'))
                context = {
                    'form': recipe_last_form,
                    'recipe': recipeObject
                }
                return render(request, 'recipe/create_recipe_last.html', context)

    # first stage
    context = {
        'form': form
    }
    return render(request, 'recipe/create_recipe_first.html', context)


def CreateContextForRecipeStage(recipeObject, request):
    recipe_stage_form = RecipeFormStage(request.POST or None)
    recipeStageIngredient = modelformset_factory(RecipeIngredient, form=RecipeStageIngredientForm, extra=0)
    formset = recipeStageIngredient(None)
    return {
        'form': recipe_stage_form,
        'recipe': recipeObject,
        'formset': formset,
    }


def recipe_select_all_view(request):
    recipe_list = []
    print("-------------------------------")
    for recipe in Recipe.objects.all():
        recipe_list.append(getRecipeSimpleDTO(recipe))
    context = {
        'recipe_list': recipe_list
    }
    return render(request, 'recipe/recipe_select_all.html', context)


def recipe_select_view(request, pk):
    recipe = getRecipeDTO(Recipe.objects.get(id=pk))
    context = {
        'recipe': recipe
    }
    return render(request, 'recipe/recipe_select.html', context)


def recipe_create_simple_view(request):
    form = RecipeForm()
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            SaveRecipeSimple(title=form.cleaned_data['title'],
                             date_create=now(),
                             cooking_time=form.cleaned_data['cooking_time'],
                             image=request.FILES.get("image"),
                             categories=form.cleaned_data['categories'])
        else:
            print("error", form.errors)
        return redirect("home")
    context = {
        'form': form
    }
    return render(request, 'recipe/recipe_create.html', context)


##=========================================================================================

from pathlib import Path


def SaveRecipeSimple(user, title, date_create, cooking_time, image, categories):
    # createimage
    print("image", image)
    if image == None:
        image = 'default/recipe_default_image.png'
    image = RecipeImage(image=image)
    image.save()
    # create recipe
    recipeObject = Recipe(author=user,
                          title=title,
                          date_create=date_create,
                          cooking_time=cooking_time,
                          image=image)
    recipeObject.save()
    # add categories
    if categories:
        for category in categories:
            recipeObject.categories.add(category)
        recipeObject.save()
    return recipeObject


def saveRecipeStage(recipe_stage_form, request):
    # create image
    image = request.FILES.get("image")
    if image == None:
        image = 'default/recipe_default_image.png'
    imageObject = RecipeImage(image=image)
    imageObject.save()
    # create recipe stage
    description = recipe_stage_form.cleaned_data['description']
    cooking_time = recipe_stage_form.cleaned_data['cooking_time']
    recipeObject = Recipe.objects.get(id=request.POST.get('recipe_id'))
    recipeStageObject = RecipeStage(
        recipe=recipeObject,
        description=description,
        cooking_time=cooking_time,
        image=imageObject)
    recipeStageObject.save()

    # create ingredients

    numberOfForms = request.POST.get('form-TOTAL_FORMS')
    for iter in range(2, int(numberOfForms) + 1):
        print("Dodaje skladnik")
        title = request.POST.get(f'form-{iter}-title')
        amount = request.POST.get(f'form-{iter}-amount')
        unit = request.POST.get(f'form-{iter}-unit')
        ingredient = RecipeIngredient(
            recipe_stage=recipeStageObject,
            title=title,
            amount=amount,
            unit=unit)
        ingredient.save()
    return recipeObject, recipeStageObject
