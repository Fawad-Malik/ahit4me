from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name',
            'autofocus': 'autofocus'
        })
    )
    email = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email'
        }),
        help_text='so that we can get back to you.'
    )
    message = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message',
            'rows': 4,
            'style': 'height:unset'
        })
    )
