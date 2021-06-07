from django.conf import settings
from django.contrib.auth import logout, authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import NoReverseMatch
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import ListView, CreateView
import json
from account.decorators import applicant_required
from .models import PostJob, Applicant, Job, JobAllocation, Feedback
from .forms import ApplicantSignUpForm, ApplicantProfileForm, ApplicantForm, FeedbackForm
from account.tokens import account_activation_token
from django.db.models import Q

from account.models import CustomUser


def error_404(request, exception):
    # View code here...
    return render(request, 'applicant/errors-404.html')


def error_403(request, exception):
    # View code here...
    return render(request, 'applicant/errors-403.html')


def error_500(request):
    # View code here...
    return render(request, 'applicant/errors-500.html')


def error_503(request, exception):
    # View code here...
    return render(request, 'applicant/errors-503.html')


class Home(ListView):
    model = PostJob
    template_name = 'applicant/index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['object_list'] = self.object_list.filter(is_active=True, is_archived=False, is_applied=False)
        return context


def login(request):
    if request.method == "POST":
        remember = request.POST.get('remember')
        if remember == "remember-me":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            request.session.set_expiry(0)
        if user is not None:
            if not user.is_active and user.is_applicant and not user.is_archived:
                if user.is_verified:
                    messages.info(request,
                                  "your email is verified, but your account is "
                                  "inactive. Check your mail for notification.")
                else:
                    messages.info(request,
                                  "your email is not verified, verify your email.")
            elif user.is_active and user.is_applicant and not user.is_archived:
                if user.is_verified:
                    auth_login(request, user)
                    user = request.user.get_full_name
                    messages.success(request, f"Hi {user}, welcome to Software Trainee Applicant's Portal.")
                    try:
                        return redirect(request.GET.get('next', 'applicant:index'))
                    except (NoReverseMatch, ImproperlyConfigured):
                        return redirect("applicant:index")
                else:
                    messages.info(request,
                                  "you've registered, but your email is not verified, verify your email and try again.")
            else:
                messages.info(request, f"Hi {user.get_full_name}, "
                                       f"you can't login here, this login page is for Applicants only.")
                logout(request)
                try:
                    return redirect(request.GET.get('next', ''))
                except (NoReverseMatch, ImproperlyConfigured):
                    return redirect("applicant:login")
        else:
            messages.info(request, "your email or password is incorrect. Please check.")
            try:
                return redirect(request.GET.get('next', ''))
            except (NoReverseMatch, ImproperlyConfigured):
                return redirect("applicant:login")
    return render(request, 'account/auth-login.html')


