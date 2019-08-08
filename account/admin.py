from django.contrib import admin
from .models import UserProfile, UserInfo


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    # 列出列表中的项目
    list_display = ("user", "birth", "phone")
    # 网页右边filter的显示过滤列表
    list_filter = ("phone",)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "company", "profession", "address", "aboutme", "photo")
    list_filter = ("school", "company", "profession")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
