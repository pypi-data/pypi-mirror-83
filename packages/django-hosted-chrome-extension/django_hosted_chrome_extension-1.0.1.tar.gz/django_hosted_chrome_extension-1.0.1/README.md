# Django Hosted Chrome Extension

This project serves two purposes:

1. Allow people to download the latest version of a private Chrome extension.
2. Provide an update server for that Chrome extension, so that the latest version is automatically downloaded.

** This is for Chrome Extensions that are NOT hosted on the Chrome Web Store. **

## Installation

### 1. Install via pip.

`pip install django-hosted-chrome-extension`

### 2. Set up your project

In your main `urls.py`, you need to include the URLs.

```
from django.urls import path, include

urlpatters = [
    path('chrome-extension/', include('hosted_chrome_extension.urls', namespace='chrome-extension')),
]
```

In your `settings.py`, add `hosted_chrome_extension` to `INSTALLED_APPS`

In your `settings.py`, add the following:

```
# the URL for your site
HOSTED_CHROME_EXTENSION_BASE_URL = 'https://yoursite.com'

# your extension's app id, see here: https://developer.chrome.com/apps/autoupdate#update_manifest
HOSTED_CHROME_EXTENSION_APP_ID = 'your app id'
```

## Usage 

In Django Admin, you'll be able to upload new versions of the extension. Extensions should have a major version, a minor version, and a patch version (e.g. 1.0.1).

You can direct users to download the latest version of the extension with `{% url 'chrome-extension:latest' %}`.

In the Chrome Extension's `manifest.json`, you can set the `update_url` key to `https://yoursite.com/chrome-extension/updates/`.
