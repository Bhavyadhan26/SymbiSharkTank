from django.contrib import admin
from django.db import connection

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(SignUp)
admin.site.register(registration_details)
admin.site.register(Round2_users)
admin.site.register(financialdetails)
admin.site.register(Round3_users)





