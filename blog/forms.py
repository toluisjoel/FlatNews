from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=225)
    email = forms.EmailField(max_length=225)
    to = forms.EmailField(max_length=225)
    comments = forms.CharField(required=False, widget=forms.Textarea)
