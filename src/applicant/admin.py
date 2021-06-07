from django.contrib import admin

from .models import Applicant, ApplicantProfile, Feedback, Job, PostJob, JobAllocation, JobCategory
from django.contrib import messages
from django.utils.translation import ngettext


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    list_filter = ('is_active', 'is_archived', 'updated', 'created')

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Applicant has successfully been marked as active.',
            '%d Applicants have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Approve Applicant"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Applicant has been archived successfully.',
            '%d Applicants have been archived successfully.',
            updated,
        ) % updated, messages.INFO)

    make_inactive.short_description = "Archive Applicant"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'nationality', 'image', 'gender', 'is_active', 'created', 'updated')
    list_filter = ('nationality', 'gender', 'is_active', 'updated', 'created')
    search_fields = ('phone_number',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, ngettext(
            '%d Profile has been successfully marked as active.',
            '%d Profiles have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Mark selected Profiles as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, ngettext(
            '%d Profile has been successfully marked as inactive.',
            '%d Profiles has been successfully marked as inactive.',
            updated,
        ) % updated)

    make_inactive.short_description = "Mark selected Profiles as inactive"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'created')
    list_filter = ('created',)
    search_fields = ('subject', 'message',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    list_filter = ('updated', 'created')
    search_fields = ('name',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class PostJobAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructions', 'sample', 'sheet', 'is_archived', 'is_active', 'created', 'updated')
    list_filter = ('is_archived', 'is_active', 'updated', 'created')
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, is_archived=False)
        self.message_user(request, ngettext(
            '%d Job has been successfully marked as active.',
            '%d Job have been successfully marked as active.',
            updated,
        ) % updated, messages.SUCCESS)

    make_active.short_description = "Mark selected Jobs as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, ngettext(
            '%d Job has been successfully marked as inactive.',
            '%d Job has been successfully marked as inactive.',
            updated,
        ) % updated)

    make_inactive.short_description = "Mark selected Jobs as inactive"

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class JobAllocationAdmin(admin.ModelAdmin):
    list_display = ('job', 'email', 'name', 'created', 'updated')
    list_filter = ('updated', 'created')
    search_fields = ('email', 'name',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    list_filter = ('created',)
    search_fields = ('name',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True


admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(ApplicantProfile, ApplicantProfileAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(PostJob, PostJobAdmin)
admin.site.register(JobAllocation, JobAllocationAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
