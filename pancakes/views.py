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
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now
from django.views.generic.edit import DeleteView

from .constant import *
from .controllers import recipe_ingredient_controller, recipe_image_controller, \
    recipe_stage_controller, recipe_stage_recipe_ingredient_controller, recipe_controller, recipe_tag_controller, \
    recipe_category_controller
from .forms import CreateUserForm, UserEditForm, ProfileUpdateForm
from .tokens import account_activation_token


#  =========================================================================================
#  ======================================USER ==============================================

class CustomUSerDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('home')

    # class CustomUserEditView(generic.UpdateView):
    #     form = UserEditForm
    #     template_name = 'user/modifications/update.html'
    #     success_url = reverse_lazy('user')

    def get_object(self):
        return self.request.user


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
                messages.success(request, 'Account created succesfully')

                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('user/registration_login/acc_activation.html', {
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
                return render(request, 'user/registration_login/confirm.html')
            else:
                form = CreateUserForm(request.POST)

            return render(request, 'user/registration_login/register.html', {'form': form})
        messages.success(request, 'Account created successfuly')
    return render(request, 'user/registration_login/register.html', {'form':form})


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
        return render(request, 'user/registration_login/registration_successful.html', {})
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
                return render(request, 'user/registration_login/login.html', context)

        return render(request, 'user/registration_login/login.html', context)


@login_required(login_url='login')
def user_main_page(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'user/registration_login/user_main.html', args)


@login_required(login_url='login')
def user_edit_view(request):
    profile = request.user.userprofile
    user = request.user
    profile_form = ProfileUpdateForm(instance=profile)
    user_form = UserEditForm(instance=user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        user_form = UserEditForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('user')

    context = {'profile_form': profile_form,
               'user_form': user_form}
    return render(request, 'user/modifications/update.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


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
    context = {
        ACTION: ACTION_CREATE
    }

    if id != 0:
        # update
        tagObj = recipe_tag_controller.find_one_by_id(id)
        if tagObj is not None:  # else create
            tag = recipe_tag_controller.DTO(tagObj)
            context[ACTION] = ACTION_UPDATE
            context[TAG] = tag
            return render(request, 'tag/tag_form.html', context)

    return render(request, 'tag/tag_form.html', context)


def tag_delete_view(request, id):
    if id == 0:
        return redirect(to="home")

    if request.method == "POST":
        action = request.POST.get(ACTION)
        if action == ACTION_DELETE:
            print("ACTION_DELETE")
            recipe_tag_controller.delete(id)
            return redirect("tag_show_all")

    object = recipe_tag_controller.find_one_by_id(id)
    if object is None:
        context = {
            ERROR: ERROR_INVALID_ID.format("tagu", id)
        }
        return render(request, 'tag/tag_delete.html', context)

    context = {
        TAG: recipe_tag_controller.DTO(object),
        ACTION: ACTION_DELETE
    }
    return render(request, 'tag/tag_delete.html', context)


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
    context = {
        ACTION: ACTION_CREATE
    }

    if id != 0:
        # update
        categoryObj = recipe_category_controller.find_one_by_id(id)
        if categoryObj is not None:  # else create
            category = recipe_category_controller.DTO(categoryObj)
            context[ACTION] = ACTION_UPDATE
            context[CATEGORY] = category
            return render(request, 'category/category_form.html', context)

    return render(request, 'category/category_form.html', context)


def category_delete_view(request, id):
    if id == 0:
        return redirect(to="home")

    if request.method == "POST":
        action = request.POST.get(ACTION)
        if action == ACTION_DELETE:
            print("ACTION_DELETE")
            recipe_category_controller.delete(id)
            return redirect("category_show_all")

    object = recipe_category_controller.find_one_by_id(id)
    if object is None:
        context = {
            ERROR: ERROR_INVALID_ID.format("kategorii", id)
        }
        return render(request, 'category/category_delete.html', context)

    context = {
        CATEGORY: recipe_category_controller.DTO(object),
        ACTION: ACTION_DELETE
    }
    return render(request, 'category/category_delete.html', context)


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
    context = {
        ACTION: ACTION_CREATE
    }

    if id != 0:
        # update
        ingredientObj = recipe_ingredient_controller.find_one_by_id(id)
        if ingredientObj is not None:  # else create
            ingredient = recipe_ingredient_controller.DTO(ingredientObj)
            context[ACTION] = ACTION_UPDATE
            context[INGREDIENT] = ingredient
            return render(request, 'ingredient/ingredient_form.html', context)

    return render(request, 'ingredient/ingredient_form.html', context)


def ingredient_delete_view(request, id):
    if id == 0:
        return redirect(to="home")

    if request.method == "POST":
        action = request.POST.get(ACTION)
        if action == ACTION_DELETE:
            print("ACTION_DELETE")
            recipe_ingredient_controller.delete(id)
            return redirect("home")

    object = recipe_ingredient_controller.find_one_by_id(id)
    if object is None:
        context = {
            ERROR: ERROR_INVALID_ID.format("składniku", id)
        }
        return render(request, 'ingredient/ingredient_delete.html', context)

    context = {
        INGREDIENT: recipe_ingredient_controller.DTO(object),
        ACTION: ACTION_DELETE
    }
    return render(request, 'ingredient/ingredient_delete.html', context)


# ======================================recipe===================================================

def recipe_show_all_view(request):
    object_list = recipe_controller.all()
    context = {
        RECIPES_LIST: recipe_controller.DTO_list(object_list)
    }
    return render(request, 'recipe/recipe_show_all.html', context)


def recipe_category_name_show_all_view(request, category_name=''):
    category_object = recipe_category_controller.find_one_by_title(category_name)
    recipe_list = []
    error = ''
    if category_object is not None:
        recipe_list = recipe_controller.find_all_by_category(category_object)
    else:
        error = ERROR_THERE_IS_NOT_CATEGORY.format(category_name)

    context = {
        RECIPES_LIST: recipe_controller.DTO_list(recipe_list),
        ERROR: error
    }
    return render(request, 'recipe/recipe_show_all.html', context)


def recipe_tag_name_show_all_view(request, tag_name=''):
    tag_object = recipe_tag_controller.find_one_by_title(tag_name)
    recipe_list = []
    error = ''
    if tag_object is not None:
        recipe_list = recipe_controller.find_all_by_tag(tag_object)
    else:
        error = ERROR_THERE_IS_NOT_TAG.format(tag_object)

    context = {
        RECIPES_LIST: recipe_controller.DTO_list(recipe_list),
        ERROR: error
    }
    return render(request, 'recipe/recipe_show_all.html', context)


def recipe_title_name_show_all_view(request, title_name=''):
    error = ''
    recipe_list = recipe_controller.find_all_by_title(title_name)
    if len(recipe_list) == 0:
        error = ERROR_THERE_IS_NOT_TITLE.format(title_name)

    context = {
        RECIPES_LIST: recipe_controller.DTO_list(recipe_list),
        ERROR: error
    }
    return render(request, 'recipe/recipe_show_all.html', context)


def recipe_title_name_from_form_show_all_view(request):
    title_name = request.POST.get(TITLE)
    return recipe_title_name_show_all_view(request, title_name)


def recipe_user_id_show_all_view(request, id=0):
    user_object = User.objects.get(id=id)
    recipe_list = []
    error = ''
    if user_object is not None:
        recipe_list = recipe_controller.find_all_by_user(user_object)
    else:
        error = ERROR_THERE_IS_NOT_AUTHOR.format(id)

    context = {
        RECIPES_LIST: recipe_controller.DTO_list(recipe_list),
        ERROR: error
    }
    return render(request, 'recipe/recipe_show_all.html', context)


def recipe_show_view(request, id):
    object = recipe_controller.find_one_by_id(id)
    context = {
        RECIPE: recipe_controller.DTO(object)
    }
    return render(request, 'recipe/recipe_show.html', context)


def recipe_form_view(request, id=0):
    action = request.POST.get(ACTION)
    recipe_form_state = request.POST.get(RECIPE_FORM_STATE)
    recipe_id = request.POST.get(RECIPE_ID)
    if recipe_form_state == RECIPE_FORM_STATE_FIRST:  # FIRST -> STAGE
        if request.method == "POST":
            # image
            image = request.FILES.get(IMAGE)
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
                recipe_object = ''  # have to be previously declared
                if action == ACTION_CREATE:
                    print("ACTION_CREATE")
                    # image
                    if image is None:
                        image = DEFAULT_RECIPE_IMAGE_PATH
                    image_object = recipe_image_controller.create_and_save(image=image)
                    # recipe
                    recipe_object = recipe_controller.create_and_save(author=author_object,
                                                                      title=title,
                                                                      cooking_time=cooking_time,
                                                                      date_create=date_create,
                                                                      image=image_object)
                if action == ACTION_UPDATE:
                    print("ACTION_UPDATE")
                    recipe_object = recipe_controller.find_one_by_id(id=id)
                    # image
                    if image is not None:
                        image_object = recipe_image_controller.update(id=recipe_object.image.id, image=image)
                    else:
                        image_object = recipe_image_controller.find_one_by_id(id=recipe_object.image.id)
                    # recipe
                    recipe_object = recipe_controller.update(id=id,
                                                             author=author_object,
                                                             title=title,
                                                             cooking_time=cooking_time,
                                                             image=image_object)

                ingredient_list = recipe_ingredient_controller.all()
                context = {
                    "ingredients_list_to_autocomplete": recipe_ingredient_controller.DTO_list(ingredient_list),
                    ACTION: action,
                    RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                    RECIPE_FORM_STATE_STAGE: RECIPE_FORM_STATE_STAGE,
                    RECIPE_FORM_STATE_LAST_STAGE: RECIPE_FORM_STATE_LAST_STAGE,

                    NUMBER_OF_INGREDIENTS_MAX: number_of_ingredients_max,
                    NUMBER_OF_INGREDIENTS_RANGE: range(0, number_of_ingredients_max),
                    INGREDIENTS_EXTENDED_LIST_LENGTH: 0,
                    ORDER: 1,
                    RECIPE_ID: recipe_object.id
                }
                if id != 0:  # update
                    context[ID] = id
                    recipe_object = recipe_controller.find_one_by_id(recipe_object.id)
                    stage_object = recipe_stage_controller.find_one_by_recipe_and_order(recipe=recipe_object, order=1)
                    ingredient_list = recipe_stage_recipe_ingredient_controller.find_all_by_stage(
                        stage_object=stage_object)
                    ingredient_extended_list = recipe_stage_recipe_ingredient_controller.DTO_extend_list(
                        ingredient_list)
                    if stage_object is not None:
                        stage = recipe_stage_controller.DTO(stage_object)
                        context[STAGE] = stage
                        context[STAGE_ID] = stage_object.id
                        context[INGREDIENTS_EXTENDED_LIST] = ingredient_extended_list
                        context[INGREDIENTS_EXTENDED_LIST_LENGTH] = len(ingredient_extended_list)
                        context[NUMBER_OF_INGREDIENTS_RANGE] = range(len(ingredient_extended_list),
                                                                     number_of_ingredients_max)
                return render(request, 'recipe/recipe_form_stage.html', context)
            else:
                # error
                error = ""
                if error_image != "":
                    error = error_image
                elif error_recipe != "":
                    error = error_recipe
                context = {
                    ACTION: action,
                    RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                    RECIPE_FORM_STATE_FIRST: RECIPE_FORM_STATE_FIRST,
                    ERROR: error,
                    RECIPE: {
                        TITLE: title,
                        COOKING_TIME: cooking_time,
                        IMAGE: image
                    }
                }
                return render(request, 'recipe/recipe_form_first.html', context)
    elif recipe_form_state == RECIPE_FORM_STATE_STAGE:  # STAGE -> STAGE
        if request.method == "POST":
            # image
            image = request.FILES.get(IMAGE)
            error_image = recipe_image_controller.valid(image=image)
            # stage_object
            recipe_object = recipe_controller.find_one_by_id(id=recipe_id)
            stage_id = request.POST.get(STAGE_ID)
            cooking_time = request.POST.get(COOKING_TIME)
            description = request.POST.get(DESCRIPTION)
            order = request.POST.get(ORDER)
            error_stage = recipe_stage_controller.valid(recipe=recipe_object,
                                                        cooking_time=cooking_time,
                                                        description=description,
                                                        image=image,
                                                        order=order)
            # ingredients
            ingredient_extended_list_validated = []
            ingredient_extended_list = []
            error_ingredient = ''
            for index in number_of_ingredients_range:
                ingredient_id = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_ID.format(index))
                ingredient_title = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_TITLE.format(index))
                ingredient_amount = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_AMOUNT.format(index))
                ingredient_unit = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_UNIT.format(index))
                ingredient_is_require = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_IS_REQUIRED.format(index))
                if ingredient_is_require is None:
                    ingredient_is_require = False
                else:
                    ingredient_is_require = True
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
                if action == ACTION_CREATE or stage_id is None:
                    print("ACTION_CREATE")
                    # image
                    if image is None:
                        image = DEFAULT_RECIPE_IMAGE_PATH
                    image_object = recipe_image_controller.create_and_save(image=image)
                    # stage_object
                    stage_object = recipe_stage_controller.create_and_save(recipe=recipe_object,
                                                                           cooking_time=cooking_time,
                                                                           description=description,
                                                                           image=image_object,
                                                                           order=order)
                    # ingredients
                    for object in ingredient_extended_list_validated:
                        recipe_stage_controller.add_ingredient_to_stage(stageObject=stage_object,
                                                                        title=object.get(TITLE),
                                                                        unit=object.get(UNIT),
                                                                        amount=object.get(AMOUNT),
                                                                        is_required=object.get(IS_REQUIRED))
                elif action == ACTION_UPDATE:
                    print("ACTION_UPDATE")
                    stage_object = recipe_stage_controller.find_one_by_id(stage_id)
                    # image
                    if image is not None:
                        image_object = recipe_image_controller.update(id=stage_object.image.id, image=image)
                    else:
                        image_object = recipe_image_controller.find_one_by_id(id=stage_object.image.id)
                    # stage_object
                    stage_object = recipe_stage_controller.update(id=stage_id,
                                                                  recipe=recipe_object,
                                                                  cooking_time=cooking_time,
                                                                  description=description,
                                                                  image=image_object,
                                                                  order=order)
                    # ingredients
                    for object in ingredient_extended_list_validated:
                        recipe_stage_controller.update_ingredient_in_stage(id=object.get(ID),
                                                                           stageObject=stage_object,
                                                                           title=object.get(TITLE),
                                                                           unit=object.get(UNIT),
                                                                           amount=object.get(AMOUNT),
                                                                           is_required=object.get(IS_REQUIRED))
                ingredient_list = recipe_ingredient_controller.all()
                context = {
                    "ingredients_list_to_autocomplete": recipe_ingredient_controller.DTO_list(ingredient_list),
                    ACTION: action,
                    RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                    RECIPE_FORM_STATE_STAGE: RECIPE_FORM_STATE_STAGE,
                    RECIPE_FORM_STATE_LAST_STAGE: RECIPE_FORM_STATE_LAST_STAGE,

                    NUMBER_OF_INGREDIENTS_MAX: number_of_ingredients_max,
                    NUMBER_OF_INGREDIENTS_RANGE: range(0, number_of_ingredients_max),
                    INGREDIENTS_EXTENDED_LIST_LENGTH: 0,
                    ORDER: int(order) + 1,
                    RECIPE_ID: recipe_object.id,
                }
                if id != 0:  # update
                    context[ID] = id
                    recipe_object = recipe_controller.find_one_by_id(recipe_object.id)
                    stage_object = recipe_stage_controller.find_one_by_recipe_and_order(recipe=recipe_object,
                                                                                        order=int(order) + 1)
                    ingredient_list = recipe_stage_recipe_ingredient_controller.find_all_by_stage(stage_object)
                    ingredient_extended_list = recipe_stage_recipe_ingredient_controller.DTO_extend_list(
                        ingredient_list)

                    if stage_object is not None:
                        stage = recipe_stage_controller.DTO(stage_object)
                        context[STAGE] = stage
                        context[STAGE_ID] = stage_object.id
                        context[INGREDIENTS_EXTENDED_LIST] = ingredient_extended_list
                        context[INGREDIENTS_EXTENDED_LIST_LENGTH] = len(ingredient_extended_list)
                        context[NUMBER_OF_INGREDIENTS_RANGE] = range(len(ingredient_extended_list),
                                                                     number_of_ingredients_max)
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
                ingredient_list = recipe_ingredient_controller.all()
                context = {
                    "ingredients_list_to_autocomplete": recipe_ingredient_controller.DTO_list(ingredient_list),
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
                    NUMBER_OF_INGREDIENTS_MAX: number_of_ingredients_max,
                    NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), number_of_ingredients_max),
                    ORDER: order,
                    RECIPE_ID: recipe_object.id,
                }
                return render(request, 'recipe/recipe_form_stage.html', context)
    elif recipe_form_state == RECIPE_FORM_STATE_LAST_STAGE:  # STAGE -> LAST
        if request.method == "POST":
            # image
            image = request.FILES.get(IMAGE)
            error_image = recipe_image_controller.valid(image=image)
            # stage_object
            recipe_object = recipe_controller.find_one_by_id(id=recipe_id)
            stage_id = request.POST.get(STAGE_ID)
            cooking_time = request.POST.get(COOKING_TIME)
            description = request.POST.get(DESCRIPTION)
            order = request.POST.get(ORDER)
            error_stage = recipe_stage_controller.valid(recipe=recipe_object,
                                                        cooking_time=cooking_time,
                                                        description=description,
                                                        image=image,
                                                        order=order)
            # ingredients
            ingredient_extended_list_validated = []
            ingredient_extended_list = []
            error_ingredient = ''
            for index in number_of_ingredients_range:
                ingredient_id = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_ID.format(index))
                ingredient_title = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_TITLE.format(index))
                ingredient_amount = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_AMOUNT.format(index))
                ingredient_unit = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_UNIT.format(index))
                ingredient_is_require = request.POST.get(MODIFIABLE_FIELD_INGREDIENT_IS_REQUIRED.format(index))
                if ingredient_is_require is None:
                    ingredient_is_require = False
                else:
                    ingredient_is_require = True
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
                if action == ACTION_CREATE or stage_id == '':
                    print("ACTION_CREATE")
                    # image
                    if image is None:
                        image = DEFAULT_RECIPE_IMAGE_PATH
                    image_object = recipe_image_controller.create_and_save(image=image)
                    # stage_object
                    stage_object = recipe_stage_controller.create_and_save(recipe=recipe_object,
                                                                           cooking_time=cooking_time,
                                                                           description=description,
                                                                           image=image_object,
                                                                           order=order)
                    # ingredients
                    for object in ingredient_extended_list_validated:
                        recipe_stage_controller.add_ingredient_to_stage(stageObject=stage_object,
                                                                        title=object.get(TITLE),
                                                                        unit=object.get(UNIT),
                                                                        amount=object.get(AMOUNT),
                                                                        is_required=object.get(IS_REQUIRED))
                elif action == ACTION_UPDATE:
                    print("ACTION_UPDATE")
                    stage_object = recipe_stage_controller.find_one_by_id(stage_id)
                    # image
                    if image is not None:
                        image_object = recipe_image_controller.update(id=stage_object.image.id, image=image)
                    else:
                        image_object = recipe_image_controller.find_one_by_id(id=stage_object.image.id)

                    # stage_object
                    stage_object = recipe_stage_controller.update(id=stage_id,
                                                                  recipe=recipe_object,
                                                                  cooking_time=cooking_time,
                                                                  description=description,
                                                                  image=image_object,
                                                                  order=order)
                    # ingredients
                    for object in ingredient_extended_list_validated:
                        recipe_stage_controller.update_ingredient_in_stage(id=object.get(ID),
                                                                           stageObject=stage_object,
                                                                           title=object.get(TITLE),
                                                                           unit=object.get(UNIT),
                                                                           amount=object.get(AMOUNT),
                                                                           is_required=object.get(IS_REQUIRED))

                category_objects_list = recipe_category_controller.all()
                category_objects_DTO_list = recipe_category_controller.DTO_list(category_objects_list)
                tag_objects_list = recipe_tag_controller.all()
                tag_objects_DTO_list = recipe_tag_controller.DTO_list(tag_objects_list)
                context = {
                    ACTION: action,
                    RECIPE_FORM_STATE: RECIPE_FORM_STATE,
                    RECIPE_FORM_STATE_LAST: RECIPE_FORM_STATE_LAST,

                    CATEGORIES_LIST: category_objects_DTO_list,
                    NUMBER_OF_CATEGORIES: len(category_objects_list),
                    TAGS_LIST: tag_objects_DTO_list,
                    NUMBER_OF_TAGS: len(tag_objects_list),

                    RECIPE_ID: recipe_object.id,
                }
                if id != 0:  # update
                    context[ID] = id
                    recipe_categories = recipe_category_controller.find_all_by_recipe(recipe_object=recipe_object)
                    for category in category_objects_DTO_list:
                        for recipe_category in recipe_categories:
                            if recipe_category.id == category.get(ID):
                                category[IS_CHECKED] = True
                                break
                    recipe_tags = recipe_tag_controller.find_all_by_recipe(recipe_object=recipe_object)
                    for tag in tag_objects_DTO_list:
                        for recipe_tag in recipe_tags:
                            if recipe_tag.id == tag.get(ID):
                                tag[IS_CHECKED] = True
                                break
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
                    NUMBER_OF_INGREDIENTS_MAX: number_of_ingredients_max,
                    NUMBER_OF_INGREDIENTS_RANGE: range(len(ingredient_extended_list), number_of_ingredients_max),
                    ORDER: order,
                    RECIPE_ID: recipe_object.id,
                }
                return render(request, 'recipe/recipe_form_stage.html', context)
    elif recipe_form_state == RECIPE_FORM_STATE_LAST:  # LAST -> END
        if request.method == "POST":
            # recipe
            recipe_object = recipe_controller.find_one_by_id(id=recipe_id)
            # categories
            number_of_categories = request.POST.get(NUMBER_OF_CATEGORIES)
            categories_objects_list = []
            for index in range(1, int(number_of_categories) + 1):
                category_id = request.POST.get(MODIFIABLE_FIELD_CATEGORY.format(index))
                if category_id is not None:
                    category_object = recipe_category_controller.find_one_by_id(id=category_id)
                    categories_objects_list.append(category_object)
            # tags
            number_of_tags = request.POST.get(NUMBER_OF_TAGS)
            tags_objects_list = []
            for index in range(1, int(number_of_tags) + 1):
                tag_id = request.POST.get(MODIFIABLE_FIELD_TAG.format(index))
                if tag_id is not None:
                    tag_object = recipe_tag_controller.find_one_by_id(id=tag_id)
                    tags_objects_list.append(tag_object)

            if action == ACTION_CREATE:
                print("ACTION_CREATE", categories_objects_list, tags_objects_list)
                recipe_controller.set_categories_to_recipe(recipe_object=recipe_object,
                                                           categories_objects_list=categories_objects_list)
                recipe_controller.set_tags_to_recipe(recipe_object=recipe_object,
                                                     tags_objects_list=tags_objects_list)
            if action == ACTION_UPDATE:
                print("ACTION_UPDATE", categories_objects_list, tags_objects_list)
                recipe_controller.remove_all_categories_from_recipe(recipe_object=recipe_object)
                recipe_controller.set_categories_to_recipe(recipe_object=recipe_object,
                                                           categories_objects_list=categories_objects_list)
                recipe_controller.remove_all_tags_from_recipe(recipe_object=recipe_object)
                recipe_controller.set_tags_to_recipe(recipe_object=recipe_object,
                                                     tags_objects_list=tags_objects_list)
            return redirect("recipe_show", id=recipe_id)

    # NONE -> FIRST
    context = {
        ACTION: ACTION_CREATE,
        RECIPE_FORM_STATE: RECIPE_FORM_STATE,
        RECIPE_FORM_STATE_FIRST: RECIPE_FORM_STATE_FIRST
    }
    if id != 0:  # update
        recipe_object = recipe_controller.find_one_by_id(id)
        if recipe_object is not None:  # else create
            recipe = recipe_controller.DTO(recipe_object)
            context[ACTION] = ACTION_UPDATE
            context[RECIPE_ID] = id
            context[RECIPE] = recipe

    return render(request, 'recipe/recipe_form_first.html', context)


def recipe_delete_view(request, id):
    if id == 0:
        return redirect(to="home")

    if request.method == "POST":
        action = request.POST.get(ACTION)
        if action == ACTION_DELETE:
            print("ACTION_DELETE")
            recipe_controller.delete(id)
            return redirect("home")

    object = recipe_controller.find_one_by_id(id)
    if object is None:
        context = {
            ERROR: ERROR_INVALID_ID.format("przepisu", id),
        }
        return render(request, 'recipe/recipe_delete.html', context)

    if request.user != object.author:
        context = {
            ERROR: ERROR_AUTHOR.format(id),
        }
        return render(request, 'recipe/recipe_delete.html', context)

    context = {
        RECIPE: recipe_controller.DTO(object),
        ACTION: ACTION_DELETE
    }
    return render(request, 'recipe/recipe_delete.html', context)
