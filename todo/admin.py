from django.contrib import admin
from .models import Status, Materiality, Todo

# Register your models here.

class TodoCreated(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Status)
admin.site.register(Materiality)
admin.site.register(Todo, TodoCreated)