from django.contrib import admin
from .models import Lunch, Location

class LocationInLine(admin.TabularInline):
    model = Location
    extra = 3

class LunchAdmin(admin.ModelAdmin):
    inlines = [LocationInLine]

admin.site.register(Lunch)
admin.site.register(Location)