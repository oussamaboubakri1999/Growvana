from django.contrib import admin
from .models import CultureHistorique

# Register your models here.

@admin.register(CultureHistorique)
class CultureHistoriqueAdmin(admin.ModelAdmin):
    list_display = ('culture', 'timestamp', 'temperature', 'humidite')
    list_filter = ('culture', 'timestamp')
    search_fields = ('culture__name',)
