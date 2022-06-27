from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserProfile, Article, ArticleImage, ArticleComment


# ===========================================================================


class CreateUserForm(UserCreationForm):

    username = forms.CharField(label='Username', min_length=5, max_length=150)
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First name', max_length=250)
    last_name = forms.CharField(label='Last name', max_length=250)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio',
                  'facebook_link',
                  'instagram_link',
                  'twitter_link',
                  'youtube_link',
                  'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_link': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control'}),
            'youtube_link': forms.TextInput(attrs={'class': 'form-control'})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'email']


# ===========================================================================


class CustomCategory(forms.ModelMultipleChoiceField):
    def label_from_instance(self, category):
        return "%s" % category.title

# ============================================================================

class ArticleSearchForm(forms.Form):
    phrase = forms.CharField(label="", min_length=2, max_length=40)

    class Meta:
        fields = ['phrase']


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label="", min_length=3, max_length=254,
                            widget=forms.Textarea(attrs={'class': 'article_input_title',
                                                         'placeholder': 'Tytuł...',
                                                         'style': 'resize:none;'}))
    description = forms.CharField(label="", min_length=10, max_length=8191,
                                  widget=forms.Textarea(attrs={'class': 'article_input_descrip', 'style': 'resize:none;'}))

    class Meta:
        model = Article
        fields = ['title', 'description']


class ArticleImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="",
        widget=forms.ClearableFileInput(
            attrs={'multiple': True, 'id': 'image_field', 'accept': 'image/png, image/jpeg', 'max_length': 6}),
        required=False,
    )

    class Meta:
        model = ArticleImage
        fields = ('image',)


class ArticleCommentForm(forms.ModelForm):
    description = forms.CharField(label="", min_length=2, max_length=8191,
                                  widget=forms.Textarea(attrs={'class': 'comment_input_descrip', 'style': 'resize:none;'}))

    class Meta:
        model = ArticleComment
        fields = ['description']
