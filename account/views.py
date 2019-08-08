from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserInfoForm, UserForm
from .models import UserProfile, UserInfo
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def user_login(request):
    """
    用户登录验证
    :param request:
    :return:
    """
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        # 验证表单数据是否合法
        if login_form.is_valid():
            cd = login_form.cleaned_data
            # authenticate验证此用户是否为本项目用户以及密码的正确性、正确返回实例对象、错误返回None
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                # login函数以authenticate返回的对象作为参数、实现用户登录。
                login(request, user)
                return HttpResponse("Welcome You. You have been authenticated successfully.")
            else:
                return HttpResponse("Sorry. Your username or password is not right.")
        else:
            return HttpResponse("Invalid login")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'account/login.html', {"form": login_form})


def register(request):
    """
    用户注册
    :param request:
    :return:
    """

    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid():
            # save() 将表单数据保存到数据库 commit=False 数据没保存到数据库、仅生成了一个数据对象 目的是为了后边对密码的
            # 校验、校验通过后再写入数据库
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            # return HttpResponse("Successfully")
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return HttpResponse("Sorry. Your can not register.")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html',
                      {'form': user_form, 'profile': userprofile_form})


# 系统自带装饰器判断用户是否登录、如果没登录根据login_url参数跳转
@login_required()
def myself(request):
    """
    获取个人信息展示
    :param request:
    :return:
    """
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') \
        else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') \
        else UserInfo.objects.create(user=request.user)
    return render(request, 'account/myself.html',
                  {'user': request.user, 'userinfo': userinfo, 'userprofile': userprofile})


@login_required(login_url='account/login/')
def myself_edit(request):
    """
    编辑个人信息
    :param request:
    :return:
    """
    userprofile = UserProfile.objects.get(user=request.user) \
        if hasattr(request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) \
        if hasattr(request.user, 'userinfo') else UserInfo.objects.create(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school,
                                              "company": userinfo.company,
                                              "profession": userinfo.profession,
                                              "address": userinfo.address,
                                              "aboutme": userinfo.aboutme})
        return render(request, "account/myself_edit.html",
                      {"user_form": user_form,
                       "userprofile_form": userprofile_form,
                       "userinfo_form": userinfo_form})


@login_required(login_url='/account/login/')
def my_image(request):
    """
    头像上传和剪切插件
    :param request:
    :return:
    """
    if request.method == "POST":
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html')
