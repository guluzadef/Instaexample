from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from custom_user.models import MyUser
from .models import Post,CommentPost,Socialsetting,Contactform


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                error_messages={
                                    "required": "Bu xana doldurulmalidir"})
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                help_text=_("Enter the same password as above, for verification."),
                                error_messages={
                                    "required": "Bu xana doldurulmalidir"})

    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))

    class Meta:
        model = MyUser

        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

        }

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }

    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        }

    ))


class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "image": forms.FileInput(attrs={
                "class": "dropify"
            })

        }
class CommentForm(forms.ModelForm):
    class Meta:
        model=CommentPost
        fields=["comment"]



class SocialForm(forms.ModelForm):
    class Meta:
        model=Socialsetting
        fields=["website","facebook","twitter"]
        widgets = {
            "website": forms.TextInput(attrs={

                "class": "form-control"
            }),
            "facebook": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "twitter": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }



class   ForgetPass(forms.Form):
    email=forms.EmailField()


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    verify_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        verify_password = self.cleaned_data.get("verify_password")
        if new_password != verify_password:
            raise forms.ValidationError("Not equal")


class Contact(forms.ModelForm):
   class Meta:
       model=Contactform
       fields=["name","email","message"]
       widgets = {
           "name": forms.TextInput(attrs={

               "class": "form-control"
           }),
           "email": forms.EmailInput(attrs={
               "class": "form-control"
           }),
           "message": forms.TextInput(attrs={
               "class": "form-control"
           }),
       }


