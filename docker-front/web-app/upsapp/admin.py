from django.contrib import admin
from .models import *

admin.site.register(ups_user)
admin.site.register(ups_package)
admin.site.register(ups_truck)
admin.site.register(ups_feedback)
