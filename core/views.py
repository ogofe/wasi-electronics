from django.shortcuts import render, redirect
from .models import (
	Project,
	Solution
)

resources = {
	'project': Project,
	'solution': Solution,
}


def homepage_view(request):
	context = {
		'proof_of_work': Project.objects.filter(completed=True, published=True)
	}

	return render(request, 'home/pages/homepage.html', context)



def get_quote_view(request):
	return render(request, 'home/pages/quote.html', {})



def detail_view(request, **kwargs):
	model = resources[kwargs['model']]
	subject = model.objects.get(id=kwargs['pk'])
	context = {
		'subject': subject,
		'subtitle': subject.__str__(),
		'images': ['png', 'jpg', 'jpeg'],
		'videos': ['3gp', 'mp4'],
	}
	return render(request, 'home/pages/learn-more.html', context)



def send_message(request, **kwargs):
	referer = request.META['HTTP_REFERER']
	return redirect(referer)




