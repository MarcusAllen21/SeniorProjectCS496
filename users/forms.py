from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Quiz, MCQuestion, Choice
from django.forms import inlineformset_factory, formset_factory

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_teacher = forms.BooleanField(label="Are you a teacher?", required=False, initial=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_teacher']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user._is_teacher = self.cleaned_data['is_teacher']

        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'video_url']

class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        fields = ['text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

MCQuestionFormSet = forms.formset_factory(
    MCQuestionForm, 
    extra=1, 
    max_num=10
)

ChoiceFormSet = forms.inlineformset_factory(
    MCQuestion, Choice, form=ChoiceForm, extra=4, max_num=4, can_delete=False
)