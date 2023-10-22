from django import forms


class PostToTwitterForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter some content'
            }
        )
    )
    media_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file'
            }
        )
    )
