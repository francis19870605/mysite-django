from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# 如果要将表单中的数据写入数据库表或者修改某些记录的值，表单继承ModelForm类；如果提交表单不对数据进行修改、继承Form类
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    # 声明本表单类所应用的数据类型(也就是表单的内容会写入哪个库那个表哪些字段)
    class Meta:
        model = User
        fields = ("username", "email")

    # 定义属性覆盖内部类Meta声明数据模型中的字段
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "photo")


# username作为唯一表示不能修改、所以只修改email
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
