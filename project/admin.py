from django.contrib import admin
from project.models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'sub_program', 'owner', 'fund', 'type', 'year', 'owner_estimation')
    search_fields = ('name',)
    list_filter = ('program', 'sub_program', 'owner', 'fund', 'type', 'year')

class ProjectLocationAdmin(admin.ModelAdmin):
    list_display = ('project', 'municipality', 'administrative_post', 'village', 'latitude_start', 'longitude_start', 'latitude_end', 'longitude_end')
    search_fields = ('project__name',)
    list_filter = ('project', 'municipality')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# ... (other admin classes)

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectLocation, ProjectLocationAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Company)
admin.site.register(Fund)
admin.site.register(Type)
admin.site.register(Owner)
admin.site.register(Program)
admin.site.register(SubProgram)
admin.site.register(ProjectStatus)
admin.site.register(ProjectJustification)