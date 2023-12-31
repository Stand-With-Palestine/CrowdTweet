from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _


class PostToTwitterForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter some content',
            }
        ),
        label=_('Content')
    )
    media_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
                'accept': 'image/*, video/*',
            }
        ),
        label=_('Media File')
    )

    def __init__(self, *args, **kwargs):
        super(PostToTwitterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['media_file'].required = False


class LoginForm(AuthenticationForm):
    """
    Operator Login.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructs all the necessary attributes for OperatorLoginFormZ form
        Args:
            *args (): Extra list attributes.
            **kwargs (): Extra dictionary attributes.
        """
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        return super().clean()
