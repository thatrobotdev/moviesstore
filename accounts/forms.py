from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import Profile

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join(
            [f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]
        ))

class CustomUserCreationForm(UserCreationForm):
    # Add a new field for the security answer.
    security_answer = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="What is your mother's maiden name? (Case sensitive)"
    )

    class Meta(UserCreationForm.Meta):
        # Include the new field in the form’s fields list.
        fields = UserCreationForm.Meta.fields + ('security_answer',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Apply styling and remove help texts for consistency.
        for fieldname in ['username', 'password1', 'password2', 'security_answer']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit)
        security_answer = self.cleaned_data.get('security_answer')
        # Store the security answer in the Profile model
        profile = Profile.objects.create(user=user, security_answer=security_answer)
        return user
