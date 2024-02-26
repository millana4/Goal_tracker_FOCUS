from django import forms
from .models import User

# # Это ранний вариант регистрации с использованием формы
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('email', 'username')
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Пароль не совпадает')
#         return cd['password2']