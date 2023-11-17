from django.contrib import admin
from django.urls import path
from toxicscan import views

urlpatterns = [
    path('scanpage/',views.scanpage,name="scanpage"),
    path('inputdata/',views.inputdata,name="inputdata"),
    path('inputimage/',views.inputimage,name="inputimage"),
    path('loginpage/',views.loginpage,name="loginpage"),
    path('saveuser/',views.saveuser,name="saveuser"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    ]
