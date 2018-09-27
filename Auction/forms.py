from django import forms
from .models import Auction

class AuctionCreateForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "price", "deadline"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={'type': "datetime-local", "pattern": "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}"})
            # /!\ not tested with an actual datepicker /!\
            # This is the tricky part : on Chrome/Opera, Edge and most mobile browsers the input type will be datetime-local. 
            # On Firefox datetime-local is not supported, and the type will fall back to text. But we can "hint" the input with a pattern. 
            # Booo Firefox :(
            # More info on this MDN article : https://developer.mozilla.org/fr/docs/Web/HTML/Element/Input/datetime-local
        }
        help_texts = {
            "deadline": "Input format : yyyy-MM-dd hh:mm"
        }
