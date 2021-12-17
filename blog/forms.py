from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=25)
    to = forms.EmailField(max_length=25)
    comments = forms.CharField(required=False, widget=forms.Textarea)
