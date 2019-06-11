from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(initial=1)
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)