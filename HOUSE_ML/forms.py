from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
     first_name = forms.CharField(
          max_length=100,
          required=True,
          widget=forms.TextInput(attrs={
               'placeholder': 'First Name',
               'class': 'form-control',
               }))
     
     last_name = forms.CharField(
          max_length=100,
          required=True,
          widget=forms.TextInput(attrs={
               'placeholder':'First Name',
               'class':'form-control',
          })
     )

     username = forms.CharField(
          max_length=100,
          required=True,
          widget=forms.TextInput(attrs={
               'placeholder':'Username',
               'class':'form-control',
          })
     )

     email = forms.CharField(
          max_length=50,
          required=True,
          widget=forms.TextInput(attrs={
               'placeholder':'Email',
               'class':'form-control',
          })
     )

     password1 = forms.CharField(
          max_length=50,
          required=True,
          widget=forms.PasswordInput(
               attrs={
                    'placeholder':'Password',
                    'class':'form-control',
                    'data-toggle':'password',
                    'id':'password'
               }
          )
     )
     
     password2 = forms.CharField(
          max_length=50,
          required=True,
          widget=forms.PasswordInput(
               attrs={
                    'placeholder':'Password',
                    'class':'form-control',
                    'data-toggle':'password',
                    'id':'password'
               }
          )
     )

     class Meta:
          model = User
          fields = ['first_name','last_name','username','email','password1','password2']

class LoginForm(AuthenticationForm):
     username = forms.CharField(
         max_length=100,
         required=True,
         widget=forms.TextInput(
              attrs={'placeholder':'Username',
              'class':'form-control',
              
              }
         )
    )
     
     password = forms.CharField(
         max_length=100,
         required=True,
         widget=forms.PasswordInput(
              attrs={
                   'placeholder':'password',
                   'class':'form-control',
                   'id':'password',
                   'data-toggle':'password',
                   'name':'password'
              }
         )
    )
     

     remember_me = forms.BooleanField(required=False)

     class Meta:
         model = User
         fields = ['username','password','remember_me']



class PredictionForm(forms.Form):
    Areasqrft = forms.CharField(label='Area in sqrft', max_length=100)
    BHK = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)
    Bath = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)
    Location = forms.ChoiceField(choices=[('Location1', 'Location1'), ('Location2', 'Location2'), ('Location3', 'Location3')])



    

  
    