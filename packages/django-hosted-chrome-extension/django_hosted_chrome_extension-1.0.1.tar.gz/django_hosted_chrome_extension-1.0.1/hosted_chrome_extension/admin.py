from django.contrib import admin
from . import models


@admin.register(models.ChromeExtensionVersion)
class ChromeExtensionVersionAdmin(admin.ModelAdmin):
	pass
