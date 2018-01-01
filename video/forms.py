from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django import forms
from .models import Video, UserFeedback


User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Password")
        if not user.is_active:
            raise forms.ValidationError("This user is not longer active")
        return super(UserLogin, self).clean(*args, **kwargs)


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnail', 'video_path']


class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['comment']
