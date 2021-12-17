from django.urls import path
from .views import (
	homepage_view,
	get_quote_view,
	detail_view,
	send_message,
)

app_name = 'core'

urlpatterns = [
	path('', homepage_view, name='home'),
	path('get-a-quote/', get_quote_view, name='get-quote'),
	path('learn-more/<model>/<pk>/', detail_view, name='learn-more'),
	path('leave-us-a-message/', send_message, name='message'),
]