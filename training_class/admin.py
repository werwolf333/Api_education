from django.contrib import admin
from .models import Teacher, Student, Group, Exercise, Solution


class ClientAdmin(admin.ModelAdmin):
    fields = []


admin.site.register(Teacher,  ClientAdmin)
admin.site.register(Student, ClientAdmin)
admin.site.register(Group, ClientAdmin)
admin.site.register(Exercise, ClientAdmin)
admin.site.register(Solution, ClientAdmin)


