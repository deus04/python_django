from django.forms import ModelForm
from .models import Profile


class ProfileAvatarForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)