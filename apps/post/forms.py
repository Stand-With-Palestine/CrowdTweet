from django import forms
from crispy_forms.helper import FormHelper


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

    def __init__(self, *args, **kwargs):
        super(PostToTwitterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
