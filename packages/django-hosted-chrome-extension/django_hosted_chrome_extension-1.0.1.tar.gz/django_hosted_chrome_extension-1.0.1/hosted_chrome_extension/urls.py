from django.urls import path, reverse_lazy, include
from . import views

app_name = 'hosted_chrome_extension'
urlpatterns = [
	path('updates/', views.UpdatesView.as_view(), name='updates'),
	path('latest/', views.LatestView.as_view(), name='latest'),
]
