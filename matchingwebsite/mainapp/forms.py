import datetime
from django import forms
from mainapp.models import Hobby, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

        def save(self, commit=True):
            user = super(SignUpForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

            return user

class EditUserForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )

class EditProfileForm(forms.ModelForm):
    dob = forms.DateField()
    gender = forms.ChoiceField(widget=forms.RadioSelect(), choices=Profile.GENDERS)
    image = forms.ImageField(widget=forms.FileInput, required=False)
    hobbies = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Hobby.HOBBY_CHOICES, required=False)
    
    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=False)
        profile.dob = self.cleaned_data['dob']
        profile.gender = self.data.get('gender')
        profile.image = self.cleaned_data['image']
        # Checked list of hobbies as stored as a list of strings         
        hobbies = self.data.getlist('hobbies')

        profile.hobbies.clear()
        for hobby in hobbies:
            hobby_obj = Hobby.objects.get(name=hobby)
            profile.hobbies.add(hobby_obj)
        
        if commit:
            profile.save()
        return profile

    class Meta:
        model = Profile
        fields = (
            'dob',
            'gender',
            'image',
            'hobbies',
        )