class ApplicantSignUpView(CreateView):
    form_class = ApplicantSignUpForm
    template_name = "account/auth-register.html"

    def get_form_kwargs(self):
        kwargs = super(ApplicantSignUpView, self).get_form_kwargs()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=200)

    def form_valid(self, form):
        name = form.instance.first_name
        last = form.instance.last_name
        username = form.instance.email
        username = username.lower()
        form.instance.email = username
        if '@gmail.com' in username:
            username = username.replace('@gmail.com', '')
        elif '@yahoo.com' in username:
            username = username.replace('@yahoo.com', '')
        elif '@hotmail.com' in username:
            username = username.replace('@hotmail.com', '')
        elif '@live.com' in username:
            username = username.replace('@live.com', '')
        elif '@msn.com' in username:
            username = username.replace('@msn.com', '')
        elif '@passport.com' in username:
            username = username.replace('@passport.com', '')
        elif '@outlook.com' in username:
            username = username.replace('@outlook.com', '')
        form.instance.username = username
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        current_site = get_current_site(self.request)
        to_email = form.cleaned_data.get('email')
        subject = f'Software Trainee Applicant Email Verification.'
        msg_plain = render_to_string('applicant/emails/email.txt', {'user_name': user.get_full_name, })
        msg_html = render_to_string('applicant/emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, msg_plain, 'Varal Software Trainee', [to_email], html_message=msg_html)
        messages.success(self.request, 'Please Confirm your email to complete registration.')
        data = {
            'status': True,
            'message': f"Hi {name} {last}, your account has been created successfully verify your email.",
        }
        return JsonResponse(data)


class VerifyEmail(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Applicant.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_verified:
                messages.info(request, "you've already confirmed your email.")
            elif not user.is_verified:
                user.is_verified = True
                user.save()
                messages.info(request, "You've successfully verified your email. use your email to login")
            return redirect('applicant:login')
        else:
            data = {
                'message': 'The confirmation link was invalid, possibly because it has already been used.'
            }
            return JsonResponse(data)


def log_out(request):
    logout(request)
    messages.info(request, f"You've logged out successfully.")
    return redirect('applicant:index')


@applicant_required
def profile(request):
    data = {}
    if request.method == "POST":
        p_form = ApplicantProfileForm(request.POST, request.FILES, instance=request.user.applicant.applicantprofile)
        form = ApplicantForm(request.POST, instance=request.user.applicant)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            data['message'] = "Your Profile has been updated!"
            return JsonResponse(data)
        else:
            data['info'] = "sorry, this form is invalid!"
            data['form'] = form.errors
            data['p_form'] = p_form.errors
            return JsonResponse(data)
    else:
        p_form = ApplicantProfileForm(instance=request.user.applicant.applicantprofile)
        form = ApplicantForm(request.POST, instance=request.user.applicant)

    data['form'] = form.errors
    data['p_form'] = p_form.errors
    return JsonResponse(data)


@applicant_required
def profile_main(request):
    if request.method == "POST":
        p_form = ApplicantProfileForm(request.POST, request.FILES, instance=request.user.applicant.applicantprofile)
        form = ApplicantForm(request.POST, instance=request.user.applicant)
    else:
        p_form = ApplicantProfileForm(instance=request.user.applicant.applicantprofile)
        form = ApplicantForm(request.POST, instance=request.user.applicant)
    context = {
        'p_form': p_form,
        'form': form,
    }
    return render(request, 'applicant/profile.html', context)


@applicant_required
def faq(request):  # Not Done
    context = {}
    return render(request, 'applicant/faq.html', context)


@applicant_required
def change_password(request):
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            context['message'] = 'Your password was successfully updated!'
            return JsonResponse(context)
        else:
            context['info'] = 'Please correct the errors below.'
    else:
        form = PasswordChangeForm(request.user)
    context['form'] = form.errors
    return JsonResponse(context)


@applicant_required
def password_change(request):
    return render(request, 'applicant/change-password.html')


@applicant_required
def feedback(request):
    return render(request, 'applicant/feedback.html')


@applicant_required
def feedback_api(request):
    data = {}
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.applicant = request.user.applicant
            admin = CustomUser.objects.filter(is_staff=True, is_superuser=True, is_active=True).first()
            instance.admin = admin
            if Feedback.objects.filter(subject=instance.subject, message=instance.message, applicant=instance.applicant, admin=admin).exists():
                data['info'] = "You've already sent this feedback, thank you."
                data['form'] = {'subject': "feedback with this title already exists"}
                data['form'] = {'message': "feedback with this message already exists"}
            elif Feedback.objects.filter(subject=instance.subject, applicant=instance.applicant, admin=admin).exists():
                data['info'] = "You've already sent this feedback, thank you."
                data['form'] = {'subject': "feedback with this title already exists"}
            elif Feedback.objects.filter(message=instance.message, applicant=instance.applicant, admin=admin).exists():
                data['info'] = "You've already sent this feedback, thank you."
                data['form'] = {'message':  "feedback with this message already exists"}
            else:
                instance.save()
                data['message'] = "Feedback has been sent. Thank you"
        else:
            data['info'] = "sorry, Form is invalid"
    else:
        form = FeedbackForm
        data['form'] = form.errors
    return JsonResponse(data)


@applicant_required
def search(request):
    q = request.GET.get('q')
    context = {}
    if q != "":
        search_jobs = Job.objects.filter(Q(name__icontains=q) or Q(instructions__icontains=q))
        jobs = []
        for search_job in search_jobs:
            if PostJob.objects.filter(name=search_job).exists():
                job = {'name': search_job.name, 'slug': search_job.slug,
                       'description': search_job.description, 'exists': True}
                jobs.append(job)
        context['jobs'] = jobs
    context['q'] = q
    return render(request, 'applicant/search.html', context)


@applicant_required
def apply_job(request):
    data = json.loads(request.body.decode("utf-8"))
    slug = data['slug']
    context = {}
    job_applied = Job.objects.filter(slug=slug).first()
    if job_applied:
        if JobAllocation.objects.filter(job=job_applied, email=request.user.applicant.email).exists():
            context['info'] = f"Sorry you've already applied for this job"
        else:
            JobAllocation.objects.create(job=job_applied, email=request.user.applicant.email,
                                         name=request.user.applicant.get_full_name)
            context['message'] = f"Application for {job_applied.name}, has been sent successfully"
    else:
        context['info'] = f"Sorry Job does not exists probably it's no longer on offer"
    return JsonResponse(context, safe=False)


@applicant_required
def applied_jobs(request):
    jobs = JobAllocation.objects.filter(email=request.user.applicant.email)
    context = {
        'jobs': jobs,
    }
    return render(request, 'applicant/applied-jobs.html', context)
