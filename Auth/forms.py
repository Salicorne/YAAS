from django.contrib.auth.models import User
from django.forms import ModelForm, PasswordInput

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets= {
            'password': PasswordInput
        }
    
