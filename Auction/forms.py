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

class ConfAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "price", "deadline"]
        widgets = {
            "title": forms.HiddenInput(), 
            "description": forms.HiddenInput(), 
            "price": forms.HiddenInput(), 
            "deadline": forms.HiddenInput(), 
        }

class AuctionEditForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "price", "deadline"]
        widgets = {
            "title": forms.DateTimeInput(attrs={'readonly': 'readonly'}),
            "price": forms.DateTimeInput(attrs={'readonly': 'readonly'}),
            "deadline": forms.DateTimeInput(attrs={'readonly': 'readonly'})
        }
        help_texts = {
            "deadline": "Input format : yyyy-MM-dd hh:mm"
        }

class BidForm(forms.Form):
    price = forms.FloatField(label="Your bid", min_value=0, widget=forms.NumberInput(attrs={'step': 0.01}))
    version = forms.IntegerField(min_value=0, widget=forms.NumberInput, label="")

