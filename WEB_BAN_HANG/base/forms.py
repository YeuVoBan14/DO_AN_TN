from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
GENDER_CHOICES = (
    (True, 'Male'),
    (False, 'Female'),
)
#for register new user(customer)
class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Username"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Enter Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Confirm Password"}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
#for edit user(customer)
class UserForm(ModelForm):
    birth = forms.DateField(widget=forms.DateInput(attrs= {'type':'date', 'class':'form-control form-inline','placeholder':'Select date of birth'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-inline', 'style': 'margin-left: 10px;'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Email Address'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    avatar = forms.ImageField(widget=forms.FileInput(),required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'birth', 'gender', 'email', 'phone', 'avatar']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

            
        

