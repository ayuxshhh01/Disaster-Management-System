from django.contrib import admin
from django.contrib import admin
# from .models import Hospital
# from leaflet.admin import LeafletGeoAdmin
# from .models import relevance

# # Register your models here.
# admin.site.register(relevance)


from news.models import MinistryNewss

admin.site.register(MinistryNewss)
class MinistryNewsAdmin(admin.ModelAdmin):
    list_display = ("title", "ministry")
    autocomplete_fields = ("ministry",)
    

# from django.contrib import admin
# from .models import Hospital
# from leaflet.admin import LeafletGeoAdmin

# @admin.register(Hospital)
# class HospitalAdmin(LeafletGeoAdmin):
#     pass

