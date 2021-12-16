from django.urls import path
from .views import (
	homepage_view,
	get_quote_view,
	service_detail_view,
	project_detail_view,
	send_message,
)

app_name = 'core'

urlpatterns = [
	path('', homepage_view, name='home'),
	path('get-a-quote', get_quote_view, name='get-quote'),
	path('services/<str:service_name>', service_detail_view, name='sevice-page'),
	path('projects/<str:project>', project_detail_view, name='project-page'),
	path('leave-us-a-message', send_message, name='message'),
]