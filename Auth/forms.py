from django.contrib.auth.models import User
from django.forms import Form, ModelForm, PasswordInput, CharField

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': PasswordInput
        }
    
class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
    