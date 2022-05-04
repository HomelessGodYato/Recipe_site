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

from .dto import getRecipeDTO, getRecipeSimpleDTO
from .forms import CreateUserForm, RecipeForm, RecipeStageIngredientForm, RecipeFormFirst, RecipeFormStage, \
    RecipeFormLast
from .tokens import account_activation_token
from .models import Recipe, RecipeStage, Ingredient, RecipeImage, RecipeCategory, RecipeRecipeCategory
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


def create_recipe_view(request):
    form = RecipeFormFirst()
    if request.method == "POST":
        if request.POST.get("ACTION") == "FIRST":
            form = RecipeFormFirst(request.POST)
            if form.is_valid():
                # create image
                imageObject = RecipeImage(image=request.FILES["image"])
                imageObject.save()
                # create recipe
                name = form.cleaned_data['name']
                cooking_time = form.cleaned_data['cooking_time']
                recipeObject = Recipe(name=name,
                                      date_create=now(),
                                      cooking_time=cooking_time,
                                      image=imageObject)
                recipeObject.save()

                # data for the next stage
                recipe_stage_form = RecipeFormStage(None)
                recipeStageIngredient = modelformset_factory(Ingredient, form=RecipeStageIngredientForm, extra=0)
                formset = recipeStageIngredient(request.POST or None)
                context = {
                    'form': recipe_stage_form,
                    'recipe': recipeObject,
                    'formset': formset,
                }
                return render(request, 'recipe/create_recipe_stage.html', context)
            else:
                # data for the same stage
                print("error", form.errors)
                context = {
                    'form': form,
                    'error': form.errors
                }
                return render(request, 'recipe/create_recipe_first.html', context)

        if request.POST.get("ACTION") == "STAGE":
            recipe_stage_form = RecipeFormStage(request.POST)
            recipeStageIngredient = modelformset_factory(Ingredient, form=RecipeStageIngredientForm, extra=0)
            formset = recipeStageIngredient(None)
            if recipe_stage_form.is_valid():
                recipeObject, recipeStageObject = saveRecipeStage(recipe_stage_form, request)

                # data for the next stage
                recipe_stage_form = RecipeFormStage(None)
                recipeStageIngredient = modelformset_factory(Ingredient, form=RecipeStageIngredientForm, extra=0)
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
                recipeStageIngredient = modelformset_factory(Ingredient, form=RecipeStageIngredientForm, extra=0)
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
            recipeStageIngredient = modelformset_factory(Ingredient, form=RecipeStageIngredientForm, extra=0)
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
                recipeStageIngredient = modelformset_factory(Ingredient, form=RecipeStageIngredientForm, extra=0)
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


def recipe_select_all_view(request):
    recipe_list = []
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
            # createimage
            image = RecipeImage(image=request.FILES["image"])
            image.save()
            # create recipe
            name = form.cleaned_data['name']
            cooking_time = form.cleaned_data['cooking_time']
            categories = form.cleaned_data['categories']
            recipe = Recipe(name=name,
                            date_create=now(),
                            cooking_time=cooking_time,
                            image=image)
            recipe.save()
            # add categories
            for category in categories:
                recipe.categories.add(category)
            recipe.save()

        else:
            print("error", form.errors)
        return redirect("recipe_create")
    context = {
        'form': form
    }
    return render(request, 'recipe/recipe_create.html', context)


##=========================================================================================

def saveRecipeStage(recipe_stage_form, request):
    # create image
    imageObject = RecipeImage(image=request.FILES["image"])
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
        name = request.POST.get(f'form-{iter}-name')
        amount = request.POST.get(f'form-{iter}-amount')
        unit = request.POST.get(f'form-{iter}-unit')
        ingredient = Ingredient(
            recipe_stage=recipeStageObject,
            name=name,
            amount=amount,
            unit=unit)
        ingredient.save()
    return recipeObject, recipeStageObject
