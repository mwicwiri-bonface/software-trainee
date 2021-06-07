from django.urls import path
from . import views
from account.decorators import applicant_required

urlpatterns = [
    path('feedback-api/', views.feedback_api, name="feedback_api"),
    path('applied-jobs/', views.applied_jobs, name="applied_jobs"),
    path('apply-job/', views.apply_job, name="apply_job"),
    path('search/', views.search, name="search"),
    path('feedback/', views.feedback, name="feedback"),
    path('faq/', views.faq, name="faq"),
    path('password_change/', views.password_change, name="password_change"),
    path('change_password/', views.change_password, name="change_password"),
    path('profile/', views.profile_main, name="profile_main"),
    path('profiles/', views.profile, name="profile"),
    path('logout/', views.log_out, name="logout"),
    path('sign-up/', views.ApplicantSignUpView.as_view(), name="sign_up"),
    path('verify/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='verify'),
    path('login/', views.login, name="login"),
    path('', applicant_required(views.Home.as_view()), name="index"),
]
