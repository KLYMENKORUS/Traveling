from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Введите Пароль'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username').strip()
        password = self.cleaned_data.get('password').strip()

        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError(f'Пользователя с логином - {username} несуществует!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Неверный пароль')

            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(f'Пользователь {username} заблокирован')

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Придумайте логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Повторите пароль'}))

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Пароли не совпадают!')

    class Meta:
        model = User
        fields = ('username',)