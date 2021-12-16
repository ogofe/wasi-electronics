from django.shortcuts import render, redirect
from .models import (
	Project
)



def homepage_view(request):
	context = {
		'proof_of_work': Project.objects.filter(completed=True, published=True)
	}

	return render(request, 'home/pages/homepage.html', context)



def get_quote_view(request):
	return render(request, 'home/pages/quote.html', {})



def project_detail_view(request, **kwargs):
	project = Project.objects.get(title=kwargs['project'])
	context = {
		'project': project,
		'subtitle': project.title,
		'images': project.images,
		'videos': project.videos,

	}
	return render(request, 'home/pages/project-page.html', context)



def service_detail_view(request, **kwargs):
	context = {
		'project': project,
		'subtitle': project.title,
		'images': project.images,
		'videos': project.videos,
	}
	return render(request, 'home/pages/homepage.html', context)



def send_message(request, **kwargs):
	referer = request.META['HTTP_REFERER']
	return redirect(referer)




