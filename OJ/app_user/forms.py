from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20)
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput, min_length=6)
    student_id = forms.CharField(max_length=9, min_length=7)
    real_name = forms.CharField(max_length=16)

    def pwd_validate(self, p1, p2):
        return p1 == p2


class LoginForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20)
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20)

    def pwd_validate(self, p1, p2):
        return p1 == p2
