from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class ChromeExtensionVersionManager(models.Manager):
	def latest(self):
		versions = self.all()
		sorted_versions = {}

		# sort everything into major, minor, patch
		for version in versions:
			vv = version.version.split('.')
			if len(vv) == 1:
				major = int(vv[0])
				minor = 0
				patch = 0
			elif len(vv) == 2:
				major = int(vv[0])
				minor = int(vv[1])
				patch = 0
			elif len(vv) == 3:
				major = int(vv[0])
				minor = int(vv[1])
				patch = int(vv[2])
			if major not in sorted_versions:
				sorted_versions[major] = {}
			if minor not in sorted_versions[major]:
				sorted_versions[major][minor] = {}
			sorted_versions[major][minor][patch] = version
		
		# latest versions
		major_versions = sorted_versions.keys()
		latest_major_version = max(major_versions)
		minor_versions = sorted_versions[latest_major_version].keys()
		latest_minor_version = max(minor_versions)
		patch_versions = sorted_versions[latest_major_version][latest_minor_version].keys()
		latest_patch_version = max(patch_versions)
		latest_version = sorted_versions[latest_major_version][latest_minor_version][latest_patch_version]
		return latest_version



def validate_version(value):
	split = value.split('.')
	err = _('Version must match format x.x.x, where each x is a positive integer (e.g. 1.0.0)')
	if len(split) != 3:
		raise ValidationError(err)
	for ss in split:
		if str(int(ss)) != ss:
			raise ValidationError(err)
		if int(ss) < 0:
			raise ValidationError(err)


class ChromeExtensionVersion(models.Model):
	file = models.FileField(upload_to='chrome-extension/')
	version = models.CharField(max_length=10, validators=[validate_version], unique=True)
	objects = ChromeExtensionVersionManager()

	def __str__(self):
		return self.version
	
	def full_file_url(self):
		return settings.HOSTED_CHROME_EXTENSION_BASE_URL + self.file.url


