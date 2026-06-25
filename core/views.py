from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, ContactMessage, SiteContent, Project
from .forms import ContactForm


def home(request):
    event = Event.objects.first()
    site = SiteContent.get()
    upcoming = Project.objects.filter(status='upcoming').order_by('date')
    recent = Project.objects.filter(status='completed').order_by('order', '-date')[:4]
    return render(request, 'core/home.html', {
        'event': event,
        'site': site,
        'upcoming_projects': upcoming,
        'recent_projects': recent,
    })


def feedback(request):
    event = Event.objects.prefetch_related('photos', 'videos', 'artists').first()
    return render(request, 'core/feedback.html', {'event': event})


def projects(request):
    upcoming = Project.objects.filter(status='upcoming').order_by('date')
    completed = Project.objects.filter(status='completed').order_by('order', '-date')
    return render(request, 'core/projects.html', {
        'upcoming': upcoming,
        'completed': completed,
    })


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.prefetch_related('collaborators', 'photos', 'videos'),
        slug=slug,
    )
    return render(request, 'core/project_detail.html', {'project': project})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'Your message has been sent.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
