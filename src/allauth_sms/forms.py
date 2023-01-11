from django import forms

from .models import OTP


class LoginForm(forms.ModelForm):
    code = forms.CharField()

    class Meta:
        model = OTP
        fields = ("phone",)

    def __init__(self, show_code=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if show_code or "code" in self.data:
            self.fields["phone"].widget.attrs["readonly"] = True
            self.fields["code"].widget.attrs["autofocus"] = True
        else:
            self.fields["phone"].widget.attrs["autofocus"] = True
            del self.fields["code"]
