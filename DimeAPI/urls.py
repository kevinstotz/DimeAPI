"""DimeAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls  import url
from django.conf.urls import include
from two_factor.admin import AdminSiteOTPRequired
from DimeAPI.views import LoginUser, RegisterUser, DimeIndex, ReadHistory, NewsLetterSubscribe,\
    VerifyRegister, IndexPage, Dime, DimePieChart
admin.autodiscover()
# admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path(r'api/dime/index', DimeIndex.as_view(), name="dimeIndex"),
    path(r'api/dime/', Dime.as_view(), name="dime"),
    path(r'api/dime/piechart/', DimePieChart.as_view(), name="dimePieChart"),
    path(r'history/index', ReadHistory.as_view(), name="readHistory"),
    path(r'api/newsletter', NewsLetterSubscribe.as_view(), name="newsLetterSubscribe"),
    path(r'api/register/', RegisterUser.as_view({"post": "create"}), name="registerUser"),
    path(r'account/login/', LoginUser.as_view(), name="loginUser"),
    path(r'api/register/verify/<slug:Authorization_Code>', VerifyRegister.as_view(), name="verifyRegisterUser"),
    # path(r'', IndexPage.as_view(), name="indexPage"),
    # path(r'^auth/status/(?P<User_Id>([0-9]+))$', UserLoginStatus.as_view(), name="userLoginStatus"),
    # path(r'^SES/v1/auth/logout', LogoutUser.as_view(), name="logoutUser"),
    # path(r'^SES/v1/auth/forgotPassword/', ForgotPassword.as_view(), name="forgotPassword"),
    # path(r'^SES/v1/auth/resetPassword/(?P<Authorization_Code>([a-z]+))$', ResetPassword.as_view(),
        # name="resetPassword"),
    # path(r'^SES/v1/key/(?P<ApiKey>([0-9]+))/$', ReadTemperature.as_view(), name="readTemperature"),
    # path(r'^SES/v1/user/(?P<User_Id>([0-9]+))$', UserInfo.as_view(), name="userInfo")
]
# path(r'^SES/v1/auth/login/', Login.as_view(), name="login"),
