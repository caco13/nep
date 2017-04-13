from django.contrib import admin

from .models import Experiment


# admin.site.register(Experiment)
@admin.register(Experiment)
class Experiment(admin.ModelAdmin):
    list_display = ('title', 'description', 'study', 'status')
