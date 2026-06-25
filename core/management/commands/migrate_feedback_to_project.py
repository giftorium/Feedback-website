from django.core.management.base import BaseCommand
from core.models import Event, Project, Collaborator, ProjectPhoto, ProjectVideo


class Command(BaseCommand):
    help = 'Migrate the Feedback event into the Projects system'

    def handle(self, *args, **kwargs):
        event = Event.objects.first()
        if not event:
            self.stdout.write(self.style.ERROR('No event found in database.'))
            return

        if Project.objects.filter(slug='live-feedback-toronto').exists():
            self.stdout.write(self.style.WARNING('Project already exists. Skipping.'))
            return

        self.stdout.write('Creating Project from Feedback event...')
        project = Project.objects.create(
            title='Live Feedback Toronto',
            slug='live-feedback-toronto',
            tagline=event.tagline,
            description=event.description,
            date=event.date,
            venue=event.location,
            status='completed',
            order=0,
        )

        self.stdout.write('Migrating artists → collaborators...')
        for artist in event.artists.all():
            Collaborator.objects.create(
                project=project,
                name=artist.name,
                role=artist.role,
                bio=artist.bio,
                photo=artist.photo,
                order=artist.order,
            )
            self.stdout.write(f'  ✓ {artist.name}')

        self.stdout.write('Migrating photos...')
        for photo in event.photos.all():
            ProjectPhoto.objects.create(
                project=project,
                image=photo.image,
                caption=photo.caption,
                order=photo.order,
            )
        self.stdout.write(f'  ✓ {event.photos.count()} photos')

        self.stdout.write('Migrating videos...')
        for video in event.videos.all():
            ProjectVideo.objects.create(
                project=project,
                title=video.title,
                embed_url=video.embed_url,
                order=video.order,
            )
        self.stdout.write(f'  ✓ {event.videos.count()} videos')

        self.stdout.write(self.style.SUCCESS(f'\nDone. Project "{project.title}" created at /projects/{project.slug}/'))
