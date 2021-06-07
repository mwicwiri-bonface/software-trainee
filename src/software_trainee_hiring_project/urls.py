from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="account/auth-forgot-password.html",
             html_email_template_name="account/email/password-reset.html",
             subject_template_name="account/email/password_reset_subject.txt",
         ),
         name="password_reset"),
    path('reset_password_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="account/password-reset-done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/auth-reset-password.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password-reset-complete.html"),
         name="password_reset_complete"),
    # ============================== Password Reset urls end ===========================================
    path('admin/', admin.site.urls),
    path('', include(('applicant.urls', 'applicant'), namespace="applicant")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'applicant.views.error_404'
handler500 = 'applicant.views.error_500'
handler403 = 'applicant.views.error_403'
handler400 = 'applicant.views.error_503'
