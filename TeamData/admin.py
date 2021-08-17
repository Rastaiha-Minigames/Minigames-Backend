from django.contrib import admin
from .models import Person,Team

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name','position')
    list_filter = ('team',)


admin.site.register(Person,PersonAdmin)
admin.site.register(Team)