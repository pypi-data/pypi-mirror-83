This app patches the following cms issues:
- https://github.com/divio/django-cms/issues/6622
- https://github.com/divio/django-cms/issues/6433
- https://github.com/divio/aldryn-sso/issues/45

And contains sentry 500 error handler with an advanced send_email function.

Installation
===============================================================================

Run `pip install djangocms-helpers`.

Update `INSTALLED_APPS` with :

```
INSTALLED_APPS = [
    ...
    'djangocms_helpers',
    ...
]
```

If you would like to enable the sentry 500 error handler, add the following to your url.py file:
```
if not settings.DEBUG:
    handler500 = collect_500_error_user_feedback_view
    handler404 = not_found_404_view
```
