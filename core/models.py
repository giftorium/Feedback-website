from django.db import models
from django.utils.text import slugify


class SiteContent(models.Model):
    hero_eyebrow = models.CharField(max_length=200, default='Curator & Audiovisual Producer — Toronto')
    hero_subtitle = models.TextField(default='Building platforms where sound, image, and live systems converge into a single experience.')
    about_heading = models.CharField(max_length=200, default='Where image and sound become one')
    about_text = models.TextField(default='', help_text='Supports line breaks for multiple paragraphs')
    about_roles = models.TextField(default='Audiovisual Curation\nLive Systems\nImmersive Performance', help_text='One role per line')

    class Meta:
        verbose_name = 'Homepage Content'
        verbose_name_plural = 'Homepage Content'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def roles_list(self):
        return [r.strip() for r in self.about_roles.splitlines() if r.strip()]

    def __str__(self):
        return 'Homepage Content'


class Project(models.Model):
    STATUS_CHOICES = [('upcoming', 'Upcoming'), ('completed', 'Completed')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    concept = models.TextField(blank=True, verbose_name='Concept / Artist Statement')
    date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=300, blank=True)
    location = models.CharField(max_length=200, blank=True)
    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    ticket_url = models.URLField(blank=True, help_text='External ticketing link (for upcoming events)')
    order = models.PositiveIntegerField(default=0, help_text='Lower number appears first')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Collaborator(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collaborators')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='collaborators/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} — {self.role}'


class ProjectPhoto(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='projects/photos/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Photo {self.id} — {self.project.title}'


class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    embed_url = models.URLField(help_text='YouTube or Vimeo embed URL')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# ── Legacy Feedback event models (kept to preserve live content) ──

class Event(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='artists')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artists/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Photo {self.id}'


class Video(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    embed_url = models.URLField(help_text='YouTube or Vimeo embed URL')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at.strftime("%Y-%m-%d")}'
