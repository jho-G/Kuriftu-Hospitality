from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group

from .models import User

_AUTH_WIDGET_ATTRS = {
    "class": "auth-input",
    "style": "width:100%;box-sizing:border-box;padding:0.6rem 0.75rem;border:1px solid rgba(45,38,32,0.22);border-radius:8px;font-size:1rem;",
}


class SiteLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(_AUTH_WIDGET_ATTRS)
        self.fields["password"].widget.attrs.update(_AUTH_WIDGET_ATTRS)


class SignUpForm(UserCreationForm):
    """Server-rendered registration (mirrors API RegisterSerializer fields)."""

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    phone = forms.CharField(max_length=32, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(attrs=_AUTH_WIDGET_ATTRS),
            "email": forms.EmailInput(attrs=_AUTH_WIDGET_ATTRS),
            "first_name": forms.TextInput(attrs=_AUTH_WIDGET_ATTRS),
            "last_name": forms.TextInput(attrs=_AUTH_WIDGET_ATTRS),
            "phone": forms.TextInput(attrs=_AUTH_WIDGET_ATTRS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(_AUTH_WIDGET_ATTRS)
        self.fields["password2"].widget.attrs.update(_AUTH_WIDGET_ATTRS)

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.phone = self.cleaned_data.get("phone", "")
        if commit:
            user.save()
            group, _ = Group.objects.get_or_create(name="Registered Guest")
            user.groups.add(group)
        return user
