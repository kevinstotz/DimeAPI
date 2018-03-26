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
from django.conf.urls.static import static
from django.urls import register_converter, path
from django.contrib import admin
from django.conf.urls import url, include
from DimeAPI.converters import FileNameConverter
from DimeAPI.views.account.document.views import DocumentTypes, DocumentUpload, UserDocuments
from DimeAPI.views.account.history.views import DepositTransactionHistory, WithdrawTransactionHistory
from DimeAPI.views.account.tools.views import CountryView, CityView, StateView, ZipCodeView
from DimeAPI.views.account.userProfile.views import UserProfileView
from DimeAPI.views.deposit.braintree.views import BraintreeDepositToken, BraintreeDepositPaypalTransaction,\
    BraintreeDepositVisaMCTransaction
from DimeAPI.views.withdraw.braintree.views import BraintreeWithdrawToken, BraintreeWithdrawPaypalTransaction, \
    BraintreeWithdrawVisaMCTransaction
from DimeAPI.views.deposit.paypal.views import PaypalCreate, PaypalCapture, PaypalReturn
from DimeAPI.views.funds.UD10.views import UD10LineChart,  UD10PieChart,  UD10TableListChart,  UD10TableChart
from DimeAPI.views.register.views import RegisterUser, RegisterAffiliate, VerifyRegister
from DimeAPI.views.www.views import NewsLetterSubscribe, IndexPage, CoinNews, ContactUs
from DimeAPI.views.account.views import LoginUser, ForgotPassword, ResetPassword, LogoutUser, GetUserId
from DimeAPI.settings.base import MEDIA_ROOT, MEDIA_URL
register_converter(FileNameConverter, 'filenamePattern')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path(r'api/fund/ud10/linechart/',  UD10LineChart.as_view(), name="ud10LineChart"),
    path(r'api/fund/ud10/piechart/',  UD10PieChart.as_view(), name="ud10PieChart"),
    path(r'api/fund/ud10/tablechart/',  UD10TableChart.as_view(), name="ud10TableChart"),
    path(r'api/fund/ud10/tablelistchart/',  UD10TableListChart.as_view(), name="ud10TableListChart"),
    path(r'api/fund/ud10/coinnews/', CoinNews.as_view(), name="coinNews"),

    path(r'api/newsletter/', NewsLetterSubscribe.as_view(), name="newsLetterSubscribe"),
    path(r'api/contactus/', ContactUs.as_view(), name="contactus"),
    path(r'api/register/user/', RegisterUser.as_view({"post": "create"}), name="registerUser"),
    path(r'api/register/affiliate/', RegisterAffiliate.as_view({"post": "create"}), name="registerAffiliate"),

    path(r'api/account/documentupload/<filenamePattern:filename>/', DocumentUpload.as_view(), name="documentUpload"),
    path(r'api/account/documenttypes/', DocumentTypes.as_view(), name="documentTypes"),
    path(r'api/account/documents/', UserDocuments.as_view(), name="userDocuments"),
    path(r'api/account/history/', DepositTransactionHistory.as_view(), name="depositTransactionHistory"),
    path(r'api/account/history/deposit/', DepositTransactionHistory.as_view(), name="depositTransactionHistory"),
    path(r'api/account/history/withdraw/', WithdrawTransactionHistory.as_view(), name="withdrawTransactionHistory"),
    path(r'api/account/document/<int:pk>', UserDocuments.as_view(), name="deleteDocuments"),
    path(r'api/account/<slug:User_Id>/', UserProfileView.as_view(), name="userProfile"),
    path(r'api/account/', GetUserId.as_view(), name="getUserId"),

    path(r'account/logout', LogoutUser.as_view(), name="logoutUser"),
    path(r'account/login/', LoginUser.as_view(), name="loginUser"),

    path(r'api/deposit/paypal/captured/', PaypalCapture.as_view(), name="paypalCapture"),
    path(r'api/deposit/paypal/create/', PaypalCreate.as_view(), name="paypalCreate"),
    path(r'api/deposit/paypal/return/', PaypalReturn.as_view(), name="paypalReturn"),
    path(r'api/deposit/braintree/visamc/sale/', BraintreeDepositVisaMCTransaction.as_view(), name="braintreeDepositVisaMCTransaction"),
    path(r'api/deposit/braintree/paypal/sale/', BraintreeDepositPaypalTransaction.as_view(), name="braintreeDepositPaypalTransaction"),
    path(r'api/deposit/braintree/token/', BraintreeDepositToken.as_view(), name="braintreeDepositToken"),

    path(r'api/withdraw/braintree/visamc/sale/', BraintreeWithdrawVisaMCTransaction.as_view(), name="braintreeWithdrawVisaMCTransaction"),
    path(r'api/withdraw/braintree/paypal/sale/', BraintreeWithdrawPaypalTransaction.as_view(), name="braintreeWithdrawPaypalTransaction"),
    path(r'api/withdraw/braintree/token/', BraintreeWithdrawToken.as_view(), name="braintreeWithdrawToken"),

    path(r'api/register/verify/<slug:Authorization_Code>', VerifyRegister.as_view(), name="verifyRegisterUser"),
    path(r'api/forgot-password/', ForgotPassword.as_view(), name="forgotPassword"),
    path(r'api/reset-password/', ResetPassword.as_view(), name="resetPassword"),

    path(r'api/country/', CountryView.as_view(), name="countryList"),
    path(r'api/city/<slug:State>/', CityView.as_view(), name="cityList"),
    path(r'api/state/<slug:Country>/', StateView.as_view(), name="stateList"),
    path(r'api/zipcode/<slug:City>/', ZipCodeView.as_view(), name="zipcodeList"),

    path(r'', IndexPage.as_view(), name="indexPage")
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

# admin.site.__class__ = AdminSiteOTPRequired
admin.autodiscover()
