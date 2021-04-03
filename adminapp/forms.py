from django import forms
from authapp.forms import UsersRegistration, UsersProfileForm
from authapp.models import Users


class UserAdminRegistration(UsersRegistration):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'avatar', 'username', 'email', 'password1', 'password2', 'age')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegistration, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file'

class UserAdminUpdate(UsersProfileForm):
    def __init__(self, *args, **kwargs):
        super(UserAdminUpdate, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = False
        self.fields['username'].widget.attrs['readonly'] = False