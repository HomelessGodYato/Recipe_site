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

from .controllers import RecipeIngredientController
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


TITLE = "title"
UNIT = "unit"

INGREDIENT = "ingredient"
INGREDIENTS_LIST = "ingredients_list"
ERROR = "error"

ACTION = "ACTION"
ACTION_CREATE = "ACTION_CREATE"
ACTION_UPDATE = "ACTION_UPDATE"

recipe_ingredient_controller = RecipeIngredientController()


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
    print("id",id)
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
                print("ACTION_UPDATE",id)
                recipe_ingredient_controller.update(id, title=title, unit=unit)
                print("ACTION_UPDATE")
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
        if ingredientObj is not None: #else create
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
    return render(request, 'ingredient/ingredient_form.html',context)

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
