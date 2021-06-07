from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Applicant, ApplicantProfile, Feedback


class ApplicantSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Applicant
        fields = ['last_name', 'first_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_applicant = True
        user.is_active = False
        if commit:
            user.save()
        return user


class ApplicantProfileForm(ModelForm):
    class Meta:
        model = ApplicantProfile
        fields = ['image', 'gender', 'phone_number', 'nationality', 'title', 'bio']


class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['last_name', 'first_name', 'email']


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
