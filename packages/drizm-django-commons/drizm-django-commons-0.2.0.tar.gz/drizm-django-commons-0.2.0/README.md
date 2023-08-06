# Django Commons

This package includes shared code used by
the Drizm organizations development team.  

It is not intended for public usage but you
may still download, redistribute or 
modify it to your liking.

## Usage

Install:  
>pip install drizm-django-commons

Once installed through pip, include
the app in your settings.py like so:  
INSTALLED_APPS += ["drizm_django_commons"]  

In order to use the applications
manage.py commands you must include the
app at the top of the INSTALLED_APPS list.

Import like so:  
import drizm_django_commons
