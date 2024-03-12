from django.contrib import admin
from .models import Student, Gallery, Testimonial, Event, Contact, MediaCoverage
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import StudentAdminForm
from django.utils.html import mark_safe
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'date_joined')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'alt_number', 'address')
    def has_add_permission(self, request):
        num_contacts = Contact.objects.count()
        return num_contacts == 0

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title','media_type', 'uploaded_by', 'like_count', 'share_count')
    actions = ['update_like_count']

    def update_like_count(self, request, queryset):
        for post in queryset:
            post.like_count = post.users_liked.count()
            post.save()

    update_like_count.short_description = "Update like count for selected posts"

class MediaCoverageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'like_count', 'share_count')
    actions = ['update_like_count']

    def update_like_count(self, request, queryset):
        for post in queryset:
            post.like_count = post.users_liked.count()
            post.save()

    update_like_count.short_description = "Update like count for selected posts"


class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'phone_number', 'date_of_birth', 'display_photolist', 'level', 'account_status')
    list_editable = ('level', 'account_status')
    form = StudentAdminForm

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'email', 'date_of_birth', 'occupation', 'display_photo')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
        ('Status', {
            'fields': ('level', 'account_status')
        })
    )

    def get_name(self, obj):
        return obj.user.username
    get_name.short_description = 'Name'

    def display_photolist(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
        else:
            return "No Photo"
    display_photolist.allow_tags = True
    display_photolist.short_description = 'Profile Image'

    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')
        else:
            return "No Photo"
    display_photo.allow_tags = True
    display_photo.short_description = 'Profile Image'

    readonly_fields = ('display_photo','display_photolist')

admin.site.register(Student, StudentAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(MediaCoverage, MediaCoverageAdmin)
admin.site.register(Testimonial)
admin.site.register(Event, EventAdmin)