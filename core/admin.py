from django.contrib import admin
from .models import (
    SiteContent, Project, Collaborator, ProjectPhoto, ProjectVideo,
    ContactMessage,
)


# ── Homepage Content ──

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Hero Section', {'fields': ['hero_eyebrow', 'hero_subtitle']}),
        ('About Section', {'fields': ['about_heading', 'about_text', 'about_roles']}),
    ]

    def has_add_permission(self, request):
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Projects ──

class CollaboratorInline(admin.TabularInline):
    model = Collaborator
    extra = 1
    fields = ['name', 'role', 'bio', 'photo', 'order']


class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 1
    fields = ['image', 'caption', 'order']


class ProjectVideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 1
    fields = ['title', 'embed_url', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'date', 'venue', 'order']
    list_editable = ['status', 'order']
    list_filter = ['status']
    search_fields = ['title', 'tagline']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'slug', 'status', 'order']}),
        ('Details', {'fields': ['tagline', 'date', 'venue', 'location', 'ticket_url']}),
        ('Content', {'fields': ['description', 'concept']}),
        ('Cover Image', {'fields': ['cover_image']}),
    ]
    inlines = [CollaboratorInline, ProjectPhotoInline, ProjectVideoInline]


# ── Contact Messages ──

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    readonly_fields = ['name', 'email', 'message', 'created_at']


