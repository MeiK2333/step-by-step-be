#coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from Org import views as Org_views
from API import views as API_views
from Step import views as Step_views

urlpatterns = [
    url(r'^$', Step_views.index, name='index'),
    url(r'^API/GetOrgList', API_views.GetOrgList, name='GetOrgList'), #获得Org列表
    url(r'^API/Login', Org_views.Login, name='Login'), #登录
    url(r'^API/Logout', Org_views.Logout, name='Logout'), #注销
    url(r'^API/Org/CreateOrgAdmin', Org_views.CreateOrgAdmin, name='CreateOrgAdmin'), #创建Org管理员
    url(r'^API/Org/GetOrgAdmin', Org_views.GetOrgAdmin, name='GetOrgAdmin'), #获得管理员列表
    url(r'^API/Org/UpdateOrgAdmin', Org_views.UpdateOrgAdmin, name='UpdateOrgAdmin'), #修改管理员信息
    url(r'^API/Org/DeleteOrgAdmin', Org_views.DeleteOrgAdmin, name='DeleteOrgAdmin'), #删除管理员
    url(r'^admin/', include(admin.site.urls)),
]
