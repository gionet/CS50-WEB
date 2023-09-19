from django.contrib import admin
from .models import posts, UserProfiles

# Register your models here.
admin.site.register(posts)
admin.site.register(UserProfiles)