from autoslug import AutoSlugField
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from account.models import CustomUser
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from account.models import Profile

TITLES = (
    (_('miss'), _('Miss.')),
    (_('mrs'), _('Mrs.')),
    (_('mr'), _('Mr.')),
    (_('dr'), _('Dr.')),
    (_('prof'), _('Prof.')),
)


class Job(models.Model):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(help_text="job description")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'MTO Job details'
        verbose_name_plural = 'MTO Job details'


class JobCategory(models.Model):
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=200)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Job Category'
        verbose_name_plural = 'Job Categories'


class PostJob(models.Model):
    name = models.OneToOneField(Job, on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    instructions = models.TextField(help_text="job instruction")
    sample = models.FileField(upload_to="applicant/%Y/%M", default="applicant/sample.pdf", help_text="job sample")
    sheet = models.URLField(max_length=200, help_text="Job output sheet (google sheet)")
    is_active = models.BooleanField(_('Active'), default=False, help_text=_('Activated, means job will be published'))
    is_archived = models.BooleanField(_('Archive'), default=False,
                                      help_text=_('Archived, means job will be Unpublished'))
    is_applied = models.BooleanField(_('Applied'), default=False,
                                     help_text=_('Means Job has been applied'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'MAL Requirements'
        verbose_name_plural = 'MAL Requirements'


class JobAllocation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, help_text="Job id")
    email = models.EmailField(help_text="Outsource Email Id")
    name = models.CharField(max_length=200, help_text="Outsource Name")
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.job}"


class Applicant(CustomUser):
    pass

    class Meta:
        verbose_name = 'Applicant'
        verbose_name_plural = 'Applicants'


class ApplicantProfile(Profile):
    user = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    title = models.CharField(
        choices=TITLES,
        default='dr',
        max_length=250,
    )

    class Meta:
        verbose_name = 'Applicant Profile'
        verbose_name_plural = 'Applicants Profile'


class Feedback(models.Model):
    slug = AutoSlugField(populate_from='subject')
    subject = models.CharField(max_length=200)
    message = models.TextField(help_text="Feedback sent by applicant to admin")
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="admin", null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'


# automatically creating profile for an applicant
@receiver(post_save, sender=Applicant)
def create_applicant_profile(sender, instance, created, **kwargs):
    if created:
        ApplicantProfile.objects.create(user=instance)
        instance.applicantprofile.save()


# automatically sends mail to applicant when their account is disabled
@receiver(pre_save, sender=Applicant, dispatch_uid='deactivate')
def deactivate(sender, instance, **kwargs):
    if instance.is_archived and Applicant.objects.filter(pk=instance.pk, is_archived=False).exists():
        subject = 'Account Deactivation'
        message = '%s your account is now inactive' % instance.get_full_name
        send_mail(subject, message, 'Varal Software Trainee', [instance.email], fail_silently=False)


# automatically sends mail to applicant when they click apply button
@receiver(post_save, sender=JobAllocation)
def job_allocation(sender, instance, created, **kwargs):
    if created:
        print(instance)
        to_email = instance.email
        subject = f'Job Instructions for {instance.job.name}.'
        msg_plain = render_to_string('applicant/emails/job_application.txt', {'name': instance.name, })
        msg_html = render_to_string('applicant/emails/job_application.html', {
            'name': instance.name,
            'instance': instance,
        })
        send_mail(subject, msg_plain, 'Software Trainee', [to_email], html_message=msg_html)


# automatically sends mail to applicant when they click apply button
@receiver(post_save, sender=Feedback)
def feedback(sender, instance, created, **kwargs):
    if created:
        print(instance.admin.email)
        to_email = instance.admin.email
        subject = instance.subject
        msg_plain = render_to_string('applicant/emails/feedback.txt', {'message': instance.message, })
        msg_html = render_to_string('applicant/emails/feedback.html', {
            'instance': instance,
        })
        send_mail(subject, msg_plain, 'Varal Software Trainee', [to_email], html_message=msg_html)
