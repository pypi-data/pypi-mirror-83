from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView, View, FormView
from . import models


class UpdatesView(TemplateView):
	""" used by the chrome extension to grab updates """
	template_name = 'hosted_chrome_extension/updates.xml'

	def get_context_data(self, *args, **kwargs):
		ctx = super().get_context_data(*args, **kwargs)
		ctx['versions'] = models.ChromeExtensionVersion.objects.all()
		ctx['app_id'] = settings.HOSTED_CHROME_EXTENSION_APP_ID
		return ctx


class LatestView(View):
	""" sends the user to download the most recent version.. """
	def get(self, *args, **kwargs):
		latest = models.ChromeExtensionVersion.objects.latest()
		return redirect(latest.file.url)
