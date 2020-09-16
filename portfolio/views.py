from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings

from info.forms import MessageForm
from info.models import (
    Competence,
    Education,
    Experience,
    Project,
    Information,
)


def email_send(data):
    subject = 'Portfolio : Mail from {}'.format(data['name'])
    message = '{}\nSender Email: {}'.format(data['message'], data['email'])
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER, ]
    send_mail(subject, message, email_from, recipient_list)


def homePage(request):
    template_name = 'homePage.html'
    context = {}

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            data = {
                'name': request.POST['name'],
                'email': request.POST['email'],
                'message': request.POST['message']
            }
            email_send(data)
            form.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    if request.method == 'GET':
        form = MessageForm()
        competences = Competence.objects.all().order_by('-id')
        education = Education.objects.all().order_by('-id')
        experiences = Experience.objects.all().order_by('-id')
        projects = Project.objects.filter(show_in_slider=True).order_by('-id')
        info = Information.objects.first()
        context = {
            'info': info,
            'competences': competences,
            'education': education,
            'experiences': experiences,
            'projects': projects,
            'form': form
        }
    return render(request, template_name, context)


def projectsPage(request):
    template_name = 'projects/projects_page.html'
    if request.method == 'GET':
        projects = Project.objects.all()
        context = {
            'projects': projects
        }
        return render(request, template_name, context)


def projectDetail(request, slug):
    template_name = 'projects/project_detail.html'
    if request.method == 'GET':
        project = get_object_or_404(Project, slug=slug)
        return render(request, template_name, {'project': project})


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def test404(request):
    return render(request, 'errors/404.html')