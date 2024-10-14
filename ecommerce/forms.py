from allauth.account.forms import LoginForm, SignupForm

input_css_class = "form-control"


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,  **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class

