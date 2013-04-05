from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    subject = forms.CharField(max_length=20, required=False)
    message = forms.CharField(widget=forms.Textarea)
