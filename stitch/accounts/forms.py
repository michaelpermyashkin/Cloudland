from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'name': 'username',
            'placeholder': 'Username',
            'type': 'text'})
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'first_name',
            'placeholder': 'Your first name',
            'type': 'text'})
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'name': 'last_name',
            'placeholder': 'Your last name',
            'type': 'text'})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'name': 'email',
            'placeholder': 'email@example.com',
            'type': 'text'})
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'name': 'password',
            'placeholder': 'Enter password',
            'type': 'password'})
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'name': 'password',
            'placeholder': 'Confirm password',
            'type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self, *args, **keyargs):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError('This email has already been registered')
        return email


class UsersLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UsersLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'name': 'username',
            'placeholder': 'Username',
            'type': 'text'})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'name': 'password',
            'placeholder': 'Password',
            'type': 'password'})
    
    def clean_username(self, *args, **keyargs):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('This user does not exists')
        return username

    def clean_password(self, *args, **keyargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        
        if user is not None and not user.check_password(password):
            raise forms.ValidationError('Invalid Password')
        elif user is None:
            pass
        else:
            return password
