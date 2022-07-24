from datetime import date
from django.contrib import admin
from .models import User,theaterlist,booking,movie,dates
# Register your models here.
admin.site.register(User)
admin.site.register(theaterlist)
admin.site.register(booking)
admin.site.register(movie)
admin.site.register(dates)

