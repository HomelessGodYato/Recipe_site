from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import RecipeCategory, Recipe, RecipeStage, Ingredient, RecipeTag


# ===========================================================================


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2']


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'email']


# ===========================================================================


class CustomCategory(forms.ModelMultipleChoiceField):
    def label_from_instance(self, category):
        return "%s" % category.title


# ===========================================================================

class RecipeFormFirst(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ["title", "cooking_time", "image"]


class RecipeFormStage(forms.ModelForm):
    image = forms.ImageField(required=False, )

    class Meta:
        model = RecipeStage
        fields = ["cooking_time", "description", "image"]


class RecipeFormLast(forms.ModelForm):
    categories = CustomCategory(
        queryset=RecipeCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    tags = CustomCategory(
        queryset=RecipeTag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Recipe
        fields = ["categories", "tags"]


# ====================================================================
class RecipeStageIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["title", "amount", "unit"]


class RecipeForm(forms.ModelForm):
    categories = CustomCategory(
        queryset=RecipeCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ["name", "cooking_time", "image", "categories"]