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
from django.conf.urls import url
from django.conf.urls import include
from two_factor.admin import AdminSiteOTPRequired
from DimeAPI.views import LoginUser, RegisterUser, ReadHistory, NewsLetterSubscribe, RegisterAffiliate, UserProfileView, CountryView, CityView, StateView, ZipCodeView, \
    VerifyRegister, ContactUs, DimeLineChart, DimePieChart, DimeTableChart, IndexPage, ForgotPassword, ResetPassword, LogoutUser, GetUserId, DimeTableListChart, DocumentUpload, \
    CoinNews, DocumentTypes, UserDocuments



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path(r'api/dime/linechart/', DimeLineChart.as_view(), name="dimeLineChart"),
    path(r'api/dime/piechart/', DimePieChart.as_view(), name="dimePieChart"),
    path(r'api/dime/tablechart/', DimeTableChart.as_view(), name="dimeTableChart"),
    path(r'api/dime/tablelistchart/', DimeTableListChart.as_view(), name="dimeTableListChart"),
    path(r'api/dime/coinnews/', CoinNews.as_view(), name="coinNews"),


    path(r'history/index', ReadHistory.as_view(), name="readHistory"),
    path(r'api/newsletter/', NewsLetterSubscribe.as_view(), name="newsLetterSubscribe"),
    path(r'api/contactus/', ContactUs.as_view(), name="contactus"),
    path(r'api/register/', RegisterUser.as_view({"post": "create"}), name="registerUser"),
    path(r'api/affiliate/register/', RegisterAffiliate.as_view({"post": "create"}), name="registerAffiliate"),
    path(r'account/login/', LoginUser.as_view(), name="loginUser"),
    path(r'api/account/documentupload/<slug:filename>/', DocumentUpload.as_view(), name="documentUpload"),

    path(r'api/account/documenttypes/', DocumentTypes.as_view(), name="documentTypes"),
    path(r'api/account/documents/', UserDocuments.as_view(), name="userDocuments"),

    path(r'api/account/', GetUserId.as_view(), name="getUserId"),
    path(r'api/register/verify/<slug:Authorization_Code>', VerifyRegister.as_view(), name="verifyRegisterUser"),
    path(r'account/logout', LogoutUser.as_view(), name="logoutUser"),
    path(r'api/forgot-password/', ForgotPassword.as_view(), name="forgotPassword"),
    path(r'api/reset-password/', ResetPassword.as_view(), name="resetPassword"),
    path(r'api/user/<slug:User_Id>/', UserProfileView.as_view(), name="userProfile"),

    path(r'api/country/', CountryView.as_view(), name="countryList"),
    path(r'api/city/<slug:State>/', CityView.as_view(), name="cityList"),
    path(r'api/state/<slug:Country>/', StateView.as_view(), name="stateList"),
    path(r'api/zipcode/<slug:City>/', ZipCodeView.as_view(), name="zipcodeList"),

    path(r'', IndexPage.as_view(), name="indexPage"),
    # path(r'^auth/status/(?P<User_Id>([0-9]+))$', UserLoginStatus.as_view(), name="userLoginStatus"),

]
# admin.site.__class__ = AdminSiteOTPRequired
admin.autodiscover()
