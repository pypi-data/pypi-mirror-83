# django_sass_finder
a Django finder that compiles Sass files

## installation
### WARNING: MAKE SURE YOU HAVE NO SASS PACKAGES INSTALLED (other than libsass)!
run `pip install django_sass_finder`, then put django_sass_finder in your `INSTALLED_APPS`, and
finally list your static file finders as so:
```py
STATICFILES_FINDERS = [
    # add the default Django finders as this setting will override the default
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # our finder
    'django_sass_finder.finders.ScssFinder',
]
```

## usage
run `python manage.py collectstatic` to compile your Sass files and put them in the STATIC_ROOT.

## license
this package is licensed under the MIT license.
