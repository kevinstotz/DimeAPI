from django.contrib import admin
from DimeAPI.models import CustomUser, Register, UserAgent, Fund, FundRebalanceDate,  NewsLetter, \
    Xchange, Notification, EmailTemplate, EmailAddress, Name, Network, PasswordReset, NameType, \
    RegisterStatus, NotificationStatus, EmailAddressStatus, NotificationType, PasswordResetStatus, UserStatus


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser)
admin.site.register(Fund)
admin.site.register(FundRebalanceDate)
admin.site.register(EmailAddress)
admin.site.register(EmailAddressStatus)
admin.site.register(EmailTemplate)
admin.site.register(Name)
admin.site.register(NameType)
admin.site.register(Network)
admin.site.register(NewsLetter)
admin.site.register(Notification)
admin.site.register(NotificationStatus)
admin.site.register(NotificationType)
admin.site.register(PasswordReset)
admin.site.register(PasswordResetStatus)
admin.site.register(Register)
admin.site.register(RegisterStatus)
admin.site.register(UserAgent)
admin.site.register(UserStatus)
admin.site.register(Xchange)

