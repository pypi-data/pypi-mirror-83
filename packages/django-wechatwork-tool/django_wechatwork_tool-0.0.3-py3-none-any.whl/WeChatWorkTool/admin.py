from django.contrib import admin

# Register your models here.
from .models import AccessToken

admin.site.register(AccessToken)
