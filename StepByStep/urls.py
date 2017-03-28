#coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from Org import views as Org_views
from API import views as API_views
from Step import views as Step_views

urlpatterns = [
    url(r'^$', Step_views.index, name='index'),
    url(r'^API/GetOrgList', API_views.GetOrgList, name='GetOrgList'), #获得Org列表
    url(r'^API/GetStepList', API_views.GetStepList, name='GetStepList'), #获得指定Org的Step列表
    url(r'^API/Login', Org_views.Login, name='Login'), #登录
    url(r'^API/Logout', Org_views.Logout, name='Logout'), #注销
    url(r'^API/GetUserStepList', API_views.GetUserStepList, name='GetUserStepList'), #获取某人参加的所有计划
    url(r'^API/GetStepUser', API_views.GetStepUser, name='GetStepUser'), #获取某计划的参与用户

    url(r'^API/Org/CreateOrgAdmin', Org_views.CreateOrgAdmin, name='CreateOrgAdmin'), #创建Org管理员
    url(r'^API/Org/GetOrgAdmin', Org_views.GetOrgAdmin, name='GetOrgAdmin'), #获得管理员列表
    url(r'^API/Org/UpdateOrgAdmin', Org_views.UpdateOrgAdmin, name='UpdateOrgAdmin'), #修改管理员信息
    url(r'^API/Org/DeleteOrgAdmin', Org_views.DeleteOrgAdmin, name='DeleteOrgAdmin'), #删除管理员
    url(r'^API/Org/CreateOrg', Org_views.CreateOrg, name='CreateOrg'), #创建Org
    url(r'^API/Org/UpdateOrg', Org_views.UpdateOrg, name='UpdateOrg'), #修改Org
    url(r'^API/Org/DeleteOrg', Org_views.DeleteOrg, name='DeleteOrg'), #删除Org

    url(r'^API/Step/CreateStep', Step_views.CreateStep, name='CreateStep'), #新建计划
    url(r'^API/Step/UpdateStep', Step_views.UpdateStep, name='UpdateStep'), #修改计划
    url(r'^API/Step/DeleteStep', Step_views.DeleteStep, name='DeleteStep'), #删除计划
    url(r'^API/Step/AddStepUser', Step_views.AddStepUser, name='AddStepUser'), #为计划添加用户
    url(r'^API/Step/DelStepUser', Step_views.DelStepUser, name='DelStepUser'), #在计划中删除用户
    url(r'^admin/', include(admin.site.urls)),
]
